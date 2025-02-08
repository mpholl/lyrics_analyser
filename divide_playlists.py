import numpy as np
import pandas as pd
import pycountry

def remove_value(arr, value):
    """
    Remove all occurrences of a specific value from a NumPy array.
    
    Parameters:
    arr (np.ndarray): Input NumPy array.
    value: The value to be removed.
    
    Returns:
    np.ndarray: New array with the value removed.
    """
    return arr[arr != value]

def remove_from_list(available_idx, list_idx):
    """
    Remove all chosen idx from the available list
    """
    for i in list_idx:
        available_idx = remove_value(available_idx, i)
    return available_idx


def save_csv(playlist, filename):
    """
    Save title and artist to a csv
    """
    playlist = np.array(playlist)
    pd.DataFrame(playlist[:, :2]).to_csv(filename, index=False, header=['Track name', 'Artist name'])

def get_years(playlist):
    years = []
    for year in playlist[:, -3]:
        year_tmp = int(year[5:7])
        if year_tmp<26:
            year_tmp += 2000
        else:
            year_tmp+= 1900
        years += [year_tmp]
    return np.array(years)

def iso_to_language_name(iso_code):
    try:
        language = pycountry.languages.get(alpha_2=iso_code)
        return language.name
    except AttributeError:
        return "Unknown"

playlist_length = 70

# load the playlist database
db_path = './data/BATMAN_db.npy'

playlist = np.load(db_path, allow_pickle=True)

all_playlists = []
# make list of indices

idx_available = np.arange(playlist.shape[0])
np.random.shuffle(idx_available)

# identify the fastest and slowest in the bpm list
# load bpm list, 
playlist_bpm = np.array(pd.read_csv('./data/BATMAN500_BPMsorted.csv'))

# identify index of slowest
slowest_id  = np.where(playlist[:, -2] == playlist_bpm[0,-1])[0][0]

# and fastest song
fastest_id  = np.where(playlist[:, -2] == playlist_bpm[-1,-1])[0][0]

# and remove indices from list
idx_available = remove_value(idx_available, slowest_id)
idx_available = remove_value(idx_available, fastest_id)
# and remove BATMAN
idx_available = remove_value(idx_available, 0)


# load introduction list 
introduction_list = np.array(pd.read_csv('./data/BATMAN500_introductions.csv'))
introduction_ids = []

for i in idx_available:
    if playlist[i, -2] in introduction_list:
        introduction_ids += [i]
# and remove from list
idx_available = remove_from_list(idx_available, introduction_ids)
all_playlists += [introduction_list]

# create disco dancy list
disco_ = np.array(pd.read_csv('./playlists/BATMAN500_disco.csv'))
disco_ids = []
for i in idx_available:
    if playlist[i, -2] in disco_[:,-1]:
        disco_ids += [i]
# and remove from list
idx_available = remove_from_list(idx_available, disco_ids)
all_playlists += [disco_]

# create ultimate na list
ultimate_na_ = [playlist[0]]
ultimate_na_ids = []
# get all candidates

for i in idx_available:
    if 'nana' in playlist[i,0].lower().replace('-', '').replace(' ', ''):
        ultimate_na_ += [playlist[i]]
        ultimate_na_ids += [i]
    if len(ultimate_na_) > playlist_length:
        break
# save csv, with header
save_csv(ultimate_na_, 'playlists/BATMAN500_ultimate_na.csv')
# and remove from list
idx_available = remove_from_list(idx_available, ultimate_na_ids)
all_playlists += [ultimate_na_]

languages = np.loadtxt('languages.txt', dtype=str)
# create unknown language list

unknown_ = [playlist[0]]
unknown_ids = []

for i in idx_available:
    language = iso_to_language_name(languages[i])
    if language == 'Unknown':
        unknown_ += [playlist[i]]
        unknown_ids += [i]
    if len(unknown_) > playlist_length:
        break
# save csv, with header
save_csv(unknown_, 'playlists/BATMAN500_unknown.csv')
# and remove from list
idx_available = remove_from_list(idx_available, unknown_ids)
all_playlists += [unknown_]

# create the questionable list
questionable_ = [playlist[0]]
questionable_ids = []
for i in idx_available: 
    try:
        with open(f"lyrics/{playlist[i, -2]}.txt", "r") as lyrics_file:
            lyrics = lyrics_file.read()

        
    except FileNotFoundError:
        # if no lyrics, it's automatic to the list
        lyrics = ''
    # make lowercase, to catch Na and NA
    lyrics = lyrics.lower()

    # replace hyphens
    lyrics = lyrics.replace('-', ' ')
    lyrics = lyrics.replace(' ', '')
    if not 'nana' in lyrics:
        questionable_ += [playlist[i]]
        questionable_ids += [i]

    if len(questionable_) > playlist_length:
        break

# save csv, with header
save_csv(questionable_, 'playlists/BATMAN500_questionable.csv')
# and remove from list
idx_available = remove_from_list(idx_available, questionable_ids)
all_playlists += [questionable_]

# create negative vibes list
negative_vibes_ = [playlist[0]]
negative_vibes_ids = []

sentiments = np.load('sentiments.npy')
negativity_ = []
for i in idx_available:
    negativity = np.sqrt(np.sum(sentiments[i, [0, 1, 3, 5]]**2))
    if np.isnan(negativity):
        negativity=0
    negativity_ += [negativity]
negativity_ = np.argsort(negativity_)[::-1]

for i in negativity_:
    negative_vibes_ += [playlist[idx_available[i]]]
    negative_vibes_ids += [idx_available[i]]
    if len(negative_vibes_) > playlist_length:
        break
# save csv, with header
save_csv(negative_vibes_, 'playlists/BATMAN500_negative_vibes.csv')
# and remove from list
idx_available = remove_from_list(idx_available, negative_vibes_ids)
all_playlists += [questionable_]

# create decades list
decades_ = [playlist[0]]
decades_ids = []

years = get_years(playlist[idx_available])
years_idx = np.argsort(years)
years_idx = years_idx[np.linspace(0, len(years_idx)-1, playlist_length, dtype=int)]
for i in years_idx:
    decades_ += [playlist[idx_available[i]]]
    decades_ids += [idx_available[i]]
# save csv, with header
save_csv(decades_, 'playlists/BATMAN500_decades.csv')
# decades_ = np.array(decades_)
# pd.DataFrame(decades_[:, :-1]).to_csv('playlists/BATMAN500_decades.csv', index=False, header=['Track name', 'Artist name', 'Album','Playlist name','Type','ISRC','Spotify - id'])

# and remove from list
idx_available = remove_from_list(idx_available, decades_ids)
all_playlists += [decades_]



# create increasing bpm list
increasingbpm_ = [playlist[0]]
increasingbpm_ += [playlist[slowest_id]]
increasingbpm_ids = []

available_bpm = []
for i in idx_available:
    try:
        idx_bpm = np.where(playlist_bpm[:, -2] == playlist[i,-3])[0][0]
    except IndexError:
        pass
    available_bpm += [idx_bpm]
available_bpm = np.argsort(available_bpm)
available_bpm = available_bpm[np.linspace(0, len(available_bpm)-1, playlist_length, dtype=int)]

for i in available_bpm:
    increasingbpm_ += [playlist[idx_available[i]]]
    increasingbpm_ids = [idx_available[i]]

increasingbpm_ += [playlist[fastest_id]]
all_playlists += [increasingbpm_]

# save csv, with header
save_csv(increasingbpm_, 'playlists/BATMAN500_increasingbpm.csv')
# and remove from list
idx_available = remove_from_list(idx_available, increasingbpm_ids)

print(len(idx_available))
sum_lists = 0
for tmp_list in all_playlists:
    print(f'{len(tmp_list)}')
    sum_lists += len(tmp_list)

print(sum_lists)


