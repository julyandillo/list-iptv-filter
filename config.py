from configparser import ConfigParser


class Config:
    """ clase para obtener las configuiraciones guardadas en el archivo config.ini """
    def __init__(self):
        self._parser = ConfigParser()
        self._parser.read('config.ini')

    def get_url_list(self) -> str:
        return self._parser.get('url', 'url_list')
