import os
import numpy as np
import pandas as pd
from lyricsgenius import Genius

# authentification data for lyricsgenius

token = 'epcJuY5iMfHrodv1JlmIJjSWct7OGMbwRbGd82MNw4kht6f-B9SzFCFs4c7JkfV1'

genius = Genius(token)

# read playlist

db_path = './data/BATMAN_db.npy'

playlist = np.array(pd.read_csv('./data/BATMAN_playlist.csv'))
print(f"the shape of the playlist is {playlist.shape}")

if os.path.exists(db_path):
    playlist_lyrics = np.load(db_path, allow_pickle=True)
else:
    playlist_lyrics = np.empty((playlist.shape[0], playlist.shape[1]+1), dtype=object)
    playlist_lyrics[:, :-1] = playlist 

# get lyrics data and combine to database

idx_nolyrics = []



for i in range(playlist_lyrics.shape[0]):
    if playlist_lyrics[i, -1] == None:
        try:
            song = genius.search_song(playlist_lyrics[i, 0], playlist_lyrics[i, 1])
        except:
            pass
        try:
            print(len(song.lyrics.split(' ')))
            playlist_lyrics[i, -1] = song.lyrics
            with open(f"lyrics/{playlist_lyrics[i, -2]}.txt", "w") as lyrics_file:
                lyrics_file.write(song.lyrics)
        except AttributeError:
            idx_nolyrics += [i]
        np.save(db_path, playlist_lyrics)
        np.savetxt('data/idx_nolyrics.csv', idx_nolyrics, delimiter=',')

