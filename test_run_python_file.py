from functions.run_python_file import run_python_file

print('Results of run_python_file("caluclator", "main.py")')
print(run_python_file("calculator", "main.py"))
print('\nResults of run_python_file("caluclator", "main.py", ["3 + 5"])')
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print('\nResults of run_python_file("caluclator", "tests.py")')
print(run_python_file("calculator", "tests.py"))
print('\nResults of run_python_file("caluclator", "../main.py")')
print(run_python_file("calculator", "../main.py"))
print('\nResults of run_python_file("caluclator", "nonexistent.py")')
print(run_python_file("calculator", "nonexistent.py"))
print('\nResults of run_python_file("caluclator", "lorem.txt")')
print(run_python_file("calculator", "lorem.txt"))
