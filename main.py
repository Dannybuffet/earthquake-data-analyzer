mport pytz 
from earthquake_analyzer.analyzer import EarthquakeDataAnalyzer, EarthquakeDataReader


def main():
    filename = "data/earthquake_data.csv"
    location_index = 20
    date_index = 0
    magnitude_index = 4

    try:
        analyzer = EarthquakeDataAnalyzer(location_index, date_index, magnitude_index)

        # Process the earthquake data from the CSV.
        data_reader = EarthquakeDataReader.read_csv_file(filename)
        analyzer.process_data(data_reader)

        # Calculate location with the most earthquakes.
        most_earthquakes_location = analyzer.calculate_location_with_most_earthquakes()
        print(f"Location with Most Earthquakes: {most_earthquakes_location}")

        # Calculate earthquakes per day in UTC timezone.
        utc_timezone = pytz.timezone('UTC')
        earthquakes_per_day_utc = analyzer.calculate_earthquakes_per_day_by_timezone(utc_timezone)
        print("Earthquakes per Day in UTC Timezone:")
        for day, count in earthquakes_per_day_utc.items():
            print(f"Date: {day}, Count: {count}")

        # Calculate earthquakes per day in Pacific timezone.
        pacific_timezone = pytz.timezone('US/Pacific')
        earthquakes_per_day_pacific = analyzer.calculate_earthquakes_per_day_by_timezone(pacific_timezone)
        print("Earthquakes per Day in Pacific Timezone:")
        for day, count in earthquakes_per_day_pacific.items():
            print(f"Date: {day}, Count: {count}")

        # Process earthquake data in real-time
        data_stream = EarthquakeDataReader.read_csv_file(filename)
        for data_row in data_stream:
            analyzer.process_data([data_row])
            # Print average magnitude for each location.
            for location, avg_magnitude_data in analyzer.location_avg_magnitudes.items():
                mean = avg_magnitude_data['mean']
                print(f"Average magnitude for location '{location}': {mean:.2f}")

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{filename}' not found.") from e
    except Exception as e:
        raise Exception(f"Error processing data: {str(e)}") from e


if __name__ == '__main__':
    main()

