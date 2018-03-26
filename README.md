# OSU Events Report

A report generator (Python 3) of OSU events based on [Localist API](https://developer.localist.com/doc/api).

## Usage

1. Install depentent packages via pip:

    ```
    $ pip install -r requirements.txt
    ```

2. Generate report to terminal:

    ```
    $ python --help
    $ python osu-events-report.py --days=30 --start='2018-01-31'
    ```

3. Or export as `report.txt`:

    ```
    $ python osu-events-report.py > report.txt
    ```

## Docker

1. Build image:

    ```
    $ docker build -t osu-events-report .
    ```

2. Pass arguments as environment variables to the container:

    ```
    $ docker run --rm -e START='2018-01-31' -e DAYS='365' osu-events-report
    ```
