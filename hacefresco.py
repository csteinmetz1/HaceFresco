import random
import json
import pprint

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

def random_word(num=1):
    """ Opens english words dictionary and returns a random entry

    Parameters
    ----------
    num : int
        Number of random words to return.

    Returns
    ----------
    word : str
        List of num random english words.
    """
    with open('english-words/words_dictionary.json') as json_file:
        wordlist = json.load(json_file)
        words = []
        for i in range(num):
            words.append(random.choice(list(wordlist.keys())))
    return words

def auth(username, scope):
    token = util.prompt_for_user_token(username, scope, redirect_uri = 'http://localhost/')
    return token

def generate_random_playlist(username, songs=20):
    # get the user id and playlist write auth
    token = auth(username, 'user-read-private playlist-modify-public')
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    user_id = sp.me()['id']
    print(user_id)

    track_ids = [] # container for random track ids

    # collect number of specified random songs
    for i in range(songs):
        result = sp.search(random_word(), limit=1, type='track')
        # if no results are returned search a new word
        while result['tracks']['items'] == []:
            result = sp.search(random_word(), limit=1, type='track')
        track_ids.append(result['tracks']['items'][0]['id'])
        print("added " + result['tracks']['items'][0]['name'] + " | " + result['tracks']['items'][0]['artists'][0]['name'])

    playlist_name = 'Random Playlist'

    # create new playlist and get its id
    playlists = sp.user_playlist_create(user_id, playlist_name, public=True)
    playlist_id = playlists['id']

    # add random tracks to new playlist
    sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)

user = 'your-username'
generate_random_playlist(user)