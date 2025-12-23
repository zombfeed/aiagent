import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    file_normpath = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if not os.path.isfile(file_normpath):
        return f'Error: File not found or is not a regular file: "{file_normpath}"'
    valid_file_path = (
        os.path.commonpath([working_directory_abs, file_normpath])
        == working_directory_abs
    )
    if not valid_file_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directed'
    try:
        with open(file_normpath, "r") as read_file:
            content = read_file.read(MAX_CHARS)
            if read_file.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as e:
        return f"Error: {e}"
