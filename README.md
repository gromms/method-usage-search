# method-usage-search
Python script for searching for keywords used in methods.

Written for finding some specific method calls from multiple projects.

Searches for the expression in all `.java` files from current directory and all of its subdirectories. Files that include the expression have all of their methods' bodies parsed and the method declaration row along with the file path and name are returned for all methods that include the keyword. In the end it prints out all methods that have the keyword used in their bodies in json format.

If output file path is provided, a prettified json output will be dumped into the specified file.

# Usage
If executable: `./find_method_usages.py "<expression_to_search_for>" <output_file_path>`

Else: `python3 ./find_method_usages.py "<expression_to_search_for>" <output_file_path>`

Output file is optional.

For convenience the script directory could be added directly to PATH or one could create a symbolic link to `usr/local/bin`.
