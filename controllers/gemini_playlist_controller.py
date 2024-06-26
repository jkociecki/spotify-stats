from models.gemini_playlist_generator import PlaylistGeneratorAiModel
from tkinter import END, messagebox
from views.trackinfo import TrackInfoWindow
from models.track import Track
from models.music_player import MusicPlayer
import customtkinter as ctk
from views.popups import show_pop_up_window


class GeminiPLaylistController:
    def __init__(self, view, spotify_user):
        self.view = view
        self.model = PlaylistGeneratorAiModel(spotify_user)
        self.view.set_controller(self)

    def generate_playlist(self):
        self.view.playlist_listbox.delete(0, END)
        self.view.generated_playlist_uris = []
        description = self.view.description_entry.get("1.0", END)
        amount = self.view.amount_entry.get()
        if not amount.isdigit():
            show_pop_up_window(self.view, "Please enter a valid number of tracks.", "Error")
            return
        if not amount:
            show_pop_up_window(self.view, "Please enter a number of tracks.", "Error")
            return
        if description and amount:
            tracks = self.model.create_playlist(description, int(amount))
            self.view.update_playlist(tracks)

    def preview_song(self):
        index = self.view.playlist_listbox.curselection()
        if index:
            index = index[0]
            if index < len(self.view.generated_playlist_uris):
                track_uri = self.view.generated_playlist_uris[index]
                print(f"Previewing song with URI: {track_uri}")

                # Create a new top-level window for the track info
                preview_window = ctk.CTkToplevel(self.view)
                preview_window.title("Track Info")

                # Create the TrackInfoWindow inside the new window
                track_info_frame = TrackInfoWindow(preview_window, Track(track_uri, self.model.sp), MusicPlayer())
                track_info_frame.pack(fill="both", expand=True)

                preview_window.grab_set()  # Make the new window modal
        else:
            messagebox.showwarning("Warning", "Please select a song to preview.")

    def delete_track(self):
        index = self.view.playlist_listbox.curselection()[0]
        self.view.playlist_listbox.delete(index)
        self.view.generated_playlist_uris.pop(index)

    def download_playlist(self):
        name = self.view.playlist_name_entry.get()
        description = self.view.description_entry.get('1.0', 'end-1c')
        if name:
            self.model.sp.user_playlist_create(user=self.model.sp.me()['id'], name=name, description=description)
            playlist_id = self.model.sp.current_user_playlists()['items'][0]['id']
            self.model.sp.playlist_add_items(playlist_id, self.view.generated_playlist_uris)
            show_pop_up_window(self.view, "Success", "Playlist downloaded successfully.")
        else:
            show_pop_up_window(self.view, "Error", "Please enter a playlist name.")
