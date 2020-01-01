import os
from configparser import ConfigParser


class Config(object):
    __instance = None

    def __init__(self, file_path: str = '.config') -> None:
        super().__init__()
        self.file_path = file_path
        self.user = ""
        self.key = ""

    def __new__(cls, file_path: str = '.config'):
        if not Config.__instance:
            Config.__instance = object.__new__(cls)
        Config.__instance.file_path = file_path
        return Config.__instance

    def load_config(self):
        config_parser = ConfigParser()
        config_file: str = self.file_path

        if not os.path.exists(config_file):
            raise Exception(f"{config_file} not found")
        config_parser.read(config_file)

        section: str = "open_data"
        self.user = config_parser.get(section=section, option="user")
        self.key = config_parser.get(section=section, option="key")
