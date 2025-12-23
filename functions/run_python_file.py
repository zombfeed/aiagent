import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    working_directory_abs = os.path.abspath(working_directory)
    file_normpath = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if not os.path.isfile(file_normpath):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    valid_file_path = (
        os.path.commonpath([working_directory_abs, file_normpath])
        == working_directory_abs
    )
    if not valid_file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directed'

    _, file_extension = os.path.splitext(file_path)
    if file_extension != ".py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", file_normpath]
    if args:
        command.extend(args)

    try:
        process_result = subprocess.run(
            command, capture_output=True, text=True, timeout=30
        )
        output_string = ""
        if process_result.returncode != 0:
            output_string += "Process exited with code {process_result.returncode}"
        if process_result.stdout:
            output_string += f"STDOUT: {process_result.stdout}"
        else:
            output_string += "STDOUT: No output produced"
        if process_result.stderr:
            output_string += f"STDERR: {process_result.stderr}"
        else:
            output_string += "STDERR: No output produced"

        return output_string

    except Exception as e:
        return f"Error: {e}"
