from views.trackinfo import TrackInfoWindow
import customtkinter as ctk
import tkinter as tk
from models.music_player import MusicPlayer
from models.track import Track


class PlaylistController:
    """
    Controller class for controlling playlist generation
    """

    def __init__(self, model, view):
        """
        :param model:
        :param view:
        """
        self.model = model
        self.view = view
        self.view.controller = self

    def search_artist(self):
        """
        Search for artist
        :return:
        """
        artist_name = self.view.search_entry.get()
        results = self.model.search_artist(artist_name)
        self.view.update_results(results)

    def show_more_info(self):
        """
        Show more info about selected artist
        :return:
        """
        selection = self.view.results_listbox.curselection()
        if selection:
            index = selection[0]
            artist = self.model.search_results[index]
            self.view.show_artist_details(artist)

    def add_artist(self):
        """
        Add selected artist to selected list
        :return:
        """
        selected_index = self.view.results_listbox.curselection()
        if selected_index:
            artist = self.model.search_results[selected_index[0]]
            self.model.add_artist(artist)
            self.view.update_selected_listbox(self.model.selected_artists)

    def clear_selected_artists(self):
        """
        Clear selected artists list
        :return:
        """
        self.model.clear_selected_artists()
        self.view.update_selected_listbox(self.model.selected_artists)

    def generate_playlist(self):
        """
        Generate playlist
        :return:
        """
        playlist = self.model.generate_playlist()
        self.view.update_playlist(playlist)

    def download_playlist(self, name, description):
        """
        Download playlist
        :param name:
        :param description:
        :return:
        """
        if name:
            self.model.download_playlist(name=name, description=description)
            playlist_added_window = ctk.CTkToplevel(self.view)
            playlist_added_window.title("Playlist Added")
            playlist_added_label = ctk.CTkLabel(playlist_added_window, text="Playlist added successfully")
            playlist_added_label.pack(padx=10, pady=10)
            ok_button = ctk.CTkButton(playlist_added_window, text="OK", command=playlist_added_window.destroy)
            ok_button.pack(pady=10)
            playlist_added_window.grab_set()
            playlist_added_window.wait_window()
            playlist_added_window.destroy()
        else:
            error_window = ctk.CTkToplevel(self.view)
            error_window.title("Error")
            error_label = ctk.CTkLabel(error_window, text="Name cannot be empty")
            error_label.pack(padx=10, pady=10)
            ok_button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
            ok_button.pack(pady=10)
            error_window.grab_set()
            error_window.wait_window()
            error_window.destroy()

    def delete_track(self, index):
        """
        Delete track from playlist and update view
        :param index:
        :return:
        """
        if index < len(self.model.generated_playlist):
            self.model.generated_playlist.pop(index)
            self.view.update_playlist(self.model.generated_playlist)

    def preview_track(self, index):
        """
        Preview selected track
        :param index:
        :return:
        """
        if index < len(self.model.generated_playlist_uris):
            track_uri = self.model.generated_playlist_uris[index]

            canvas = ctk.CTkCanvas(self.view, width=500, bg='#2C2C2C')

            canvas.grid(row=0, column=3, padx=10, pady=10, rowspan=500, sticky="nsew")

            # Tworzenie przewijanej ramki na płótnie
            track_info_frame = TrackInfoWindow(canvas, Track(track_uri, self.model.sp), MusicPlayer())
            canvas_frame = canvas.create_window((0, 0), window=track_info_frame, anchor="nw")

            track_info_frame.wait_window()  # Czekanie na zamknięcie okna
            canvas.grid_forget()  # Usunięcie canvas po zamknięciu okna
