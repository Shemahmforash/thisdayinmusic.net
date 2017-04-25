import requests


class EventService:
    def events(month=None, day=None):
        payload = None

        if(month is not None and day is not None):
            payload = {'day': day, 'month': month}

        result = requests.get(
            'http://thisdayinmusic.icdif.com/api/v0.1/event',
            params=payload
        )

        return result.json()
