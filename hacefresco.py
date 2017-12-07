import spotipy
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
import os

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

results = sp.search("sondorblue", limit=1)
pprint.pprint(results['tracks']['items'][0]['album'])