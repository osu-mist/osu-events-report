import argparse
import requests
import sys
from datetime import datetime, timedelta


def parse_arguments():
    today = datetime.now()
    last_year_today = (today - timedelta(days=365))

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--start',
        dest='start',
        default=last_year_today.strftime('%Y-%m-%d'),
        help='start of range (default: {})'.format(last_year_today))
    parser.add_argument(
        '--end',
        dest='end',
        default=today.strftime('%Y-%m-%d'),
        help='end of range (default: {})'.format(last_year_today)
    )

    args = parser.parse_args()
    return args


def send_request(url, params=None):
    res = requests.get(url, params=params)
    if res.status_code != 200:
        sys.exit('HTTP status code: {}'.format(res.status_code))
    else:
        return res.json()
