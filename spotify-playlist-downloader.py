# This Scripts downloads every Song in every Playlist which is yours and sort them in Folders named like the Playlist.
# Important: You need to install youtube-dl via pip "pip install youtube-dl" and you need to install ffmpeg in the same Directory where the youtube-dl.exe is
# After that you need to create an App on https://developers.spotify.com and paste the client_id, client_secret and redirect_uri into the script.
# Thanks to the Examples from the spotipy github repo (https://github.com/plamere/spotipy/tree/master/examples)

import spotipy
import os
import urllib.request
import re
import string
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID="Your CLient_ID goes here"
CLIENT_SECRET="Your Client_Secret goes here"
REDIRECT_URI="Your Redirection URI of the App"
PATH="The Path where this Script should save the music"

def get_tracks(results):
    artists = []
    tracks = []

    for i, item in enumerate(results['items']):
        track = item['track']
        artists.append(track['artists'][0]['name'])
        tracks.append(track['name'])
    return artists, tracks
            
if __name__ == '__main__':
    scope = 'playlist-read-private'
    watch_link = "https://www.youtube.com/watch?v="
    search_link = "https://www.youtube.com/results?search_query="
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI))
    playlists = sp.current_user_playlists()
    user_id = sp.me()['id']
    for playlist in playlists['items']:
        if playlist['owner']['id'] == user_id:
            print(f"\n\nDownloading Playlist: {playlist['name']}...")
            print(f"Total tracks: {playlist['tracks']['total']}\n")
            directory = playlist['name'] + "\\"
            create_dir = os.path.join(PATH, directory)
            if os.path.exists(create_dir):
                os.chdir(create_dir)
            else:
                os.mkdir(create_dir)
                os.chdir(create_dir)
            results = sp.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            kuenstler, songs = get_tracks(tracks)
            for i, song in enumerate(songs):
                pre_url = str(kuenstler[i]) + " - " + str(song)
                pre_url = pre_url.replace(" ", "+").replace("ä", "ae").replace("ü", "ue"). replace("ö", "oe")
                for char in string.punctuation:
                    if char != "+":
                        pre_url = pre_url.replace(char, "")
                pre_url = pre_url.encode("ascii", "ignore").decode()
                url = search_link + pre_url
                html = urllib.request.urlopen(url)
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                youtube_vid = watch_link + video_ids[0]
                os.system("youtube-dl -x --audio-format mp3 " + youtube_vid)
