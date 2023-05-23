import csv


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

