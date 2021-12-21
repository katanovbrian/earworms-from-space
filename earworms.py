import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

import tweepy

import random
import time
import schedule
import tkinter

import os
from dotenv import load_dotenv
load_dotenv()


NASA_KEY = os.environ.get('NASA_KEY')

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

TWITTER_KEY = os.environ.get('TWITTER_KEY')
TWITTER_SECRET  = os.environ.get('TWITTER_SECRET')

TWITTER_ACCESS  = os.environ.get('TWITTER_ACCESS')
TWITTER_ACCESS_SECRET  = os.environ.get('TWITTER_ACCESS_SECRET')


def earworm():
    nasa_raw_response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}').text
    nasa_response = json.loads(nasa_raw_response)
    nasa_title = nasa_response['title'].strip()
    nasa_title_split = nasa_title.split()
    nasa_date = nasa_response['date']
    
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist = []
    for word in nasa_title_split:
        spotify_response = sp.search(q=word, type='track',limit = 10)
        for track in spotify_response['tracks']['items']:
            playlist.append((track['name'],track['external_urls']['spotify']))
        
    spotify_url = random.choice(playlist)[1]

    auth = tweepy.OAuthHandler(TWITTER_KEY,TWITTER_SECRET)
    auth.set_access_token(TWITTER_ACCESS,TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)

    print(nasa_date,nasa_title,spotify_url)
    status = nasa_date + '\nAPOD Title: ' + nasa_title + '\nSong: ' + spotify_url   
    api.update_status(status)
    print("STATUS UPDATED")
    


schedule.every().day.at("14:50").do(earworm)

    
def main():
    earworm()
    while True:
        schedule.run_pending()
        time.sleep(1)
    
    
if __name__ == "__main__":
    main();
