from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults
from wsgiref.validate import validator

from processing.view import processing
from reporting.view import reporting


def app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/xml; charset=utf-8')]

    start_response(status, headers)

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request = environ['wsgi.input'].read(request_body_size).decode('utf-8')
    response = None

    if 'processing' in environ['PATH_INFO'] and environ['REQUEST_METHOD'] == 'POST':
        response = processing(request)

    if 'reporting' in environ['PATH_INFO'] and environ['REQUEST_METHOD'] == 'POST':
        response = reporting(request)

    print(environ['PATH_INFO'] + " request :\n" + request + "\n"
          + environ['PATH_INFO'] + " response :\n" + response.__str__())
    return [response.__str__().encode()]

validator_app = validator(app)
httpd = make_server('', 8000, validator_app)
print("Serving on port 8000...")
httpd.serve_forever()
