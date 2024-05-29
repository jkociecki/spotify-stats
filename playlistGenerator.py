from tkinter.constants import SINGLE
from models.user_data import SpotifyUser
import customtkinter as ctk
from tkinter import Listbox, StringVar, Toplevel, Label, END
from PIL import Image, ImageTk
import io
import requests
from controllers.playlist_controler import PlaylistController
from models.playlist_model import PlaylistModel


class PlaylistView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.controller = None  # Początkowo ustaw na None
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.setup_ui()

    def setup_ui(self):
        # Search Frame
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search for artists...")
        self.search_entry.pack(fill="x", padx=10, pady=10)
        self.button_frame = ctk.CTkFrame(self.search_frame)
        self.button_frame.pack(fill="x", padx=10, pady=10)
        self.search_button = ctk.CTkButton(self.button_frame, text="Search",
                                           command=lambda: self.controller.search_artist())
        self.search_button.pack(side="left", padx=10, pady=10)
        self.more_info_button = ctk.CTkButton(self.button_frame, text="More Info",
                                              command=lambda: self.controller.show_more_info())
        self.more_info_button.pack(side="left", padx=10, pady=10)
        self.results_listbox = Listbox(self.search_frame, selectmode=SINGLE, bg="#2C2C2C", fg="#FFFFFF")
        self.results_listbox.pack(expand=True, fill="both", padx=10, pady=10)
        self.add_artist_frame = ctk.CTkFrame(self.search_frame)
        self.add_artist_frame.pack(fill="x", padx=10, pady=10)
        self.add_artist_button = ctk.CTkButton(self.add_artist_frame, text="Add Selected Artist",
                                               command=lambda: self.controller.add_artist())
        self.add_artist_button.pack(fill="x", padx=10, pady=10)
        self.clear_button = ctk.CTkButton(self.add_artist_frame, text="Clear Selected Artists",
                                          command=lambda: self.controller.clear_selected_artists())
        self.clear_button.pack(fill="x", padx=10, pady=10)

        # Artist List Frame
        self.artist_list_frame = ctk.CTkFrame(self)
        self.artist_list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.selected_artists_listbox = Listbox(self.artist_list_frame, bg="#2C2C2C", fg="#FFFFFF",
                                                highlightthickness=0)
        self.selected_artists_listbox.pack(expand=True, fill="both", padx=10, pady=10)

        # Playlist Generation Form Frame
        self.form_frame = ctk.CTkFrame(self.artist_list_frame)
        self.form_frame.pack(fill="x", padx=10, pady=10)
        self.playlist_name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter playlist name")
        self.playlist_name_entry.pack(pady=10, fill="x")
        self.playlist_desc_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter playlist description")
        self.playlist_desc_entry.pack(pady=10, fill="x")
        self.num_tracks_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Number of tracks")
        self.num_tracks_entry.pack(pady=10, fill="x")

        self.country_var = StringVar(value="PL")
        countries = [("PL", "PL"), ("US", "US"), ("GB", "GB")]
        for text, country in countries:
            radio_button = ctk.CTkRadioButton(self.form_frame, text=text, variable=self.country_var, value=country)
            radio_button.pack(pady=2, anchor='w')

        self.generate_playlist_button = ctk.CTkButton(self.form_frame, text="Generate Playlist",
                                                      command=lambda: self.controller.generate_playlist())
        self.generate_playlist_button.pack(pady=10)
        self.download_playlist_button = ctk.CTkButton(self.form_frame, text="Download Playlist",
                                                      command=lambda: self.controller.download_playlist())
        self.download_playlist_button.pack(pady=10)

        # Playlist Frame
        self.playlist_frame = ctk.CTkFrame(self)
        self.playlist_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.generated_listbox = Listbox(self.playlist_frame, bg="#2C2C2C", fg="#FFFFFF", highlightthickness=0)
        self.generated_listbox.pack(expand=True, fill="both", padx=10, pady=10)

        # Playlist Buttons Frame
        self.playlist_buttons_frame = ctk.CTkFrame(self.playlist_frame)
        self.playlist_buttons_frame.pack(fill="x", padx=10, pady=10)

        # Konfiguracja kolumn dla równomiernego rozłożenia przycisków
        self.playlist_buttons_frame.grid_columnconfigure(0, weight=1)
        self.playlist_buttons_frame.grid_columnconfigure(1, weight=1)

        self.delete_track_button = ctk.CTkButton(self.playlist_buttons_frame, text="Delete Track",
                                                 command=lambda: self.controller.delete_track(
                                                     self.generated_listbox.curselection()[0]
                                                 ))
        self.delete_track_button.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.preview_track_button = ctk.CTkButton(self.playlist_buttons_frame, text="Preview Track",
                                                  command=lambda: self.controller.preview_track(
                                                        self.generated_listbox.curselection()[0]
                                                  ))
        self.preview_track_button.grid(row=0, column=1, padx=10, pady=10, sticky="we")

    def preview_track(self):
        pass

    def update_results(self, results):
        self.results_listbox.delete(0, END)
        for artist in results:
            self.results_listbox.insert(END, artist['name'])

    def update_selected_artists_listbox(self, selected_artists):
        self.selected_artists_listbox.delete(0, END)
        for artist in selected_artists:
            self.selected_artists_listbox.insert(END, artist['name'])

    def update_playlist(self, playlist):
        self.generated_listbox.delete(0, END)
        for track in playlist:
            self.generated_listbox.insert(END, track)

    def show_artist_details(self, artist):
        detail_window = Toplevel(self)
        detail_window.title(artist['name'])
        detail_window.geometry("300x400")
        if 'images' in artist and artist['images']:
            image_url = artist['images'][0]['url']
            response = requests.get(image_url)
            img_data = Image.open(io.BytesIO(response.content))
            img = img_data.resize((250, 250), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label_img = Label(detail_window, image=photo)
            label_img.image = photo
            label_img.pack(pady=10)
        ctk.CTkLabel(detail_window, text=artist['name'], font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(detail_window, text=f"Followers: {artist['followers']['total']}", font=("Arial", 14)).pack(pady=10)
        ctk.CTkLabel(detail_window, text=f"Popularity: {artist['popularity']}", font=("Arial", 14)).pack(pady=10)




if __name__ == "__main__":
    spotify_user = SpotifyUser().get_authorized_spotify_object()
    root = ctk.CTk()
    root.geometry("1200x800")

    model = PlaylistModel(spotify_user)
    view = PlaylistView(root)  # Przekazanie tylko root bez kontrolera na tym etapie
    controller = PlaylistController(model, view)
    view.controller = controller  # Przypisanie kontrolera do widoku po jego utworzeniu

    view.pack(expand=True, fill="both")
    root.mainloop()

#
# class PlaylistView(ctk.CTkFrame):
#     def __init__(self, master, spotify_user):
#         super().__init__(master)
#         self.sp = spotify_user
#         self.search_results = []
#         self.selected_artists = []
#         self.generated_playlist = []
#         self.generated_playlist_uris = []
#
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure((0, 1, 2), weight=1)
#
#         self.setup_ui()
#
#     def setup_ui(self):
#         # ==================SEARCH RESULTS FRAME==============================
#         self.search_frame = ctk.CTkFrame(self)
#         self.search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
#         self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search for artists...")
#         self.search_entry.pack(fill="x", padx=10, pady=10)
#
#         self.button_frame = ctk.CTkFrame(self.search_frame)
#         self.button_frame.pack(fill="x", padx=10, pady=10)
#         self.search_button = ctk.CTkButton(self.button_frame, text="Search", command=self.search_artist)
#         self.search_button.pack(side="left", padx=10, pady=10)
#         self.more_info_button = ctk.CTkButton(self.button_frame, text="More Info", command=self.show_more_info)
#         self.more_info_button.pack(side="left", padx=10, pady=10)
#
#         self.results_listbox = Listbox(self.search_frame, selectmode=SINGLE, bg="#2C2C2C", fg="#FFFFFF")
#         self.results_listbox.pack(expand=True, fill="both", padx=10, pady=10)
#
#         self.add_artist_frame = ctk.CTkFrame(self.search_frame)
#         self.add_artist_frame.pack(fill="x", padx=10, pady=10)
#         self.add_artist_button = ctk.CTkButton(self.add_artist_frame, text="Add Selected Artist",
#                                                command=self.add_artist)
#         self.add_artist_button.pack(fill="x", padx=10, pady=10)
#         self.clear_button = ctk.CTkButton(self.add_artist_frame, text="Clear Selected Artists",
#                                           command=self.clear_selected_artists)
#         self.clear_button.pack(fill="x", padx=10, pady=10)
#
#         # ========================ARTIST LIST FRAME================================
#         self.artist_list_frame = ctk.CTkFrame(self)
#         self.artist_list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
#         self.selected_artists_listbox = Listbox(self.artist_list_frame, bg="#2C2C2C", fg="#FFFFFF",
#                                                 highlightthickness=0)
#         self.selected_artists_listbox.pack(expand=True, fill="both", padx=10, pady=10)
#
#         # PLAYLIST GENERATION FORM FRAME
#         self.form_frame = ctk.CTkFrame(self.artist_list_frame)
#         self.form_frame.pack(fill="x", padx=10, pady=10)
#
#         # Entry for Playlist Name
#         self.playlist_name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter playlist name")
#         self.playlist_name_entry.pack(pady=10, fill="x")
#
#         # Entry for Playlist Description
#         self.playlist_desc_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter playlist description")
#         self.playlist_desc_entry.pack(pady=10, fill="x")
#
#         # Entry for Number of Tracks
#         self.num_tracks_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Number of tracks")
#         self.num_tracks_entry.pack(pady=10, fill="x")
#
#         # Radio buttons for country selection
#         self.country_var = StringVar(value="PL")
#         countries = [("PL", "PL"), ("US", "US"), ("GB", "GB")]
#         for text, country in countries:
#             radio_button = ctk.CTkRadioButton(self.form_frame, text=text, variable=self.country_var, value=country)
#             radio_button.pack(pady=2, anchor='w')
#
#         # Button to generate playlist
#         self.generate_playlist_button = ctk.CTkButton(self.form_frame, text="Generate Playlist",
#                                                       command=self.generate_playlist)
#         self.generate_playlist_button.pack(pady=10)
#
#         # Button to download playlist
#         self.download_playlist_button = ctk.CTkButton(self.form_frame, text="Download Playlist",
#                                                       command=self.download_playlist)
#         self.download_playlist_button.pack(pady=10)
#
#         # ==============================PLAYLIST FRAME===================================
#         self.playlist_frame = ctk.CTkFrame(self)
#         self.playlist_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
#         self.generated_listbox = Listbox(self.playlist_frame, bg="#2C2C2C", fg="#FFFFFF", highlightthickness=0)
#         self.generated_listbox.pack(expand=True, fill="both", padx=10, pady=10)
#
#     def download_playlist(self):
#         pass
#
#     def search_artist(self):
#         artist = self.search_entry.get()
#         if artist:
#             result = self.sp.search(q=artist, type="artist", limit=10)
#             self.search_results = result['artists']['items']
#             self.update_results()
#
#     def update_results(self):
#         self.results_listbox.delete(0, END)
#         for artist in self.search_results:
#             self.results_listbox.insert(END, artist['name'])
#
#     def show_more_info(self):
#         selection = self.results_listbox.curselection()
#         if selection:
#             index = selection[0]
#             artist = self.search_results[index]
#             self.show_artist_details(artist)
#
#     def add_artist(self):
#         selected_index = self.results_listbox.curselection()
#         if selected_index:
#             artist = self.search_results[selected_index[0]]
#             if artist not in self.selected_artists:
#                 self.selected_artists.append(artist)
#                 self.update_selected_artists_listbox()
#
#     def show_artist_details(self, artist):
#         detail_window = Toplevel(self)
#         detail_window.title(artist['name'])
#         detail_window.geometry("300x400")
#
#         if 'images' in artist and artist['images']:
#             image_url = artist['images'][0]['url']
#             response = requests.get(image_url)
#             img_data = Image.open(io.BytesIO(response.content))
#             img = img_data.resize((250, 250), Image.Resampling.LANCZOS)
#             photo = ImageTk.PhotoImage(img)
#             label_img = Label(detail_window, image=photo)
#             label_img.image = photo
#             label_img.pack(pady=10)
#
#         ctk.CTkLabel(detail_window, text=artist['name'], font=("Arial", 18, "bold")).pack(pady=10)
#         ctk.CTkLabel(detail_window, text=f"Followers: {artist['followers']['total']}", font=("Arial", 14)).pack(pady=10)
#         ctk.CTkLabel(detail_window, text=f"Popularity: {artist['popularity']}", font=("Arial", 14)).pack(pady=10)
#
#     def generate_playlist(self):
#         list_of_uris = [artist['uri'] for artist in self.selected_artists]
#         recommended_tracks = self.sp.recommendations(seed_artists=list_of_uris, limit=10)['tracks']
#         self.generated_playlist = [track['name'] for track in recommended_tracks]
#         self.generated_playlist_uris = [track['uri'] for track in recommended_tracks]
#         self.update_playlist()
#
#     def update_playlist(self):
#         self.generated_listbox.delete(0, END)
#         for track in self.generated_playlist:
#             self.generated_listbox.insert(END, track)
#
#     def update_selected_artists_listbox(self):
#         self.selected_artists_listbox.delete(0, END)
#         for artist in self.selected_artists:
#             self.selected_artists_listbox.insert(END, artist['name'])
#
#     def clear_selected_artists(self):
#         self.selected_artists = []
#         self.update_selected_artists_listbox()


# if __name__ == "__main__":
#     spotify_user = SpotifyUser()
#     app = ctk.CTk()
#     app.title("Playlist Generator")
#     app.geometry("720x550")
#     app.resizable(True, True)
#     playlist_view = PlaylistView(app, spotify_user.get_authorized_spotify_object())
#     playlist_view.pack(expand=True, fill="both")
#     app.mainloop()
