import os
import numpy as np

def find_duplicates(input_list):
    # Create a dictionary to store the count of each element
    element_count = {}
    duplicates = []
    
    # Iterate over the list and count each element
    for item in input_list:
        if item in element_count:
            element_count[item] += 1
        else:
            element_count[item] = 1
    
    # Identify duplicates (elements with a count greater than 1)
    for item, count in element_count.items():
        if count > 1:
            duplicates.append(item)
    
    return duplicates

db_path = './data/BATMAN1000_db.npy'

playlist_lyrics = np.load(db_path, allow_pickle=True)

ids = playlist_lyrics[:, -2]

unique_titles = len(set(ids))

duplicates = find_duplicates(ids)

print(f"There's {len(ids)} titles in the playlist, of which {unique_titles} are unique.")

duplicate_titles = []

for duplicate in duplicates:
    title = playlist_lyrics[np.where(playlist_lyrics[:, -2] == duplicate), 0]
    print(title[0][0])

print(f"the duplicates' ids are {duplicates}")