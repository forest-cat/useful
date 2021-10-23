import requests
import re
import os
import urllib
import string
import threading

CLIENT_ID = 'ID here' # The Client ID of your Application
CLIENT_SECRET = 'Secret here' #  The Client Secret of your Application

BASE_URL = 'https://api.spotify.com/v1/' # The Base URL which points to the Spotify API
AUTH_URL = 'https://accounts.spotify.com/api/token' # This URL points towards the Authentification System from Spotify

LIMIT = 50 # Change how much Songs per request will be received, range from 1-100 allowed.
OFFSET = 0 # Please don't change this one to make sure every Song is covered and donwloaded

PATH="Your Path here" # Here is the Path were the files should be saved


watch_link = "https://www.youtube.com/watch?v="
search_link = "https://www.youtube.com/results?search_query="

os.system("cls")
playlist_link = input("Please input the Spotify Playlist URL: ")

all_songs, song_video_list, first_list, second_list, third_list, fourth_list, fith_list = [], [], [], [], [], [], []

auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

access_token = auth_response.json()['access_token']

# This is the Building what is in the Request, if you know what youre doing you can change it. But be carefully. 
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
parameters = {
    'offset': OFFSET,
    'limit': LIMIT
}

id = str(playlist_link)[34:56]

def make_request(headers, parameters):
    r = requests.get(BASE_URL + 'playlists/' + id + "/tracks", headers=headers, params=parameters)
    r_json = r.json()
    for item in r_json['items']:
        all_songs.append(item['track']['name'] + " - " + item['track']['artists'][0]['name'])
    return r_json

def download_track(song_vid_list):
    os.chdir(PATH)
    for video_link in song_vid_list:
        os.system("youtube-dl -x --audio-format mp3 -i" + video_link)

def create_thread(function, name, arguments, ):
    thread = threading.Thread(target=function, name=name, args=(arguments,), daemon=True)
    thread.start()
    return thread

try:
    request = make_request(headers=headers, parameters=parameters)
except Exception as e:
    os.system("cls")
    print(f"An Unknown error occurred:\n{e}")


while len(request['items']) >= 50:
    OFFSET += 50
    parameters = {
        'offset': OFFSET,
        'limit': LIMIT
    }
    request = make_request(headers=headers, parameters=parameters)
    

for i, item in enumerate(all_songs):
    pre_url = item.replace(" ", "+").replace("ä", "ae").replace("ü", "ue"). replace("ö", "oe")
    for char in string.punctuation:
        if char != "+":
            pre_url = pre_url.replace(char, "")
    pre_url = pre_url.encode("ascii", "ignore").decode()
    url = search_link + pre_url
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    youtube_vid = watch_link + video_ids[0]
    song_video_list.append(youtube_vid)
    os.system("cls")
    print(f'Getting Youtube Link for: "{item}" {i+1}/{len(all_songs)}')
    

counter = 0
for track in song_video_list:
    if counter == 0:
        first_list.append(track)
        counter += 1
        continue
    elif counter == 1:
        second_list.append(track)
        counter += 1
        continue
    elif counter == 2:
        third_list.append(track)
        counter += 1
        continue
    elif counter == 3:
        fourth_list.append(track)
        counter += 1
        continue
    elif counter == 4:
        fith_list.append(track)
        counter = 0
        continue

thread_1 = create_thread(download_track, "Thread_1", first_list)
thread_2 = create_thread(download_track, "Thread_2", second_list)
thread_3 = create_thread(download_track, "Thread_3", third_list)
thread_4 = create_thread(download_track, "Thread_4", fourth_list)
thread_5 = create_thread(download_track, "Thread_5", fith_list)

thread_1.join()
thread_2.join()
thread_3.join()
thread_4.join()
thread_5.join()
