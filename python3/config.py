import configparser
import os
from pathlib import Path


class Config:
    DEFAULT_PATH = os.path.join(Path.home(), ".cuca/config")

    def __init__(self, notebook=None):
        self.config = configparser.ConfigParser()

        self.config.read(Config.DEFAULT_PATH)
        if notebook:
            self.config.read(notebook.cuca_data_dir("config"))

    def get(self, key, default=None):
        section, key = key.split(".", 1)
        if section in self.config:
            s = self.config[section]
            if key in s:
                return s[key]

        return default
