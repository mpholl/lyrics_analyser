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
        # make lowercase, to catch Na and NA
        with open(f"lyrics/{playlist_lyrics[i, -2]}.txt", "r") as lyrics_file:
            lyrics = lyrics_file.read()

        lyrics = lyrics.lower()

        # replace hyphens
        lyrics = lyrics.replace('-', ' ')
        nr_words = len(lyrics.split(' '))
        nr_na += [playlist_lyrics[i, -1].lower().count("na")]
        freq_na += [nr_na[-1]/nr_words]
        if nr_na[-1]> 300:
            print('#'*20)
            print(playlist_lyrics[i, 0])
            print(nr_words)
            print(nr_na[-1])
            print(freq_na[-1])
            print(lyrics)
    except FileNotFoundError:
        nr_na += [np.nan]
        freq_na += [np.nan]

plt.hist(nr_na)
plt.show()