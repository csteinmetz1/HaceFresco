import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import random
import json

# choose random search term for wordlist
def randomWord():
    with open('english-words/words_dictionary.json') as wordlist:
        w = json.load(wordlist)
        q = random.choice(list(w.keys()))

    return q

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

result = sp.search(randomWord(), limit=1, type='track')
searches = 1

while result['tracks']['items'] == []:
    result = sp.search(randomWord(), limit=1, type='track')
    searches += 1

print(searches)
print(result)