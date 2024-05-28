class PlaylistController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self

    def search_artist(self):
        artist_name = self.view.search_entry.get()
        results = self.model.search_artist(artist_name)
        self.view.update_results(results)

    def show_more_info(self):
        selection = self.view.results_listbox.curselection()
        if selection:
            index = selection[0]
            artist = self.model.search_results[index]
            self.view.show_artist_details(artist)

    def add_artist(self):
        selected_index = self.view.results_listbox.curselection()
        if selected_index:
            artist = self.model.search_results[selected_index[0]]
            self.model.add_artist(artist)
            self.view.update_selected_artists_listbox(self.model.selected_artists)

    def clear_selected_artists(self):
        self.model.clear_selected_artists()
        self.view.update_selected_artists_listbox(self.model.selected_artists)

    def generate_playlist(self):
        playlist = self.model.generate_playlist()
        self.view.update_playlist(playlist)

    def download_playlist(self):
        self.model.download_playlist()

    def delete_track(self, index):
        if index < len(self.model.generated_playlist):
            self.model.generated_playlist.pop(index)
            self.view.update_playlist(self.model.generated_playlist)