import requests
from datetime import datetime


def _create_date_params(day, month):
    payload = {}
    if month is not None and day is not None:
        date = datetime.strptime(
            '{} {}'.format(day, month), '%d %B')

        payload['day'] = date.strftime('%d')
        payload['month'] = date.strftime('%m')

    return payload


def _call_api(address, payload):
    result = requests.get(
        address,
        params=payload
    )
    return result.json()


class EventService:
    RESULTS_PER_PAGE = 15
    DEFAULT_FIELDS = ['artist', 'date', 'description', 'type']

    def __init__(self, base_address):
        self.base_address = base_address

    def events(self, month=None, day=None, page=1):
        address = '%s/event/' % self.base_address

        date_payload = _create_date_params(day, month)

        payload = {
            'offset': self.offset(page),
            'fields[]': self.DEFAULT_FIELDS,
        }

        payload.update(date_payload)

        return _call_api(address, payload)

    def playlist(self, month=None, day=None):
        address = '%s/playlist/' % self.base_address

        payload = _create_date_params(day, month)

        return _call_api(address, payload)

    def offset(self, page):
        return self.RESULTS_PER_PAGE * (page - 1) if page and page > 0 else 0
