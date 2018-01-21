import random
import json
import pprint
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# add profanity slider to add profande words
# add option to choose randomly from songs in my personal playlists
# filter by popularity - just give two options - unpopular or popular or no filter
# add super low probablity of adding dad's beem songs or something else weird
# add as much language support as possible - have a mode where all word lists are fair game
# urban dictionary word of the day playlist

class random_word_generator():

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
    token = util.prompt_for_user_token(user_id, scope, redirect_uri = 'http://localhost/')
    return token

def generate_random_playlist(username, playlist_name, random_word_generator, songs=10, special=""):
    # get the user id and playlist write auth
    token = auth(username, 'user-read-private playlist-modify-public')
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    user_id = sp.me()['id']

    track_ids = [] # container for random track ids

    # collect number of specified random songs
    for i in range(songs):
        random_offset = random.randint(0,2)
        random_word = random_word_generator.get_random_word()
        print ("searching " + special + " " + random_word + "...")
        result = sp.search(special + " " + random_word, limit=10, type='track', offset=random_offset)
        # if no results are returned search a new word
        while result['tracks']['items'] == []:
            random_word = random_word_generator.get_random_word()
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

def get_user_playlist_tracks():
    scope = 'user-read-private playlist-modify-public'
    token = auth('user', scope)
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    user_id = sp.me()['id']
    user_playlist_data = sp.user_playlists(user_id, limit=25, offset=random.randint(0,50))
    user_playlist_ids = [playlist['id'] for playlist in user_playlist_data['items'] if playlist['name'][0:10] != "Popularity"]
    print("Found", len(user_playlist_ids), "user playlists")
    user_playlist_track_ids = []
    for playlist_id in user_playlist_ids:
        try: 
            track_ids_data = sp.user_playlist_tracks(user_id, playlist_id)
        except:
            print("Playlist not found. Skipping.")
        else:
            track_ids = [str(track_id['track']['id']) for track_id in track_ids_data['items']]
            user_playlist_track_ids += (track_ids)
    print("Found", len(user_playlist_track_ids), "tracks in user playlists")

    popularity = 10
    # add filter for exluding artists that are already in your playlists
    # rework the structure so there is a clear filtering architecture - this is about the filtering
    random_track_ids = random.sample(user_playlist_track_ids, 5)

    new_tracks = sp.recommendations(seed_tracks=random_track_ids, limit=10, max_popularity=popularity)
    new_track_ids = [track['id'] for track in new_tracks['tracks']]
    print("Found", len(new_track_ids), "new tracks based on seeds")

    playlist_name = "Popularity " + str(popularity) 
    # create new playlist and get its id
    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    new_playlist_id = new_playlist['id']

    # add random tracks to new playlist
    sp.user_playlist_add_tracks(user_id, new_playlist_id, new_track_ids)

get_user_playlist_tracks()

#r = random_word_generator(weirdness=3)
#generate_random_playlist(user, "My random playlist", r)

