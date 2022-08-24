import os
import yaml


class initializer:
    def get_attributes(conf_file):
        with open(conf_file, 'r') as cf:
            data_raw = yaml.load(cf, Loader=yaml.FullLoader)
            data_raw = {tuple(sect.items())[0][0]:tuple((sect.items()))[0][1] for sect in data_raw}
            data = {}
            for value in data_raw.values():
                data.update(value)
                
            return data