import requests


class EventService:
    def events():
        payload = None

        requests.get(
            'http://thisdayinmusic.icdif.com/api/v0.1/event',
            params=payload
        )
