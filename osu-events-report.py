import json
import requests


# constants variables
API_BASE_URL = 'https://events.oregonstate.edu/api/2/'
EVENTS_URL = API_BASE_URL + 'events'
DEPARTMENTS_URL = API_BASE_URL + 'departments'


def main():
    res = requests.get(EVENTS_URL, params={'start': '2017-03-21', 'days': '365'})
    print(json.dumps(res.json(), indent=4))


if __name__ == '__main__':
    main()
