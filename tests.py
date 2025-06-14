from functions.get_files_info import get_files_info

print(get_files_info("calculator", ".")) # print result to console

print(get_files_info("calculator", "pkg")) # print result to console

print(get_files_info("calculator", "/bin")) # print result to console (should return an error string)

print(get_files_info("calculator", "../")) # print result to console (should return an error string)

