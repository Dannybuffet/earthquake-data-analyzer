import csv
from datetime import datetime
from collections import defaultdict


class EarthquakeDataReader:
    # Reads earthquake data from a CSV file.

    @staticmethod
    def read_csv_file(filename):
        # Reads CSV file and yields each row.
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  
                for index, row in enumerate(csv_reader):
                    yield index, row
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File '{filename}' not found.") from e
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}") from e


class EarthquakeDataHandler:
    # Handles earthquake data processing.

    def __init__(self, analyzer, location_index, magnitude_index):
        # Initializes the EarthquakeDataHandler.
        self.analyzer = analyzer
        self.location_index = location_index
        self.magnitude_index = magnitude_index

    def process_data(self, data_row):
        # Processes a single CSV row for live stream.
        try:
            _, row = data_row
            self.analyzer.calculate_average_magnitudes(row)
        except Exception as e:
            raise Exception(f"Error processing data: {str(e)}") from e


class EarthquakeDataAnalyzer:
    # Analyzes earthquake data.

    def __init__(self, data_reader, location_index, date_index, magnitude_index):
        # Initializes the EarthquakeDataAnalyzer.
        self.data_reader = data_reader
        self.location_index = location_index
        self.date_index = date_index
        self.magnitude_index = magnitude_index
        self.location_avg_magnitudes = defaultdict(lambda: {'count': 0, 'mean': 0})
        self.location_earthquake_count = defaultdict(int)

    def analyze_earthquake_data(self, filename):
        # Analyzes earthquake data and returns the location with the most earthquakes.
        try:
            earthquake_count = self.calculate_earthquakes_per_location(filename)
            location_with_most_earthquakes = max(earthquake_count, key=earthquake_count.get)
            return location_with_most_earthquakes
        except ValueError as e:
            raise ValueError("No earthquake data available.") from e
        except Exception as e:
            raise Exception(f"Error analyzing earthquake data: {str(e)}") from e

    def calculate_earthquakes_per_location(self, filename):
        # Calculates the number of earthquakes per location.
        try:
            for _, row in self.data_reader.read_csv_file(filename):
                location = row[self.location_index]
                self.location_earthquake_count[location] += 1
            return self.location_earthquake_count
        except Exception as e:
            raise Exception(f"Error calculating earthquakes per location: {str(e)}") from e

    def calculate_earthquakes_per_day(self, filename, timezone):
        # Calculates the number of earthquakes per day in the specified timezone.
        try:
            earthquake_count_per_day = defaultdict(int)
            for _, row in self.data_reader.read_csv_file(filename):
                date_str = row[self.date_index]
                date = self._parse_date(date_str)
                day = self._extract_day(date.astimezone(timezone))
                earthquake_count_per_day[day] += 1
            return earthquake_count_per_day
        except Exception as e:
            raise Exception(f"Error calculating earthquakes per day: {str(e)}") from e

    def calculate_average_magnitudes(self, row):
        # Calculates the average earthquake magnitude for each location.
        try:
            magnitude = float(row[self.magnitude_index])
            location_source = row[self.location_index]

            data = self.location_avg_magnitudes[location_source]
            data['count'] += 1
            delta = magnitude - data['mean']
            data['mean'] += delta / data['count']

        except (ValueError, IndexError) as e:
            raise Exception(f"Error computing average magnitudes: {str(e)}") from e

    @staticmethod
    def _parse_date(date_str):
        # Parses the date string into a datetime object.
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date

    @staticmethod
    def _extract_day(date):
        # Extracts the day from a datetime object.
        return date.strftime('%Y-%m-%d')
