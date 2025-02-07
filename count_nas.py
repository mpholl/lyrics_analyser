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
        nr_na += [lyrics.lower().count("na")]
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
plt.xlabel('Number of "na"')
plt.ylabel('Songs')
plt.tight_layout()
plt.savefig('figures/absolute_nas_hist.png', facecolor='white')
plt.close()

nr_na = np.array(nr_na)
nr_na[np.where(np.isnan(nr_na))] = 0
freq_na = np.array(freq_na)
freq_na[np.where(np.isnan(freq_na))] = 0
absolute_idx = np.argsort(nr_na)
absolute_idx = absolute_idx[::-1]

relative_idx = np.argsort(freq_na)
relative_idx = relative_idx[::-1]

fig = plt.figure()
figsize = fig.get_size_inches()
plt.close()

fig = plt.figure(figsize=(figsize[0]*1.5, figsize[1]))

plt.barh(playlist_lyrics[absolute_idx[:10][::-1], 0], nr_na[absolute_idx[:10][::-1]])
plt.yticks(ha='right', fontsize=16)
plt.xlabel('Number of "na"')
plt.tight_layout()
plt.savefig('figures/absolute_nas.png', facecolor='white')
plt.show()

fig = plt.figure(figsize=(figsize[0]*1.5, figsize[1]))

plt.barh(playlist_lyrics[relative_idx[:10][::-1], 0], freq_na[relative_idx[:10][::-1]])
plt.yticks(ha='right', fontsize=16)
plt.xlabel('"na" per word')
plt.tight_layout()
plt.savefig('figures/relative_nas.png', facecolor='white')
plt.show()