import requests
from PIL import Image
from io import BytesIO
import customtkinter as ctk
from models.artist import Artist
from models.music_player import MusicPlayer
from models.user_data import SpotifyUser
from controllers.music_player_controler import ArtistInfoController


class ArtistInfoView(ctk.CTkFrame):
    def __init__(self, parent, artist: Artist, music_player: MusicPlayer):
        super().__init__(parent)
        self.artist = artist
        self.music_player = music_player
        self.progress_var = ctk.DoubleVar()
        self.current_track_uri = None
        self.controller = ArtistInfoController(self, music_player)

        self.create_widgets()
        self.update_progress()

    def create_widgets(self):
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

    def update_and_play(self, track_uri):
        self.current_track_uri = track_uri
        self.controller.play_toggle(track_uri)

    def play_current_track(self):
        if self.current_track_uri:
            self.update_and_play(self.current_track_uri)
        else:
            print("No track selected")
    def update_progress(self):
        self.controller.update_progress()
        self.after(300, self.update_progress)

    def close_window(self):
        # destroy music player and remove file
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
