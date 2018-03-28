# OSU Events Report

A OSU events report generator (Python 3) based on [Localist API](https://developer.localist.com/doc/api). `csv`, `html` or `txt` output format are supported.

## Usage

1. Install depentent packages via pip:

    ```
    $ pip install -r requirements.txt
    ```

2. Generate report as chosen format:

    ```
    $ python --help
    $ python osu-events-report.py -o csv -s '2018-01-31 -e 2018-04-30'
    ```

## Docker

1. Build image:

    ```
    $ docker build -t osu-events-report .
    ```

2. Pass arguments as environment variables to the container:

    ```
    $ docker run --rm \
                 -e OUTPUT='csv' \
                 -e START='2018-01-31' \
                 -e END='2018-04-30' \
                 -v "$(pwd)"/:/usr/src/app/ \ osu-events-report
    ```
