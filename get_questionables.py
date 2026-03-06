import numpy as np
import pandas as pd


def save_csv(playlist, filename):
    """
    Save title and artist to a csv
    """
    playlist = np.array(playlist)
    pd.DataFrame(playlist[:, :2]).to_csv(filename, index=False, header=['Track name', 'Artist name'])

def save_excel(playlist, filename):
    """
    Save the title and artist to excel
    """
    playlist = np.array(playlist)
    playlist_toxls = np.empty(shape=(playlist.shape[0], 4), dtype=object)
    playlist_toxls[:, :2] = playlist[:, :2]
    playlist_toxls[:, 2] = [f'=HYPERLINK("https://open.spotify.com/track/{playlist[i,-2]}", "Play")' for i in range(playlist.shape[0])]

    pd.DataFrame(playlist_toxls).to_excel(filename, index=False, header=['Track name', 'Artist name', 'link', 'checked'])

# load the playlist database
db_path = './data/BATMAN1000_db.npy'

playlist = np.load(db_path, allow_pickle=True)

idx_available = np.arange(playlist.shape[0])

no_lyrics = 0

# create the questionable list
questionable_ = []
questionable_ids = []
for i in idx_available[500:]: 
    try:
        with open(f"lyrics1000/{playlist[i, -2]}.txt", "r") as lyrics_file:
            lyrics = lyrics_file.read()

        
    except FileNotFoundError:
        # if no lyrics, it's automatic to the list
        lyrics = ''
        no_lyrics+=1
    # make lowercase, to catch Na and NA
    lyrics = lyrics + playlist[i, 0]
    lyrics = lyrics.lower()

    # replace hyphens
    lyrics = lyrics.replace('-', ' ')
    lyrics = lyrics.replace(' ', '')
    lyrics = lyrics.replace(',', '')
    if not 'nana' in lyrics and not 'nahnah' in lyrics:
        if False:#len(lyrics)>0:
            print(lyrics)
            print('')
            print(playlist[i,:2])
            print('')
            input('enter to continue')
        questionable_ += [playlist[i]]
        questionable_ids += [i]


# save csv, with header
save_csv(questionable_, 'playlists/BATMAN1000_questionable.csv')
save_excel(questionable_, 'playlists/BATMAN1000_questionable.xlsx')
print(f'songs without lyrics: {no_lyrics}')