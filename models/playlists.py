from models.user_data import SpotifyUser
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from controllers.playlist_stats_controller import PlaylistStatsController


class PlaylistsView(ctk.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)

        self.playlist_list_frame = ctk.CTkScrollableFrame(self)
        self.playlist_list_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.tracks_frame = ctk.CTkScrollableFrame(self)
        self.tracks_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=2)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.plot_frame = ctk.CTkFrame(self.right_frame)
        self.plot_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.bottom_right_frame = ctk.CTkFrame(self.right_frame)
        self.bottom_right_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.bottom_right_frame.grid_columnconfigure(0, weight=1)
        self.bottom_right_frame.grid_columnconfigure(1, weight=1)

        self.playlist_cover_frame = ctk.CTkFrame(self.bottom_right_frame)
        self.playlist_cover_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.playlist_summary_frame = ctk.CTkFrame(self.bottom_right_frame)
        self.playlist_summary_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.populate_playlists()

    def populate_playlists(self):
        playlists = self.controller.get_user_playlists()
        for i, playlist in enumerate(playlists):
            button = ctk.CTkButton(self.playlist_list_frame, text=playlist.name,
                                   command=lambda p=playlist: self.display_playlist(p))
            button.grid(row=i, column=1, padx=5, pady=5)
            label = ctk.CTkLabel(self.playlist_list_frame, text=f"{i + 1}.", font=("Arial", 12, "bold"))
            label.grid(row=i, column=0, padx=5, pady=5)

    def display_playlist(self, playlist):
        self.display_tracks(playlist)
        self.display_summary(playlist)
        self.display_radar_chart(None, playlist)

    def display_tracks(self, playlist):
        for widget in self.tracks_frame.winfo_children():
            widget.destroy()

        tracks = self.controller.get_tracks(playlist)
        for track in tracks:
            track_name = track.title
            button = ctk.CTkButton(self.tracks_frame, text=track_name,
                                   command=lambda t=track: self.display_track_info(t, playlist))
            button.pack(padx=5, pady=5, fill="x")

    def display_track_info(self, track, playlist):
        self.display_radar_chart(track, playlist)

    def display_radar_chart(self, track, playlist):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        categories, avg_values, track_values = self.controller.create_radar_chart_data(playlist, track)

        if track_values:
            self.controller.create_double_radar_chart(ax, categories, avg_values, track_values)
        else:
            print("Displaying playlist radar chart")
            print(avg_values)
            self.controller.create_radar_chart(ax, categories, avg_values)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)

    def display_summary(self, playlist):
        for widget in self.playlist_cover_frame.winfo_children():
            widget.destroy()
        for widget in self.playlist_summary_frame.winfo_children():
            widget.destroy()

        try:
            response = requests.get(playlist.cover_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image_ctk = ctk.CTkImage(light_image=image, dark_image=image, size=(150, 150))
            image_label = ctk.CTkLabel(self.playlist_cover_frame, image=image_ctk, text='')
            image_label.pack(pady=10)
        except requests.RequestException as e:
            print(f"Failed to load image: {e}")

        ctk.CTkLabel(self.playlist_summary_frame,
                     text=f"Most common artist: {self.controller.get_most_common_artists(playlist)}").pack(pady=5)
        ctk.CTkLabel(self.playlist_summary_frame,
                     text=f"Most common genre: {self.controller.get_most_common_genres(playlist)}").pack(pady=5)
        ctk.CTkLabel(self.playlist_summary_frame,
                     text=f"Most common year: {self.controller.get_most_common_years(playlist)}").pack(pady=5)


import customtkinter as ctk

if __name__ == "__main__":
    user = SpotifyUser()

    app = ctk.CTk()
    app.geometry("1200x800")
    app.title("Spotify Playlist Analysis")

    controller = PlaylistStatsController(user)
    playlist_view = PlaylistsView(app, controller, bg_color="#8AA7A9", width=200, height=500)
    playlist_view.pack(padx=20, pady=20, fill="both", expand=True)

    app.mainloop()

# import requests
# from PIL import Image
# from io import BytesIO
# import statistics
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import customtkinter as ctk
# from math import pi
# import numpy as np
#
# from models.track import Track
# from models.user_data import SpotifyUser
#
#
# class Playlist:
#     def __init__(self, playlist_id, sp):
#         self.playlist_id = playlist_id
#         self.sp = sp
#         self.tracks = self.sp.playlist_tracks(playlist_id=self.playlist_id)
#         self.playlist = self.sp.playlist(playlist_id)
#         self.name = self.playlist['name']
#         self.cover_url = self.playlist['images'][0]['url']
#         self.tracklist = []
#
#     def get_tracks(self):
#         for track in self.tracks['items']:
#             track_id = track['track']['id']
#             self.tracklist.append(Track(track_id, self.sp))
#         return self.tracklist
#
#     def get_playlist_summary(self):
#         avg_danceability = statistics.mean([track.danceability for track in self.tracklist])
#         avg_acousticness = statistics.mean([track.acousticness for track in self.tracklist])
#         avg_energy = statistics.mean([track.energy for track in self.tracklist])
#         avg_loudness = statistics.mean([track.loudness for track in self.tracklist])
#         avg_speechiness = statistics.mean([track.speechiness for track in self.tracklist])
#         avg_instrumentalness = statistics.mean([track.instrumentalness for track in self.tracklist])
#         avg_liveness = statistics.mean([track.liveness for track in self.tracklist])
#         avg_valence = statistics.mean([track.valence for track in self.tracklist])
#         avg_duration = statistics.mean([track.duration_ms for track in self.tracklist])
#
#         return {
#             'avg_danceability': avg_danceability,
#             'avg_acousticness': avg_acousticness,
#             'avg_energy': avg_energy,
#             'avg_loudness': avg_loudness,
#             'avg_speechiness': avg_speechiness,
#             'avg_instrumentalness': avg_instrumentalness,
#             'avg_liveness': avg_liveness,
#             'avg_valence': avg_valence,
#             'avg_duration': avg_duration
#         }
#
#     def get_most_common_artists(self):
#         artists = [track.artist for track in self.tracklist]
#         return statistics.mode(artists)
#
#     def get_most_common_genres(self):
#         genres = []
#         for track in self.tracklist:
#             genres.extend(track.genres)
#         return statistics.mode(genres)
#
#     def get_most_common_years(self):
#         years = [track.release_date.split('-')[0] for track in self.tracklist]
#         return statistics.mode(years)
#
#
# def get_user_playlists(user):
#     playlists = user.get_user_playlists()
#     return [Playlist(playlist['id'], user.sp) for playlist in playlists['items']]
#
#
# class PlaylistsView(ctk.CTkFrame):
#     def __init__(self, master, user):
#         super().__init__(master)
#
#         self.user = user
#
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure(2, weight=2)
#
#         # Playlist list frame
#         self.playlist_list_frame = ctk.CTkScrollableFrame(self)
#         self.playlist_list_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
#
#         # Playlist tracks frame
#         self.tracks_frame = ctk.CTkScrollableFrame(self)
#         self.tracks_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
#
#         # Right side frame for plot and additional info
#         self.right_frame = ctk.CTkFrame(self)
#         self.right_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")
#         self.right_frame.grid_rowconfigure(0, weight=2)
#         self.right_frame.grid_rowconfigure(1, weight=1)
#         self.right_frame.grid_columnconfigure(0, weight=1)
#
#         # Plot frame
#         self.plot_frame = ctk.CTkFrame(self.right_frame)
#         self.plot_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#
#         # Bottom right frame for cover and summary
#         self.bottom_right_frame = ctk.CTkFrame(self.right_frame)
#         self.bottom_right_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
#         self.bottom_right_frame.grid_columnconfigure(0, weight=1)
#         self.bottom_right_frame.grid_columnconfigure(1, weight=1)
#
#         # Playlist cover frame
#         self.playlist_cover_frame = ctk.CTkFrame(self.bottom_right_frame)
#         self.playlist_cover_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#
#         # Playlist summary frame
#         self.playlist_summary_frame = ctk.CTkFrame(self.bottom_right_frame)
#         self.playlist_summary_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
#
#         self.populate_playlists()
#         self.current_playlist_summary = None
#
#     def populate_playlists(self):
#         playlists = get_user_playlists(self.user)
#         for i, playlist in enumerate(playlists):
#             button = ctk.CTkButton(self.playlist_list_frame, text=playlist.name,
#                                    command=lambda p=playlist: self.display_playlist(p))
#             button.grid(row=i, column=1, padx=5, pady=5)
#             label = ctk.CTkLabel(self.playlist_list_frame, text=f"{i + 1}.", font=("Arial", 12, "bold"))
#             label.grid(row=i, column=0, padx=5, pady=5)
#
#     def display_playlist(self, playlist):
#         self.display_tracks(playlist)
#         self.display_summary(playlist)
#         self.display_radar_chart(None, playlist)  # Display radar chart with playlist summary
#
#     def display_tracks(self, playlist):
#         for widget in self.tracks_frame.winfo_children():
#             widget.destroy()
#
#         tracks = playlist.get_tracks()
#         for track in tracks:
#             track_name = track.title
#             button = ctk.CTkButton(self.tracks_frame, text=track_name,
#                                    command=lambda t=track: self.display_track_info(t, playlist))
#             button.pack(padx=5, pady=5, fill="x")
#
#     def display_track_info(self, track, playlist):
#         # Overlay radar chart with track values
#         self.display_radar_chart(track, playlist)
#
#     def normalize_value(self, value, min_value, max_value):
#         return (value - min_value) / (max_value - min_value)
#
#     def create_radar_chart(self, ax, categories, values, color='lightblue'):
#         N = len(categories)
#         angles = [n / float(N) * 2 * pi for n in range(N)]
#         angles += angles[:1]
#         values += values[:1]
#
#         ax.clear()
#         ax.set_facecolor('#2e2e2e')
#         ax.figure.set_facecolor('#2e2e2e')
#         ax.set_xticks(angles[:-1])
#         ax.set_xticklabels(categories, fontsize=10, color='white')
#
#         ax.set_rlabel_position(0)
#         ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
#         ax.set_yticklabels(["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"], color="grey", size=7)
#         ax.set_ylim(0, 1)
#
#         ax.plot(angles, values, linewidth=2, linestyle='solid', color=color, marker='o')
#         ax.fill(angles, values, color, alpha=0.25)
#
#         return ax
#
#     def create_double_radar_chart(self, ax, categories, values1, values2, color1='lightblue', color2='orange'):
#         N = len(categories)
#         angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
#         angles += angles[:1]  # Zamknięcie wykresu dodając pierwszy punkt na koniec
#         values1 = values1[:N]  # Upewniamy się, że values1 ma odpowiednią długość
#         values1 += values1[:1]  # Zamknięcie wykresu dodając pierwszy punkt na koniec
#         values2 = values2[:N]  # Upewniamy się, że values2 ma odpowiednią długość
#         values2 += values2[:1]  # Zamknięcie wykresu dodając pierwszy punkt na koniec
#         categories += categories[:1]  # Zamknięcie listy kategorii
#
#         ax.plot(angles, values1, 'o-', linewidth=2, label='Playlist', color=color1)
#         ax.fill(angles, values1, alpha=0.25, facecolor=color1)
#
#         ax.plot(angles, values2, 'o-', linewidth=2, label='Track', color=color2)
#         ax.fill(angles, values2, alpha=0.25, facecolor=color2)
#
#         ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1], fontsize=10,
#                           color='white')  # Używamy categories bez ostatniego elementu
#         ax.set_rlabel_position(250)
#         ax.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
#         ax.set_yticklabels(["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"], color="grey", size=7)
#         ax.set_ylim(0, 1)
#         ax.set_facecolor('#2e2e2e')
#         ax.figure.set_facecolor('#2e2e2e')
#         ax.grid(True)
#         ax.spines['polar'].set_visible(False)
#         ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1.05))
#
#     def display_radar_chart(self, track, playlist):
#         for widget in self.plot_frame.winfo_children():
#             widget.destroy()
#
#         categories = ['danceability', 'acousticness', 'energy', 'loudness', 'speechiness', 'instrumentalness',
#                       'liveness', 'valence']
#         fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
#
#         if self.current_playlist_summary is None:
#             playlist_summary = playlist.get_playlist_summary()
#             avg_values = [
#                 self.normalize_value(playlist_summary['avg_danceability'], 0, 1),
#                 self.normalize_value(playlist_summary['avg_acousticness'], 0, 1),
#                 self.normalize_value(playlist_summary['avg_energy'], 0, 1),
#                 self.normalize_value(playlist_summary['avg_loudness'], -60, 0),
#                 # Zakładamy, że głośność mieści się w zakresie od -60 do 0
#                 self.normalize_value(playlist_summary['avg_speechiness'], 0, 1),
#                 self.normalize_value(playlist_summary['avg_instrumentalness'], 0, 1),
#                 self.normalize_value(playlist_summary['avg_liveness'], 0, 1),
#                 self.normalize_value(playlist_summary['avg_valence'], 0, 1)
#             ]
#             self.current_playlist_summary = avg_values
#
#         if track:
#             values = [
#                 self.normalize_value(track.danceability, 0, 1),
#                 self.normalize_value(track.acousticness, 0, 1),
#                 self.normalize_value(track.energy, 0, 1),
#                 self.normalize_value(track.loudness, -60, 0),
#                 self.normalize_value(track.speechiness, 0, 1),
#                 self.normalize_value(track.instrumentalness, 0, 1),
#                 self.normalize_value(track.liveness, 0, 1),
#                 self.normalize_value(track.valence, 0, 1)
#             ]
#             self.create_double_radar_chart(ax, categories, self.current_playlist_summary, values, color1='lightblue',
#                                            color2='orange')
#         else:
#             self.create_radar_chart(ax, categories, self.current_playlist_summary, color='lightblue')
#
#         canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
#         canvas.draw()
#         canvas.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)
#
#     def display_summary(self, playlist):
#         for widget in self.playlist_cover_frame.winfo_children():
#             widget.destroy()
#         for widget in self.playlist_summary_frame.winfo_children():
#             widget.destroy()
#
#         try:
#             response = requests.get(playlist.cover_url)
#             response.raise_for_status()
#             image = Image.open(BytesIO(response.content))
#             image_ctk = ctk.CTkImage(light_image=image, dark_image=image, size=(150, 150))
#             image_label = ctk.CTkLabel(self.playlist_cover_frame, image=image_ctk, text='')
#             image_label.pack(pady=10)
#         except requests.RequestException as e:
#             print(f"Failed to load image: {e}")
#
#         ctk.CTkLabel(self.playlist_summary_frame,
#                      text=f"Most common artist: {playlist.get_most_common_artists()}").pack(pady=5)
#         ctk.CTkLabel(self.playlist_summary_frame,
#                      text=f"Most common genre: {playlist.get_most_common_genres()}").pack(pady=5)
#         ctk.CTkLabel(self.playlist_summary_frame,
#                      text=f"Most common year: {playlist.get_most_common_years()}").pack(pady=5)
#
#
# if __name__ == "__main__":
#     user = SpotifyUser()
#
#     app = ctk.CTk()
#     app.geometry("1200x800")
#     app.title("Spotify Playlist Analysis")
#
#     playlist_view = PlaylistsView(app, user)
#     playlist_view.pack(padx=20, pady=20, fill="both", expand=True)
#
#     app.mainloop()
