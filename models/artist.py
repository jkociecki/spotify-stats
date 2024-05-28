id = '1co4F2pPNH8JjTutZkmgSm'
from models.user_data import SpotifyUser


class Artist:
    def __init__(self, id, sp) -> None:
        self.id = id
        self.sp = sp

        # self.artist_data = self.sp.


if __name__ == '__main__':
    user = SpotifyUser().get_authorized_spotify_object()
    user.art
    a = Artist(id, user)

