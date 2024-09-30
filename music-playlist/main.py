from bs4 import BeautifulSoup
# import lxml
import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv("C:/PyNotes/.env")
CLIENT_ID_SPOTIFY = os.getenv("MySpotifyClientID")
CLIENT_SECRET_SPOTIFY = os.getenv("MySpotifyClientSecret")
REDIRECT_URI_SPOTIFY = os.getenv("MySpotifyRedirectURI")

sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri=REDIRECT_URI_SPOTIFY,
            client_id=CLIENT_ID_SPOTIFY,
            client_secret=CLIENT_SECRET_SPOTIFY,
            show_dialog=True,
            cache_path="token.txt",
        )
    )
user_id = sp.current_user()["id"]
user_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Regex pattern for YYYY-MM-DD format
pattern = r"^\d{4}-\d{2}-\d{2}$"

# Check if the input matches the pattern
if re.match(pattern, user_input):
    print("Valid date format!")

    response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}")
    billboard_hot100_webpage = response.content
    soup = BeautifulSoup(billboard_hot100_webpage, "html.parser")
    songs_tag = soup.select("li ul li h3")
    artists_tag = soup.find_all(name="span", class_="c-label")
    songs_list = [song.getText().strip() for song in songs_tag]
    artists_list = [span.get_text(strip=True) for span in artists_tag if not span.get_text(strip=True).isdigit()]
    cleaned_artists = [name.split()[0] for name in artists_list if name not in ['-', 'NEW', 'RE-\nENTRY']]
    print(songs_list)
    print(cleaned_artists)
    print(len(cleaned_artists))
    combined_list = list(zip(songs_list, cleaned_artists))
    print(combined_list)

    song_uris = []
    year = user_input.split("-")[0]
    for song, artist in combined_list:
        result = sp.search(q=f"track:{song} artist:{artist} year:{int(year)-1}-{int(year)+1}", type="track")
        print(result)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

    playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} Billboard 100", public=False)
    # print(playlist)

    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

else:
    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
