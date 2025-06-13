def get_files_info(working_directory, directory=None):
    if directory is not working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not directory:
        return f'Error: "{directory}" is not a directory'
    else:
        return f"Listing files in directory:\n {directory}\n
        - README.md: file_size=1032 bytes
        \n - src: file_size=128 bytes
        \n - package.json: file_size=2048 bytes\n - .gitignore: file_size=512 bytes\n - .env: file_size=256 bytes\n - .vscode: file_size=1234 bytes\n"
