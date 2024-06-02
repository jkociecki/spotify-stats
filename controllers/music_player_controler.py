import customtkinter as ctk
from models.music_player import MusicPlayer


class MusicControlController:
    """
    Controller class for controlling music player
    """
    def __init__(self, view, music_player: MusicPlayer):
        """
        :param view:
        :param music_player:
        """
        self.view = view
        self.music_player = music_player

    def play_toggle(self, track_uri=None):
        """
        Play or pause music
        :param track_uri:
        :return:
        """
        self.music_player.play_music(track_uri)
        self.update_button_text()

    def stop_music(self):
        """
        Stop (reset) music
        :return:
        """
        self.music_player.stop_music()
        self.view.play_button.configure(text="Play")
        self.view.progress_var.set(0)

    def update_progress(self):
        """
        Update progress bar
        :return:
        """
        progress = self.music_player.get_progress()
        self.view.progress_var.set(progress)

    def update_button_text(self):
        """
        Update button text play/pause
        :return:
        """
        if self.music_player.playing:
            if self.music_player.paused:
                self.view.play_button.configure(text="Play")
            else:
                self.view.play_button.configure(text="Pause")
        else:
            self.view.play_button.configure(text="Play")


class ArtistInfoController(MusicControlController):
    """
    Wrapper controller class for ArtistInfoView
    """
    def __init__(self, view, music_player):
        super().__init__(view, music_player)


class TrackInfoController(MusicControlController):
    """
    Wrapper controller class for TrackInfoView with additional track attribute
    """
    def __init__(self, view, music_player):
        super().__init__(view, music_player)
        self.track = view.track

    def close_window(self):
        self.view.destroy()
        self.music_player.reset_player()

    def play_toggle(self):
        super().play_toggle(self.track.preview_url)
