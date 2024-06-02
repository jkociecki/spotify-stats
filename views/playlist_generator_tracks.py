from models.user_data import SpotifyUser
from views.playlist_generator_layout import *


class TrackPlaylistView(BasePlaylistView):
    """
    A view for managing and displaying track playlists.

    Inherits from BasePlaylistView.

    Attributes:
        controller (PlaylistController): The controller for handling user interactions.
        spotify_user (SpotifyUser): The Spotify user object.
    """

    def __init__(self, master, spotify_user: SpotifyUser):
        """
        Initialize the TrackPlaylistView.

        Args:
            master: The parent Tkinter window or frame.
            spotify_user (SpotifyUser): The Spotify user object.
        """
        super().__init__(master, spotify_user)

    def show_details(self, track):
        """
        Show details for the selected track.

        This method should be implemented to display track details in the view.

        Args:
            track: The track for which details should be shown.
        """
        pass
