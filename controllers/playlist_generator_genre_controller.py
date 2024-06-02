import customtkinter as ctk
from models.track import Track
from models.music_player import MusicPlayer
from models.inter_radar_chart import RadarChartFrame
from views.trackinfo import TrackInfoWindow


class PlaylistGeneratorGenController:
    """
    Controller class for controlling playlist generation based on genres and features
    """
    def __init__(self, view, spotify_user):
        """
        :param view:
        :param spotify_user:
        """
        self.view = view
        self.model = spotify_user
        self.generated_playlist_uris = []

        print(self.model.get_genres())
        self.view.load_genres(self.model.get_genres())

    def get_radar_chart_frame(self, parent):
        """
        Get radar chart frame
        :param parent:
        :return:
        """
        categories = ['energy', 'danceability', 'explicit', 'valence', 'liveness', 'instrumentalness', 'acousticness',
                      'speechiness', 'mode']
        values = [0.5, 0.4, 0.3, 0.2, 0.3, 0.4, 0.3, 0.3, 0.3]
        return RadarChartFrame(parent, categories, values)

    def generate_playlist(self):
        """
        Generate playlist based on selected genres and features
        :return:
        """
        selected_genres = self.view.get_selected_genres()
        features = dict(self.view.chart_frame.get_current_state())

        number_of_tracks = 10
        tracks_entry = self.view.get_playlist_tracks_entry()
        if tracks_entry and tracks_entry.isdigit():
            number_of_tracks = int(tracks_entry)
            self.view.clear_tracks_entry()

        result = self.model.generate_playlist(selected_genres=selected_genres,
                                              number_of_tracks=number_of_tracks,
                                              features=features,
                                              market=self.view.country_var.get())
        track_names = [track['name'] for track in result['tracks']]
        self.generated_playlist_uris = [track['uri'] for track in result['tracks']]
        self.view.update_playlist(track_names)

    def preview_track(self):
        """
        Preview track - show more info about selected track in a new frame
        :return:
        """
        index = self.view.playlist_listbox.curselection()[0]
        if index < len(self.generated_playlist_uris):
            track_uri = self.generated_playlist_uris[index]
            canvas = ctk.CTkCanvas(self.view, width=500, bg='#2C2C2C')
            canvas.grid(row=0, column=3, padx=10, pady=10, rowspan=500, sticky="nsew")
            track_info_frame = TrackInfoWindow(canvas, Track(track_uri, self.model.get_authorized_spotify_object()),
                                               MusicPlayer())
            canvas_frame = canvas.create_window((0, 0), window=track_info_frame, anchor="nw")
            track_info_frame.wait_window()
            canvas.grid_forget()

    def delete_track(self):
        """
        Delete track from playlist and update view
        :return:
        """
        selected_index = self.view.playlist_listbox.curselection()
        if selected_index:
            del self.generated_playlist_uris[selected_index[0]]
            track_names = self.model.get_track_names(self.generated_playlist_uris)
            self.view.update_playlist(track_names)

    def download_playlist(self, name, description):
        """
        Download playlist and add it to user's Spotify account
        :param name:
        :param description:
        :return:
        """
        if name and self.generated_playlist_uris:
            self.model.download_playlist(name=name, description=description, uris=self.generated_playlist_uris)
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
