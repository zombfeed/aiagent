import os


def build_file_info_str(directory_data):
    return_string = ""
    for file_info in directory_data:
        return_string += f"- {file_info}: file_size={directory_data[file_info]['file_size']}, is_dir={directory_data[file_info]['is_dir']}\n"
    return return_string.rstrip("\n")


def get_files_info(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    valid_target_dir = (
        os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
    )

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directed'

    file_info = {}
    try:
        for file in os.listdir(path=target_dir):
            file_info[file] = {
                "file_size": os.path.getsize(
                    os.path.normpath(os.path.join(target_dir, file))
                ),
                "is_dir": os.path.isdir(
                    os.path.normpath(os.path.join(target_dir, file))
                ),
            }

        return build_file_info_str(file_info)
    except Exception as e:
        return f"Error: {e}"
