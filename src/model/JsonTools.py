import json
import os

def write_json(tags_promps_db, data):
    with open(tags_promps_db, 'w') as write_file:
        json.dump(data, write_file)


def read_json(json_file):
    if not os.path.exists(json_file):
        with open(json_file, 'w') as file:
            json.dump({}, file)
    with open(json_file, "r") as read_file:
        return json.load(read_file)