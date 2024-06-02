from views.playlist_generator_layout import BasePlaylistView
from models.user_data import SpotifyUser
from models.music_player import MusicPlayer
from models.artist import Artist
from views.artistview import ArtistInfoView
from models.track import Track
from views.trackinfo import TrackInfoWindow
import customtkinter as ctk


class ArtistPlaylistView(BasePlaylistView):
    """
    A class to represent the Artist Playlist view.

    This class inherits from the BasePlaylistView class and provides functionalities
    to display artist details in a playlist view.

    Methods:
        show_artist_details(artist):
            Display detailed information of the selected artist.
    """

    def __init__(self, master: ctk.CTk, spotify_user: SpotifyUser):
        """
        Initialize the ArtistPlaylistView class.

        Parameters:
            master (ctk.CTk): The parent widget.
            spotify_user (SpotifyUser): The SpotifyUser object for the authenticated user.
        """
        super().__init__(master, spotify_user)

    def show_artist_details(self, artist):
        """
        Display detailed information of the selected artist.

        Parameters:
            artist (dict): The artist information.
        """
        artist = Artist(artist['id'], self.spotify_user)
        music_player = MusicPlayer()
        view = ArtistInfoView(self.controller.view, artist, music_player)
        view.grid(row=0, column=0, padx=10, pady=10, rowspan=230, sticky="nsew")


class TracksPlaylistView(BasePlaylistView):
    """
    A class to represent the Tracks Playlist view.

    This class inherits from the BasePlaylistView class and provides functionalities
    to display track details in a playlist view.

    Methods:
        show_artist_details(track):
            Display detailed information of the selected track.
    """

    def __init__(self, master: ctk.CTk, spotify_user: SpotifyUser):
        """
        Initialize the TracksPlaylistView class.

        Parameters:
            master (ctk.CTk): The parent widget.
            spotify_user (SpotifyUser): The SpotifyUser object for the authenticated user.
        """
        super().__init__(master, spotify_user)

    def show_artist_details(self, track):
        """
        Display detailed information of the selected track.

        Parameters:
            track (dict): The track information.
        """
        track = Track(track['id'], self.spotify_user)
        canvas = ctk.CTkCanvas(self.controller.view, width=500, height=600, bg='#2C2C2C')
        canvas.grid(row=0, column=3, padx=10, pady=10, rowspan=500, sticky="nsew")
        track_info_frame = TrackInfoWindow(canvas, track, MusicPlayer())
        canvas_frame = canvas.create_window((0, 0), window=track_info_frame, anchor="nw")
        track_info_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        track_info_frame.wait_window()
        canvas.grid_forget()
