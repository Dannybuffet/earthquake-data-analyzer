import csv
from datetime import datetime
from collections import defaultdict


class EarthquakeDataReader:
    @staticmethod
    def read_csv_file(filename):
        """
        Reads a CSV file and yields rows.
        """
        try:
            with open(filename, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  
                for row in csv_reader:
                    yield row
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File '{filename}' not found.") from e
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}") from e


class EarthquakeDataAnalyzer:
    def __init__(self, location_index, date_index, magnitude_index):
        """
        Initializes the EarthquakeDataAnalyzer.
        """
        self.location_index = location_index
        self.date_index = date_index
        self.magnitude_index = magnitude_index
        self.location_avg_magnitudes = defaultdict(lambda: {'mean': 0, 'count': 0})
        self.location_earthquake_count = defaultdict(int)
        self.earthquake_count_per_day = defaultdict(int)

    def process_data(self, data_rows):
        """
        Processes the data rows, calculating average magnitudes, earthquakes per day, and earthquakes per location.
        """
        for row in data_rows:
            self.calculate_average_magnitudes(row)
            self.calculate_earthquakes_per_day(row)
            self.calculate_earthquakes_per_location(row)

    def calculate_average_magnitudes(self, row):
        """
        Calculates the average magnitudes for each location.
        The average magnitude is stored instead of the sum.

        By storing the average and updating it incrementally, we avoid the need to store the sum,
        ensuring memory efficiency and preventing potential memory overflow.

        The average magnitude is calculated by updating the count and mean values for each location source.

        """
        try:
            magnitude = float(row[self.magnitude_index])
            location_source = row[self.location_index]

            data = self.location_avg_magnitudes[location_source]
            data['count'] += 1
            total_magnitude = data['mean'] * (data['count'] - 1)
            data['mean'] = (total_magnitude + magnitude) / data['count']

        except (ValueError, IndexError) as e:
            raise Exception(f"Error computing average magnitudes: {str(e)}") from e

    def calculate_earthquakes_per_location(self, row):
        """
        Calculates the number of earthquakes per location.
        """
        try:
            location = row[self.location_index]
            self.location_earthquake_count[location] += 1
        except Exception as e:
            raise Exception(f"Error calculating earthquakes per location: {str(e)}") from e

    def calculate_earthquakes_per_day(self, row):
        """
        Calculates the number of earthquakes per day.
        """
        try:
            date_str = row[self.date_index]
            date = self._parse_date(date_str)
            self.earthquake_count_per_day[date] += 1
        except Exception as e:
            raise Exception(f"Error calculating earthquakes per day: {str(e)}") from e

    def calculate_location_with_most_earthquakes(self):
        """
        Determines the location with the most earthquakes.
        """
        try:
            location_with_most_earthquakes = max(
                self.location_earthquake_count, key=self.location_earthquake_count.get
            )
            return location_with_most_earthquakes
        except ValueError as e:
            raise ValueError("No earthquake data available.") from e
        except Exception as e:
            raise Exception(f"Error analyzing earthquake data: {str(e)}") from e

    def calculate_earthquakes_per_day_by_timezone(self, timezone):
        """
        Analyzes the number of earthquakes per day by timezone.
        """
        try:
            timezone_earthquake_count = defaultdict(int)
            for date, count in self.earthquake_count_per_day.items():
                date_with_timezone = date.astimezone(timezone).date()
                timezone_earthquake_count[date_with_timezone] += count
            return timezone_earthquake_count
        except Exception as e:
            raise Exception(f"Error analyzing earthquakes per day: {str(e)}") from e

    @staticmethod
    def _parse_date(date_str):
        """
        Parses the date string and returns a datetime object.
        """
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date

