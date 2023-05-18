import sys
import os
import unittest
from unittest.mock import MagicMock
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from earthquake_analyzer.analyzer import EarthquakeDataAnalyzer, EarthquakeDataReader, EarthquakeDataHandler

class EarthquakeDataReaderTests(unittest.TestCase):
    def test_read_csv_file(self):
        # Test to verify the read_csv_file method in the EarthquakeDataReader.
        data_reader = EarthquakeDataReader()

        data = list(data_reader.read_csv_file('data/test_data.csv'))

        expected_data = [
            (0, ['1', 'California', '5.6']),
            (1, ['2', 'Japan', '7.2'])
        ]

        self.assertEqual(data, expected_data)


class EarthquakeDataHandlerTests(unittest.TestCase):
    # Test to verify the `process_data` method in the EarthquakeDataHandler.
    def test_process_data(self):
        analyzer = MagicMock()
        handler = EarthquakeDataHandler(analyzer, location_index=1, magnitude_index=2)

        row = (0, ['1', 'California', '5.6'])
        handler.process_data(row)

        analyzer.calculate_average_magnitudes.assert_called_once_with(['1', 'California', '5.6'])


class EarthquakeDataAnalyzerTests(unittest.TestCase):
    def setUp(self):
        # Test setup method for the EarthquakeDataAnalyzer
        self.data_reader = MagicMock()
        self.analyzer = EarthquakeDataAnalyzer(
            self.data_reader, location_index=1, date_index=2, magnitude_index=3
        )


    def test_calculate_earthquakes_per_location(self):
        #Test to verify the functionality of the calculate_earthquakes_per_location method
        self.data_reader.read_csv_file.return_value = [
            (0, ['1', 'California', '2023-05-18', '5.6']),
            (1, ['2', 'Japan', '2023-05-18', '7.2']),
            (2, ['3', 'California', '2023-05-18', '6.4']),
        ]

        earthquake_count = self.analyzer.calculate_earthquakes_per_location('data.csv')

        expected_count = defaultdict(int)
        expected_count['California'] = 2
        expected_count['Japan'] = 1

        self.assertEqual(earthquake_count, expected_count)


    def test_calculate_average_magnitudes(self):
        # Test to verify the functionality of the calculate_average_magnitudes method
        self.analyzer.location_avg_magnitudes = defaultdict(lambda: {'count': 2, 'mean': 5.0})

        row = ['1', 'California', '2023-05-18', '5.6']
        self.analyzer.calculate_average_magnitudes(row)

        self.assertEqual(self.analyzer.location_avg_magnitudes['California']['count'], 3)
        self.assertAlmostEqual(self.analyzer.location_avg_magnitudes['California']['mean'], 5.2, places=1)


if __name__ == '__main__':
    unittest.main()
