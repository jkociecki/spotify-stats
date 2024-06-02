import spotipy
from functools import lru_cache

from models.user_auth import start_auth_server


class SpotifyUser:
    def __init__(self):
        #self.access_token = start_auth_server()
        #self.sp = spotipy.Spotify(auth=self.access_token)
        token = 'BQCTZ-dWI6UZc-4qfhGSck6-SCO7lJR_k0YbKBeMeOtKrL9QhVX9WL-9MoXHAGNToRhZJGJXJ43qKYV3woI7VWQCO65Dl6wZYh3DS7KQ2eLY3np3OaVdT249VPCKBehhihS9R9-MVzG8qQg1NldL7peWDvnhUiVHap6E8nMKBywb9ktlwRtBV25LO14rXmBlEPSVbmcMJHq9D7kzwsDaswb-G1VmzUwzAYUBfShzERt89pBurOmyfQD-LiOK7hCbPJRe788N76ncpnbUVtGiZexzZzgc49Ws3kp0IJXuOr0'
        self.sp = spotipy.Spotify(auth=token)

    @lru_cache(maxsize=128)
    def get_top_tracks(self, limit=10, time_range='short_term'):
        '''
        get the user's top tracks
        :param limit: number of tracks to return
        :param time_range: short_term, medium_term, long_term
        :return: list of tracks
        '''
        return self.sp.current_user_top_tracks(limit=limit, time_range=time_range)

    @lru_cache(maxsize=128)
    def get_top_artists(self, limit=10, time_range='short_term'):
        '''
        get the user's top artists
        :param limit: number of artists to return
        :param time_range: short_term, medium_term, long_term
        :return: list of artists
        '''
        return self.sp.current_user_top_artists(limit=limit, time_range=time_range)

    @lru_cache(maxsize=128)
    def get_saved_tracks(self, limit=10):
        '''
        get the user's saved tracks
        :param limit: number of tracks to return
        :return: list of tracks
        '''
        return self.sp.current_user_saved_tracks(limit=limit)

    @lru_cache(maxsize=128)
    def get_user_profile(self):
        '''
        get the user's profile
        :return: user's profile
        '''
        return self.sp.current_user()

    @lru_cache(maxsize=128)
    def get_user_top_items(self, limit=10, time_range='short_term'):
        '''
        get the user's top items
        :param limit: number of items to return
        :param time_range: short_term, medium_term, long_term
        :return: list of items
        '''
        return self.sp.current_user_top_items(limit=limit, time_range=time_range)

    @lru_cache(maxsize=128)
    def get_user_playlists(self, limit=10):
        '''
        get the user's playlists
        :param limit: number of playlists to return
        :return: list of playlists
        '''
        return self.sp.current_user_playlists(limit=limit)

    @lru_cache(maxsize=128)
    def get_authorized_spotify_object(self):
        '''
        get the authorized Spotify object
        :return: Spotify object
        '''
        return self.sp

    def get_genres(self):
        return self.sp.recommendation_genre_seeds()['genres']

    def generate_playlist(self, selected_genres, features, number_of_tracks, market):
        print(features)
        return self.sp.recommendations(seed_genres=selected_genres,
                          target_danceability=features['danceability'],
                          target_energy=features['energy'],
                          target_valence=features['valence'],
                          target_liveness=features['liveness'],
                          target_instrumentalness=features['instrumentalness'],
                          target_acousticness=features['acousticness'],
                          target_speechiness=features['speechiness'],
                          limit=str(number_of_tracks),
                          market=market)

    def download_playlist(self, name, description, uris):
        self.sp.user_playlist_create(user=self.sp.me()['id'], name=name, description=description)
        playlist_id = self.sp.current_user_playlists()['items'][0]['id']
        self.sp.playlist_add_items(playlist_id, uris)

    def get_track_names(self, uris):
        return [self.sp.track(uri)['name'] for uri in uris]