from controllers.gemini_playlist_controller import GeminiPLaylistController
import customtkinter as ctk
from tkinter import Listbox, SINGLE, END


class GeminiPlaylistView(ctk.CTkFrame):
    """
    A class to represent the Gemini Playlist view.

    This class inherits from the CTkFrame class and provides functionalities to create and manage playlists
    using a customtkinter GUI framework.

    Attributes:
        controller (GeminiPLaylistController): The controller object to manage the view's logic.
        generated_playlist_uris (list): List of URIs of the generated playlist tracks.

    Methods:
        create_widgets(): Create and arrange widgets in the view.
        update_playlist(tracks): Update the playlist view with new tracks.
        set_controller(controller): Set the controller for the view and configure button commands.
    """

    def __init__(self, master: ctk.CTk):
        """
        Initialize the GeminiPlaylistView class.

        Parameters:
            master (ctk.CTk): The parent widget.
        """
        super().__init__(master)
        self.controller = None
        self.generated_playlist_uris = []

        self.configure(fg_color="#2C2C2C")
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """
        Create and arrange widgets in the view.
        """
        # FRAME FROM ENTRY
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.entry_frame, text="Enter description:").pack(pady=10)
        self.description_entry = ctk.CTkTextbox(self.entry_frame, width=350, height=400)
        self.description_entry.pack(pady=10)
        self.amount_frame = ctk.CTkFrame(self.entry_frame)
        self.amount_frame.pack(pady=10)
        ctk.CTkLabel(self.amount_frame, text="Enter amount of songs:").pack(padx=10, side="left")
        self.amount_entry = ctk.CTkEntry(self.amount_frame)
        self.amount_entry.pack(padx=10, side="left")
        self.generate_button = ctk.CTkButton(self.entry_frame, text="Generate Playlist")
        self.generate_button.pack(pady=10)

        # FRAME FOR RESULTS
        self.playlist_frame = ctk.CTkFrame(self)
        self.playlist_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(self.playlist_frame, text="Generated Playlist:").pack(pady=10)
        self.playlist_listbox = Listbox(self.playlist_frame, bg="#2C2C2C", fg="#FFFFFF", selectmode=SINGLE)
        self.playlist_listbox.pack(expand=True, fill="both", padx=10, pady=10)

        # FRAME FOR CONTROLS
        self.controlls_frame = ctk.CTkFrame(self)
        self.controlls_frame.grid(row=0, column=2, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.playlist_controll_frame = ctk.CTkFrame(self.controlls_frame)
        self.playlist_controll_frame.pack(pady=10)
        self.preview_button = ctk.CTkButton(self.playlist_controll_frame, text="Preview Song")
        self.preview_button.pack(side="left", padx=10)
        self.delete_button = ctk.CTkButton(self.playlist_controll_frame, text="Delete Track")
        self.delete_button.pack(side="left", padx=10)
        ctk.CTkLabel(self.controlls_frame, text='Enter playlist name:').pack(pady=10)
        self.playlist_name_entry = ctk.CTkEntry(self.controlls_frame)
        self.playlist_name_entry.pack(pady=10)
        ctk.CTkLabel(self.controlls_frame, text='Enter playlist description:').pack(pady=10)
        self.playlist_desc_entry = ctk.CTkEntry(self.controlls_frame)
        self.playlist_desc_entry.pack(pady=10)
        self.download_button = ctk.CTkButton(self.controlls_frame, text="Download Playlist")
        self.download_button.pack(pady=10)

    def update_playlist(self, tracks):
        """
        Update the playlist view with new tracks.

        Parameters:
            tracks (list): List of Track objects to display in the playlist.
        """
        self.playlist_listbox.delete(0, END)
        self.generated_playlist_uris = [track.uri for track in tracks]
        for track in tracks:
            self.playlist_listbox.insert(END, track.title)

    def set_controller(self, controller):
        """
        Set the controller for the view and configure button commands.

        Parameters:
            controller (GeminiPLaylistController): The controller object to manage the view's logic.
        """
        self.controller = controller
        self.generate_button.configure(command=self.controller.generate_playlist)
        self.preview_button.configure(command=self.controller.preview_song)
        self.delete_button.configure(command=self.controller.delete_track)
        self.download_button.configure(command=self.controller.download_playlist)


#For testing purposes
if __name__ == "__main__":
    from models.user_data import SpotifyUser

    app = ctk.CTk()
    app.title("Playlist Generator")
    app.geometry("800x600")

    spotify_user = SpotifyUser()
    frame = GeminiPlaylistView(app)  # Na tym etapie kontroler jest None
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    controller = GeminiPLaylistController(frame, spotify_user)
    frame.set_controller(controller)  # Ustawiamy kontroler w widoku

    app.mainloop()
