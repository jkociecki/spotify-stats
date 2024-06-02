from views.topviews.toptrackslayout import *
from views.artistview import ArtistInfoView
from models.artist import Artist
from models.music_player import MusicPlayer


class TopArtistView(BaseView):
    """
    A class to display the top artists view.

    This class provides methods to add table headers, add table data, and show top artists for different time ranges.
    It also includes a method to display detailed artist information.
    """

    def add_table_headers(self):
        """
        Add headers to the table displaying top artists.
        """
        headers = ["Place", "Artist", "Info", "Genres", "Release Date"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

    def add_table_data(self, data):
        """
        Add data to the table displaying top artists.

        Parameters:
            data (dict): Data containing top artists information.
        """
        for i, artist in enumerate(data['items']):
            artist_name = artist['name']
            genre = artist['genres']
            genre_str = ' | '.join(genre)

            ctk.CTkLabel(self.scrollable_frame, text=str(i + 1)).grid(row=i + 1, column=0, padx=5, pady=5, sticky="ew")
            ctk.CTkLabel(self.scrollable_frame, text=artist_name).grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")

            info_button = ctk.CTkButton(
                self.scrollable_frame, text="Info", width=15, hover=False,
                command=lambda artist_id=artist['id']: self.show_info(artist_id)
            )
            info_button.grid(row=i + 1, column=2, padx=5, pady=5)

            ctk.CTkLabel(self.scrollable_frame, text=genre_str, font=('Arial', 12, 'bold')).grid(
                row=i + 1, column=3, padx=5, pady=5, sticky="ew"
            )

    def show_short_term(self):
        """
        Show the top artists for the short-term time range.
        """
        if not self.short_term_data or self.current_limit != self.previous_limit:
            data = self.sp.get_top_artists(time_range='short_term', limit=self.current_limit)
            self.short_term_data = data
            self.add_table_data(data)
        else:
            print("Short term data already fetched")
            self.add_table_data(self.short_term_data)

    def show_medium_term(self):
        """
        Show the top artists for the medium-term time range.
        """
        if not self.medium_term_data or self.current_limit != self.previous_limit:
            data = self.sp.get_top_artists(time_range='medium_term', limit=self.current_limit)
            self.medium_term_data = data
            self.add_table_data(data)
        else:
            print("Medium term data already fetched")
            self.add_table_data(self.medium_term_data)

    def show_long_term(self):
        """
        Show the top artists for the long-term time range.
        """
        if not self.long_term_data or self.current_limit != self.previous_limit:
            data = self.sp.get_top_artists(time_range='long_term', limit=self.current_limit)
            self.long_term_data = data
            self.add_table_data(data)
        else:
            print("Long term data already fetched")
            self.add_table_data(self.long_term_data)

    def show_info(self, artist_id):
        """
        Show detailed information for a selected artist.

        Parameters:
            artist_id (str): The ID of the artist to display information for.
        """
        artist = Artist(artist_id, self.sp)
        view = ArtistInfoView(self, artist, MusicPlayer())
        view.grid(row=0, column=4, rowspan=200, sticky="nsew")
