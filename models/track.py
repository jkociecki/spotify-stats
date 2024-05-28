import requests
from PIL import Image
from io import BytesIO


class Track:
    def __init__(self, track_id, sp):
        self.track_id = track_id
        self.sp = sp

        response = self.sp.track(self.track_id)
        audio_features = self.sp.audio_features(self.track_id)

        self._artist = response['artists'][0]['name']
        self._title = response['name']
        self._release_date = response['album']['release_date']
        self._cover_url = response['album']['images'][0]['url']
        self._preview_url = response['preview_url']
        self._popularity = response['popularity']

        self._danceability = audio_features[0]['danceability']
        self._energy = audio_features[0]['energy']
        self._loudness = audio_features[0]['loudness']
        self._speechiness = audio_features[0]['speechiness']
        self._acousticness = audio_features[0]['acousticness']
        self._instrumentalness = audio_features[0]['instrumentalness']
        self._liveness = audio_features[0]['liveness']
        self._valence = audio_features[0]['valence']
        self._duration_ms = audio_features[0]['duration_ms']

    @property
    def duration_ms(self):
        return self._duration_ms

    @property
    def popularity(self):
        return self._popularity

    @property
    def artist(self):
        return self._artist

    @property
    def title(self):
        return self._title

    @property
    def release_date(self):
        return self._release_date

    @property
    def cover_url(self):
        return self._cover_url

    @property
    def preview_url(self):
        return self._preview_url

    @property
    def danceability(self):
        return self._danceability

    @property
    def energy(self):
        return self._energy

    @property
    def loudness(self):
        return self._loudness

    @property
    def speechiness(self):
        return self._speechiness

    @property
    def acousticness(self):
        return self._acousticness

    @property
    def instrumentalness(self):
        return self._instrumentalness

    @property
    def liveness(self):
        return self._liveness

    @property
    def valence(self):
        return self._valence

    def get_audio_cover_image(self) -> Image:
        '''
        get the cover image of the track
        :return: PIL image
        '''
        response = requests.get(self.cover_url)
        image = Image.open(BytesIO(response.content))
        return image
