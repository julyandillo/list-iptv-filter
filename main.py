from downloader import Downloader
from config import Config

from mym3u8 import MyM3u8


def main():
    config = Config()
    downloader = Downloader(config)

    my_m3u8 = MyM3u8(downloader.download_file_if_not_exists())

    with open('lists/iptv_MUNDIAL.m3u', 'w') as file:
        file.write(my_m3u8.extract_group_from_list('07. MUNDIAL QATAR 2022'))


if __name__ == '__main__':
    main()
