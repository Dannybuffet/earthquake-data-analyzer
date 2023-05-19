import sys
import os
from collections import defaultdict
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from earthquake_analyzer.analyzer import EarthquakeDataReader, EarthquakeDataAnalyzer


class EarthquakeDataReaderTests(unittest.TestCase):
    def test_read_csv_file(self):
        # Test to verify the read_csv_file method in the EarthquakeDataReader.
        data_reader = EarthquakeDataReader()

        data = list(data_reader.read_csv_file('data/test_data.csv'))

        expected_data = [
            ['1', 'California', '5.6'],
            ['2', 'Japan', '7.2']
        ]

        self.assertEqual(data, expected_data)


class EarthquakeDataAnalyzerTests(unittest.TestCase):
    def setUp(self):
        # Test setup method for the EarthquakeDataAnalyzer
        self.analyzer = EarthquakeDataAnalyzer(location_index=1, date_index=2, magnitude_index=3)

    def test_calculate_earthquakes_per_location(self):
        # Test to verify the functionality of calculate_earthquakes_per_location method
        self.analyzer.location_earthquake_count = defaultdict(int)

        rows = [
            ['1', 'California', '2023-05-18', '5.6'],
            ['2', 'Japan', '2023-05-18', '7.2'],
            ['3', 'California', '2023-05-18', '6.4'],
        ]

        for row in rows:
            self.analyzer.calculate_earthquakes_per_location(row)

        expected_count = defaultdict(int)
        expected_count['California'] = 2
        expected_count['Japan'] = 1

        self.assertEqual(self.analyzer.location_earthquake_count, expected_count)

    def test_calculate_average_magnitudes(self):
        # Test to verify the functionality of calculate_average_magnitudes method
        self.analyzer.location_avg_magnitudes = defaultdict(lambda: {'count': 2, 'mean': 5.0})

        row = ['1', 'California', '2023-05-18', '5.6']
        self.analyzer.calculate_average_magnitudes(row)

        self.assertEqual(self.analyzer.location_avg_magnitudes['California']['count'], 3)
        self.assertAlmostEqual(self.analyzer.location_avg_magnitudes['California']['mean'], 5.2, places=1)


if __name__ == '__main__':
    unittest.main()


