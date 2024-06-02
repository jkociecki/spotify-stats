"""
This file contains a class and a function to facilitate the Spotify authorization process by creating a simple HTTP server
to receive the authorization code and exchange it for an access token.

Classes:
    SpotifyAuthHandler

Functions:
    start_auth_server
"""

import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import webbrowser
import os
from dotenv import load_dotenv


class SpotifyAuthHandler(BaseHTTPRequestHandler):
    """
    A class to handle the Spotify authorization process.

    This class creates an HTTP server to receive the Spotify authorization code via a GET request,
    then exchanges this code for an access token.

    Methods:
        do_GET(self):
            Handles GET requests sent to the server. Extracts the authorization code and requests an access token.

        get_access_token(self, code):
            Exchanges the authorization code for an access token by making a POST request to the Spotify API.
    """

    def do_GET(self):
        """
        Handle GET requests to the server.

        This method sends a 200 response and extracts the authorization code from the request URL.
        It then uses the authorization code to get an access token and writes a success message to the client.
        """
        self.send_response(200)
        self.end_headers()
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if 'code' in params:
            code = params['code'][0]
            self.server.access_token = self.get_access_token(code)
            self.wfile.write(b'Access Token received. You can close this window now.')
            print("Access Token:", self.server.access_token)

    def get_access_token(self, code):
        """
        Get an access token using the provided authorization code.

        This method makes a POST request to the Spotify API to exchange the authorization code for an access token.

        Parameters:
            code (str): The authorization code received from Spotify.

        Returns:
            str: The access token received from Spotify.
        """
        load_dotenv()
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        redirect_uri = 'http://localhost:8888/callback'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        response = requests.post('https://accounts.spotify.com/api/token', data=data)
        token_info = response.json()
        return token_info['access_token']


def start_auth_server():
    """
    Start the authorization server and open the Spotify authorization URL in a web browser.

    This function sets up an HTTP server to handle the Spotify authorization callback.
    It constructs the authorization URL with the required scopes and opens it in the default web browser.

    Returns:
        str: The access token received from Spotify.
    """
    server_address = ('', 8888)
    httpd = HTTPServer(server_address, SpotifyAuthHandler)
    scope = (
        'user-library-read user-top-read user-read-playback-state user-read-currently-playing '
        'user-follow-read user-read-recently-played playlist-read-private playlist-modify-public playlist-modify-private'
    )
    auth_url = f"https://accounts.spotify.com/authorize?client_id=1da6cc873e344e9f9ac5838978410461&response_type=code&redirect_uri=http://localhost:8888/callback&scope={urllib.parse.quote(scope)}&show_dialog=true"
    print("Opening the authorization URL in your default web browser...")
    webbrowser.open(auth_url)
    httpd.handle_request()
    return httpd.access_token


if __name__ == "__main__":
    access_token = start_auth_server()
    print(f"Access Token: {access_token}")
