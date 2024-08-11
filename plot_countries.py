import numpy as np
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
import country_converter as coco


def count_countries(isrc_list):
    # Create a dictionary to store the count of each element

    countrylist = []

    for isrc in isrc_list:
        country = isrc[:2]

        # some countries have alternative codes 
        # USA
        if country in "QZ QT QM":
            country = "US"
        # Brazil
        if country in "BX BK BC":
            country = "BR"
        # Turks and Caicos
        if country in "DG":
            country = "TC"
        # UK
        if country in "GX":
            country = "UK"
        countrylist += [country]

    element_count = {}

    # Iterate over the list and count each element
    for item in countrylist:
        if item in element_count:
            element_count[item] += 1
        else:
            element_count[item] = 1
    
    return element_count

plt.style.use('thesisplots')

db_path = './data/BATMAN_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)


country_counts = count_countries(playlist_lyrics[:,-3])

country_counts = dict(sorted(country_counts.items(), key=lambda x:x[1], reverse=True))

country_names = coco.convert(country_counts.keys(), to="name_short")

for i in range(len(country_names)):
    if country_names[i] == "Turks and Caicos Islands":
        country_names[i] = "Turks \& Caicos"

song_numbers = list(country_counts.values())

plt.bar(country_names, song_numbers)

plt.xticks(rotation=70, ha='right')

plt.tight_layout()

plt.show()


