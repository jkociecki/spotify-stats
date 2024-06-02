from models.user_data import SpotifyUser
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from controllers.playlist_stats_controller import PlaylistStatsController


class PlaylistsStatsView(ctk.CTkFrame):
    """
    A custom Tkinter frame for displaying playlist statistics and details.

    Attributes:
        controller (PlaylistStatsController): The controller for handling user interactions and data retrieval.
    """

    def __init__(self, master, controller, *args, **kwargs):
        """
        Initialize the PlaylistsStatsView.

        Args:
            master: The parent Tkinter window or frame.
            controller (PlaylistStatsController): The controller for handling user interactions and data retrieval.
            *args: Additional arguments for the Tkinter Frame.
            **kwargs: Additional keyword arguments for the Tkinter Frame.
        """
        super().__init__(master, *args, **kwargs)
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
        """
        Populate the playlist list frame with buttons for each user playlist.
        """
        playlists = self.controller.get_user_playlists()
        for i, playlist in enumerate(playlists):
            button = ctk.CTkButton(self.playlist_list_frame, text=playlist.name,
                                   command=lambda p=playlist: self.display_playlist(p))
            button.grid(row=i, column=1, padx=5, pady=5)
            label = ctk.CTkLabel(self.playlist_list_frame, text=f"{i + 1}.", font=("Arial", 12, "bold"))
            label.grid(row=i, column=0, padx=5, pady=5)

    def display_playlist(self, playlist):
        """
        Display the tracks, summary, and radar chart for the selected playlist.

        Args:
            playlist: The selected playlist object.
        """
        self.display_tracks(playlist)
        self.display_summary(playlist)
        self.display_radar_chart(None, playlist)

    def display_tracks(self, playlist):
        """
        Display the tracks of the selected playlist in the tracks frame.

        Args:
            playlist: The selected playlist object.
        """
        for widget in self.tracks_frame.winfo_children():
            widget.destroy()

        tracks = self.controller.get_tracks(playlist)
        for track in tracks:
            track_name = track.title
            button = ctk.CTkButton(self.tracks_frame, text=track_name,
                                   command=lambda t=track: self.display_track_info(t, playlist))
            button.pack(padx=5, pady=5, fill="x")

    def display_track_info(self, track, playlist):
        """
        Display radar chart information for the selected track.

        Args:
            track: The selected track object.
            playlist: The playlist object containing the track.
        """
        self.display_radar_chart(track, playlist)

    def display_radar_chart(self, track, playlist):
        """
        Display the radar chart for the selected track or playlist.

        Args:
            track: The selected track object (or None for playlist level chart).
            playlist: The playlist object.
        """
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        categories, avg_values, track_values = self.controller.create_radar_chart_data(playlist, track)

        if track_values:
            self.controller.create_double_radar_chart(ax, categories, avg_values, track_values)
        else:
            self.controller.create_radar_chart(ax, categories, avg_values)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, fill="both", expand=True)

    def display_summary(self, playlist):
        """
        Display the summary and cover image for the selected playlist.

        Args:
            playlist: The selected playlist object.
        """
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
    playlist_view = PlaylistsStatsView(app, controller, bg_color="#8AA7A9", width=200, height=500)
    playlist_view.pack(padx=20, pady=20, fill="both", expand=True)

    app.mainloop()
