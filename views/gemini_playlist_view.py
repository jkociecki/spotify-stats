
from controllers.gemini_playlist_controller import GeminiPLaylistController
import customtkinter as ctk
from tkinter import Listbox, Text, SINGLE, END, messagebox


class GeminiPlaylistView(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
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
        self.playlist_listbox.delete(0, END)
        self.generated_playlist_uris = [track.uri for track in tracks]
        for track in tracks:
            self.playlist_listbox.insert(END, track.title)

    def set_controller(self, controller):
        self.controller = controller
        self.generate_button.configure(command=self.controller.generate_playlist)
        self.preview_button.configure(command=self.controller.preview_song)
        self.delete_button.configure(command=self.controller.delete_track)
        self.download_button.configure(command=self.controller.download_playlist)




import customtkinter as ctk
from models.user_data import SpotifyUser

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Playlist Generator")
    app.geometry("800x600")

    spotify_user = SpotifyUser()
    frame = GeminiPlaylistView(app)  # Na tym etapie kontroler jest None
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    controller = GeminiPLaylistController(frame, spotify_user)
    frame.set_controller(controller)  # Ustawiamy kontroler w widoku

    app.mainloop()

# import customtkinter as ctk
# from tkinter import Listbox, StringVar, END, messagebox, SINGLE, Text
# from models.user_data import SpotifyUser
# from models.track import Track
# from controllers.playlist_controler import PlaylistController
# from models.music_player import MusicPlayer
# from views.trackinfo import TrackInfoWindow
#
# # Konfiguracja Google Generative AI
# from google.generativeai import GenerativeModel, configure
#
# gemini_api_key = 'AIzaSyAxkGl9kNzM6LZFNlolK4xnZKxNhZOzuog'
# configure(api_key=gemini_api_key)
#
#
# # # Konfiguracja Spotify
# # spotify_auth_manager = SpotifyUser()
# # spotify = spotify_auth_manager.get_authorized_spotify_object()
#
#
# class PlaylistGeneratorAiModel:
#     def __init__(self, spotify: SpotifyUser = None):
#         self.model = GenerativeModel()
#         self.tracks = []
#         self.sp = spotify.get_authorized_spotify_object()
#
#     def generate_playlist(self, description, amount=10):
#         try:
#             response = self.model.generate_content(
#                 f"Generate a playlist of songs for the following description: {description}. I want {amount} songs. "
#                 f"Please include ONLY song names. I want the response to be in the following form:\n"
#                 f"SongName1\nSongName2\nSongName3"
#             )
#             return response.text
#         except Exception as e:
#             print(f"Error generating playlist: {e}")
#             return None
#
#     def search_spotify(self, song_name):
#         try:
#             results = self.sp.search(q=song_name, limit=1, type='track')
#             if results and results['tracks']['items']:
#                 first_result = results['tracks']['items'][0]
#                 id = first_result['id']
#                 track = Track(id, self.sp)
#                 return track
#             else:
#                 return None
#         except Exception as e:
#             print(f"Error searching Spotify: {e}")
#             return None
#
#     def create_playlist(self, description, amount):
#         ai_playlist = self.generate_playlist(description, amount)
#         print(ai_playlist)
#         if ai_playlist:
#             songs = ai_playlist.split('\n')
#             for song in songs:
#                 track = self.search_spotify(song.strip())
#                 if track:
#                     self.tracks.append(track)
#
#             print(f"Playlist generated: {len(self.tracks)} songs.")
#             for track in self.tracks:
#                 print(f"{track.title} - {track.uri}")
#             return self.tracks
#         else:
#             print("No playlist generated. Could not create playlist.")
#             return []
#
#
# import customtkinter as ctk
# from tkinter import Listbox, Text, SINGLE, END
#
#
# class PlaylistFrame(ctk.CTkFrame):
#     def __init__(self, master: ctk.CTk, spotify_user: SpotifyUser = None):
#         super().__init__(master)
#         self.model = PlaylistGeneratorAiModel(spotify_user)
#         self.generated_playlist_uris = []
#         self.sp = spotify_user.get_authorized_spotify_object()
#
#         self.configure(fg_color="#2C2C2C")
#         self.grid_rowconfigure(0, weight=3)
#         self.grid_rowconfigure(1, weight=3)
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure(2, weight=1)
#         self.create_widgets()
#
#     def create_widgets(self):
#         # FRAME FROM ENTRY
#         self.entry_frame = ctk.CTkFrame(self)
#         self.entry_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
#
#         ctk.CTkLabel(self.entry_frame, text="Enter description:").pack(pady=10)
#         self.description_entry = ctk.CTkTextbox(self.entry_frame, width=350, height=400)
#         self.description_entry.pack(pady=10)
#         self.amount_frame = ctk.CTkFrame(self.entry_frame)
#         self.amount_frame.pack(pady=10)
#         ctk.CTkLabel(self.amount_frame, text="Enter amount of songs:").pack(padx=10, side="left")
#         self.amount_entry = ctk.CTkEntry(self.amount_frame)
#         self.amount_entry.pack(padx=10, side="left")
#         self.generate_button = ctk.CTkButton(self.entry_frame, text="Generate Playlist", command=self.generate_playlist)
#         self.generate_button.pack(pady=10)
#
#         # FRAME FOR RESULTS
#         self.playlist_frame = ctk.CTkFrame(self)
#         self.playlist_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
#         ctk.CTkLabel(self.playlist_frame, text="Generated Playlist:").pack(pady=10)
#         self.playlist_listbox = Listbox(self.playlist_frame, bg="#2C2C2C", fg="#FFFFFF", selectmode=SINGLE)
#         self.playlist_listbox.pack(expand=True, fill="both", padx=10, pady=10)
#
#         # FRAME FOR CONTROLS
#         self.controlls_frame = ctk.CTkFrame(self)
#         self.controlls_frame.grid(row=0, column=2, columnspan=3, sticky="nsew", padx=10, pady=10)
#         self.playlist_controll_frame = ctk.CTkFrame(self.controlls_frame)
#         self.playlist_controll_frame.pack(pady=10)
#         self.preview_button = ctk.CTkButton(self.playlist_controll_frame, text="Preview Song",
#                                             command=self.preview_song)
#         self.preview_button.pack(side="left", padx=10)
#         self.delete_button = ctk.CTkButton(self.playlist_controll_frame, text="Delete Track", command=self.delete_track)
#         self.delete_button.pack(side="left", padx=10)
#         ctk.CTkLabel(self.controlls_frame, text='Enter playlist name:').pack(pady=10)
#         self.playlist_name_entry = ctk.CTkEntry(self.controlls_frame)
#         self.playlist_name_entry.pack(pady=10)
#         ctk.CTkLabel(self.controlls_frame, text='Enter playlist description:').pack(pady=10)
#         self.playlist_desc_entry = ctk.CTkEntry(self.controlls_frame)
#         self.playlist_desc_entry.pack(pady=10)
#         self.download_button = ctk.CTkButton(self.controlls_frame, text="Download Playlist",
#                                              command=self.download_playlist)
#         self.download_button.pack(pady=10)
#
#     def generate_playlist(self):
#         description = self.description_entry.get("1.0", END)
#         amount = self.amount_entry.get()
#
#         if description and amount:
#             self.model.create_playlist(description, int(amount))
#             self.playlist_listbox.delete(0, END)
#             for track in self.model.tracks:
#                 self.playlist_listbox.insert(END, track.title)
#                 self.generated_playlist_uris.append(track.uri)
#
#     def preview_song(self):
#         index = self.playlist_listbox.curselection()
#         if index:
#             index = index[0]
#             if index < len(self.generated_playlist_uris):
#                 track_uri = self.generated_playlist_uris[index]
#                 print(f"Previewing song with URI: {track_uri}")
#
#                 # Create a new top-level window for the track info
#                 preview_window = ctk.CTkToplevel(self)
#                 preview_window.title("Track Info")
#
#                 # Create the TrackInfoWindow inside the new window
#                 track_info_frame = TrackInfoWindow(preview_window, Track(track_uri, self.sp), MusicPlayer())
#                 track_info_frame.pack(fill="both", expand=True)
#
#                 preview_window.grab_set()  # Make the new window modal
#         else:
#             messagebox.showwarning("Warning", "Please select a song to preview.")
#
#     def delete_track(self):
#         index = self.playlist_listbox.curselection()[0]
#         self.playlist_listbox.delete(index)
#         self.generated_playlist_uris.pop(index)
#
#     def download_playlist(self):
#         name = self.playlist_name_entry.get()
#         description = self.description_entry.get('1.0', 'end-1c')
#         if name:
#             self.sp.user_playlist_create(user=self.sp.me()['id'], name=name, description=description)
#             playlist_id = self.sp.current_user_playlists()['items'][0]['id']
#             self.sp.playlist_add_items(playlist_id, self.generated_playlist_uris)
#             playlist_added_window = ctk.CTkToplevel(self)
#             playlist_added_window.title("Playlist Added")
#             playlist_added_label = ctk.CTkLabel(playlist_added_window, text="Playlist added successfully")
#             playlist_added_label.pack(padx=10, pady=10)
#             ok_button = ctk.CTkButton(playlist_added_window, text="OK", command=playlist_added_window.destroy)
#             ok_button.pack(pady=10)
#             playlist_added_window.grab_set()
#             playlist_added_window.wait_window()
#             playlist_added_window.destroy()
#         else:
#             error_window = ctk.CTkToplevel(self)
#             error_window.title("Error")
#             error_label = ctk.CTkLabel(error_window, text="Name cannot be empty")
#             error_label.pack(padx=10, pady=10)
#             ok_button = ctk.CTkButton(error_window, text="OK", command=error_window.destroy)
#             ok_button.pack(pady=10)
#             error_window.grab_set()
#             error_window.wait_window()
#             error_window.destroy()
#
#
# if __name__ == "__main__":
#     app = ctk.CTk()
#     app.title("Playlist Generator")
#     app.geometry("800x600")
#     frame = PlaylistFrame(app, SpotifyUser())
#     frame.pack(padx=20, pady=20, fill="both", expand=True)
#     app.mainloop()
