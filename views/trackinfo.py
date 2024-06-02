import requests
import pygame
from tkinter import *
from PIL import Image
from io import BytesIO
import customtkinter as ctk
from controllers.music_player_controler import TrackInfoController
from models.track import Track
from models.music_player import MusicPlayer


class TrackInfoWindow(ctk.CTkFrame):
    """
    A custom Tkinter frame to display and control track information and playback.

    Attributes:
        track (Track): The track to display information for.
        music_player (MusicPlayer): The music player instance for controlling playback.
        progress_var (DoubleVar): Variable to track the progress of the track.
    """

    def __init__(self, parent, track: Track, music_player: MusicPlayer, *args, **kwargs):
        """
        Initialize the TrackInfoWindow.

        Args:
            parent: The parent Tkinter widget.
            track (Track): The track to display information for.
            music_player (MusicPlayer): The music player instance for controlling playback.
            *args: Additional arguments for the Tkinter Frame.
            **kwargs: Additional keyword arguments for the Tkinter Frame.
        """
        super().__init__(parent, *args, **kwargs)
        self.track = track
        self.music_player = music_player
        self.progress_var = DoubleVar()

        self.controller = TrackInfoController(self, music_player)

        # Set width and height of window
        self.width = 2000
        self.height = 550

        self.create_widgets()
        self.update_progress()

    def close_window(self):
        """
        Close the track information window.
        """
        self.controller.close_window()

    def create_widgets(self):
        """
        Create and arrange the widgets in the TrackInfoWindow.
        """
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=10, pady=10)

        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(pady=10)

        self.close_button = ctk.CTkButton(controls_frame, text="Zamknij", command=self.close_window)
        self.close_button.grid(row=0, column=0, padx=10)

        image_frame = ctk.CTkFrame(main_frame)
        image_frame.pack(pady=10)

        try:
            response = requests.get(self.track.cover_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image_ctk = ctk.CTkImage(light_image=image, dark_image=image, size=(250, 250))
            image_label = ctk.CTkLabel(image_frame, image=image_ctk, text='')
            image_label.pack(pady=10)
        except requests.RequestException as e:
            print(f"Failed to load image: {e}")

        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(pady=10)

        artist_label = ctk.CTkLabel(info_frame, text="Artist: " + self.track.artist)
        artist_label.grid(row=0, column=0, padx=10, pady=5)

        track_label = ctk.CTkLabel(info_frame, text="Track Name: " + self.track.title)
        track_label.grid(row=1, column=0, padx=10, pady=5)

        release_label = ctk.CTkLabel(info_frame, text="Release Date: " + self.track.release_date)
        release_label.grid(row=2, column=0, padx=10, pady=5)

        popularity_label = ctk.CTkLabel(info_frame, text="Popularity: " + str(self.track.popularity))
        popularity_label.grid(row=3, column=0, padx=10, pady=5)

        duration_label = ctk.CTkLabel(info_frame, text="Duration: " + str(self.track.duration_ms / 1000) + "s")
        duration_label.grid(row=4, column=0, padx=10, pady=5)

        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(side='bottom', pady=17)

        self.play_button = ctk.CTkButton(controls_frame, text="Play", command=self.controller.play_toggle)
        self.play_button.grid(row=0, column=0, padx=10)

        self.stop_button = ctk.CTkButton(controls_frame, text="Stop", command=self.controller.stop_music)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.progress_bar = ctk.CTkProgressBar(controls_frame, variable=self.progress_var)
        self.progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def update_progress(self):
        """
        Update the progress bar to reflect the current playback position of the track.
        """
        self.controller.update_progress()
        self.after(300, self.update_progress)
