import numpy as np
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt

plt.style.use('thesisplots')

db_path = './data/BATMAN700_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)


years = []
year_count = {}
for year in playlist_lyrics[:, -3]:
    year_tmp = int(year[5:7])
    if year_tmp<25:
        year_tmp += 2000
    else:
        year_tmp+= 1900
    if year_tmp in year_count:
        year_count[year_tmp] += 1
    else:
        year_count[year_tmp] = 1
    years += [year_tmp]

maxcount = 0
maxyear = 0
for year, count in zip(year_count.keys(), year_count.values()):
    if count > maxcount:
        maxcount = count*1
        maxyear = year*1

print(f'{maxcount} songs were recorded in {maxyear}')

low = min(years)//10*10
high = max(years)//10*10 + 11

for i in range(len(years)): 
    if years[i]<1960:
        print(f'{years[i]}: {playlist_lyrics[i, 0:2]}')

plt.hist(years, bins=np.arange(low, high, 10))
plt.xlabel('Decade Recorded')
plt.ylabel('Number of songs')

plt.xticks(np.arange(low, high-5, 10), rotation=20)

plt.tight_layout()

plt.savefig('figures/years_histograms.png', facecolor="white")
plt.show()