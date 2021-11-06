#!/usr/bin/env python3

import sys
import os
import mmap
import re
import json


def parse_methods(content):
    methods = re.finditer(
        "(?:public |protected |private )?(?:static )?(?:<T.*> )?[\w\<\>\[\]]+\s+(?:\w+) *\([^\)]*\)*(?:\{?|[^;]) *(?:throws.*|{)",
        content)

    method_bounds = []

    for method in methods:
        start = method.start(0)
        if len(method_bounds) > 0:
            method_bounds[-1][1] = content.rindex("}", method_bounds[-1][0], start)

        method_bounds.append([start, content.rindex("}", start, content.rindex("}")), method.group()])

    result = []

    for bounds in method_bounds:
        result.append((bounds[2], content[bounds[0]:bounds[1]]))

    return result


def find_occurrences_in_methods(target, methods):

    result = []

    for method in methods:
        if method[1].find(target) > 0:
            result.append(method[0])

    return result


def find_method_calls(target, file_extension, path):
    result = []

    for (path, dir_names, file_names) in os.walk(path):
        for file_name in file_names:
            if file_name.endswith("." + file_extension):
                file_path = path + ("" if path[-1] == "/" else "/") + file_name
                with open(file_path) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                    occurrence = s.find(bytes(method_to_search, 'utf-8'))

                    if occurrence > 0:
                        content = file.read()
                        methods = parse_methods(content)

                        result.append((file_path, file_name, find_occurrences_in_methods(target, methods)))

    return result


def construct_json_response(matches, file_path=None):
    data = {"matches": []}
    for file in matches:
        data["matches"].append({
            "file": file[1],
            "path": file[0],
            "methods": file[2]
        })

    if file_path:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    return data


search_path = "./"
file_extension = "java"
method_to_search = sys.argv[1]
out_file = None if len(sys.argv) < 3 else sys.argv[2]

matches = find_method_calls(method_to_search, file_extension, search_path)
print(construct_json_response(matches, out_file))
