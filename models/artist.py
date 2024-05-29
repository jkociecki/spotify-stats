id = '1co4F2pPNH8JjTutZkmgSm'
from models.user_data import SpotifyUser


class Artist:
    def __init__(self, id, sp: SpotifyUser) -> None:
        self.id = id
        self.sp = sp.get_authorized_spotify_object()
        self.data = self.sp.artist(self.id)

    def get_artist_name(self):
        return self.data['name']

    def get_artist_genres(self):
        return self.data['genres']

    def get_artist_popularity(self):
        return self.data['popularity']

    def get_artist_followers(self):
        return self.data['followers']['total']

    def get_artist_image_url(self):
        return self.data['images'][0]['url']

    def get_artist_albums(self):
        return self.sp.artist_albums(self.id)

    def get_artist_top_tracks(self):
        return self.sp.artist_top_tracks(self.id)



if __name__ == '__main__':
    user = SpotifyUser()
    a = Artist(id, user)

