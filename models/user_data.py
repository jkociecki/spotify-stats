import spotipy
from functools import lru_cache
from models.user_auth import start_auth_server


class SpotifyUser:
    """
    A class to interact with Spotify API using Spotipy.

    This class initializes the Spotify client with an access token and provides various methods to retrieve user data
    and manage playlists.
    """

    def __init__(self):
        """
        Initialize the SpotifyUser with an access token and Spotify client.
        """
        self.access_token = start_auth_server()
        self.sp = spotipy.Spotify(auth=self.access_token)

    @lru_cache(maxsize=128)
    def get_top_tracks(self, limit=10, time_range='short_term'):
        """
        Get the user's top tracks.

        Parameters:
            limit (int): Number of tracks to return.
            time_range (str): Time range for top tracks (short_term, medium_term, long_term).

        Returns:
            list: A list of top tracks.
        """
        return self.sp.current_user_top_tracks(limit=limit, time_range=time_range)

    @lru_cache(maxsize=128)
    def get_top_artists(self, limit=10, time_range='short_term'):
        """
        Get the user's top artists.

        Parameters:
            limit (int): Number of artists to return.
            time_range (str): Time range for top artists (short_term, medium_term, long_term).

        Returns:
            list: A list of top artists.
        """
        return self.sp.current_user_top_artists(limit=limit, time_range=time_range)

    @lru_cache(maxsize=128)
    def get_saved_tracks(self, limit=10):
        """
        Get the user's saved tracks.

        Parameters:
            limit (int): Number of tracks to return.

        Returns:
            list: A list of saved tracks.
        """
        return self.sp.current_user_saved_tracks(limit=limit)

    @lru_cache(maxsize=128)
    def get_user_profile(self):
        """
        Get the user's profile.

        Returns:
            dict: User's profile data.
        """
        return self.sp.current_user()

    @lru_cache(maxsize=128)
    def get_user_top_items(self, limit=10, time_range='short_term'):
        """
        Get the user's top items.

        Parameters:
            limit (int): Number of items to return.
            time_range (str): Time range for top items (short_term, medium_term, long_term).

        Returns:
            list: A list of top items.
        """
        return self.sp.current_user_top_items(limit=limit, time_range=time_range)

    @lru_cache(maxsize=128)
    def get_user_playlists(self, limit=10):
        """
        Get the user's playlists.

        Parameters:
            limit (int): Number of playlists to return.

        Returns:
            list: A list of playlists.
        """
        return self.sp.current_user_playlists(limit=limit)

    @lru_cache(maxsize=128)
    def get_authorized_spotify_object(self):
        """
        Get the authorized Spotify object.

        Returns:
            spotipy.Spotify: Authorized Spotify client.
        """
        return self.sp

    def get_genres(self):
        """
        Get available genres for recommendations.

        Returns:
            list: A list of available genres.
        """
        return self.sp.recommendation_genre_seeds()['genres']

    def generate_playlist(self, selected_genres, features, number_of_tracks, market):
        """
        Generate a playlist based on selected genres and track features.

        Parameters:
            selected_genres (list): List of selected genres.
            features (dict): Dictionary of track features.
            number_of_tracks (int): Number of tracks in the playlist.
            market (str): Market (e.g., 'US').

        Returns:
            dict: Playlist recommendations.
        """
        return self.sp.recommendations(
            seed_genres=selected_genres,
            target_danceability=features['danceability'],
            target_energy=features['energy'],
            target_valence=features['valence'],
            target_liveness=features['liveness'],
            target_instrumentalness=features['instrumentalness'],
            target_acousticness=features['acousticness'],
            target_speechiness=features['speechiness'],
            limit=str(number_of_tracks),
            market=market
        )

    def download_playlist(self, name, description, uris):
        """
        Create and download a playlist with specified track URIs.

        Parameters:
            name (str): Name of the playlist.
            description (str): Description of the playlist.
            uris (list): List of track URIs.

        Returns:
            None
        """
        self.sp.user_playlist_create(user=self.sp.me()['id'], name=name, description=description)
        playlist_id = self.sp.current_user_playlists()['items'][0]['id']
        self.sp.playlist_add_items(playlist_id, uris)

    def get_track_names(self, uris):
        """
        Get track names from track URIs.

        Parameters:
            uris (list): List of track URIs.

        Returns:
            list: A list of track names.
        """
        return [self.sp.track(uri)['name'] for uri in uris]
