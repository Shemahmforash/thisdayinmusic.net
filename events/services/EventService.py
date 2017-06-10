import requests
from datetime import datetime


class EventService:

    API_ADDRESS = "http://thisdayinmusic.icdif.com/api/v0.1/event"

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
            EventService.API_ADDRESS,
            params=payload
        )

        return result.json()
