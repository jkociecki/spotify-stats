from tkinter.constants import SINGLE
from models.user_data import SpotifyUser
import customtkinter as ctk
from tkinter import Listbox, StringVar, END
from controllers.playlist_controler import PlaylistController


class BasePlaylistView(ctk.CTkFrame):
    """
    A custom Tkinter frame for generating playlists based on selected artists.

    Attributes:
        controller (PlaylistController): The controller for handling user interactions.
        spotify_user (SpotifyUser): The Spotify user object.
    """

    def __init__(self, master, spotify_user: SpotifyUser):
        """
        Initialize the BasePlaylistView.

        Args:
            master: The parent Tkinter window or frame.
            spotify_user (SpotifyUser): The Spotify user object.
        """
        super().__init__(master)
        self.controller: PlaylistController = None
        self.spotify_user = spotify_user
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        self.create_search_frame()
        self.create_artist_list_frame()
        self.create_playlist_frame()

    def create_search_frame(self):
        """Create the search frame."""
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search...")
        self.search_entry.pack(fill="x", padx=10, pady=10)
        self.search_entry.bind("<Return>", lambda event: self.controller.search_artist())
        self.button_frame = ctk.CTkFrame(self.search_frame)
        self.button_frame.pack(fill="x", padx=10, pady=10)
        self.search_button = ctk.CTkButton(self.button_frame, text="Search", command=lambda: self.controller)
        self.search_button.pack(side="left", padx=10, pady=10)
        self.more_info_button = ctk.CTkButton(self.button_frame, text="More Info",
                                              command=lambda: self.controller.show_more_info())
        self.more_info_button.pack(side="left", padx=10, pady=10)
        self.results_listbox = Listbox(self.search_frame, selectmode=SINGLE, bg="#2C2C2C", fg="#FFFFFF")
        self.results_listbox.pack(expand=True, fill="both", padx=10, pady=10)
        self.add_frame = ctk.CTkFrame(self.search_frame)
        self.add_frame.pack(fill="x", padx=10, pady=10)
        self.add_button = ctk.CTkButton(self.add_frame, text="Add Selected",
                                        command=lambda: self.controller.add_artist())
        self.add_button.pack(fill="x", padx=10, pady=10)
        self.clear_button = ctk.CTkButton(self.add_frame, text="Clear Selected",
                                          command=lambda: self.controller.clear_selected_artists())
        self.clear_button.pack(fill="x", padx=10, pady=10)

    def create_artist_list_frame(self):
        """Create the artist list frame."""
        self.artist_list_frame = ctk.CTkFrame(self)
        self.artist_list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.selected_listbox = Listbox(self.artist_list_frame, bg="#2C2C2C", fg="#FFFFFF", highlightthickness=0)
        self.selected_listbox.pack(expand=True, fill="both", padx=10, pady=10)
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
                                                      command=lambda: self.controller.generate_playlist(
                                                          num_tracks=self.num_tracks_entry.get()
                                                      ))
        self.generate_playlist_button.pack(pady=10)
        self.download_playlist_button = ctk.CTkButton(self.form_frame, text="Download Playlist",
                                                      command=lambda: self.controller.download_playlist(
                                                          name=self.playlist_name_entry.get(),
                                                          description=self.playlist_desc_entry.get()
                                                      ))
        self.download_playlist_button.pack(pady=10)
        self.clear_artists_button = ctk.CTkButton(self.form_frame, text="Clear Artists",
                                                  command=lambda: self.controller.clear_selected_artists())
        self.clear_artists_button.pack(pady=10)

    def create_playlist_frame(self):
        """Create the playlist frame."""
        self.playlist_frame = ctk.CTkFrame(self)
        self.playlist_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.generated_listbox = Listbox(self.playlist_frame, bg="#2C2C2C", fg="#FFFFFF", highlightthickness=0)
        self.generated_listbox.pack(expand=True, fill="both", padx=10, pady=10)
        self.playlist_buttons_frame = ctk.CTkFrame(self.playlist_frame)
        self.playlist_buttons_frame.pack(fill="x", padx=10, pady=10)
        self.playlist_buttons_frame.grid_columnconfigure(0, weight=1)
        self.playlist_buttons_frame.grid_columnconfigure(1, weight=1)
        self.delete_track_button = ctk.CTkButton(self.playlist_buttons_frame, text="Delete Track",
                                                 command=lambda: self.controller.delete_track(
                                                     self.generated_listbox.curselection()[0]))
        self.delete_track_button.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.preview_track_button = ctk.CTkButton(self.playlist_buttons_frame, text="Preview Track",
                                                  command=lambda: self.controller.preview_track(
                                                      self.generated_listbox.curselection()[0]))
        self.preview_track_button.grid(row=0, column=1, padx=10, pady=10, sticky="we")

    def update_results(self, results: list):
        """
        Update the search results listbox with the provided results.

        Args:
            results (list): A list of search results.
        """
        self.results_listbox.delete(0, END)
        for item in results:
            self.results_listbox.insert(END, item['name'])

    def update_selected_listbox(self, selected_items: list):
        """
        Update the selected artists listbox with the provided items.

        Args:
            selected_items (list): A list of selected items.
        """
        self.selected_listbox.delete(0, END)
        for item in selected_items:
            self.selected_listbox.insert(END, item['name'])

    def update_playlist(self, playlist: list):
        """
        Update the generated playlist listbox with the provided tracks.

        Args:
            playlist (list): A list of tracks.
        """
        self.generated_listbox.delete(0, END)
        for track in playlist:
            self.generated_listbox.insert(END, track)

    def show_details(self, item):
        """
        Show details for the selected item. Should be implemented in the subclass.

        Args:
            item: The item for which details should be shown.
        """
        pass
