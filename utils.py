import argparse
import requests
import sys
from datetime import datetime, timedelta


def parse_arguments():
    today = datetime.now().strftime('%Y-%m-%d')
    last_year_today = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--csv',
        dest='csv',
        action='store_true',
        help='export as a csv file')
    parser.add_argument(
        '--start',
        dest='start',
        metavar='<start date>',
        default=last_year_today,
        help='start of range (default: {})'.format(last_year_today))
    parser.add_argument(
        '--end',
        dest='end',
        metavar='<end date>',
        default=today,
        help='end of range (default: {})'.format(today)
    )

    args = parser.parse_args()
    return args


def send_request(url, params=None):
    res = requests.get(url, params=params)
    if res.status_code != 200:
        sys.exit('HTTP status code: {}'.format(res.status_code))
    else:
        return res.json()
