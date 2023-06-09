from collections import defaultdict
from datetime import datetime
import pytz


class EarthquakeDataAnalyzer:
    def __init__(self, location_index, date_index, magnitude_index, timezones):
        """
        Initializes the EarthquakeDataAnalyzer.
        """
        self.location_index = location_index
        self.date_index = date_index
        self.magnitude_index = magnitude_index
        self.timezones = timezones
        self.location_avg_magnitudes = defaultdict(lambda: {'mean': 0, 'count': 0})
        self.location_earthquake_count = defaultdict(int)
        self.timezone_earthquake_count = defaultdict(lambda: defaultdict(int))

    def process_data(self, data_rows):
        """
        Processes the data rows, calculating average magnitudes, earthquakes per day, and earthquakes per location.
        """
        try:
            for row in data_rows:
                self.calculate_average_magnitudes(row)
                self.calculate_earthquakes_per_location(row)
                self.calculate_earthquakes_per_day_by_timezone(row)
        except Exception as e:
            raise Exception(f"Error processing data: {str(e)}") from e

    def calculate_average_magnitudes(self, row):
        """
        Calculates the average magnitudes for each location.
        The average magnitude is stored instead of the sum.

        By storing the average and updating it incrementally, we avoid the need to store the sum.

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

    def get_location_with_most_earthquakes(self):
        """
        Returns the location with the most earthquakes.
        """
        try:
            most_earthquakes_location = max(
                self.location_earthquake_count,
                key=self.location_earthquake_count.get
            )
            return most_earthquakes_location
        except Exception as e:
            raise Exception(f"Error getting location with most earthquakes: {str(e)}") from e

    def calculate_earthquakes_per_day_by_timezone(self, row):
        """
        Analyzes the number of earthquakes per day by timezone.
        """
        try:
            date_str = row[self.date_index]
            date = self._parse_date(date_str)
            for timezone in self.timezones:
                try:
                    date_with_timezone = date.astimezone(pytz.timezone(timezone)).date()
                    self.timezone_earthquake_count[timezone][date_with_timezone] += 1
                except pytz.UnknownTimeZoneError:
                    raise ValueError(f"Unknown time zone: {timezone}")
        except Exception as e:
            raise Exception(f"Error analyzing earthquakes per day by timezone: {str(e)}") from e

    def get_earthquakes_per_day_by_timezone(self, timezone):
        """
        Returns the count of earthquakes per day based on the timezone.
        """
        try:
            return self.timezone_earthquake_count[timezone]
        except Exception as e:
            raise Exception(f"Error getting earthquakes per day by timezone: {str(e)}") from e

    @staticmethod
    def _parse_date(date_str):
        """
        Parses the date string and returns a datetime object.
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return date
        except Exception as e:
            raise Exception(f"Error parsing date: {str(e)}") from e
