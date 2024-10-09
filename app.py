import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from Music import get_top_artists, get_top_tracks


# Function to visualize top artists with popularity
def visualize_top_artists(df_artists):
    # Check if 'popularity' exists in the DataFrame columns
    if 'popularity' in df_artists.columns:
        # Check if the DataFrame is not empty
        if not df_artists.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df_artists, x='popularity', y='name', palette='viridis')
            plt.title('Top Artists by Popularity')
            plt.xlabel('Popularity')
            plt.ylabel('Artist')
            st.pyplot(plt)  # Display the plot in Streamlit
        else:
            st.write("No data found to display top artists.")
    else:
        st.write("Column 'popularity' not found in the DataFrame.")


def visualize_top_tracks(df_tracks):
    if not df_tracks.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_tracks, x='popularity', y='name', palette='magma')
        plt.title('Top Tracks by Popularity')
        plt.xlabel('Popularity')
        plt.ylabel('Track')
        st.pyplot(plt)
    else:
        st.write("No track data available.")


# Main function
def main():
    st.title("Spotify Music Streaming Analysis")

    # Fetch and display top artists
    st.subheader("Top Artists")
    df_artists = get_top_artists(limit=10)
    st.write(df_artists)
    visualize_top_artists(df_artists)

    # Fetch and display top tracks
    st.subheader("Top Tracks")
    df_tracks = get_top_tracks(limit=10)
    st.write(df_tracks)
    visualize_top_tracks(df_tracks)


if __name__ == "__main__":
    main()
