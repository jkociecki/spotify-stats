# Spotify Playlist Generator

## Project Description

The Spotify Playlist Generator is an application built using Tkinter and CustomTkinter for generating and managing Spotify playlists. The application leverages various Spotify API functionalities to authenticate users, retrieve data about tracks and artists, and create personalized playlists. Additionally, it incorporates AI capabilities for playlist generation.

## Features

- **User Authentication**: Log in to Spotify and authenticate the user.
- **Playlist Generation**: Create playlists based on artists, tracks, genres, or even AI-generated descriptions.
- **Add Playlists to Spotify Account**: Add the generated playlists directly to your Spotify account.
- **Preview and Play Tracks**: Preview and listen to the generated tracks.
- **View Top Tracks and Artists**: Display the user's top tracks and artists.
- **Playlist Statistics**: Show statistics for selected playlists.
- **Eat Your Playlist**: Play the game of snake eating your playlist's track covers while listening to music

## Installation 

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jkociecki/spotify-stats
   cd spotify-stats
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Set environment variables**:
   ```bash
   export CLIENT_ID="YOUR SPOTIFY API CLIENT ID"
   export CLIENT_SECRET="YOUR SPOTIFY API CLIENT SECRET KEY"
   export GEMINI_API_KEY="YOUR GOOGLE GEMINI API KEY"
   ```

   On Windows:
   ```bash
   set CLIENT_ID="YOUR SPOTIFY API CLIENT ID"
   set CLIENT_SECRET="YOUR SPOTIFY API CLIENT SECRET KEY"
   set GEMINI_API_KEY="YOUR GOOGLE GEMINI API KEY"
   ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Project Overview

### Generating playlist via AI prompt
<img width="700" alt="ai generator" src="https://github.com/jkociecki/spotify-stats/assets/116763591/0db2c58a-e481-48b9-9f3b-9a9723323189">

### Generating playlist by choosing artists
<img width="700" alt="playlist generator" src="https://github.com/jkociecki/spotify-stats/assets/116763591/5259dec4-3cc8-4217-8f77-16608f7bf011">

### Generating playlist and tracks statistics
<img width="700" alt="playlist overview" src="https://github.com/jkociecki/spotify-stats/assets/116763591/26093a78-4a66-4599-b8f9-e672247f69df">

## Running the Application

1. **Start the application**:
   ```bash
   python app.py
   ```

## Usage Example

1. **User Authentication**:
   Log in to your Spotify account using the "Authorize" button.

2. **Generate Playlist**:
   Select criteria for generating a playlist (e.g., based on artists, tracks, genres, or an AI-generated description) and click the appropriate button to generate the playlist.

3. **Add Playlist to Spotify Account**:
   After generating a playlist, you can add it directly to your Spotify account by clicking the "Add to Spotify" button.

4. **Preview and Play Tracks**:
   Click on a track in the generated playlist to preview and listen to it.

5. **View Top Tracks**:
   Navigate to the top tracks and artists views to see your top tracks and artists.

6. **Display Statistics**:
   View statistics for your playlists and analyze them using radar charts.

## Project Structure

```
myproject/
├── controllers/
│   ├── gemini_playlist_controller.py
│   ├── music_player_controller.py
│   ├── playlist_controller.py
│   ├── playlist_generator_genre_controller.py
│   └── playlist_stats_controller.py
├── models/
│   ├── music_player.py
│   ├── playlist_model.py
│   ├── track.py
│   └── user_data.py
├── snake/
│   ├── snake_data_controller.py
│   ├── snake.py
├── views/
│   ├── gemini_playlist_view.py
│   ├── homepage.py
│   ├── playlist_generator_artists.py
│   ├── playlist_generator_genre.py
│   ├── playlist_generator_layout.py
│   ├── playlist_generator_tracks.py
│   ├── playlists_stats_view.py
│   ├── trackinfo.py
│   ├── topviews/
│   │   ├── topartistview.py
│   │   └── toptracksview.py
├── app.py
├── README.md
└── requirements.txt
```

### Controllers

The `controllers` directory contains the logic for handling user interactions and data management. This includes controllers for music player functionality, playlist generation, and displaying statistics.

### Models

The `models` directory contains the data structures and logic for interacting with Spotify's API. This includes classes for handling tracks, playlists, and user data.

### Views

The `views` directory contains the user interface components built with Tkinter and CustomTkinter. This includes different views for generating playlists, displaying top tracks and artists, and showing playlist statistics.

## Requirements

- Python 3.6+
- Spotify Developer Account (to obtain API keys)
- customtkinter==5.2.2
- matplotlib==3.8.0
- numpy==1.26.4
- Pillow==10.3.0
- protobuf==5.27.0
- pygame==2.5.2
- python-dotenv==1.0.1
- Requests~=2.31.0
- spotipy==2.23.0
- future~=1.0.0
- aiohttp~=3.9.5
- aiofiles~=22.1.0

## Spotify API Configuration

To use the Spotify API, you need to create an application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and obtain the API keys.

## Google AI Studi
In order to generate playlists with the help of artificial intelligence, after entering a given description, an API token is needed. You can get yours [here](https://aistudio.google.com/app/apikey?_gl=1*15ldrt3*_ga*MTA2MDczNDkwLjE3MTcxOTM1MDQ.*_ga_P1DBVKWT6V*MTcxNzM0ODYyMC4yLjEuMTcxNzM0ODY1Ni4wLjAuMzgyNTk5OTU3)

## Documentation

The documentation for the project is available at the following links:

- [Controllers](https://jkociecki.github.io/spotify-stats/controllers/controllers.html)
- [Models](https://jkociecki.github.io/spotify-stats/models/models.html)
- [Views](https://jkociecki.github.io/spotify-stats/views/views.html)

## Contributing

Contributions to the project are welcome! To suggest features, report bugs, or contribute code, please open an issue or a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```

Feel free to modify and expand this `README.md` to suit the specifics of your project. This version includes detailed sections for project description, features, installation, usage, project structure, requirements, and contribution guidelines, along with the addition of example images showcasing different windows of the application.
