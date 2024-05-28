from views.topviews.toptrackslayout import *


class TopArtistView(BaseView):
    def add_table_headers(self):
        headers = ["Place", "Artist", "Info", "Genres", "Release Date"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.scrollable_frame, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

    def add_table_data(self, data):
        for i, artist in enumerate(data['items']):
            artist_name = artist['name']
            genre = artist['genres']

            genre_str = ' | '.join(genre)

            ctk.CTkLabel(self.scrollable_frame, text=str(i + 1)).grid(row=i + 1, column=0, padx=5, pady=5, sticky="ew")
            ctk.CTkLabel(self.scrollable_frame, text=artist_name).grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")

            info_button = ctk.CTkButton(self.scrollable_frame, text="Info", width=15, hover=False,
                                        command=lambda artist_id=artist['id']: self.show_info(artist_id))
            info_button.grid(row=i + 1, column=2, padx=5, pady=5)

            ctk.CTkLabel(self.scrollable_frame, text=genre_str, font=('Arial', 12, 'bold')).grid(row=i + 1, column=3,
                                                                                                 padx=5, pady=5,
                                                                                                 sticky="ew")

    def show_short_term(self):
        if not self.short_term_data or self.current_limit != self.previous_limit:
            data = self.sp.get_top_artists(time_range='short_term', limit=self.current_limit)
            self.short_term_data = data
            self.add_table_data(data)
        else:
            print("Short term data already fetched")
            self.add_table_data(self.short_term_data)

    def show_info(self, artist_id):
        pass
