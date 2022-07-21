import cgi
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from method_db import add_part, conection, cursor


class echoHANDLER(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/senddata'):
            self._set_response()
            site = open('site.html', 'rb')
            site = site.read()
            self.wfile.write(site)

        if self.path.endswith('/sendfile'):
            self._set_response()
            site = open('send_file.html', 'rb')
            site = site.read()
            self.wfile.write(site)

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', self.path)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                if self.path.endswith('/sendfile'):
                    insert_data = fields.get('file')
                    insert_data = insert_data[0].decode('utf-8').splitlines()
                    self.add_to_DB(insert_data)

                elif self.path.endswith('/senddata'):
                    categories = fields.get('category')
                    key = fields.get('tel')
                    timeout = fields.get('timeout')
                    add_part(conection, cursor, categories=categories, key=key[0], timeout=timeout[0])
            file = open('result.html', 'rb')
            site = file.read()
            self.wfile.write(site)
        except:
            self.send_error(404, "{}".format(sys.exc_info()[0]))
            print(sys.exc_info())

    def add_to_DB(self, insert_data):
        header = insert_data[0].split(',')
        data = insert_data[1].split(',')
        data[0] = data[0].split(';')
        categories = data[header.index('categories')]
        key = data[header.index('phone')]
        timeout = data[header.index('timeout')]
        add_part(conection, cursor, categories=categories, key=key, timeout=timeout)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()


def main():
    PORT = 8000
    server = HTTPServer(('', PORT), echoHANDLER)
    print('Server running on port %s' % PORT)
    server.serve_forever()





