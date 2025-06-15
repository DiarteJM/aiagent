import os
  
def get_file_content(working_directory, file_path):
    # Ensure the working directory is absolute
    current_working_directory = os.path.abspath(working_directory)
    
    # Construct the absolute file path
    absolute_target_path = os.path.abspath(os.path.join(current_working_directory, file_path))
    
        
    def read_content(path):
        relative_path = os.path.basename(path)
        MAX_CHARS = 10000
        """Helper function to read file content with truncation."""
        with open(path, 'r') as file:
            file_content_string = file.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += f"\n- [...File '{relative_path}' truncated at 10000 characters]"
        return file_content_string

    try:
      if not absolute_target_path.startswith(current_working_directory):
          return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
      elif not os.path.isfile(absolute_target_path):
          return f"Error: File not found or is not a regular file: '{file_path}'"
      else:
          file_content_string = read_content(absolute_target_path)
          return file_content_string
    except Exception as e:
      return f"Error: {e}"