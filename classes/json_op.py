import os
import json


class Json:
    def __init__(self, path):
        self.json_path = path

    def load_json(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    file = json.load(f)
                return file
            except json.decoder.JSONDecodeError:
                return []
        else:
            return []

    def upload_json(self, d):
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(d, f, indent=4)
