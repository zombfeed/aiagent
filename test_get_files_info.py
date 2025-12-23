from functions.get_files_info import get_files_info


def format_results(data):
    formatted_data = data.split("\n")
    return f"    {'\n    '.join(formatted_data)}"


test_one = format_results(get_files_info("calculator", "."))
test_two = format_results(get_files_info("calculator", "pkg"))
test_three = format_results(get_files_info("calculator", "/bin"))
test_four = format_results(get_files_info("calculator", "../"))
print(f"Result for current directory:\n{test_one}\n")
print(f"Result for 'pkg' directory:\n{test_two}\n")
print(f"Result for '/bin/' directory:\n{test_three}\n")
print(f"Result for '../' directory:\n{test_four}\n")
