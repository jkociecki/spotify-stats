from user_data import SpotifyUser
from track import Track
import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests
import statistics


class Playlist:
    def __init__(self, playlist_id, sp):
        self.playlist_id = playlist_id
        self.sp = sp
        self.tracks = self.sp.playlist_tracks(playlist_id=self.playlist_id)
        self.playlist = self.sp.playlist(playlist_id)
        self.name = self.playlist['name']
        self.cover_url = self.playlist['images'][0]['url']
        self.tracklist = []

    def get_tracks(self):
        for track in self.tracks['items']:
            track_id = track['track']['id']
            self.tracklist.append(Track(track_id, self.sp))
        return self.tracklist

    def get_playlist_summary(self):
        avg_danceability = statistics.mean([track.danceability for track in self.tracklist])
        avg_acousticness = statistics.mean([track.acousticness for track in self.tracklist])
        avg_energy = statistics.mean([track.energy for track in self.tracklist])
        avg_loudness = statistics.mean([track.loudness for track in self.tracklist])
        avg_speechiness = statistics.mean([track.speechiness for track in self.tracklist])
        avg_instrumentalness = statistics.mean([track.instrumentalness for track in self.tracklist])
        avg_liveness = statistics.mean([track.liveness for track in self.tracklist])
        avg_valence = statistics.mean([track.valence for track in self.tracklist])
        avg_duration = statistics.mean([track.duration_ms for track in self.tracklist])

        return {
            'avg_danceability': avg_danceability,
            'avg_acousticness': avg_acousticness,
            'avg_energy': avg_energy,
            'avg_loudness': avg_loudness,
            'avg_speechiness': avg_speechiness,
            'avg_instrumentalness': avg_instrumentalness,
            'avg_liveness': avg_liveness,
            'avg_valence': avg_valence,
            'avg_duration': avg_duration
        }

    def get_most_common_artists(self):
        artists = [track.artist for track in self.tracklist]
        return statistics.mode(artists)

    def get_most_common_genres(self):
        genres = []
        for track in self.tracklist:
            genres.extend(track.genres)
        return statistics.mode(genres)

    def get_most_common_years(self):
        years = [track.release_date.split('-')[0] for track in self.tracklist]
        return statistics.mode(years)


def get_user_playlists(user):
    playlists = user.get_user_playlists()
    return [Playlist(playlist['id'], user.sp) for playlist in playlists['items']]


class PlaylistsView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)

        self.user = user

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tracks_frame = ctk.CTkScrollableFrame(self)
        self.tracks_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.track_info_frame = ctk.CTkFrame(self)
        self.track_info_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.playlist_summary_frame = ctk.CTkFrame(self)
        self.playlist_summary_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.populate_playlists()

    def populate_playlists(self):
        playlists = get_user_playlists(self.user)
        for i, playlist in enumerate(playlists):
            button = ctk.CTkButton(self.scrollable_frame, text=playlist.name,
                                   command=lambda p=playlist: self.display_playlist(p))
            button.grid(row=i, column=1, padx=5, pady=5)
            label = ctk.CTkLabel(self.scrollable_frame, text=f"{i + 1}.", font=("Arial", 12, "bold"))
            label.grid(row=i, column=0, padx=5, pady=5)

    def display_playlist(self, playlist):
        self.display_tracks(playlist)
        self.display_summary(playlist)

    def display_tracks(self, playlist):
        for widget in self.tracks_frame.winfo_children():
            widget.destroy()

        tracks = playlist.get_tracks()
        for track in tracks:
            track_name = track.title
            button = ctk.CTkButton(self.tracks_frame, text=track_name,
                                   command=lambda t=track: self.display_track_info(t))
            button.pack(padx=5, pady=5, fill="x")

    def display_track_info(self, track):
        for widget in self.track_info_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.track_info_frame, text=track.title).pack(pady=5)
        ctk.CTkLabel(self.track_info_frame, text=f"Danceability: {track.danceability}").pack(pady=5)
        ctk.CTkLabel(self.track_info_frame, text=f"Acousticness: {track.acousticness}").pack(pady=5)
        ctk.CTkLabel(self.track_info_frame, text=f"Energy: {track.energy}").pack(pady=5)

    def display_summary(self, playlist):
        for widget in self.playlist_summary_frame.winfo_children():
            widget.destroy()

        try:
            response = requests.get(playlist.cover_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image_ctk = ctk.CTkImage(light_image=image, dark_image=image, size=(250, 250))
            image_label = ctk.CTkLabel(self.playlist_summary_frame, image=image_ctk, text='')
            image_label.pack(pady=10)
        except requests.RequestException as e:
            print(f"Failed to load image: {e}")

        ctk.CTkLabel(self.playlist_summary_frame,
                     text=f"Most common artist: {playlist.get_most_common_artists()}").pack(pady=5)
        ctk.CTkLabel(self.playlist_summary_frame,
                     text=f"Most common genre: {playlist.get_most_common_genres()}").pack(pady=5)
        ctk.CTkLabel(self.playlist_summary_frame,
                     text=f"Most common year: {playlist.get_most_common_years()}").pack(pady=5)


if __name__ == "__main__":
    user = SpotifyUser()

    app = ctk.CTk()
    app.geometry("1200x800")

    frame = PlaylistsView(app, user)
    frame.pack(fill="both", expand=True)

    app.mainloop()
