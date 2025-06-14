import os

# If file path is outside the working directory, return a string with an error 
#   ("Cannot read <file_path> as it is outside the permitted working directory")
# if file_path is not a file, return string with an error 
#   ("File not found or is not a regular file: <file_path>")
# Else read the file and return the content as a string
    # use some of the functions in the standard library in the Tips section
    # if file is longer than 10000 characters, truncate to 10000 characters 
    # and append following message to end 
    # - [...File "<file_path>" truncated to 10000 characters]
    
# OS functions to use:
  # os.path.abspath() - to get the absolute path of the file
  # os.path.join() - joins two paths together safely (handles slashes)
  # .startswith() - check if a string starts with a specific substring
  # os.path.isfile() - check if a path is a file
  # to read the file, use the built-in open() function with 'r' mode
    # with open(file_path, 'r') as file:
    #    content_string = file.read(MAX_CHARS=10000)
  
def get_file_content(working_directory, file_path):
    print(f"Working Directory: {working_directory}")
    print(f"File Path: {file_path}")
    
    # Ensure the working directory is absolute
    current_working_directory = os.path.abspath(working_directory)
    current_file_path = os.path.abspath(file_path)
    # Construct the absolute file path
    absolute_target_path = os.path.abspath(os.path.join(current_working_directory, current_file_path))    
    
    try:
      if not absolute_target_path.startswith(current_working_directory):
          return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
      elif not os.path.isfile(absolute_target_path):
          return f"Error: File not found or is not a regular file: '{file_path}'"
      else:
          MAX_CHARS = 10000
          with open(absolute_target_path, 'r') as file:
              content = file.read(MAX_CHARS)
              if len(content) > MAX_CHARS:
                  content += f"\n- [...File {file_path} truncated to {MAX_CHARS} characters]"
    except Exception as e:
      return f"Error: {e}"