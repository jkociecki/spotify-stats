import os
import asyncio
import aiohttp
import aiofiles
from spotipy import Spotify
from models.user_data import SpotifyUser
from typing import List, Tuple
from snake.snake import run

async def download_file(session, url, dest):
    """
    Asynchronously download a file from the given URL to the specified destination.

    Args:
        session (aiohttp.ClientSession): The session to use for the request.
        url (str): The URL of the file to download.
        dest (str): The destination path to save the downloaded file.

    Raises:
        asyncio.TimeoutError: If the request times out.
        aiohttp.ClientError: If there is an error with the client.
        Exception: For any other unexpected errors.
    """
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                async with aiofiles.open(dest, mode='wb') as f:
                    await f.write(await response.read())
            else:
                print(f"Error {response.status} while downloading {url}")
    except asyncio.TimeoutError:
        print(f"Timeout error while downloading {url}")
    except aiohttp.ClientError as e:
        print(f"Client error {e} while downloading {url}")
    except Exception as e:
        print(f"Unexpected error {e} while downloading {url}")

async def download_files(tracks: List[Tuple[str, str, str]]):
    """
    Asynchronously download cover images and preview files for a list of tracks.

    Args:
        tracks (List[Tuple[str, str, str]]): A list of tuples containing track title, preview URL, and cover URL.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, (title, preview_url, cover_url) in enumerate(tracks):
            cover_dest = f'covers/{i}.jpg'
            preview_dest = f'previews/{i}.mp3'
            tasks.append(download_file(session, cover_url, cover_dest))
            if preview_url:
                tasks.append(download_file(session, preview_url, preview_dest))
        await asyncio.gather(*tasks)

def extract_playlist_data(playlist_id: str, sp: Spotify) -> List[Tuple[str, str, str]]:
    """
    Extract track data from a Spotify playlist.

    Args:
        playlist_id (str): The ID of the Spotify playlist.
        sp (Spotify): The Spotify client object.

    Returns:
        List[Tuple[str, str, str]]: A list of tuples containing track title, preview URL, and cover URL.
    """
    tracks = sp.playlist_items(playlist_id)['items']
    track_data = []
    for item in tracks:
        track = item['track']
        title = track['name']
        preview_url = track['preview_url']
        album_cover_url = track['album']['images'][0]['url']
        track_data.append((title, preview_url, album_cover_url))
    return track_data

async def main_async(playlist_id: str, spotify_user: SpotifyUser):
    """
    Asynchronously process the playlist and download the necessary files.

    Args:
        playlist_id (str): The ID of the Spotify playlist.
        spotify_user (SpotifyUser): The Spotify user object.
    """
    # Inicjalizacja Spotify
    # playlist_id = '4aaJ3TMPw6Wvd1RoPfiWBK'
    spotify_user = spotify_user
    # spotify = spotify_user.get_authorized_spotify_object()

    # Pobranie danych z playlisty
    tracks_data = extract_playlist_data(playlist_id, spotify_user)

    # Pobranie plików asynchronicznie
    await download_files(tracks_data)

def main(playlist_id: str, spotify_user: SpotifyUser):
    """
    Main function to set up directories and run the asynchronous main function.

    Args:
        playlist_id (str): The ID of the Spotify playlist.
        spotify_user (SpotifyUser): The Spotify user object.
    """
    os.makedirs('covers', exist_ok=True)
    os.makedirs('previews', exist_ok=True)
    # Uruchomienie głównej funkcji asynchronicznej
    asyncio.run(main_async(playlist_id, spotify_user))
    run()
