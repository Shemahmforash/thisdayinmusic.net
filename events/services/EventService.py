import requests
from datetime import datetime


class EventService:
    RESULTS_PER_PAGE = 15
    DEFAULT_FIELDS = ['artist', 'date', 'description', 'type']

    def __init__(self, base_address):
        self.base_address = base_address

    def events(self, month=None, day=None, page=1):
        address = '%s/event/' % self.base_address

        payload = {
            'offset': self.offset(page),
            'fields[]': self.DEFAULT_FIELDS
        }

        if month is not None and day is not None:
            date = datetime.strptime(
                '{} {}'.format(day, month), '%d %B')

            payload['day'] = date.strftime('%d')
            payload['month'] = date.strftime('%m')

        result = requests.get(
            address,
            params=payload,
        )

        return result.json()

    def playlist(self):
        address = '%s/playlist/' % self.base_address

        result = requests.get(
            address,
        )

        return result.json()

    def offset(self, page):
        return self.RESULTS_PER_PAGE * (page - 1) if page and page > 0 else 0
