import configparser
import os
import sys


class ConfigReader:

    @staticmethod
    def read_config(section, key):
        root_dir = sys.path[0]
        config_path = os.path.join(root_dir, 'config.ini')

        config = configparser.ConfigParser()
        config.read(config_path)

        if config.has_section(section) and config.has_option(section, key):
            return config[section][key]
        else:
            raise KeyError(f"Section '{section}' or key '{key}' not found in config.ini")
