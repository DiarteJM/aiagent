from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

# Test cases for get_files_info function
# print(get_files_info("calculator", ".")) # print result to console
# print(get_files_info("calculator", "pkg")) # print result to console
# print(get_files_info("calculator", "/bin")) # print result to console (should return an error string)
# print(get_files_info("calculator", "../")) # print result to console (should return an error string)

# Test cases for get_file_content function
print("----------Test Case 1----------")
print(get_file_content("calculator", "lorem.txt")) # print result to console (should return file content) - ensure it truncates properly
print("----------Test Case 2----------")
print(get_file_content("calculator", "main.py")) # print result to console (should return file content) - ensure it truncates properly
print("----------Test Case 3----------")
print(get_file_content("calculator", "pkg/calculator.py")) # print result to console (should return file content) - ensure it truncates properly
print("----------Test Case 4----------")
print(get_file_content("calculator", "/bin/cat")) # print result to console (should return error string)
