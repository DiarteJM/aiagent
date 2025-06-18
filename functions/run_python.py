import os
import subprocess
import sys


def run_python_file(working_directory, file_path):
    """
    - Runs a Python file at the specified path within the working directory.
      - Only allows LLM to run code in specified directory.
      - 30-second timeout to prevent it from running indefinitely.
    - If file_path is outside the working directory, return an error string
    - If file_path does not exist, return an error string.
    - if file_path does not end with .py, return an error string.
    - Use subprocess.run to execute the file.
      - set timeout to 30 seconds.
      - capture both stdout and stderr.
      - set working directory properly.
    - Format the output to include the following:
      - stdout: the standard output of the script - prefixed with "STDOUT:"
      - stderr: the standard error of the script - prefixed with "STDERR:"
      - if process exits with non-zero code, include "Process exited with code: X"
      - if no output produced, return "No output produced."
    - Catch any exceptions during execution and return an error string - must start with "Error: "
    """

    try:
        current_working_directory = os.path.abspath(working_directory)
        absolute_target_path = os.path.abspath(
            os.path.join(current_working_directory, file_path))

        if not absolute_target_path.startswith(current_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(absolute_target_path):
            return f'Error: File "{file_path}" not found.'
        if not absolute_target_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            [sys.executable, absolute_target_path],
            capture_output=True,
            text=True,
            cwd=current_working_directory,
            timeout=30
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output.append(f"Process exited with code: {result.returncode}")

        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"
