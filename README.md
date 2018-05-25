# ThisDayInMusic

[![Build Status](https://travis-ci.org/Shemahmforash/thisdayinmusic.net.svg?branch=master)](https://travis-ci.org/Shemahmforash/thisdayinmusic.net)

ThisDayInMusic is a python app built with django that aims at showing the list of events that happened on a particular day in the history of music and, at the same time, generate spotify playlists for those same events.

It's currently running live at www.thisdayinmusic.net

## Running
To run the app you first must create a .env file:

```
cp thisdayinmusic/.env.example thisdayinmusic/.env
```

and set the django secret key in it. After that, you can run it with:

```
docker-compose up -d
```

You can now point your browser to http://127.0.0.1:8000 to use the app.

## Testing

To run the tests:
```
make test
```
