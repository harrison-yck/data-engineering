import json

from pkg_resources import resource_string


def read_file_as_json(path) -> json:
    return json.loads(resource_string("tests", path).decode('utf-8'))
