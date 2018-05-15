def transform_playlist_to_track_list(playlist):
    return playlist['response']['tracks']


def transform_tracks_to_track_ids_string(tracks):
    return ",".join([_remove_spotify_prefix(track) for track in tracks])


def _remove_spotify_prefix(track):
    return track['spotifyId'].rsplit(':', 1)[1]


def transform_event_api_response_to_model_list(events):
    return [_api_event_to_event_model(event) for event in events]


def _api_event_to_event_model(event):
    name = event.get('name', None)

    return Event(event["date"], event["description"], event["type"], name)


class Event(object):
    TWITTER_MSG_LEN = 140
    TWITTER_HASH_TAG = "#thisdayinmusic"
    TWITTER_USER = "@today_in_music"

    def __init__(self, event_date, description, event_type="Event", name=None):
        self.event_date = event_date
        self.description = description
        self.type = event_type
        self.name = name

        self.twitter_message = self._set_message()

    def _set_message(self):
        message = '%s - %s' % (self.event_date, self.description)

        if len(message) + len(' ' + self.TWITTER_HASH_TAG) <= self.TWITTER_MSG_LEN:
            message = '%s %s' % (message, self.TWITTER_HASH_TAG)

        if len(message) + len(' via ' + self.TWITTER_USER) <= self.TWITTER_MSG_LEN:
            message = '%s via %s' % (message, self.TWITTER_USER)

        return message
