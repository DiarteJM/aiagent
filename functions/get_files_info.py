import os
from google.genai import types


def get_files_info(working_directory, directory=None):

    absolute_working_directory = os.path.abspath(working_directory)
    target_path = absolute_working_directory
    if directory:
        target_path = os.path.abspath(os.path.join(working_directory, directory))
    if not target_path.startswith(absolute_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'
    try:
        files = []
        filelist = os.listdir(target_path)

        for file in filelist:
            filename = os.path.join(target_path, file)
            filesize = 0
            is_dir = os.path.isdir(file)
            filesize = os.path.getsize(file)
            files.append(f" - {filename}: file_size={filesize} bytes, is_dir={is_dir}")
        return "\n".join(files)
    except Exception as e:
        return f"Error: {e}"


# Schema for the function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
