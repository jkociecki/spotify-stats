from views.topviews.toptrackslayout import *
from views.trackinfo import TrackInfoWindow
from models.track import Track
from models.music_player import MusicPlayer


class TopTracksView(BaseView):
    """
    A class to represent the top tracks view.

    This class inherits from the BaseView class and provides functionalities to display top tracks 
    of a Spotify user in different time ranges: short term, medium term, and long term.

    Methods:
        add_table_headers(): Add headers to the table displaying data.
        add_table_data(data): Add data to the table.
        show_short_term(): Show the short-term data.
        show_medium_term(): Show the medium-term data.
        show_long_term(): Show the long-term data.
        show_info(track_id): Show detailed information for a selected track.
    """

    def add_table_headers(self):
        """
        Add headers to the table displaying data.
        """
        headers = ["Place", "Artist", "Info", "Track Name", "Release Date"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

    def add_table_data(self, data):
        """
        Add data to the table.

        Parameters:
            data (dict): Data to be displayed in the table.
        """
        for i, track_data in enumerate(data['items']):
            track = Track(track_data['id'], self.sp.get_authorized_spotify_object())

            artist = track.artist
            track_name = track.title
            release_date = track.release_date

            ctk.CTkLabel(self.scrollable_frame, text=str(i + 1)).grid(row=i + 1, column=0, padx=5, pady=5, sticky="ew")
            ctk.CTkLabel(self.scrollable_frame, text=artist).grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")

            info_button = ctk.CTkButton(self.scrollable_frame, text="Info", width=15, hover=False,
                                        command=lambda track_id=track_data['id']: self.show_info(track_id))
            info_button.grid(row=i + 1, column=2, padx=5, pady=5)

            ctk.CTkLabel(self.scrollable_frame, text=track_name).grid(row=i + 1, column=3, padx=5, pady=5,
                                                                      sticky="ew")
            ctk.CTkLabel(self.scrollable_frame, text=release_date).grid(row=i + 1, column=4, padx=5, pady=5,
                                                                        sticky="ew")

    def show_short_term(self):
        """
        Show the short-term data.
        """
        if not self.short_term_data or self.current_limit != self.previous_limit:
            data = self.sp.get_top_tracks(time_range='short_term', limit=self.current_limit)
            self.short_term_data = data
            self.add_table_data(data)
        else:
            print("Short term data already fetched")
            self.add_table_data(self.short_term_data)

    def show_medium_term(self):
        """
        Show the medium-term data.
        """
        if not self.medium_term_data or self.current_limit != self.previous_limit:
            data = self.sp.get_top_tracks(time_range='medium_term', limit=self.current_limit)
            self.medium_term_data = data
            self.add_table_data(data)
        else:
            print("Medium term data already fetched")
            self.add_table_data(self.medium_term_data)

    def show_long_term(self):
        """
        Show the long-term data.
        """
        if not self.long_term_data or self.current_limit != self.previous_limit:
            data = self.sp.get_top_tracks(time_range='long_term', limit=self.current_limit)
            self.long_term_data = data
            self.add_table_data(data)
        else:
            print("Long term data already fetched")
            self.add_table_data(self.long_term_data)

    def show_info(self, track_id):
        """
        Show detailed information for a selected track.

        Parameters:
            track_id (str): The ID of the track to display information for.
        """
        track_info = Track(track_id, self.sp.get_authorized_spotify_object())
        info_popup = TrackInfoWindow(self, track_info, MusicPlayer())
        info_popup.grid(row=0, column=5, rowspan=3000, sticky="nsew")
        info_popup.wait_window(info_popup)
        info_popup.grid_forget()

