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
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                if self.path.endswith('/sendfile'):
                    insert_data = fields.get('file')
                    insert_data = insert_data[0].decode('utf-8').splitlines()
                    self.add_to_DB_file(insert_data)

                elif self.path.endswith('/senddata'):
                    categories = fields.get('category')
                    phone_number = fields.get('tel')
                    timeout = fields.get('timeout')
                    if categories == [''] or phone_number == [''] or timeout == ['']:
                        return self.send_error(404, "not all parameters were enter")
                    else:
                        add_part(conection, cursor, categories=categories, phone_number=phone_number[0], timeout=timeout[0])
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', self.path)
            self.end_headers()
            file = open('result.html', 'rb')
            site = file.read()
            self.wfile.write(site)
        except:
            self.send_error(502, "{}".format(sys.exc_info()[0]))
            print(sys.exc_info())

    def add_to_DB_file(self, insert_data):
        header = insert_data[0].split(',')
        data = insert_data[1].split(',')
        try:
            insert_data = {header[0]: data[0].split(';'),
                           header[1]: data[1],
                           header[2]: data[2]
                           }
            add_part(conection,
                     cursor,
                     categories=insert_data["categories"],
                     phone_number=insert_data["phone"],
                     timeout=insert_data["timeout"],
                     )
        except IndexError:
            self.send_error(404, 'not all parameters were enter')

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()


def main():
    PORT = 8000
    server = HTTPServer(('', PORT), echoHANDLER)
    print('Server running on port %s' % PORT)
    server.serve_forever()





