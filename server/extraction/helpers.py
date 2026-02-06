import urllib.request as request
from server.config.config import get_temp_file, get_upload_filepath

def _write_to_disk(stream, ext):
    temp_file = get_temp_file(ext)
    with open(temp_file, 'wb') as f:
        f.write(stream.file.read())
    return temp_file

def _profiles_write_to_disk(stream, ext, _dir):
    temp_file = get_upload_filepath(ext, _dir)
    with open(temp_file, 'wb') as f:
        f.write(stream.file.read())
    return temp_file

def _read_from_url(url):
    return request.urlopen(url).read()
