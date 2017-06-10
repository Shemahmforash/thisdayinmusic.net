import requests
from datetime import datetime


class EventService:

    def events(month=None, day=None):
        payload = None

        if(month is not None and day is not None):
            date = datetime.strptime(
                '{} {}'.format(day, month), '%d %B')

            payload = {
                'day': date.strftime('%d'),
                'month': date.strftime('%m')
            }

        result = requests.get(
            'http://thisdayinmusic.icdif.com/api/v0.1/event',
            params=payload
        )

        return result.json()
