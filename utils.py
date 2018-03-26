import argparse
from datetime import datetime, timedelta


def parse_arguments():
    last_year_today = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--days',
        dest='days',
        default=365,
        help='return events within this many days after start (default: 365)'
    )
    parser.add_argument(
        '--start',
        dest='start',
        default=last_year_today,
        help='start of range (default: {})'.format(last_year_today))

    args = parser.parse_args()
    return args
