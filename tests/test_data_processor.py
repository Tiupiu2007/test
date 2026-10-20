import unittest
from data_processor import analyze_csv

class DataProcessorTests(unittest.TestCase):
    def test_row_and_column_counts(self):
        result = analyze_csv('id,name\n1,Ada\n2,Linus\n')
        self.assertEqual(result['row_count'], 2)
        self.assertEqual(result['column_count'], 2)

    def test_missing_cell(self):
        result = analyze_csv('id,email\n1,\n')
        self.assertEqual(len(result['missing_cells']), 1)

if __name__ == '__main__':
    unittest.main()
