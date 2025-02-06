import requests
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

plt.style.use('thesisplots')

def get_spotify_token(client_id: str, client_secret: str) -> str:
    """Authenticate with the Spotify API and get an access token."""
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()["access_token"]

def get_playlist_tracks(playlist_id: str, client_id: str, client_secret: str) -> Dict[str, Dict[str, str]]:
    """Retrieve all playlist tracks along with the user who added them and when they were added."""
    access_token = get_spotify_token(client_id, client_secret)
    headers = {"Authorization": f"Bearer {access_token}"}
    
    track_info = {}
    limit = 100
    offset = 0
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    
    while True:
        response = requests.get(url, headers=headers, params={"limit": limit, "offset": offset})
        response.raise_for_status()
        data = response.json()
        
        for item in data.get("items", []):
            try:
                track_name = item["track"]["name"]
                added_by = item["added_by"]["id"]  # User who added the track
                added_at = item["added_at"]  # Timestamp when the track was added
                track_info[track_name] = {"added_by": added_by, "added_at": added_at}
            except TypeError:
                pass
        
        if len(data.get("items", [])) < limit:
            break  # Stop if fewer than `limit` items are returned
        offset += limit
    
    return track_info

def plot_playlist_additions(tracks: Dict[str, Dict[str, str]]):
    """Plot a histogram showing how many songs each user added per month."""
    data = defaultdict(lambda: defaultdict(int))
    
    namedict = {'sara.yrjonmaki': 'Sara',
                '12170270392': 'Chris', 
                'vasi.wil-de': 'vasi.wil-de',
                'zaeqqp3yof6e9w6lmzg6hlnbc': 'Clara', 
                'mphlipp': 'Max', 
                '1157348520': 'Paula', 
                '1135087484': 'Tekla',
                'emzu97': 'Emma', 
                'lukasbaker': 'Lukas', 
                'henryxciv': 'Henrik', 
                'yrjonmmi': 'yrjonmmi',
                'ahjni74wqroz32qd6qjloux0c': 'Eliel', 
                '1117209255': 'Michiel',
                '31zixrmqfngwxisdfnze33rikesq': 'Christopher', 
                'mineaeme': 'Minea', 
                'dana.re-de': 'Dana', 
                '1185794421': 'Saga',
                '1125122972': 'Moa', 
                '1i7xn2di4dwak7t843juy7mvt': 'Ruben', 
                'siryrj': 'siryrj', 
                }

    for track, info in tracks.items():
        # added_by = info["added_by"]
        added_by = namedict[info["added_by"]]
        added_at = datetime.fromisoformat(info["added_at"].replace("Z", ""))
        month = added_at.strftime("%Y-%m")
        data[month][added_by] += 1
    
    df = pd.DataFrame.from_dict(data, orient='index').fillna(0)
    df.sort_index(inplace=True)
    
    df.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab20b')
    plt.xlabel("Month")
    plt.ylabel("Number of Songs Added")
    # plt.title("Songs Added to Playlist Over Time by User")
    plt.legend(ncol=2, loc='upper left', facecolor='None', edgecolor='None')
    xticks = [i for i, date in enumerate(df.index) if date.endswith("-01") or date.endswith("-04") or date.endswith("-07") or date.endswith("-10")]
    plt.xticks(xticks, [df.index[i] for i in xticks], rotation=45)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    plt.figtext(0.99, 0.01, f'data from {dt_string}', ha='right', va='bottom', fontsize=16)
    plt.tight_layout()

CLIENT_ID = "5ce14ad82fd3490db1cd22c4f9ece633"
CLIENT_SECRET = "1c8c5ae74ee1433abdf5ec14b4dc795f"
PLAYLIST_ID = "2Ux546RCcWPReqzCemYbDr"

tracks = get_playlist_tracks(PLAYLIST_ID, CLIENT_ID, CLIENT_SECRET)
plot_playlist_additions(tracks)
plt.savefig('figures/added_month_user.png', facecolor='white')
plt.show()
