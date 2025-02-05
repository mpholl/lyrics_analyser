import numpy as np
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt
import pycountry
from langdetect import detect

def count_languages(lyrics_list):
    # get the languages from the lyrics
    language_list = []
    for lyrics in lyrics_list:
        if lyrics == '':
            language = 'None'
        else:
            language = detect(lyrics)
        # print(language)
        language_list += [language]

    # Create a dictionary to store the count of each element

    element_count = {}

    # Iterate over the list and count each element
    for item in language_list:
        if item in element_count:
            element_count[item] += 1
        else:
            element_count[item] = 1
    
    return element_count, language_list

def iso_to_language_name(iso_code):
    try:
        language = pycountry.languages.get(alpha_2=iso_code)
        return language.name
    except AttributeError:
        return "Unknown"

plt.style.use('thesisplots')

db_path = './data/BATMAN_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)


lyrics_ = []
for i in range(playlist_lyrics.shape[0]):
    try:
        with open(f"lyrics/{playlist_lyrics[i, -2]}.txt", "r") as lyrics_file:
            lyrics_ += [lyrics_file.read()]
    except FileNotFoundError:
        lyrics_ += ['']

language_counts, language_list = count_languages(lyrics_)

np.savetxt('languages.txt', language_list, fmt='%s')

language_counts = dict(sorted(language_counts.items(), key=lambda x:x[1], reverse=True))

language_names = [iso_to_language_name(key) for key in language_counts.keys()]

for i in range(len(language_names)):
    if language_names[i] == 'Swahili (macrolanguage)':
        language_names[i] = 'Swahili'

print(language_names)

song_numbers = list(language_counts.values())

plt.bar(language_names, song_numbers)

plt.xticks(rotation=70, ha='right')

plt.ylim(top=40)

for i, number in enumerate(song_numbers):
    if number>39:
        plt.text(language_names[i], 41, f'{number}', fontsize=16, rotation=70, ha='center')

plt.tight_layout()
plt.savefig('figures/languages_bars.png')
plt.show()


