import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import streamlit as st

# Spotify API credentials (replace with your own)
SPOTIPY_CLIENT_ID = '21d6d83c437c476dad8b3b75f8875f55'
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'


# Scope to access user's top tracks and artists
SCOPE = 'user-top-read'

# Authenticate with Spotify API
auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)

sp = spotipy.Spotify(auth_manager=auth_manager)

# Test if the authentication is working by printing the current user profile
'''user_profile = sp.current_user()
print("Authenticated user:", user_profile['display_name'])
token_info = auth_manager.get_access_token(as_dict=False)
print("Access Token:", token_info)'''

try:
    user_profile = sp.current_user()
    print("Authenticated user:", user_profile['display_name'])
except spotipy.exceptions.SpotifyException as e:
    print(f"Spotify API Error: {e}")


# Fetch user's top artists
def get_top_artists(limit=10,time_range='long_term'):
    top_artists = sp.current_user_top_artists(limit=limit)

    # Debugging: Print the raw API response
    print("API Response: ", top_artists)

    if top_artists and 'items' in top_artists:
        artist_data = []
        for artist in top_artists['items']:
            artist_data.append({
                'name': artist['name'],
                'genres': ', '.join(artist['genres']),
                'popularity': artist['popularity'],
                'followers': artist['followers']['total']
            })
        return pd.DataFrame(artist_data)
    else:
        print("No artist data found.")
        return pd.DataFrame()


df_artists_short = get_top_artists(time_range='short_term')
df_artists_medium = get_top_artists(time_range='medium_term')
df_artists_long = get_top_artists(time_range='long_term')

# Print data for each time range
print("Short term artists data:", df_artists_short)
print("Medium term artists data:", df_artists_medium)
print("Long term artists data:", df_artists_long)


def get_top_tracks(limit=10, time_range='medium_term'):
    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)

    if top_tracks and 'items' in top_tracks:
        track_data = []
        for track in top_tracks['items']:
            track_data.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'popularity': track['popularity'],
                'album': track['album']['name']
            })
        return pd.DataFrame(track_data)
    else:
        print(f"No track data found for time range: {time_range}")
        return pd.DataFrame()


df_tracks = get_top_tracks(time_range='long_term')
print(df_tracks)

# Main Streamlit app
def main():
    st.title("Spotify Music Streaming Analysis")

    # Fetch top artists and display in Streamlit
    df_artists = get_top_artists(limit=10)

    # Debug: Print DataFrame
    st.write(df_artists)

    # Plot if data is available
    if not df_artists.empty:
        st.write("Displaying top artists data...")
    else:
        st.write("No data available.")


if __name__ == "__main__":
    main()
