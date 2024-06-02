from models.track import Track
import statistics


class Playlist:
    """
    Class for handling playlist data
    """
    def __init__(self, playlist_id, sp):
        """
        Initialize the playlist object
        :param playlist_id: id of the playlist in the Spotify API
        :param sp: SpotifyUser object
        """
        self.playlist_id = playlist_id
        self.sp = sp
        self.tracks = self.sp.playlist_tracks(playlist_id=self.playlist_id)
        self.playlist = self.sp.playlist(playlist_id)
        self.name = self.playlist['name']
        self.cover_url = self.playlist['images'][0]['url']
        self.tracklist = []

    def get_tracks(self):
        """
        Get tracks from the playlist
        :return: list of Track objects
        """
        for track in self.tracks['items']:
            track_id = track['track']['id']
            self.tracklist.append(Track(track_id, self.sp))
        return self.tracklist

    def get_playlist_summary(self):
        """
        Get summary of the playlist including average values of audio features
        :return: dictionary with summary data
        """
        avg_danceability = statistics.mean([track.danceability for track in self.tracklist])
        avg_acousticness = statistics.mean([track.acousticness for track in self.tracklist])
        avg_energy = statistics.mean([track.energy for track in self.tracklist])
        avg_loudness = statistics.mean([track.loudness for track in self.tracklist])
        avg_speechiness = statistics.mean([track.speechiness for track in self.tracklist])
        avg_instrumentalness = statistics.mean([track.instrumentalness for track in self.tracklist])
        avg_liveness = statistics.mean([track.liveness for track in self.tracklist])
        avg_valence = statistics.mean([track.valence for track in self.tracklist])
        avg_duration = statistics.mean([track.duration_ms for track in self.tracklist])

        return {
            'avg_danceability': avg_danceability,
            'avg_acousticness': avg_acousticness,
            'avg_energy': avg_energy,
            'avg_loudness': avg_loudness,
            'avg_speechiness': avg_speechiness,
            'avg_instrumentalness': avg_instrumentalness,
            'avg_liveness': avg_liveness,
            'avg_valence': avg_valence,
            'avg_duration': avg_duration
        }

    def get_most_common_artists(self):
        """
        Get the most common artist in the playlist
        :return: Artist name
        """
        artists = [track.artist for track in self.tracklist]
        return statistics.mode(artists)

    def get_most_common_genres(self):
        """
        Get the most common genre in the playlist
        :return: genre name
        """
        genres = []
        for track in self.tracklist:
            genres.extend(track.genres)
        return statistics.mode(genres)

    def get_most_common_years(self):
        """
        Get the most common release year in the playlist
        :return: year
        """
        years = [track.release_date.split('-')[0] for track in self.tracklist]
        return statistics.mode(years)
