from models.user_data import SpotifyUser
from models.track import Track
from google.generativeai import GenerativeModel, configure

gemini_api_key = 'AIzaSyAxkGl9kNzM6LZFNlolK4xnZKxNhZOzuog'
configure(api_key=gemini_api_key)

class PlaylistGeneratorAiModel:
    def __init__(self, spotify: SpotifyUser = None):
        self.model = GenerativeModel()
        self.tracks = []
        self.sp = spotify.get_authorized_spotify_object()

    def generate_playlist(self, description, amount=10):
        try:
            response = self.model.generate_content(
                f"Generate a playlist of songs for the following description: {description}. I want {amount} songs. "
                f"Please include ONLY song names. I want the response to be in the following form:\n"
                f"SongName1\nSongName2\nSongName3"
            )
            return response.text
        except Exception as e:
            print(f"Error generating playlist: {e}")
            return None

    def search_spotify(self, song_name):
        try:
            results = self.sp.search(q=song_name, limit=1, type='track')
            if results and results['tracks']['items']:
                first_result = results['tracks']['items'][0]
                id = first_result['id']
                track = Track(id, self.sp)
                return track
            else:
                return None
        except Exception as e:
            print(f"Error searching Spotify: {e}")
            return None

    def create_playlist(self, description, amount):
        ai_playlist = self.generate_playlist(description, amount)
        print(ai_playlist)
        if ai_playlist:
            songs = ai_playlist.split('\n')
            for song in songs:
                track = self.search_spotify(song.strip())
                if track:
                    self.tracks.append(track)

            print(f"Playlist generated: {len(self.tracks)} songs.")
            for track in self.tracks:
                print(f"{track.title} - {track.uri}")
            return self.tracks
        else:
            print("No playlist generated. Could not create playlist.")
            return []
