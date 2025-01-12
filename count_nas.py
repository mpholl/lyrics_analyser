import numpy as np
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt

plt.style.use('thesisplots')

db_path = './data/BATMAN_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)

nr_na = []
freq_na = []

for i in range(playlist_lyrics.shape[0]):
    try:
        with open(f"lyrics/{playlist_lyrics[i, -2]}.txt", "r") as lyrics_file:
            lyrics = lyrics_file.read()

        # make lowercase, to catch Na and NA
        lyrics = lyrics.lower()

        # replace hyphens
        lyrics = lyrics.replace('-', ' ')
        nr_words = len(lyrics.split(' '))
        nr_na += [playlist_lyrics[i, -1].lower().count("na")]
        freq_na += [nr_na[-1]/nr_words]
        if nr_na[-1]> 300:
            print('#'*20)
            print(f'title: {playlist_lyrics[i, 0]}')
            print(f' number of word: {nr_words}')
            print(f' number of nas {nr_na[-1]}')
            print(f' frequency of nas {freq_na[-1]}')
            print(lyrics)
    except FileNotFoundError:
        nr_na += [np.nan]
        freq_na += [np.nan]

plt.hist(nr_na)
plt.show()