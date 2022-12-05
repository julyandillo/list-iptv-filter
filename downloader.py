import os.path
import requests

from config import Config


class Downloader:
    """ utilidades para descargar en el archivo con la lista completa """

    def __init__(self, config: Config):
        self._config = config
        self._iptv_file = f"{os.path.abspath(os.getcwd())}/lists/iptv_all.m3u"

    def download_file_if_not_exists(self) -> str:
        if not os.path.exists(self._iptv_file):
            self.donwload_file()

        return self._iptv_file

    def donwload_file(self) -> str:
        with requests.get(self._config.get_url_list()) as response:
            response.raise_for_status()

            with open(self._iptv_file, 'w', encoding='utf-8') as file:
                file.write(response.content.decode('utf-8'))

        return self._iptv_file
