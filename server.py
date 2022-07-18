from http.server import HTTPServer, BaseHTTPRequestHandler
from method_db import add_part, conection, cursor


class echoHANDLER(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/senddata'):
            self.send_response(200)
            self.send_header('Content-type',  'text/html; charset=utf-8')
            self.end_headers()
            site = open('site.html', 'rb')
            site = site.read()
            self.wfile.write(site)

    def do_POST(self):
        content_length = int(self.headers.get('content-length'), 0)
        insert_data = self.rfile.read(content_length).decode('utf-8')
        self.send_response(200)
        self.end_headers()
        file = open('result.html', 'rb')
        file = file.read()
        self.wfile.write(file)
        self.add_to_DB(insert_data)

    def add_to_DB(self, insert_data):
        insert_data = insert_data.split('&')
        result = []
        categories = []
        for i in insert_data:
            i = i.split('=')
            if i[0] == 'category':
                categories.append(i[1])
            else:
                result.append(i[1])
        add_part(conection, cursor, categories=categories, key=result[0], timeout=result[1])


def main():
    PORT = 8000
    server = HTTPServer(('', PORT), echoHANDLER)
    print('Server running on port %s' % PORT)
    server.serve_forever()





