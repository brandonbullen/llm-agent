import unittest
from functions.get_files_info import get_files_info, get_file_content, write_file, run_python_file


# class TestGetFiles(unittest.TestCase):
#     def test_current_working_directory(self):
#         expected = (
#             "- main.py: file_size=576 bytes, is_dir=False\n"
#             "- tests.py: file_size=1343 bytes, is_dir=False\n"
#             "- pkg: file_size=92 bytes, is_dir=True"
#         )

#         result = get_files_info("calculator", ".")
#         print(f"Result for current directory:\n     {result}")
#         self.assertEqual(result, expected)

#     def test_subdirectory(self):
#         expected = (
#             "- calculator.py: file_size=1739 bytes, is_dir=False\n"
#             "- render.py: file_size=768 bytes, is_dir=False"
#         )

#         result = get_files_info("calculator", "pkg")
#         print(f"Result for 'pkg' directory:\n     {result}")
#         self.assertEqual(result, expected)
        
#     def test_directory_override(self):
#         expected = (
#             'Error: Cannot list "/bin" as it is outside the permitted working directory'
#         )

#         result = get_files_info("calculator", "/bin")
#         print(f"Result for '/bin' directory:\n     {result}")
#         self.assertEqual(result, expected)

#     def test_outside_working_directory(self):
#         expected = (
#             'Error: Cannot list "../" as it is outside the permitted working directory'
#         )

#         result = get_files_info("calculator", "../")
#         print(f"Result for ../ directory:\n     {result}")
#         self.assertEqual(result, expected)
        

# if __name__ == "__main__":
#     unittest.main()

# Starting our get_files_info tests
# result = get_files_info("calculator", ".")
# print(f"Result for current directory:\n {result}")

# result = get_files_info("calculator", "pkg")
# print(f"Result for 'pkg' directory:\n {result}")

# result = get_files_info("calculator", "/bin")
# print(f"Result for '/bin' directory:\n    {result}")

# result = get_files_info("calculator", "../")
# print(f"Result for ../ directory:\n    {result}")

# Starting our get_file_content tests
# result = get_file_content("calculator", "main.py")
# print(result)

# result = get_file_content("calculator", "pkg/calculator.py")
# print(result)

# result = get_file_content("calculator", "/bin/cat")
# print(result)

# result = get_file_content("calculator", "pkg/does_not_exist.py")
# print(result)

# Starting our write_file tests
# result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# print(result)

# result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# print(result)

# result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
# print(result)

# Starting our run_python tests.
result = run_python_file("calculator", "main.py")
print(result)

result = run_python_file("calculator", "main.py", ["3 + 5"])
print(result)

result = run_python_file("calculator", "tests.py")
print(result)

result = run_python_file("calculator", "../main.py")
print(result)

result = run_python_file("calculator", "nonexistent.py")
print(result)