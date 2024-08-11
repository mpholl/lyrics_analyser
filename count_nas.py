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
        lyrics = playlist_lyrics[i,-1].lower()

        # replace hyphens
        lyrics = lyrics.replace('-', ' ')
        nr_words = len(lyrics.split(' '))
        nr_na += [playlist_lyrics[i, -1].lower().count("na")]
        freq_na += [nr_na[-1]/nr_words]
    except AttributeError:
        nr_na += [0]
        freq_na += [0]
print(nr_na)