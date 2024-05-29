import spotipy
from functools import lru_cache

from models.user_auth import start_auth_server


class SpotifyUser:
    def __init__(self):
        #self.access_token = start_auth_server()
        #self.sp = spotipy.Spotify(auth=self.access_token)
        token = 'BQDCQLfGzQfCPCT1hfoSuayI0STurZQZyQVtaYPGKa_h2U4IcVsbFKMVmbNcaXQIq8od29HMpFiXcArJcJIJctNSPsBM1Jk7X-Rr5s70MlPPVbLcMRU7EX3YFP6ey50b-fDIwYoBc65riENJIOvNbzVOYQAzZmU8TLRaMzYiap4mL4KPQ8vh7zkw3K6ZCZxIAvpoztxDew-e3j-4-raVg6wf'
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