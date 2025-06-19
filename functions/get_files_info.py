import os
from google.genai import types

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

def get_files_info(working_directory, directory=None):

    current_directory = os.path.abspath(working_directory)

    resolved_target_path = os.path.abspath(
        os.path.join(current_directory, directory))

    try:
        if not resolved_target_path.startswith(current_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(resolved_target_path):
            return f'Error: "{directory}" is not a directory'
        else:
            filelist = os.listdir(resolved_target_path)
            files = []

            for file in filelist:
                filename = os.path.join(resolved_target_path, file)
                file_info = f"- {file}: file_size={os.path.getsize(filename)} bytes, is_dir={os.path.isdir(filename)}"
                files.append(file_info)
            return "\n".join(files)
    except Exception as e:
        return f"Error: {e}"
