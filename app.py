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

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme('green')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setting up Initial Things
        self.title("Sample Tkinter Structuring")
        self.geometry("720x550")
        self.resizable(True, True)
        self.sp = SpotifyUser()
        # self.sp = None

        # Creating the left navigation frame
        navigation_frame = ctk.CTkFrame(self, width=200, bg_color="#8AA7A9")
        navigation_frame.pack(side="left", fill="y")

        # Creating the container for the main content
        container = ctk.CTkFrame(self, bg_color="#8AA7A9")
        container.pack(side="right", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize Frames
        self.frames = {}
        self.HomePage = HomePage
        self.Validation = TopTracksView

        # starting page
        self.frames[HomePage] = HomePage(container, bg_color="#8AA7A9", spotify_user=self.sp)

        # top tracks frame
        self.frames[TopTracksView] = TopTracksView(container, bg_color="#8AA7A9", spotify_user=self.sp)
        self.frames[TopArtistView] = TopArtistView(container, bg_color="#8AA7A9", spotify_user=self.sp)

        # playlist stats frame
        playlist_controller = PlaylistStatsController(self.sp)
        self.frames[PlaylistsView] = PlaylistsView(container, playlist_controller, width=500, height=500)

        # top artist frame
        self.frames[ArtistPlaylistView] = ArtistPlaylistView(container, self.sp)
        playlist_model = PlaylistModelArtists(self.sp.get_authorized_spotify_object(), 'artist')
        playlist_controller = PlaylistController(playlist_model, self.frames[ArtistPlaylistView])
        self.frames[ArtistPlaylistView].controller = playlist_controller

        # playlist generator frame
        self.frames[TrackPlaylistView] = TracksPlaylistView(container, self.sp.get_authorized_spotify_object())
        playlist_model_tracks = PlaylistModelArtists(self.sp.get_authorized_spotify_object(), 'track')
        playlist_controller_tracks = PlaylistController(playlist_model_tracks, self.frames[TrackPlaylistView])
        self.frames[TrackPlaylistView].controller = playlist_controller_tracks

        #playkist generator by genre and other features
        view = GenresPlaylistGeneratorView(container)
        self.frames[GenresPlaylistGeneratorView] = view
        view.set_controller(PlaylistGeneratorGenController(view, self.sp))


        # placing the frames in the container
        for F in [HomePage, TopTracksView, TopArtistView, ArtistPlaylistView, TrackPlaylistView,
                  PlaylistsView, GenresPlaylistGeneratorView]:
            frame = self.frames[F]
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

        # Adding navigation buttons
        home_button = ctk.CTkButton(navigation_frame, text="Home Page", command=lambda: self.show_frame(HomePage))
        home_button.pack(pady=10, padx=10)

        validation_button = ctk.CTkButton(navigation_frame, text="Top Tracks",
                                          command=lambda: self.show_frame(TopTracksView))
        validation_button.pack(pady=10, padx=10)

        top_artists_button = ctk.CTkButton(navigation_frame, text="Top Artists",
                                           command=lambda: self.show_frame(TopArtistView))
        top_artists_button.pack(pady=10, padx=10)

        playlist_overview_button = ctk.CTkButton(navigation_frame, text="Playlist Overview",
                                                 command=lambda: self.show_frame(PlaylistsView))
        playlist_overview_button.pack(pady=10, padx=10)

        playlist_button = ctk.CTkButton(navigation_frame, text="Playlist Generator",
                                        command=lambda: self.show_frame(ArtistPlaylistView))
        playlist_button.pack(pady=10, padx=10)

        track_playlist_button = ctk.CTkButton(navigation_frame, text='Generate Playlist by Tracks',
                                              command=lambda: self.show_frame(TrackPlaylistView))
        track_playlist_button.pack(pady=10, padx=10)

        genre_playlist_button = ctk.CTkButton(navigation_frame, text='Generate Playlist by Genres',
                                                command=lambda: self.show_frame(GenresPlaylistGeneratorView))
        genre_playlist_button.pack(pady=10, padx=10)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
