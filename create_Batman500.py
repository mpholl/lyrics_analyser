import numpy as np
import pandas as pd
import os
from fuzzywuzzy import fuzz


def flag_similar_strings(playlist, threshold=80):
    strings = playlist[:, 0]
    flagged = []
    checked = set()
    remove = []
    
    for i, str1 in enumerate(strings):
        if str1 in checked:
            continue
        
        similar = []
        for j, str2 in enumerate(strings):
            if i != j and str2 not in checked:
                similarity = fuzz.ratio(str1, str2)
                if similarity >= threshold:
                    similar.append((j, similarity))
                    checked.add(str2)
        
        if similar:
            print(f'Similar Songs detected:')
            print(f'{i}: {playlist[i, 0]} by {playlist[i, 1]} is similar to')
            for sim_idx, score in similar:
                print(f'\t{sim_idx} {playlist[sim_idx, 0]} by {playlist[sim_idx, 1]}, with a score {score}')
                res = input('remove from playlist? [Y/n]')
                if res == 'n':
                    pass
                else:
                    remove += [sim_idx]
            flagged.append((i, similar))
            checked.add(str1)
    
    return flagged, remove



playlist = np.array(pd.read_csv('./data/Batman_playlist700.csv'))

flagged_strings, remove_idx = flag_similar_strings(playlist, threshold=80)

print(remove_idx)

print(flagged_strings)

# pd.DataFrame(playlist[:500]).to_csv('./data/BATMAN_playlist.csv', header=False, index=False)

