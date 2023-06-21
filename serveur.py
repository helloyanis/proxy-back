from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import urllib.request

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        url = urllib.parse.parse_qs(post_data)['url'][0]
        if url:
            response = self.fetch_url(url)
            if response:
                self.send_response(response.status)
                self.send_header('Content-type', response.headers['Content-type'])
                self.end_headers()
                self.wfile.write(response.content)
            else:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Error fetching URL.')
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'No URL provided.')

    def do_GET(self):
        url = 'https://' + self.headers['Host'] + self.path
        response = self.fetch_url(url)
        if response:
            self.send_response(response.status)
            self.send_header('Content-type', response.headers['Content-type'])
            self.end_headers()
            self.wfile.write(response.content)
        else:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Error fetching URL.')

    def fetch_url(self, url):
        try:
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler())
            response = opener.open(url)
            content = response.read()
            return FetchResult(response.status, response.headers, content)
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return None


class FetchResult:
    def __init__(self, status, headers, content):
        self.status = status
        self.headers = headers
        self.content = content


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server listening on port {port}...")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
