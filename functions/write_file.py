import os


def write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)
    file_normpath = os.path.normpath(os.path.join(working_directory_abs, file_path))
    if os.path.isdir(file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    valid_file_path = (
        os.path.commonpath([working_directory_abs, file_normpath])
        == working_directory_abs
    )
    if not valid_file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directed'

    try:
        os.makedirs(os.path.dirname(file_normpath), exist_ok=True)
        with open(file_normpath, "w") as file_to_write:
            file_to_write.write(content)
        return f'Successfuly wrote to "{file_path}" {len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
