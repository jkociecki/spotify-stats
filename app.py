import customtkinter as ctk
from models.user_data import *
from views.topviews.toptracksview import TopTracksView
from views.homepage import HomePage
from views.topviews.topartistview import TopArtistView
from playlistGenerator import PlaylistView
from models.playlist_model import PlaylistModel
from controllers.playlist_controler import PlaylistController


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

        self.frames[HomePage] = HomePage(container, bg_color="#8AA7A9", spotify_user=self.sp)
        self.frames[TopTracksView] = TopTracksView(container, bg_color="#8AA7A9", spotify_user=self.sp)
        self.frames[TopArtistView] = TopArtistView(container, bg_color="#8AA7A9", spotify_user=self.sp)
        self.frames[PlaylistView] = PlaylistView(container)
        playlist_model = PlaylistModel(self.sp.get_authorized_spotify_object())
        playlist_controller = PlaylistController(playlist_model, self.frames[PlaylistView])
        self.frames[PlaylistView].controller = playlist_controller

        for F in [HomePage, TopTracksView, TopArtistView, PlaylistView]:
            frame = self.frames[F]
            frame.grid(row=0, column=0, sticky="nsew")

        # Defining Frames and Packing it
        # for F in [HomePage, TopTracksView, TopArtistView, PlaylistView]:
        #     frame = F(container, bg_color="#8AA7A9", spotify_user=self.sp)
        #     self.frames[F] = frame
        #     frame.grid(row=0, column=0, sticky="nsew")

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

        playlist_button = ctk.CTkButton(navigation_frame, text="Playlist Generator",
                                        command=lambda: self.show_frame(PlaylistView))
        playlist_button.pack(pady=10, padx=10)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
