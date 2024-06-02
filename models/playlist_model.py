from spotipy import Spotify


class PlaylistModelArtists:
    """
    Model for the playlist generator based on given type of search
    """
    def __init__(self, spotify_user: Spotify, type: str):
        """
        Initialize the model, set the Spotify object and type of search
        Initialize placeholders for search results, selected artists, generated playlist and playlist uris
        :param spotify_user: SpotifyUser object
        :param type: type of search e.g. 'artist' or 'track'
        """
        self.sp = spotify_user
        self.search_results = []
        self.selected_artists = []
        self.generated_playlist = []
        self.generated_playlist_uris = []
        self.type = type

    def search_artist(self, artist_name):
        """
        Search for artists based on the given name in the Spotify API
        :param artist_name: name of the artist
        :return: response from the API
        """
        if artist_name:
            result = self.sp.search(q=artist_name, type=self.type, limit=10)
            self.search_results = result[self.type + 's']['items']
            return self.search_results

    def add_artist(self, artist):
        """
        Add artist to the selected artists list
        :param artist: Artist object
        :return: None
        """
        if artist not in self.selected_artists:
            self.selected_artists.append(artist)

    def clear_selected_artists(self):
        """
        Clear the selected artists list
        :return: None
        """
        self.selected_artists = []

    def generate_playlist(self):
        """
        Generate playlist based on the selected artists or tracks
        Collect the uris of the selected artists or tracks and generate recommendations
        :return: None
        """
        list_of_uris = [artist['uri'] for artist in self.selected_artists]
        if self.type == 'artist':
            recommended_tracks = self.sp.recommendations(seed_artists=list_of_uris, limit=10)['tracks']
        if self.type == 'track':
            recommended_tracks = self.sp.recommendations(seed_tracks=list_of_uris, limit=10)['tracks']
        self.generated_playlist = [track['name'] for track in recommended_tracks]
        self.generated_playlist_uris = [track['uri'] for track in recommended_tracks]
        return self.generated_playlist

    def download_playlist(self, name, description):
        """
        Create a playlist in the user Spotify account
        :param name: name of the playlist
        :param description: description of the playlist
        :return: None
        """
        self.sp.user_playlist_create(user=self.sp.me()['id'], name=name, description=description)
        playlist_id = self.sp.current_user_playlists()['items'][0]['id']
        self.sp.playlist_add_items(playlist_id, self.generated_playlist_uris)

#
# class PlaylistModelTracks:
#     def __init__(self, spotify_user: Spotify):
#         self.sp = spotify_user
#         self.search_results = []
#         self.selected_artists = []
#         self.generated_playlist = []
#         self.generated_playlist_uris = []
#         self.type = type
#
#     def search_track(self, track_name):
#         result = self.sp.search(q=track_name, type='track', limit=10)
#         self.search_results = result['tracks']['items']
#         print(self.search_results)
#         return self.search_results
#
#     def add
#
#     def generate_playlist(self):
#         list_of_uris = [artist['uri'] for artist in self.selected_artists]
#         recommended_tracks = self.sp.recommendations(seed_artists=list_of_uris, limit=10)['tracks']
#         self.generated_playlist = [track['name'] for track in recommended_tracks]
#         self.generated_playlist_uris = [track['uri'] for track in recommended_tracks]
#         return self.generated_playlist

#
# if __name__ == '__main__':
#     t = PlaylistModelTracks(SpotifyUser().get_authorized_spotify_object())
#     t.search_track('jeremy sochan')
#
#
