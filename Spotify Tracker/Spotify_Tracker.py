import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

from pathlib import Path

# Authorization Code Flow: Enter your credentials below.


def get_spotify_current_song(sp, username):
    # Used to get the current song playing on Spotify

    results = sp.current_user_playing_track()
    song_name = results['item']['name']
    artist_name = results['item']['artists'][0]['name']
    album_name = results['item']['album']['name']
    release_date = results['item']['album']['release_date'][0:4]

    print(
        f"{username} is currently listening to:\n\n{artist_name} - {song_name}\n({album_name}, {release_date})\n")


def setup_credentials(credentials):
    # sets up the credentials for accessing Spotify API

    scope = "user-read-currently-playing"
    client_credentials_manager = SpotifyClientCredentials(
        client_id=credentials["client_id"], client_secret=credentials["client_secret"])

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    token = util.prompt_for_user_token(
        credentials["username"], scope, credentials["client_id"], credentials["client_secret"], credentials["redirect_uri"])

    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", credentials["username"])

    return sp


def get_credentials(credentials):

    filepath = Path.cwd()
    filename = f"{filepath}\Files\credentials.txt"

    with open(filename, "r") as file:
        lines = file.readlines()

    # TODO: Update this, very messy code
    credentials["client_id"] = lines[0].strip()
    credentials["client_secret"] = lines[1].strip()
    credentials["redirect_uri"] = lines[2].strip()
    credentials["username"] = lines[3].strip()


def main():
    credentials = {
        "client_id": "0",
        "client_secret": "0",
        "redirect_uri": "0",
        "username": "0"
    }

    # get credentials from file
    get_credentials(credentials)

    # setup credentials for accessing Spotify API
    sp = setup_credentials(credentials)

    # get current song playing on Spotify
    get_spotify_current_song(sp, credentials["username"])

    # keep the terminal from closing
    keep_open = input("")


if __name__ == "__main__":
    main()