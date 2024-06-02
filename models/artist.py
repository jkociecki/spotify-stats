id = '1co4F2pPNH8JjTutZkmgSm'
from models.user_data import SpotifyUser


class Artist:
    """
    Class for handling artist data
    """
    def __init__(self, id: str, sp: SpotifyUser) -> None:
        """
        :param id: id of the artist in the Spotify API
        :param sp: SpotifyUser object
        """
        self.id = id
        self.sp = sp.get_authorized_spotify_object()
        self.data = self.sp.artist(self.id)

    def get_artist_name(self) -> str:
        """
        Get artist name
        :return: name of the artist
        """
        return self.data['name']

    def get_artist_genres(self) -> list:
        """
        Get artist genres
        :return: list of genres
        """
        return self.data['genres']

    def get_artist_popularity(self) -> str:
        """
        Get artist popularity, number between 0 and 100
        :return: number between 0 and 100
        """
        return self.data['popularity']

    def get_artist_followers(self) -> str:
        """
        Get number of followers of the artist
        :return: number of followers
        """
        return self.data['followers']['total']

    def get_artist_image_url(self) -> str:
        """
        Url of the artist image
        :return: url
        """
        return self.data['images'][0]['url']

    def get_artist_albums(self) -> list:
        """
        Get list of albums of the artist
        :return: albums
        """
        return self.sp.artist_albums(self.id)

    def get_artist_top_tracks(self) -> list:
        """
        Get top tracks of the artist
        :return: tracks
        """
        return self.sp.artist_top_tracks(self.id)



if __name__ == '__main__':
    user = SpotifyUser()
    a = Artist(id, user)

