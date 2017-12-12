import random
import json
import pprint

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

def get_random_word():
    """ Opens english words dictionary and returns a random entry

    Returns
    ----------
    word : str
        Random english word.
    """
    #with open('english-words/words_dictionary.json') as json_file:
        #wordlist = json.load(json_file)
        #word = random.choice(list(wordlist.keys()))
    with open('dictionary/popular.txt') as text_file:
        wordlist = text_file.read().split()
        word = random.choice(wordlist)
    return word

def auth(username, scope):
    token = util.prompt_for_user_token(username, scope, redirect_uri = 'http://localhost/')
    return token

def generate_random_playlist(username, songs=20, special=""):
    # get the user id and playlist write auth
    token = auth(username, 'user-read-private playlist-modify-public')
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    user_id = sp.me()['id']
    print(user_id)

    track_ids = [] # container for random track ids

    # collect number of specified random songs
    for i in range(songs):
        random_offset = 0#random.randint(0,9)
        random_word = get_random_word()
        print ("searching " + special + " " + random_word + "...")
        result = sp.search(special + " " + random_word, limit=10, type='track', offset=random_offset)
        # if no results are returned search a new word
        while result['tracks']['items'] == []:
            random_word = get_random_word()
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

user = 'csteinmetz1'
generate_random_playlist(user)