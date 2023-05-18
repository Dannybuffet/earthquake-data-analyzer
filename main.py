from pytz import timezone
from earthquake_analyzer.analyzer import EarthquakeDataAnalyzer, EarthquakeDataReader, EarthquakeDataHandler


def main():
    filename = "data/earthquake_data.csv"
    location_index = 20
    date_index = 0
    magnitude_index = 4

    # Create instances
    data_reader = EarthquakeDataReader()
    analyzer = EarthquakeDataAnalyzer(data_reader, location_index, date_index, magnitude_index)
    handler = EarthquakeDataHandler(analyzer, location_index, magnitude_index)

    # Calculate location with the most earthquakes
    most_earthquakes_location = analyzer.analyze_earthquake_data(filename)
    print(f"Location with Most Earthquakes: {most_earthquakes_location}")

    # Calculate earthquakes per day in UTC timezone
    utc_timezone = timezone('UTC')
    earthquakes_per_day_utc = analyzer.calculate_earthquakes_per_day(filename, utc_timezone)
    print("Earthquakes per Day in UTC Timezone:")
    for day, count in earthquakes_per_day_utc.items():
        print(f"Date: {day}, Count: {count}")

    # Calculate earthquakes per day in Pacific timezone
    pacific_timezone = timezone('US/Pacific')
    earthquakes_per_day_pacific = analyzer.calculate_earthquakes_per_day(filename, pacific_timezone)
    print("Earthquakes per Day in Pacific Timezone:")
    for day, count in earthquakes_per_day_pacific.items():
        print(f"Date: {day}, Count: {count}")

    # Process the earthquake data in real-time
    data_stream = data_reader.read_csv_file(filename)
    for data_row in data_stream:
        handler.process_data(data_row)
        # Print average magnitude for each location after processing each row
        for location, avg_magnitude_data in analyzer.location_avg_magnitudes.items():
            mean = avg_magnitude_data['mean']
            print(f"Average magnitude for location '{location}': {mean:.2f}")

if __name__ == '__main__':
    main()

