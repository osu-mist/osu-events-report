import requests
import sys
from argparse import ArgumentParser
from datetime import datetime, timedelta


def parse_arguments():
    today = datetime.now().strftime('%Y-%m-%d')
    last_year_today = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    parser = ArgumentParser()
    parser.add_argument(
        '-o',
        dest='output',
        choices=['txt', 'csv', 'html'],
        default='txt',
        help='output format (default: txt)')
    parser.add_argument(
        '-s',
        dest='start',
        metavar='<start date>',
        default=last_year_today,
        help='start of range (default: {})'.format(last_year_today))
    parser.add_argument(
        '-e',
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
