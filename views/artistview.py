import requests
from PIL import Image
from io import BytesIO
import customtkinter as ctk
from models.artist import Artist
from models.music_player import MusicPlayer
from models.user_data import SpotifyUser
from controllers.music_player_controler import ArtistInfoController


class ArtistInfoView(ctk.CTkFrame):
    """
    A class to represent the artist information view.

    This class inherits from the CTkFrame class and provides functionalities to display detailed information
    about a Spotify artist, including their name, image, popularity, followers, and top tracks.

    Attributes:
        artist (Artist): The artist object containing artist information.
        music_player (MusicPlayer): The music player object to control music playback.
        progress_var (ctk.DoubleVar): Variable to track the progress of the music.
        current_track_uri (str): URI of the current track being played.
        controller (ArtistInfoController): Controller to manage music playback.

    Methods:
        create_widgets(): Create and arrange widgets in the view.
        update_and_play(track_uri): Update the current track URI and play the track.
        play_current_track(): Play the current track if a track is selected.
        update_progress(): Update the progress bar of the current track.
        close_window(): Close the window and reset the music player.
    """

    def __init__(self, parent, artist: Artist, music_player: MusicPlayer):
        """
        Initialize the ArtistInfoView class.

        Parameters:
            parent: The parent widget.
            artist (Artist): The artist object containing artist information.
            music_player (MusicPlayer): The music player object to control music playback.
        """
        super().__init__(parent)
        self.artist = artist
        self.music_player = music_player
        self.progress_var = ctk.DoubleVar()
        self.current_track_uri = None
        self.controller = ArtistInfoController(self, music_player)

        self.create_widgets()
        self.update_progress()

    def create_widgets(self):
        """
        Create and arrange widgets in the view.
        """
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        name_label = ctk.CTkLabel(main_frame, text=self.artist.get_artist_name(), font=("Arial", 18, "bold"))
        name_label.pack(pady=(0, 5))

        try:
            response = requests.get(self.artist.get_artist_image_url())
            image = Image.open(BytesIO(response.content))
            image_ctk = ctk.CTkImage(light_image=image, dark_image=image, size=(150, 150))
            image_label = ctk.CTkLabel(main_frame, image=image_ctk, text='')
            image_label.image = image_ctk
            image_label.pack(pady=5)
        except requests.RequestException as e:
            print(f"Failed to load image: {e}")

        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(pady=5)
        popularity_label = ctk.CTkLabel(info_frame, text=f"Popularity: {self.artist.get_artist_popularity()}")
        popularity_label.pack()
        followers_label = ctk.CTkLabel(info_frame, text=f"Followers: {self.artist.get_artist_followers()}")
        followers_label.pack()

        top_tracks_label = ctk.CTkLabel(info_frame, text="Top Tracks:", font=("Arial", 12, "bold"))
        top_tracks_label.pack(pady=(5, 0))

        for i, track in enumerate(self.artist.get_artist_top_tracks()['tracks']):
            play_button = ctk.CTkButton(info_frame, text=f"Play {track['name']}",
                                        command=lambda track_uri=track['preview_url']: self.update_and_play(track_uri),
                                        width=250, anchor="w")
            play_button.pack(pady=2, fill="x")
            if i == 5:
                break

        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(pady=5)

        self.play_button = ctk.CTkButton(controls_frame, text="Play", command=self.play_current_track)
        self.play_button.grid(row=0, column=0, padx=10)

        self.stop_button = ctk.CTkButton(controls_frame, text="Stop", command=self.controller.stop_music)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.progress_bar = ctk.CTkProgressBar(controls_frame, variable=self.progress_var)
        self.progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.close_button = ctk.CTkButton(main_frame, text="Close", command=self.close_window)
        self.close_button.pack(pady=10)

    def update_and_play(self, track_uri: str):
        """
        Update the current track URI and play the track.

        Parameters:
            track_uri (str): URI of the track to be played.
        """
        self.current_track_uri = track_uri
        self.controller.play_toggle(track_uri)

    def play_current_track(self):
        """
        Play the current track if a track is selected.
        """
        if self.current_track_uri:
            self.update_and_play(self.current_track_uri)
        else:
            print("No track selected")

    def update_progress(self):
        """
        Update the progress bar of the current track.
        """
        self.controller.update_progress()
        self.after(300, self.update_progress)

    def close_window(self):
        """
        Close the window and reset the music player.
        """
        self.music_player.stop_music()
        self.music_player.reset_player()
        self.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    artist = Artist('1co4F2pPNH8JjTutZkmgSm', SpotifyUser())
    music_player = MusicPlayer()
    view = ArtistInfoView(root, artist, music_player)
    view.pack(expand=True, fill="both")
    root.mainloop()
