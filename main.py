from downloader import Downloader
from config import Config

from mym3u8 import MyM3u8


def main():
    config = Config()
    downloader = Downloader(config)

    my_m3u8 = MyM3u8(downloader.download_file_if_not_exists())

    available_groups = sorted(my_m3u8.get_groups())
    playlist = ''
    id_group_selected = show_menu_with_groups(available_groups)
    while id_group_selected > 0:
        playlist += f"{my_m3u8.extract_group_from_list(available_groups[id_group_selected-1])}\n"
        id_group_selected = show_menu_with_groups(available_groups)

    filename = get_full_filename_for(input("Nombre de la lista: "))
    save_filter_list(filename, playlist)


def show_menu_with_groups(groups: list) -> int:
    print("Grupos disponibles:")
    print("------------------------------------")
    for n, group in enumerate(groups):
        print(f"{n+1}. {group[group.find('.')+1:].strip()}")

    group_selected = show_user_input()

    while group_selected < 0 or group_selected > len(groups):
        print("ERROR: no es un grupo válido")
        group_selected = show_user_input()

    return group_selected


def show_user_input() -> int:
    return int(input("Grupo para extraer: "))


def sanitize_group_name(group: str) -> str:
    return group.strip().replace(' ', '_')


def get_output_filename_for_group_name(group_name: str) -> str:
    return f"lists/{group_name}.m3u"


def get_full_filename_for(filename: str) -> str:
    return f"lists/{filename}.m3u"


def save_filter_list(filename: str, list_url: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("#EXTM3U\n")
        file.write(list_url)


if __name__ == '__main__':
    main()
