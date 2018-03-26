import json
import requests
import sys
from collections import defaultdict, OrderedDict
from prettytable import PrettyTable
from utils import parse_arguments


API_BASE_URL = 'https://events.oregonstate.edu/api/2/'
EVENTS_URL = API_BASE_URL + 'events/'
DEPARTMENTS_URL = API_BASE_URL + 'departments/'


def send_request(url, params=None):
    res = requests.get(url, params=params)
    if res.status_code != 200:
        sys.exit('HTTP status code: {}'.format(res.status_code))
    else:
        return res.json()


def get_events():
    params = {
        'start': args.start,
        'days': args.days,
        'pp': 100,
        'page': 1
    }
    res = send_request(EVENTS_URL, params)
    events = res['events']
    while res['page']['current'] < res['page']['total']:
        params['page'] += 1
        res = send_request(EVENTS_URL, params)
        events += res['events']

    return events


def create_events_report(events):
    events_by_department = defaultdict(int)

    for event in events:
        if 'departments' in event['event']:
            for department in event['event']['departments']:
                events_by_department[str(department['id'])] += len(event['event']['event_instances'])
        else:
            events_by_department['N/A'] += len(event['event']['event_instances'])

    events_by_department = OrderedDict(sorted(events_by_department.items()))

    department_table = PrettyTable(['ID', 'Name', '# of Events'])
    department_table.align = 'l'

    for department_id, events in events_by_department.items():
        if department_id == 'N/A':
            department_name = 'Uncatagorized'
        else:
            department_name = send_request(DEPARTMENTS_URL + department_id)['department']['name']
        department_table.add_row([department_id, department_name, events])
    print(department_table)


def main():
    events = get_events()
    create_events_report(events)


if __name__ == '__main__':
    args = parse_arguments()
    main()
