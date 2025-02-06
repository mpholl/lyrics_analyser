import numpy as np
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt

plt.style.use('thesisplots')

db_path = './data/BATMAN_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)


years = []
for year in playlist_lyrics[:, -3]:
    year_tmp = int(year[5:7])
    if year_tmp<25:
        year_tmp += 2000
    else:
        year_tmp+= 1900
    years += [year_tmp]


low = min(years)//10*10
high = max(years)//10*10 + 11



plt.hist(years, bins=np.arange(low, high, 10))
plt.xlabel('Years')
plt.ylabel('Number of songs')

plt.xticks(np.arange(low, high-5, 10), rotation=20)

plt.tight_layout()

plt.savefig('figures/years_histograms.png')
plt.show()