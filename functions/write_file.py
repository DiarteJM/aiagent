import os

def write_file(working_directory, file_path, content):
    """
    Writes content to a file at the specified path within the working directory.
    
    Parameters:
    - working_directory: The base directory where the file should be written.
    - file_path: The relative path of the file to write.
    - content: The content to write to the file.
    
    Returns:
    - A success message if the file is written successfully.
    - An error message if the file cannot be written due to permission issues or other errors.
    """
    
    current_working_directory = os.path.abspath(working_directory)
    absolute_target_path = os.path.abspath(os.path.join(current_working_directory, file_path))
    
    def write_content(path, content):
        """Helper function to write content to a file."""
        relative_path = os.path.basename(path)

        with open(path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{relative_path}" ({len(content)} characters written)'
    
    try:
        if not absolute_target_path.startswith(current_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif not os.path.exists(current_working_directory):
            created_path = os.makedirs(current_working_directory, exist_ok=True)
        else:
            content_file = write_content(absolute_target_path, content)
            return content_file
    
    except Exception as e:
        return f"Error: {e}"