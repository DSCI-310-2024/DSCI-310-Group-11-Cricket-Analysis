import unittest
import pandas as pd

class TestDataProcessing(unittest.TestCase):

    def test_data_loading_and_drop(self):
        # Load data
        data = pd.read_csv("data/Cricket_main.csv")
        # Drop 'Unnamed: 0' column
        data = data.drop(columns=["Unnamed: 0"])
        
        # Check if 'Unnamed: 0' column is dropped
        self.assertNotIn("Unnamed: 0", data.columns)

        # Check if data is loaded successfully
        self.assertFalse(data.empty)

        # Check if the first 5 rows are displayed properly
        self.assertEqual(data.head().shape, (5, len(data.columns)))

        # Check if the caption is set correctly
        self.assertEqual(data.head().style.caption, "Table 1: Overview of full dataset")

        # Check if table styles are set correctly
        self.assertEqual(data.head().style.table_styles[0]['selector'], 'caption')
        self.assertEqual(data.head().style.table_styles[0]['props'], 'caption-side: bottom; font-size:1.25em;')

if __name__ == '__main__':
    unittest.main()
