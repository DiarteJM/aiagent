from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

# Test cases for get_files_info function
# print(get_files_info("calculator", ".")) # print result to console
# print(get_files_info("calculator", "pkg")) # print result to console
# print(get_files_info("calculator", "/bin")) # print result to console (should return an error string)
# print(get_files_info("calculator", "../")) # print result to console (should return an error string)

# Test cases for get_file_content function
# print(get_file_content("calculator", "lorem.txt")) # print result to console (should return file content) - ensure it truncates properly
# print(get_file_content("calculator", "main.py")) # print result to console (should return file content) - ensure it truncates properly
# print(get_file_content("calculator", "pkg/calculator.py")) # print result to console (should return file content) - ensure it truncates properly
# print(get_file_content("calculator", "/bin/cat")) # print result to console (should return error string)

# Test cases for write_file function
# print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")) # print result - should return success message
# print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")) # print result - should return success message (via creating the file and adding to it)
# print(write_file("calculator", "tmp/temp.txt", "this should not be allowed")) # print result - should return error string

# Test cases for run_python_file function
print("----------Test Case 1----------")
print(run_python_file("calculator", "main.py"))
print("----------Test Case 2----------")
print(run_python_file("calculator", "tests.py"))
print("----------Test Case 3----------")
print(run_python_file("calculator", "../main.py")) # should return an error string
print("----------Test Case 4----------")
print(run_python_file("calculator", "nonexistent.py")) # should return an error string