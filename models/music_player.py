import pygame
import requests
import os
import uuid
import threading
import time


class MusicPlayer:
    """
    Class responsible for playing music
    Music is given in the form of a URL
    """
    def __init__(self):
        """
        Initialize the music player
        """
        pygame.mixer.init()
        self.local_file_path = None
        self.last_url = None
        self.paused = False
        self.playing = False
        self.start_time = None
        self.paused_start = None
        self.total_paused_time = 0
        self.duration = 0
        self.update_timer = None

    def play_music(self, preview_url):
        """
        Temporarily download and play the music from the given URL
        :param preview_url: link to the music preview
        :return: None
        """

        #Check if the URL is different from the last one
        if self.last_url != preview_url:
            self.reset_player()
            self.download_preview(preview_url)
            self.last_url = preview_url

        if not self.playing:
            pygame.mixer.music.load(self.local_file_path)
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            self.start_time = time.time()
            self.total_paused_time = 0
            self.duration = pygame.mixer.Sound(self.local_file_path).get_length()
            self.start_update_timer()
        else:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.total_paused_time += time.time() - self.paused_start
                self.start_update_timer()
            else:
                pygame.mixer.music.pause()
                self.paused = True
                self.paused_start = time.time()
                if self.update_timer:
                    self.update_timer.cancel()

    def stop_music(self):
        """
        Stop the music, handle the timer
        :return: None
        """
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        self.total_paused_time = 0
        if self.update_timer:
            self.update_timer.cancel()

    def reset_player(self):
        """
        Reset the player, unload the music and remove the local file
        :return: None
        """
        self.stop_music()
        pygame.mixer.music.unload()
        if self.local_file_path and os.path.exists(self.local_file_path):
            os.remove(self.local_file_path)
        self.local_file_path = None
        self.last_url = None  # Resetowanie ostatniego URL

    def download_preview(self, preview_url):
        """
        Download the music preview from the given URL
        :param preview_url: link to the music preview
        :return: None
        """
        response = requests.get(preview_url)
        response.raise_for_status()
        unique_filename = f"preview_{uuid.uuid4()}.mp3"
        self.local_file_path = unique_filename
        with open(self.local_file_path, "wb") as f:
            f.write(response.content)

    def get_progress(self):
        """
        Calculate the progress of the music
        :return: percentage of the music played
        """
        if self.playing:
            if self.paused:
                elapsed_time = self.paused_start - self.start_time - self.total_paused_time
            else:
                elapsed_time = time.time() - self.start_time - self.total_paused_time
            if self.duration > 0:
                return min(elapsed_time / self.duration, 1)
        return 0

    def start_update_timer(self):
        """
        Start the update timer in a separate thread
        :return: None
        """
        if self.update_timer:
            self.update_timer.cancel()
        self.update_timer = threading.Timer(0.5, self.update_progress)
        self.update_timer.start()

    def update_progress(self):
        """
        Update the progress of the music
        :return: None
        """
        progress = self.get_progress()
        if self.playing and not self.paused:
            self.start_update_timer()
