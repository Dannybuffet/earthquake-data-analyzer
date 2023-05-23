from earthquake_analyzer.data_analyzer import EarthquakeDataAnalyzer
from earthquake_analyzer.data_reader import EarthquakeDataReader


def main():
    filename = "data/earthquake_data.csv"
    location_index = 20
    date_index = 0
    magnitude_index = 4
    timezones = ['UTC', 'US/Pacific']

    try:
        analyzer = EarthquakeDataAnalyzer(location_index, date_index, magnitude_index, timezones)

        # Process the earthquake data from the CSV.
        data_reader = EarthquakeDataReader.read_csv_file(filename)

        for row in data_reader:
            analyzer.process_data([row])

            # Print average magnitudes for each location after processing the row.
            for location, avg_magnitude_data in analyzer.location_avg_magnitudes.items():
                mean = avg_magnitude_data['mean']
                print(f"Average magnitude for location '{location}': {mean:.2f}")

        # Calculate location with the most earthquakes.
        most_earthquakes_location = analyzer.get_location_with_most_earthquakes()
        print(f"Location with Most Earthquakes: {most_earthquakes_location}")

        # Calculate earthquakes per day in specified timezones.
        for timezone in timezones:
            earthquakes_per_day = analyzer.get_earthquakes_per_day_by_timezone(timezone)
            print(f"Earthquakes per Day in {timezone} Timezone:")
            for day, count in earthquakes_per_day.items():
                print(f"Date: {day}, Count: {count}")

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{filename}' not found.") from e
    except Exception as e:
        raise Exception(f"Error processing data: {str(e)}") from e


if __name__ == '__main__':
    main()
