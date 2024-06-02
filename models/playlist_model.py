from spotipy import Spotify


class PlaylistModelArtists:
    def __init__(self, spotify_user: Spotify, type: str):
        self.sp = spotify_user
        self.search_results = []
        self.selected_artists = []
        self.generated_playlist = []
        self.generated_playlist_uris = []
        self.type = type

    def search_artist(self, artist_name):
        if artist_name:
            result = self.sp.search(q=artist_name, type=self.type, limit=10)
            self.search_results = result[self.type + 's']['items']
            return self.search_results

    def add_artist(self, artist):
        if artist not in self.selected_artists:
            self.selected_artists.append(artist)

    def clear_selected_artists(self):
        self.selected_artists = []

    def generate_playlist(self):
        list_of_uris = [artist['uri'] for artist in self.selected_artists]
        if self.type == 'artist':
            recommended_tracks = self.sp.recommendations(seed_artists=list_of_uris, limit=10)['tracks']
        if self.type == 'track':
            recommended_tracks = self.sp.recommendations(seed_tracks=list_of_uris, limit=10)['tracks']
        self.generated_playlist = [track['name'] for track in recommended_tracks]
        self.generated_playlist_uris = [track['uri'] for track in recommended_tracks]
        return self.generated_playlist

    def download_playlist(self, name, description):
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
