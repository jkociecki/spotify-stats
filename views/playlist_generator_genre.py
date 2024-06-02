import customtkinter as ctk
from tkinter import Listbox, END, Scrollbar, RIGHT, LEFT, Y, StringVar
from controllers.playlist_generator_genre_controller import PlaylistGeneratorGenController


class GenresPlaylistGeneratorView(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk):
        super().__init__(parent)
        self.controller = None
        self.generated_playlist_uris = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_widgets()

    def set_controller(self, controller: PlaylistGeneratorGenController):
        self.controller = controller
        self.chart_frame = self.controller.get_radar_chart_frame(self)
        self.chart_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Update the button command now that the controller is set
        self.generate_button.configure(command=self.controller.generate_playlist)

    def create_widgets(self):
        # Create the radar chart frame
        self.chart_frame_placeholder = ctk.CTkFrame(self, corner_radius=10)
        self.chart_frame_placeholder.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Create the results frame
        self.results_frame = ctk.CTkFrame(self, corner_radius=10)
        self.results_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=1)

        self.genres_label = ctk.CTkLabel(self.results_frame, text="Select Genres:", font=('Arial', 12, 'bold'))
        self.genres_label.grid(row=0, column=0, pady=10, columnspan=2)

        self.genres_listbox_frame = ctk.CTkFrame(self.results_frame, corner_radius=10)
        self.genres_listbox_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.genres_list = Listbox(self.genres_listbox_frame, selectmode='multiple', bg='#2e2e2e', fg='white',
                                   selectbackground='#1f77b4', font=('Arial', 12))
        self.genres_list.pack(side=LEFT, fill=Y, expand=True)

        self.genres_scrollbar = Scrollbar(self.genres_listbox_frame, orient='vertical', command=self.genres_list.yview)
        self.genres_scrollbar.pack(side=RIGHT, fill=Y)

        self.genres_list.config(yscrollcommand=self.genres_scrollbar.set)

        self.playlist_listbox_frame = ctk.CTkFrame(self.results_frame, corner_radius=10)
        self.playlist_listbox_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.playlist_listbox = Listbox(self.playlist_listbox_frame, bg='#2e2e2e', fg='white', font=('Arial', 12))
        self.playlist_listbox.pack(fill='both', expand=True)

        self.generate_button = ctk.CTkButton(self.results_frame, text="Generate Playlist", command=lambda: None)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Create the controls frame
        self.controls_markets_frame = ctk.CTkFrame(self)
        self.controls_markets_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.controls_markets_frame.grid_columnconfigure(0, weight=1)
        self.controls_markets_frame.grid_columnconfigure(1, weight=1)

        self.controls_frame = ctk.CTkFrame(self.controls_markets_frame, corner_radius=10)
        self.controls_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.markets_frame = ctk.CTkFrame(self.controls_markets_frame, corner_radius=10)
        self.markets_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.playlist_name_label = ctk.CTkLabel(self.controls_frame, text="Playlist Name:", font=('Arial', 12, 'bold'))
        self.playlist_name_label.pack(pady=5)
        self.playlist_name_entry = ctk.CTkEntry(self.controls_frame)
        self.playlist_name_entry.pack(fill='x', padx=10, pady=5)

        self.playlist_desc_label = ctk.CTkLabel(self.controls_frame, text="Playlist Description:",
                                                font=('Arial', 12, 'bold'))
        self.playlist_desc_label.pack(pady=5)
        self.playlist_desc_entry = ctk.CTkEntry(self.controls_frame)
        self.playlist_desc_entry.pack(fill='x', padx=10, pady=5)

        self.preview_button = ctk.CTkButton(self.controls_frame, text="Preview Track",
                                            command=lambda: self.controller.preview_track())
        self.preview_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(self.controls_frame, text="Delete Track",
                                           command=lambda: self.controller.delete_track())
        self.delete_button.pack(pady=5)

        self.country_var = StringVar(value="PL")
        countries = [("PL", "PL"), ("US", "US"), ("GB", "GB")]
        for text, country in countries:
            radio_button = ctk.CTkRadioButton(self.markets_frame, text=text, variable=self.country_var, value=country)
            radio_button.pack(pady=2, anchor='w')

        self.playlist_tracks_entry = ctk.CTkEntry(self.markets_frame, placeholder_text="Number of tracks")
        self.playlist_tracks_entry.pack(fill='x', padx=10, pady=10)

        self.download_button = ctk.CTkButton(self.controls_frame, text="Download Playlist",
                                            command=lambda: self.controller.download_playlist(
                                                name=self.playlist_name_entry.get(),
                                                description=self.playlist_desc_entry.get()
                                            ))
        self.download_button.pack(pady=5)

    def load_genres(self, genres: list):
        for genre in genres:
            self.genres_list.insert(END, genre)

    def get_selected_genres(self):
        selected_indices = self.genres_list.curselection()
        return [self.genres_list.get(i) for i in selected_indices]

    def get_playlist_tracks_entry(self):
        return self.playlist_tracks_entry.get()

    def clear_tracks_entry(self):
        self.playlist_tracks_entry.delete(0, END)

    def update_playlist(self, track_names: list):
        self.playlist_listbox.delete(0, END)
        for name in track_names:
            self.playlist_listbox.insert(END, name)


import customtkinter as ctk
from models.user_data import SpotifyUser

if __name__ == "__main__":
    spotify_user = SpotifyUser()

    root = ctk.CTk()
    root.geometry("1200x800")

    # Create the view
    view = GenresPlaylistGeneratorView(root)
    # Create the controller
    controller = PlaylistGeneratorGenController(view, spotify_user)
    # Assign the controller to the view
    view.set_controller(controller)

    view.pack(expand=True, fill="both")
    root.mainloop()
