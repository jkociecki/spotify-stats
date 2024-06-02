import numpy as np
from math import pi
from models.playlist_stats_model import Playlist


class PlaylistStatsController:
    """
    Controller class for controlling playlist statistics
    """

    def __init__(self, user):
        """
        :param user:
        """
        self.user = user
        self.current_playlist_summary = None

    def get_user_playlists(self):
        """
        Get user playlists
        :return:  list of playlists
        """
        playlists = self.user.get_user_playlists()
        return [Playlist(playlist['id'], self.user.sp) for playlist in playlists['items']]

    def get_playlist_summary(self, playlist):
        """
        Get playlist summary
        :param playlist:
        :return: summary of playlist features (danceability, energy, etc.)
        """
        return playlist.get_playlist_summary()

    def get_tracks(self, playlist):
        """
        Get tracks from playlist
        :param playlist:
        :return: list of tracks
        """
        return playlist.get_tracks()

    def get_most_common_artists(self, playlist):
        """
        Get most common artists from playlist
        :param playlist:
        :return: artist that appears the most in the playlist
        """
        return playlist.get_most_common_artists()

    def get_most_common_genres(self, playlist):
        """
        Get most common genres from playlist
        :param playlist:
        :return: genre that appers the most common in the playlist
        """
        return playlist.get_most_common_genres()

    def get_most_common_years(self, playlist):
        """
        Get most common years from playlist
        :param playlist:
        :return: year that appears the most common in the playlist
        """

        return playlist.get_most_common_years()

    def normalize_value(self, value, min_value, max_value):
        """
        Normalize value
        :param value:
        :param min_value:
        :param max_value:
        :return: Scaled value between min_value and max_value
        """
        return (value - min_value) / (max_value - min_value)

    def create_radar_chart_data(self, playlist, track=None):
        """
        Calculates necessary data for radar chart
        :param playlist:
        :param track:
        :return: categories, avg_values, track_values or categories, avg_values, None
        """

        categories = ['danceability', 'acousticness', 'energy', 'loudness', 'speechiness', 'instrumentalness',
                      'liveness', 'valence']

        if track is None:
            playlist_summary = self.get_playlist_summary(playlist)
            avg_values = [
                self.normalize_value(playlist_summary['avg_danceability'], 0, 1),
                self.normalize_value(playlist_summary['avg_acousticness'], 0, 1),
                self.normalize_value(playlist_summary['avg_energy'], 0, 1),
                self.normalize_value(playlist_summary['avg_loudness'], -60, 0),
                self.normalize_value(playlist_summary['avg_speechiness'], 0, 1),
                self.normalize_value(playlist_summary['avg_instrumentalness'], 0, 1),
                self.normalize_value(playlist_summary['avg_liveness'], 0, 1),
                self.normalize_value(playlist_summary['avg_valence'], 0, 1)
            ]
            self.current_playlist_summary = avg_values
        else:
            avg_values = self.current_playlist_summary

        if track:
            track_values = [
                self.normalize_value(track.danceability, 0, 1),
                self.normalize_value(track.acousticness, 0, 1),
                self.normalize_value(track.energy, 0, 1),
                self.normalize_value(track.loudness, -60, 0),
                self.normalize_value(track.speechiness, 0, 1),
                self.normalize_value(track.instrumentalness, 0, 1),
                self.normalize_value(track.liveness, 0, 1),
                self.normalize_value(track.valence, 0, 1)
            ]
            return categories, avg_values, track_values
        else:
            return categories, avg_values, None

    def create_radar_chart(self, ax, categories, values, color='lightblue'):
        """
        Create radar chart
        :param ax:
        :param categories:
        :param values:
        :param color:
        :return: creates radar chart for given data
        """
        N = len(categories)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        values += values[:1]

        ax.clear()
        ax.set_facecolor('#2e2e2e')
        ax.figure.set_facecolor('#2e2e2e')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10, color='white')

        ax.set_rlabel_position(0)
        ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        ax.set_yticklabels(["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"], color="grey", size=7)
        ax.set_ylim(0, 1)

        ax.plot(angles, values, linewidth=2, linestyle='solid', color=color, marker='o')
        ax.fill(angles, values, color, alpha=0.25)

        return ax

    def create_double_radar_chart(self, ax, categories, values1, values2, color1='lightblue', color2='orange'):
        """
        Create double radar chart (includes playlist average and track values)
        :param ax:
        :param categories:
        :param values1:
        :param values2:
        :param color1:
        :param color2:
        """
        N = len(categories)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]  # Zamknięcie wykresu dodając pierwszy punkt na koniec
        values1 = values1[:N]  # Upewniamy się, że values1 ma odpowiednią długość
        values1 += values1[:1]  # Zamknięcie wykresu dodając pierwszy punkt na koniec
        values2 = values2[:N]  # Upewniamy się, że values2 ma odpowiednią długość
        values2 += values2[:1]  # Zamknięcie wykresu dodając pierwszy punkt na koniec
        categories += categories[:1]  # Zamknięcie listy kategorii

        ax.plot(angles, values1, 'o-', linewidth=2, label='Playlist', color=color1)
        ax.fill(angles, values1, alpha=0.25, facecolor=color1)

        ax.plot(angles, values2, 'o-', linewidth=2, label='Track', color=color2)
        ax.fill(angles, values2, alpha=0.25, facecolor=color2)

        ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1], fontsize=10,
                          color='white')  # Używamy categories bez ostatniego elementu
        ax.set_rlabel_position(250)
        ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        ax.set_yticklabels(["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"], color="grey", size=7)
        ax.set_ylim(0, 1)
        ax.set_facecolor('#2e2e2e')
        ax.figure.set_facecolor('#2e2e2e')
        ax.grid(True)
        ax.spines['polar'].set_visible(False)
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
