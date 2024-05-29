from views.trackinfo import TrackInfoWindow
import customtkinter as ctk
import tkinter as tk
from models.music_player import MusicPlayer
from models.track import Track


class PlaylistController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self

    def search_artist(self):
        artist_name = self.view.search_entry.get()
        results = self.model.search_artist(artist_name)
        self.view.update_results(results)

    def show_more_info(self):
        selection = self.view.results_listbox.curselection()
        if selection:
            index = selection[0]
            artist = self.model.search_results[index]
            self.view.show_artist_details(artist)

    def add_artist(self):
        selected_index = self.view.results_listbox.curselection()
        if selected_index:
            artist = self.model.search_results[selected_index[0]]
            self.model.add_artist(artist)
            self.view.update_selected_artists_listbox(self.model.selected_artists)

    def clear_selected_artists(self):
        self.model.clear_selected_artists()
        self.view.update_selected_artists_listbox(self.model.selected_artists)

    def generate_playlist(self):
        playlist = self.model.generate_playlist()
        self.view.update_playlist(playlist)

    def download_playlist(self):
        self.model.download_playlist()

    def delete_track(self, index):
        if index < len(self.model.generated_playlist):
            self.model.generated_playlist.pop(index)
            self.view.update_playlist(self.model.generated_playlist)

    def preview_track(self, index):
        if index < len(self.model.generated_playlist_uris):
            track_uri = self.model.generated_playlist_uris[index]

            # Tworzenie przewijanego kontenera z Canvas i Scrollbar
            canvas = ctk.CTkCanvas(self.view)  # Możesz spróbować z ctk.CTkCanvas, jeśli zachowuje odpowiednie funkcje
            scrollbar = ctk.CTkScrollbar(self.view, command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.grid(row=0, column=3, padx=10, pady=10, rowspan=600, sticky="nsew")
            scrollbar.grid(row=0, column=4, padx=10, pady=10, rowspan=200, sticky="ns")

            # Tworzenie przewijanej ramki na płótnie
            track_info_frame = TrackInfoWindow(canvas, Track(track_uri, self.model.sp), MusicPlayer())
            canvas_frame = canvas.create_window((0, 0), window=track_info_frame, anchor="nw")

            # Ustawienie obszaru przewijania
            track_info_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            track_info_frame.wait_window()  # Czekanie na zamknięcie okna
            canvas.grid_forget()  # Usunięcie canvas po zamknięciu okna



