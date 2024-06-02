import customtkinter as ctk
from models.user_data import *
from views.topviews.toptracksview import TopTracksView
from views.homepage import HomePage
from views.topviews.topartistview import TopArtistView
from views.playlist_generator_artists import ArtistPlaylistView, TracksPlaylistView
from views.playlist_generator_tracks import TrackPlaylistView
from models.playlist_model import PlaylistModelArtists
from controllers.playlist_controler import PlaylistController
from models.playlists import PlaylistsView
from controllers.playlist_stats_controller import PlaylistStatsController
from views.playlist_generator_genre import GenresPlaylistGeneratorView
from controllers.playlist_generator_genre_controller import PlaylistGeneratorGenController
from views.gemini_playlist_view import GeminiPlaylistView
from controllers.gemini_playlist_controller import GeminiPLaylistController

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme('green')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setting up Initial Things
        self.title("Sample Tkinter Structuring")
        self.geometry("720x550")
        self.resizable(True, True)

        self.sp = None  # SpotifyUser will be initialized after authorization

        # Creating the left navigation frame
        self.navigation_frame = ctk.CTkFrame(self, width=200, bg_color="#8AA7A9")

        # Creating the container for the main content
        self.container = ctk.CTkFrame(self, bg_color="#8AA7A9")

        # Initialize Frames
        self.frames = {}
        self.initialized_frames = set()

        # Start with the authorization frame
        self.show_authorization_frame()

    def show_authorization_frame(self):
        self.authorization_frame = ctk.CTkFrame(self, bg_color="#8AA7A9")
        self.authorization_frame.pack(fill="both", expand=True)
        authorize_button = ctk.CTkButton(self.authorization_frame, text="Autoryzuj", command=self.authorize_user)
        authorize_button.pack(pady=20, padx=20)

    def authorize_user(self):
        self.sp = SpotifyUser()  # Autoryzacja użytkownika

        # Removing authorization frame
        self.authorization_frame.pack_forget()

        # Packing the main frames
        self.navigation_frame.pack(side="left", fill="y")
        self.container.pack(side="right", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Adding navigation buttons
        self.add_navigation_buttons()

        self.show_frame(HomePage)

    def add_navigation_buttons(self):
        home_button = ctk.CTkButton(self.navigation_frame, text="Home Page", command=lambda: self.show_frame(HomePage))
        home_button.pack(pady=10, padx=10)

        validation_button = ctk.CTkButton(self.navigation_frame, text="Top Tracks",
                                          command=lambda: self.show_frame(TopTracksView))
        validation_button.pack(pady=10, padx=10)

        top_artists_button = ctk.CTkButton(self.navigation_frame, text="Top Artists",
                                           command=lambda: self.show_frame(TopArtistView))
        top_artists_button.pack(pady=10, padx=10)

        playlist_overview_button = ctk.CTkButton(self.navigation_frame, text="Playlist Overview",
                                                 command=lambda: self.show_frame(PlaylistsView))
        playlist_overview_button.pack(pady=10, padx=10)

        playlist_button = ctk.CTkButton(self.navigation_frame, text="Playlist Generator",
                                        command=lambda: self.show_frame(ArtistPlaylistView))
        playlist_button.pack(pady=10, padx=10)

        track_playlist_button = ctk.CTkButton(self.navigation_frame, text='Generate Playlist by Tracks',
                                              command=lambda: self.show_frame(TrackPlaylistView))
        track_playlist_button.pack(pady=10, padx=10)

        genre_playlist_button = ctk.CTkButton(self.navigation_frame, text='Generate Playlist by Genres',
                                              command=lambda: self.show_frame(GenresPlaylistGeneratorView))
        genre_playlist_button.pack(pady=10, padx=10)

        gemini_playlist_button = ctk.CTkButton(self.navigation_frame, text='AI playlist generator',
                                                command=lambda: self.show_frame(GeminiPlaylistView))
        gemini_playlist_button.pack(pady=10, padx=10)

    def create_frame(self, frame_class):
        if frame_class == HomePage:
            frame = HomePage(self.container, bg_color="#8AA7A9", spotify_user=self.sp)
        elif frame_class == TopTracksView:
            frame = TopTracksView(self.container, bg_color="#8AA7A9", spotify_user=self.sp)
        elif frame_class == TopArtistView:
            frame = TopArtistView(self.container, bg_color="#8AA7A9", spotify_user=self.sp)
        elif frame_class == PlaylistsView:
            playlist_controller = PlaylistStatsController(self.sp)
            frame = PlaylistsView(self.container, playlist_controller, width=500, height=500)
        elif frame_class == ArtistPlaylistView:
            frame = ArtistPlaylistView(self.container, self.sp)
            playlist_model = PlaylistModelArtists(self.sp.get_authorized_spotify_object(), 'artist')
            playlist_controller = PlaylistController(playlist_model, frame)
            frame.controller = playlist_controller
        elif frame_class == TrackPlaylistView:
            frame = TracksPlaylistView(self.container, self.sp.get_authorized_spotify_object())
            playlist_model_tracks = PlaylistModelArtists(self.sp.get_authorized_spotify_object(), 'track')
            playlist_controller_tracks = PlaylistController(playlist_model_tracks, frame)
            frame.controller = playlist_controller_tracks
        elif frame_class == GenresPlaylistGeneratorView:
            frame = GenresPlaylistGeneratorView(self.container)
            frame.set_controller(PlaylistGeneratorGenController(frame, self.sp))
        elif frame_class == GeminiPlaylistView:
            frame = GeminiPlaylistView(self.container)
            frame.set_controller(GeminiPLaylistController(frame, self.sp))
        return frame

    def show_frame(self, cont):
        if cont not in self.frames:
            frame = self.create_frame(cont)
            self.frames[cont] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
