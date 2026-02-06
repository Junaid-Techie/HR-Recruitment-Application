# _*_ coding:utf-8 _*_
import falcon
import cgi
import json
import xmltodict
import yaml
from io import BytesIO
from server.config.applogging import ResponseLoggerMiddleware
import re
from urllib.parse import parse_qs


class BodyTransformation:
    def __init__(self, parser=None):
        self.parser = cgi.FieldStorage
        #self.applogging = ResponseLoggerMiddleware()
    def parse(self, stream, environ):
        return self.parser(fp=stream, environ=environ)

    def parse_field(self, field):
        if isinstance(field, list):
            return [self.parse_field(subfield) for subfield in field]

        encoded = field.disposition_options.get('filename*')

        if encoded:
            encoding, filename = encoded.split("'")
            field.filename = filename
            field.file = BytesIO(field.file.read().encode(encoding))

        if getattr(field, 'filename', False):
            return field
        return field.value

    def process_yaml_data(self, req, resp, params):

        if 'text/yaml' in req.content_type:
            try:
                raw_data = req.bounded_stream.read(int(req.content_length) or 0)
                data = yaml.load(raw_data)
                req._params.update(data)
                req.context.model = data
            except ValueError as e:
                raise falcon.HTTPBadRequest('Error parsing form data', str(e))

    def process_xml_data(self, req, resp, params):
        if 'application/xml' in req.content_type:
            try:
                raw_data = req.bounded_stream.read(int(req.content_length) or 0)
                data = xmltodict.parse(raw_data)
                req._params.update(data)
                req.context.model = data
            except ValueError as e:
                raise falcon.HTTPBadRequest('Error parsing form data', str(e))

    def process_multipart_formdata(self, req, resp, params):
        if 'multipart/form-data' in req.content_type:

            # req.env.setdefault('QUERYSTRING', '')
            stream = (req.stream.stream if hasattr(req.stream, 'stream') else req.stream)
            try:
                form = self.parse(stream=stream, environ=req.env)
            except ValueError as e:
                raise falcon.HTTPBadRequest('Error parsing file', str(e))

            for key in form:
                req._params[key] = self.parse_field(form[key])
            req.context.model = req._params


    def process_form_url_encoded(self, req: falcon.Request, resp: falcon.Response, params):
        if 'application/x-www-form-urlencoded' in req.content_type:
            try:
                raw_data = req.bounded_stream.read(int(req.content_length) or 0)
                query_string = raw_data.decode()
                data = {}
                print(query_string)
                for kvp in query_string.split('&'):
                    if kvp == '&' or kvp is None:
                        continue
                    key, value = kvp.split('=')
                    data[key] = value
                req._params.update(data)
                query_string = parse_qs(raw_data.decode('utf-8'))

                req.context.model = query_string
            except ValueError as e:
                raise falcon.HTTPBadRequest('Error parsing form data', str(e))


    def process_resource(self, req, resp, resource, params):
        pass

    def process_request(self, req: falcon.Request, resp, **kwargs):
        #self.applogging.logging.info()
        self.process_multipart_formdata(req, resp, kwargs)
        self.process_form_url_encoded(req, resp, kwargs)
        self.process_xml_data(req, resp, kwargs)
        self.process_yaml_data(req, resp, kwargs)
        if 'application/json' in req.content_type:
            req.context.model = req.media


class Authirzation:
    def __init__(self):
        super().__init__()

    def process_resource(self, req, resp, resource, params):
        pass

