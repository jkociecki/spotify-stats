import tkinter as tk
import customtkinter as ctk
from spotipy import Spotify
from PIL import Image, ImageTk
import requests
from io import BytesIO
from models.user_data import SpotifyUser


class HomePage(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, bg_color="#8AA7A9", spotify_user: SpotifyUser = None):
        super().__init__(parent, bg_color=bg_color)
        self.spotify_user = spotify_user

        self.spotify: Spotify = self.spotify_user.get_authorized_spotify_object()
        user_info = self.spotify.current_user()
        current_track_info = self.spotify.current_user_playing_track()
        playlists = self.spotify.current_user_playlists(limit=50)
        recently_played = self.spotify.current_user_recently_played(limit=10)
        following = self.spotify.current_user_followed_artists(limit=50)
        top_artists = self.spotify.current_user_top_artists(limit=5)['items']

        self.create_widgets(user_info, current_track_info, playlists, recently_played, following, top_artists)

    def create_widgets(self, user_info, current_track_info, playlists, recently_played, following, top_artists):
        # User Info Frame
        user_info_frame = ctk.CTkFrame(self)
        user_info_frame.pack(padx=20, pady=5, fill="x")

        # User Profile Picture
        profile_url = user_info['images'][0]['url'] if user_info['images'] else None
        if profile_url:
            response = requests.get(profile_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            profile_label = tk.Label(user_info_frame, image=photo)
            profile_label.image = photo
            profile_label.pack(side="left", padx=10)

        # User Name and Follower Count
        user_name_label = ctk.CTkLabel(user_info_frame,
                                       text=f"{user_info['display_name']} (Followers: {user_info['followers']['total']})",
                                       font=("Arial", 20))
        user_name_label.pack(side="left", padx=10)

        currently_playing_label = ctk.CTkLabel(self, text="Currently Playing", font=("Arial", 16))
        currently_playing_label.pack(pady=5)
        # Current Track Frame
        track_info_frame = ctk.CTkFrame(self)
        track_info_frame.pack(padx=20, pady=5, fill="x")

        if current_track_info and current_track_info['is_playing']:
            track = current_track_info['item']

            # Track Cover Image
            album_cover_url = track['album']['images'][0]['url']
            response = requests.get(album_cover_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            album_photo = ImageTk.PhotoImage(img)
            album_cover_label = tk.Label(track_info_frame, image=album_photo)
            album_cover_label.image = album_photo
            album_cover_label.pack(side="left", padx=10)

            # Track Info
            track_name_label = ctk.CTkLabel(track_info_frame, text=f"Track: {track['name']}", font=("Arial", 16))
            track_name_label.pack(anchor="w", padx=10)

            artist_name_label = ctk.CTkLabel(track_info_frame, text=f"Artist: {track['artists'][0]['name']}",
                                             font=("Arial", 16))
            artist_name_label.pack(anchor="w", padx=10)

            album_name_label = ctk.CTkLabel(track_info_frame, text=f"Album: {track['album']['name']}",
                                            font=("Arial", 16))
            album_name_label.pack(anchor="w", padx=10)

        else:
            no_track_label = ctk.CTkLabel(track_info_frame, text="No track currently playing", font=("Arial", 16))
            no_track_label.pack(padx=10, pady=5)

        # Playlists Frame
        playlists_frame = ctk.CTkFrame(self)
        playlists_frame.pack(padx=20, pady=5, fill="x")

        playlists_label = ctk.CTkLabel(playlists_frame, text=f"Total Playlists: {playlists['total']}",
                                       font=("Arial", 18))
        playlists_label.pack(anchor="w", padx=10, pady=5)

        # Recently Played Tracks Frame
        recently_played_frame = ctk.CTkScrollableFrame(self)
        recently_played_frame.pack(padx=20, pady=5, fill="both", expand=True)

        recently_played_label = ctk.CTkLabel(recently_played_frame, text="Recently Played Tracks", font=("Arial", 18))
        recently_played_label.pack(anchor="w", padx=10, pady=5)

        for item in recently_played['items']:
            track = item['track']
            track_label = ctk.CTkLabel(recently_played_frame, text=f"{track['name']} by {track['artists'][0]['name']}",
                                       font=("Arial", 14))
            track_label.pack(anchor="w", padx=10)

        # Following Frame
        following_frame = ctk.CTkScrollableFrame(self)
        following_frame.pack(padx=20, pady=5, fill="both", expand=True)

        following_label = ctk.CTkLabel(following_frame, text=f"Following: {len(following['artists']['items'])} artists",
                                       font=("Arial", 18))
        following_label.pack(anchor="w", padx=10, pady=5)

        for artist in following['artists']['items']:
            artist_label = ctk.CTkLabel(following_frame, text=artist['name'], font=("Arial", 14))
            artist_label.pack(anchor="w", padx=10)

        # Top Artists Frame
        top_artists_frame = ctk.CTkFrame(self)
        top_artists_frame.pack(padx=20, pady=5, fill="x")

        top_artists_label = ctk.CTkLabel(top_artists_frame, text="Top Artists", font=("Arial", 18))
        top_artists_label.pack(anchor="w", padx=10, pady=5)

        for artist in top_artists:
            artist_label = ctk.CTkLabel(top_artists_frame, text=artist['name'], font=("Arial", 14))
            artist_label.pack(anchor="w", padx=10)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("600x800")
    app = HomePage(root, spotify_user=SpotifyUser())
    app.pack(expand=True, fill="both")
    root.mainloop()
