# Earthquake Analyzer

This repository contains a Python script for analyzing earthquake data from a CSV file. It calculates the location with the most earthquakes, earthquakes per day in different timezones, and average magnitudes per location.

## Requirements

- Python 3.x
- Pytz

## Installation

1. Clone the repository:

```bash
git clone https://github.com/dannybuffet/earthquake_data_analizer.git
```

2. Navigate to the repository directory:

```bash
cd earthquake_data_analizer
```

3. Set up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the main script and perform earthquake data analysis, use the following command:

```bash
python3 main.py
```

This will output the location with the most earthquakes, earthquakes per day in UTC timezone, earthquakes per day in Pacific timezone, and average magnitudes per location.

To run the tests and verify the correctness of the code, use the following command:

```bash
python3 tests/test.py
```
This will execute the unit tests for the classes EarthquakeDataReader and EarthquakeDataAnalyzer.

