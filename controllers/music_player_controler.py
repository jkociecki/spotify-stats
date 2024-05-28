
class TrackInfoController:
    def __init__(self, view, music_player):
        self.view = view
        self.music_player = music_player
        self.track = view.track

    def close_window(self):
        self.view.destroy()
        self.music_player.reset_player()

    def play_toggle(self):
        self.music_player.play_music(self.track.preview_url)
        if self.music_player.playing:
            if self.music_player.paused:
                self.view.play_button.configure(text="Play")
            else:
                self.view.play_button.configure(text="Pause")
        else:
            self.view.play_button.configure(text="Play")

    def stop_music(self):
        self.music_player.stop_music()
        self.view.play_button.configure(text="Play")
        self.view.progress_var.set(0)

    def update_progress(self):
        progress = self.music_player.get_progress()
        self.view.progress_var.set(progress)
