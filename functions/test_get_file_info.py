import unittest
import os
from get_file_info import get_file_content

class TestGetFileContent(unittest.TestCase):
    def setUp(self):
        self.working_directory = os.path.dirname(__file__)
        self.test_file = "test_file.txt"
        self.test_content = "Test for ~!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/`çãõéüñ"
        with open(os.path.join(self.working_directory, self.test_file), "w", encoding="utf-8") as f:
            f.write(self.test_content)

    def tearDown(self):
        os.remove(os.path.join(self.working_directory, self.test_file))

    def test_read_file_success(self):
        content = get_file_content(self.working_directory, self.test_file)
        self.assertIn(self.test_content, content)

    def test_file_not_found(self):
        content = get_file_content(self.working_directory, "nonexist.txt")
        self.assertIn("Error: File not found", content)

    def test_output_directory(self):
        content = get_file_content(self.working_directory, "../output.txt")
        self.assertIn("Error: Cannot read", content)

if __name__ == "__main__":
    unittest.main()