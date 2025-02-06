import numpy as np
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
from sys import stdout


def count_artists(isrc_list):
    # Create a dictionary to store the count of each element

    element_count = {}

    # Iterate over the list and count each element
    counter = 0
    for item in isrc_list:
        if item in element_count:
            element_count[item] += 1
        else:
            element_count[item] = 1
        counter += 1

        
    return element_count

# plt.style.use('thesisplots')

db_path = './data/BATMAN_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)

artist_counts = count_artists(playlist_lyrics[:,1])

artist_counts = dict(sorted(artist_counts.items(), key=lambda x:x[1], reverse=True))

artist_names = np.array([key.replace('&', '\&') for key in artist_counts.keys()])

song_numbers = np.array([value for value in artist_counts.values()])

plt.style.use('thesisplots')
fig = plt.figure()
figsize = fig.get_size_inches()
plt.close()

# fig = plt.figure(figsize=(figsize[0]*2, figsize[1]))
min_songs = 2

plt.bar(artist_names[np.where(song_numbers>min_songs)], song_numbers[np.where(song_numbers>min_songs)])

plt.xticks(rotation=70, ha='right')
plt.ylabel('Songs')

plt.tight_layout()
plt.savefig('figures/artists_bars.png', facecolor='white')
plt.show()


