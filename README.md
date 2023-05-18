# Earthquake Analyzer

This repository contains a Python script for analyzing earthquake data from a CSV file. It calculates the location with the most earthquakes, earthquakes per day in different timezones, and average magnitudes per location.

## Requirements

- Python 3.x
- PyTZ

## Installation

1. Clone the repository:

```shell
git clone https://github.com/username/repository.git
```

2. Navigate to the repository directory:

```shell
cd repository
```

3. Install the required dependencies:

```shell
pip install -r requirements.txt
```

## Usage

To run the main script and perform earthquake data analysis, use the following command:

```shell
python main.py
```

This will output the location with the most earthquakes, earthquakes per day in UTC timezone, earthquakes per day in Pacific timezone, and average magnitudes per location.

To run the tests and verify the correctness of the code, use the following command:

```shell
python tests/test.py
```
This will execute the unit tests for the classes EarthquakeDataReader, EarthquakeDataHandler, and EarthquakeDataAnalyzer.

