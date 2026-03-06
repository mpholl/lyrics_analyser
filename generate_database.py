import os
import numpy as np
import pandas as pd
from lyricsgenius import Genius

# authentification data for lyricsgenius
# ToDo: put token in file
with open('genius_token.txt', 'r') as token_file:
    token = token_file.read()

print(token)
genius = Genius(token)

# read playlist 
# to download the playlist, go to https://www.tunemymusic.com/transfer/spotify-to-file 
# and follow instructions there
db_path = './data/BATMAN1000_db.npy'

playlist = np.array(pd.read_csv('./data/Batman_playlist1000.csv',header=None))
print(f"the shape of the playlist is {playlist.shape}")

if os.path.exists(db_path):
    playlist_lyrics = np.load(db_path, allow_pickle=True)
else:
    playlist_lyrics = np.empty((playlist.shape[0], playlist.shape[1]+1), dtype=object)
    playlist_lyrics[:, :-1] = playlist 

# get lyrics data and combine to database

idx_nolyrics = []


song = None
for i in range(playlist_lyrics.shape[0]):
    if playlist_lyrics[i, -1] == None:
        print(f'{i}/{playlist_lyrics.shape[0]}')
        try:
            song = genius.search_song(playlist_lyrics[i, 0], playlist_lyrics[i, 1])
        except:
            pass
        try:
            print(len(song.lyrics.split(' ')))
            playlist_lyrics[i, -1] = song.lyrics
            with open(f"lyrics1000/{playlist_lyrics[i, -2]}.txt", "w") as lyrics_file:
                lyrics_file.write(song.lyrics)
        except AttributeError:
            idx_nolyrics += [i]
        np.save(db_path, playlist_lyrics)
        np.savetxt('data/idx_nolyrics.csv', idx_nolyrics, delimiter=',')

