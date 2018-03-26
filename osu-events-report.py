import json
import requests
from utils import parse_arguments


# constants variables
API_BASE_URL = 'https://events.oregonstate.edu/api/2/'
EVENTS_URL = API_BASE_URL + 'events'
DEPARTMENTS_URL = API_BASE_URL + 'departments'


def main():
    res = requests.get(EVENTS_URL, params={'start': args.start, 'days': args.days})
    print(json.dumps(res.json(), indent=4))


if __name__ == '__main__':
    args = parse_arguments()
    main()
