# ThisDayInMusic

[![Build Status](https://travis-ci.org/Shemahmforash/thisdayinmusic.net.svg?branch=master)](https://travis-ci.org/Shemahmforash/thisdayinmusic.net)

ThisDayInMusic is a python app built with django that aims at showing the list of events that happened on a particular day in the history of music and, at the same time, generate spotify playlists for those same events.

It's currently running live at www.thisdayinmusic.net

## Installation

This app makes use of [pipenv](https://github.com/kennethreitz/pipenv), so you need to have it installed first.

After installing pipenv, use it to install the requirements of this project: `pipenv install`.

## Running
To run the app you first must create a .env file:

```
cp thisdayinmusic/.env.example thisdayinmusic/.env
```

and set the django secret key in it. After that, you can run it with:

```
pipenv run python manage.py runserver
```

You can now point your browser to http://127.0.0.1:8000 to use the app.

## Testing

To run the tests:
```
pipenv run python manage.py test
```

In order to run the functional tests, you'll need first to have the Firefox browser installed and the [geckodriver](https://github.com/mozilla/geckodriver/releases) installed and available in your system path.
