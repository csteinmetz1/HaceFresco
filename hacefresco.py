import random
import json
import pprint

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

class random_words():

    def __init__(self, weirdness=1):
        if weirdness == 1:
           self. wordlist = open('dictionary/popular.txt').read().split()
        elif weirdness == 2:
            self.wordlist = open('dictionary/enable1.txt').read().split()
        else:
            self.wordlist = open('dictionary/unix-words').read().split()

    def get_random_word(self):
        """ Opens english words dictionary and returns a random entry

        Returns
        ----------
        word : str
            Random english word.
        """
        word = random.choice(self.wordlist)
        return word

def auth(username, scope):
    token = util.prompt_for_user_token(username, scope, redirect_uri = 'http://localhost/')
    return token

def generate_random_playlist(username, r, songs=20, special=""):
    # get the user id and playlist write auth
    token = auth(username, 'user-read-private playlist-modify-public')
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    user_id = sp.me()['id']
    print(user_id)

    track_ids = [] # container for random track ids

    # collect number of specified random songs
    for i in range(songs):
        random_offset = random.randint(0,2)
        random_word = r.get_random_word()
        print ("searching " + special + " " + random_word + "...")
        result = sp.search(special + " " + random_word, limit=10, type='track', offset=random_offset)
        # if no results are returned search a new word
        while result['tracks']['items'] == []:
            random_word = r.get_random_word()
            print ("searching " + special + " " + random_word + "...")
            result = sp.search(special + " " + random_word, limit=10, type='track', offset=random_offset)
        track_ids.append(result['tracks']['items'][0]['id'])
        print("added " + result['tracks']['items'][0]['name'] + " | " + result['tracks']['items'][0]['artists'][0]['name'])

    if special != '':
        playlist_name = special + ' Random Playlist'
    else:
        playlist_name = 'Random Playlist'

    # create new playlist and get its id
    playlists = sp.user_playlist_create(user_id, playlist_name, public=True)
    playlist_id = playlists['id']

    # add random tracks to new playlist
    sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)

r = random_words(weirdness=3)
user = 'csteinmetz1'
generate_random_playlist(user, r)