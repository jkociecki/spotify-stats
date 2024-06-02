from models.user_data import SpotifyUser
from views.playlist_generator_layout import *


class TrackPlaylistView(BasePlaylistView):
    def __init__(self, master, spotify_user: SpotifyUser):
        super().__init__(master, spotify_user)

    def show_details(self, track):
        pass
