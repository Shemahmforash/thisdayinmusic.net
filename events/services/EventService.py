import requests
from datetime import datetime


class EventService:
    API_ADDRESS = "http://thisdayinmusic.icdif.com/api/v0.1/event"
    RESULTS_PER_PAGE = 15

    @staticmethod
    def events(month=None, day=None, page=1):
        payload = None

        if month is not None and day is not None:
            date = datetime.strptime(
                '{} {}'.format(day, month), '%d %B')

            payload = {
                'day': date.strftime('%d'),
                'month': date.strftime('%m'),
                'offset': EventService.offset(page),
            }

        result = requests.get(
            EventService.API_ADDRESS,
            params=payload
        )

        return result.json()

    @staticmethod
    def offset(page):
        return EventService.RESULTS_PER_PAGE * (page - 1) if page and page > 0 else 0
