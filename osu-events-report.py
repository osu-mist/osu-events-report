from collections import defaultdict, OrderedDict
from prettytable import PrettyTable
from utils import parse_arguments, send_request


API_BASE_URL = 'https://events.oregonstate.edu/api/2/'
EVENTS_URL = API_BASE_URL + 'events/'
EVENT_FILTERS_URL = EVENTS_URL + 'filters/'
DEPARTMENTS_URL = API_BASE_URL + 'departments/'


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

    # adjust response so that we can reuse the logic of create_table_by easily
    for event in events:
        for filter_name, filter_info in event['event']['filters'].items():
            event['event'][filter_name] = filter_info

    return events


def create_table_by(field):
    global events

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

    table = PrettyTable(['ID', '{}'.format(field), '# of Events'])
    table.align = 'l'

    for field_id, info in event_dict.items():
        table.add_row([field_id, info['name'], info['count']])

    print('{0} number of events by [{1}] since {2} {0}'.format(
        '*' * 5,
        field,
        args.start)
    )
    print('{}\n'.format(table))


def main():
    global events

    events = get_events()
    # create table for each event filter
    for event_filter in send_request(EVENT_FILTERS_URL).keys():
        create_table_by(event_filter)
    create_table_by('departments')


if __name__ == '__main__':
    args = parse_arguments()
    main()
