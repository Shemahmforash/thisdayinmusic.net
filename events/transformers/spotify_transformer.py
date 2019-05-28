def _convert_playlist_url_to_embed(url):
    return url.replace("/playlist/", "/embed/playlist/")


def transform_spotify_playlist_to_thisdayinmusic_playlist(playlist):
    url_embed = _convert_playlist_url_to_embed(playlist["external_urls"]["spotify"])

    return {"id": playlist["id"], "url": url_embed}


def transform_spotify_user_to_thisdayinmusic_user(user):
    return user["id"]
