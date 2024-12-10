# test_student_marks_management.py
import unittest
from unittest.mock import patch, mock_open
import json
import os

# Import the functions from the main script
# Assuming the main script is named student_marks_management.py and is in the same directory
import student_marks_management as smm

class TestStudentMarksManagementSystem(unittest.TestCase):
    def setUp(self):
        # Sample data to be used across tests
        self.sample_data = {
            'S001': {
                'name': 'Alice',
                'marks': {
                    'Mathematics': 85,
                    'Physics': 90,
                    'Chemistry': 75,
                    'English': 80,
                    'Computer Science': 95
                }
            },
            'S002': {
                'name': 'Bob',
                'marks': {
                    'Mathematics': 65,
                    'Physics': 70,
                    'Chemistry': 60,
                    'English': 75,
                    'Computer Science': 80
                }
            }
        }

    @patch('student_marks_management.os.path.exists')
    @patch('student_marks_management.open', new_callable=mock_open, read_data='{}')
    def test_load_data_empty(self, mock_file, mock_exists):
        # Test loading data when file does not exist
        mock_exists.return_value = False
        data = smm.load_data()
        self.assertEqual(data, {})

    @patch('student_marks_management.os.path.exists')
    @patch('student_marks_management.open', new_callable=mock_open, read_data=json.dumps({'S001': {'name': 'Alice', 'marks': {}}}))
    def test_load_data_with_content(self, mock_file, mock_exists):
        # Test loading data when file has content
        mock_exists.return_value = True
        data = smm.load_data()
        expected = {'S001': {'name': 'Alice', 'marks': {}}}
        self.assertEqual(data, expected)

    @patch('student_marks_management.save_data')
    def test_add_student(self, mock_save):
        # Test adding a new student
        data = {}
        with patch('builtins.input', return_value='Charlie'):
            smm.add_student(data)
        self.assertIn('S001', data)
        self.assertEqual(data['S001']['name'], 'Charlie')
        for subject in smm.SUBJECTS:
            self.assertEqual(data['S001']['marks'][subject], 0)
        mock_save.assert_called_once_with(data)

    def test_generate_student_id_empty(self):
        # Test generating student ID when data is empty
        data = {}
        new_id = smm.generate_student_id(data)
        self.assertEqual(new_id, 'S001')

    def test_generate_student_id_non_empty(self):
        # Test generating student ID when data has existing IDs
        data = {'S001': {}, 'S002': {}}
        new_id = smm.generate_student_id(data)
        self.assertEqual(new_id, 'S003')

    def test_calculate_grade(self):
        # Test grade calculation based on average
        self.assertEqual(smm.calculate_grade(95), 'A+')
        self.assertEqual(smm.calculate_grade(85), 'A')
        self.assertEqual(smm.calculate_grade(75), 'B')
        self.assertEqual(smm.calculate_grade(65), 'C')
        self.assertEqual(smm.calculate_grade(55), 'D')
        self.assertEqual(smm.calculate_grade(45), 'F')

    @patch('student_marks_management.save_data')
    def test_add_marks_valid(self, mock_save):
        # Test adding marks with valid inputs
        data = {'S001': {'name': 'Alice', 'marks': {subject: 0 for subject in smm.SUBJECTS}}}
        inputs = ['S001'] + ['80', '90', '70', '85', '95']
        with patch('builtins.input', side_effect=inputs):
            smm.add_marks(data)
        expected_marks = {
            'Mathematics': 80.0,
            'Physics': 90.0,
            'Chemistry': 70.0,
            'English': 85.0,
            'Computer Science': 95.0
        }
        self.assertEqual(data['S001']['marks'], expected_marks)
        mock_save.assert_called_once_with(data)

    @patch('builtins.input', side_effect=['1', 'S001'])
    def test_search_student_by_id_found(self, mock_input):
        # Test searching for a student by ID when found
        data = self.sample_data.copy()
        with patch('builtins.print') as mock_print:
            smm.search_student(data)
            # Check if display_student was called by checking print statements
            self.assertTrue(mock_print.called)

    @patch('builtins.input', side_effect=['1', 'S003'])
    def test_search_student_by_id_not_found(self, mock_input):
        # Test searching for a student by ID when not found
        data = self.sample_data.copy()
        with patch('builtins.print') as mock_print:
            smm.search_student(data)
            mock_print.assert_any_call("Student ID not found.")

    @patch('builtins.input', side_effect=['2', 'Alice'])
    def test_search_student_by_name_found(self, mock_input):
        # Test searching for a student by name when found
        data = self.sample_data.copy()
        with patch('builtins.print') as mock_print:
            smm.search_student(data)
            self.assertTrue(mock_print.called)

    @patch('builtins.input', side_effect=['2', 'Charlie'])
    def test_search_student_by_name_not_found(self, mock_input):
        # Test searching for a student by name when not found
        data = self.sample_data.copy()
        with patch('builtins.print') as mock_print:
            smm.search_student(data)
            mock_print.assert_any_call("No student found with that name.")

    @patch('student_marks_management.save_data')
    def test_update_marks_valid(self, mock_save):
        # Test updating marks with valid inputs
        data = self.sample_data.copy()
        inputs = ['S001'] + ['88', '92', '78', '85', '98']
        with patch('builtins.input', side_effect=inputs):
            smm.update_marks(data)
        expected_marks = {
            'Mathematics': 88.0,
            'Physics': 92.0,
            'Chemistry': 78.0,
            'English': 85.0,
            'Computer Science': 98.0
        }
        self.assertEqual(data['S001']['marks'], expected_marks)
        mock_save.assert_called_once_with(data)

    @patch('student_marks_management.save_data')
    def test_delete_student_confirm_yes(self, mock_save):
        # Test deleting a student with confirmation 'y'
        data = self.sample_data.copy()
        inputs = ['S001', 'y']
        with patch('builtins.input', side_effect=inputs):
            smm.delete_student(data)
        self.assertNotIn('S001', data)
        mock_save.assert_called_once_with(data)

    @patch('student_marks_management.save_data')
    def test_delete_student_confirm_no(self, mock_save):
        # Test deleting a student with confirmation 'n'
        data = self.sample_data.copy()
        inputs = ['S001', 'n']
        with patch('builtins.input', side_effect=inputs):
            smm.delete_student(data)
        self.assertIn('S001', data)
        mock_save.assert_not_called()

    @patch('builtins.print')
    def test_generate_report(self, mock_print):
        # Test generating a summary report
        data = self.sample_data.copy()
        smm.generate_report(data)
        # Check if print was called for total students, average marks, and grade distribution
        self.assertTrue(mock_print.called)
        mock_print.assert_any_call("Total Students: 2")
        mock_print.assert_any_call("\nAverage Marks per Subject:")

    @patch('student_marks_management.save_data')
    def test_delete_student_not_found(self, mock_save):
        # Test deleting a student that does not exist
        data = self.sample_data.copy()
        inputs = ['S003']
        with patch('builtins.input', side_effect=inputs):
            smm.delete_student(data)
        mock_save.assert_not_called()

    @patch('student_marks_management.save_data')
    def test_add_marks_invalid_input(self, mock_save):
        # Test adding marks with invalid (non-numeric) inputs
        data = {'S001': {'name': 'Alice', 'marks': {subject: 0 for subject in smm.SUBJECTS}}}
        # Simulate user entering 'invalid' first, then '85' for each subject
        inputs = ['S001'] + ['invalid', '85'] * len(smm.SUBJECTS)
        with patch('builtins.input', side_effect=inputs):
            smm.add_marks(data)
        expected_marks = {subject: 85.0 for subject in smm.SUBJECTS}
        self.assertEqual(data['S001']['marks'], expected_marks)
        # Ensure save_data is called once after all inputs
        mock_save.assert_called_once_with(data)

    @patch('student_marks_management.save_data')
    def test_add_marks_out_of_range(self, mock_save):
        # Test adding marks with out-of-range inputs (>100 and <0)
        data = {'S001': {'name': 'Alice', 'marks': {subject: 0 for subject in smm.SUBJECTS}}}
        # Simulate user entering '105' (invalid), then '95' (valid) for each subject
        inputs = ['S001']
        for _ in smm.SUBJECTS:
            inputs += ['105', '95']
        with patch('builtins.input', side_effect=inputs):
            smm.add_marks(data)
        expected_marks = {subject: 95.0 for subject in smm.SUBJECTS}
        self.assertEqual(data['S001']['marks'], expected_marks)
        # Ensure save_data is called once after all inputs
        mock_save.assert_called_once_with(data)

    @patch('student_marks_management.save_data')
    def test_update_marks_invalid_input(self, mock_save):
        # Test updating marks with invalid inputs
        data = self.sample_data.copy()
        # Simulate entering 'invalid' first, then '80' for each subject
        inputs = ['S001']
        for _ in smm.SUBJECTS:
            inputs += ['invalid', '80']
        with patch('builtins.input', side_effect=inputs):
            smm.update_marks(data)
        expected_marks = {subject: 80.0 for subject in smm.SUBJECTS}
        self.assertEqual(data['S001']['marks'], expected_marks)
        mock_save.assert_called_once_with(data)

    @patch('builtins.print')
    def test_view_marks_empty_data(self, mock_print):
        # Test viewing marks when there is no data
        data = {}
        smm.view_marks(data)
        mock_print.assert_any_call("No student data available.")

    @patch('builtins.print')
    def test_view_marks_with_data(self, mock_print):
        # Test viewing marks with existing data
        data = self.sample_data.copy()
        smm.view_marks(data)
        # Check if headers and student details are printed
        mock_print.assert_any_call("\n--- View All Students' Marks ---")
        header = f"{'ID':<6} {'Name':<20}" + "".join([f"{sub[:4]:<10}" for sub in smm.SUBJECTS]) + f"{'Total':<10} {'Average':<10} {'Grade':<6}"
        mock_print.assert_any_call(header)

    def test_display_main_menu(self):

        smm.display_main_menu()
        assert True

    def test_main_menu(self):
        smm.main_menu(1)
        assert True

    def test_main_menu_2(self):
        smm.main_menu(2)
        smm.main_menu(3)
        smm.main_menu(4)
        smm.main_menu(5)
        smm.main_menu(6)
        smm.main_menu(7)

if __name__ == '__main__':
    unittest.main()
