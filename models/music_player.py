import pygame
import requests
import os
import uuid
import threading
import time


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.local_file_path = None
        self.paused = False
        self.playing = False
        self.start_time = None
        self.duration = 0
        self.update_timer = None

    def play_music(self, preview_url):
        if not self.playing:
            if not self.local_file_path:
                self.download_preview(preview_url)
            pygame.mixer.music.load(self.local_file_path)
            pygame.mixer.music.play()
            self.playing = True
            self.paused = False
            self.start_time = time.time()
            self.duration = pygame.mixer.Sound(self.local_file_path).get_length()
            self.start_update_timer()
        else:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.start_time = time.time() - self.paused_duration
                self.start_update_timer()
            else:
                pygame.mixer.music.pause()
                self.paused = True
                self.paused_duration = time.time() - self.start_time
                if self.update_timer:
                    self.update_timer.cancel()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        if self.update_timer:
            self.update_timer.cancel()

    def reset_player(self):
        self.stop_music()
        if os.path.exists(self.local_file_path):
            os.remove(self.local_file_path)
        self.local_file_path = None

    def download_preview(self, preview_url):
        response = requests.get(preview_url)
        response.raise_for_status()
        unique_filename = f"preview_{uuid.uuid4()}.mp3"
        self.local_file_path = unique_filename
        with open(self.local_file_path, "wb") as f:
            f.write(response.content)

    def get_progress(self):
        if self.playing and not self.paused:
            elapsed_time = time.time() - self.start_time
            if self.duration > 0:
                return elapsed_time / self.duration
        return 0

    def start_update_timer(self):
        if self.update_timer:
            self.update_timer.cancel()
        self.update_timer = threading.Timer(0.5, self.update_progress)
        self.update_timer.start()

    def update_progress(self):
        progress = self.get_progress()
        # Update the GUI with the current progress
        print(f"Progress: {progress * 100:.2f}%")
        if self.playing and not self.paused:
            self.start_update_timer()
