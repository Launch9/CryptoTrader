import json


class GF:
    
    CONFIG = {}

    @staticmethod
    def pretty_print(json_data):
        print(json.dumps(json_data, indent=4, sort_keys=True))

    
