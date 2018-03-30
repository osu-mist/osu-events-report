import csv
import os
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta
from prettytable import PrettyTable
from utils import parse_arguments, send_request


API_BASE_URL = 'https://events.oregonstate.edu/api/2'
EVENTS_URL = API_BASE_URL + '/events'
EVENT_FILTERS_URL = EVENTS_URL + '/filters'


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
    global events, file_name

    event_dicts = []
    titles = ['Field ID', 'Field Name', '# of Events', 'Field Type']

    # orgnaize event details
    for field in fields:
        event_dict = defaultdict(lambda: {
            'name': 'Uncatagorized',
            'count': 0,
            'type': field
        })

        for event in events:
            event_instances = len(event['event']['event_instances'])

            if field in event['event']:
                for item in event['event'][field]:
                    event_dict[str(item['id'])]['name'] = item['name']
                    event_dict[str(item['id'])]['count'] += event_instances
            else:
                event_dict['N/A']['count'] += event_instances

        event_dicts.append(OrderedDict(sorted(event_dict.items())))

    # generate output file
    if output == 'csv':
        with open('{}.{}'.format(file_name, output), 'w') as f:
            csv_write = csv.DictWriter(f, fieldnames=titles)
            csv_write.writeheader()
            for event_dict in event_dicts:
                for field_id, info in event_dict.items():
                    csv_write.writerow({
                        'Field ID': field_id,
                        'Field Name': info['name'],
                        '# of Events': info['count'],
                        'Field Type': info['type']
                    })
    else:
        table = PrettyTable(titles)
        table.align = 'l'
        for event_dict in event_dicts:
            for field_id, info in event_dict.items():
                table.add_row([field_id, info['name'], info['count'], info['type']])
        content = table.get_html_string() if output == 'html' else table.get_string()
        with open('{}.{}'.format(file_name, output), 'w') as f:
            f.write(content)


def main():
    global output, events, end, file_name, start

    args = parse_arguments()
    output = os.environ['OUTPUT'] if 'OUTPUT' in os.environ else args.output

    start = os.environ['START'] if 'START' in os.environ else args.start
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end = os.environ['END'] if 'END' in os.environ else args.end
    final_end_date = end_date = datetime.strptime(end, '%Y-%m-%d')
    days = (end_date - start_date).days
    file_name = 'osu-events-from-{}-to-{}'.format(start, end)

    events = []
    while days > 365:
        end_date = start_date + timedelta(days=365)
        end = end_date.strftime('%Y-%m-%d')

        events += get_events()

        start_date = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
        start = start_date.strftime('%Y-%m-%d')
        end_date = final_end_date
        end = end_date.strftime('%Y-%m-%d')

        days = (end_date - start_date).days

    events += get_events()

    fields = [event_filter for event_filter in send_request(EVENT_FILTERS_URL).keys()]
    fields.append('departments')
    create_report_by(fields)


if __name__ == '__main__':
    main()
