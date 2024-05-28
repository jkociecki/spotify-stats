
class PlaylistModel:
    def __init__(self, spotify_user):
        self.sp = spotify_user
        self.search_results = []
        self.selected_artists = []
        self.generated_playlist = []
        self.generated_playlist_uris = []

    def search_artist(self, artist_name):
        if artist_name:
            result = self.sp.search(q=artist_name, type="artist", limit=10)
            self.search_results = result['artists']['items']
            return self.search_results

    def add_artist(self, artist):
        if artist not in self.selected_artists:
            self.selected_artists.append(artist)

    def clear_selected_artists(self):
        self.selected_artists = []

    def generate_playlist(self):
        list_of_uris = [artist['uri'] for artist in self.selected_artists]
        recommended_tracks = self.sp.recommendations(seed_artists=list_of_uris, limit=10)['tracks']
        self.generated_playlist = [track['name'] for track in recommended_tracks]
        self.generated_playlist_uris = [track['uri'] for track in recommended_tracks]
        return self.generated_playlist

    def download_playlist(self):
        # Implement download functionality
        pass