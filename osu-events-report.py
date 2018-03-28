import csv
import os
from collections import defaultdict, OrderedDict
from prettytable import PrettyTable
from utils import parse_arguments, send_request


API_BASE_URL = 'https://events.oregonstate.edu/api/2/'
EVENTS_URL = API_BASE_URL + 'events/'
EVENT_FILTERS_URL = EVENTS_URL + 'filters/'
DEPARTMENTS_URL = API_BASE_URL + 'departments/'


def get_events():
    params = {'start': start, 'end': end, 'pp': 100, 'page': 1}
    res = send_request(EVENTS_URL, params)
    events = res['events']
    while res['page']['current'] < res['page']['total']:
        params['page'] += 1
        res = send_request(EVENTS_URL, params)
        events += res['events']

    # adjust response so that we can reuse the logic of create_table_by easily
    for event in events:
        for filter_name, filter_info in event['event']['filters'].items():
            event['event'][filter_name] = filter_info

    return events


def create_report_by(fields):
    global events

    titles = ['Field ID', 'Field Name', '# of Events', 'Field Type']
    table = PrettyTable(titles)
    table.align = 'l'

    for field in fields:
        event_dict = defaultdict(lambda: {'name': 'Uncatagorized', 'count': 0})

        for event in events:
            event_instances = len(event['event']['event_instances'])

            if field in event['event']:
                for item in event['event'][field]:
                    event_dict[str(item['id'])]['name'] = item['name']
                    event_dict[str(item['id'])]['count'] += event_instances
            else:
                event_dict['N/A']['count'] += event_instances

        event_dict = OrderedDict(sorted(event_dict.items()))

        for field_id, info in event_dict.items():
            table.add_row([field_id, info['name'], info['count'], field])

    if csv_file:
        csv_file_name = 'osu-events-from-{}-to-{}.csv'.format(start, end)
        print(csv_file_name)
    else:
        print(table.get_string())
        print('{0} OSU events from {1} to {2} {0}'.format('*' * 4, start, end))


def main():
    global csv_file, events, end, start

    args = parse_arguments()
    csv_file = os.environ['CSV'] if 'CSV' in os.environ else args.csv
    start = os.environ['START'] if 'START' in os.environ else args.start
    end = os.environ['END'] if 'END' in os.environ else args.end

    events = get_events()
    fileds = [event_filter for event_filter in send_request(EVENT_FILTERS_URL).keys()]
    fileds.append('departments')
    create_report_by(fileds)


if __name__ == '__main__':
    main()
