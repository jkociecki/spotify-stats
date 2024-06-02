import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import webbrowser


class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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
        client_id = '1da6cc873e344e9f9ac5838978410461'
        client_secret = '197ad99f433340e298e6c1e67c1b0089'
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
