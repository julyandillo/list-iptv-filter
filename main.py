from downloader import Downloader
from config import Config

from mym3u8 import MyM3u8


def main():
    config = Config()
    downloader = Downloader(config)

    my_m3u8 = MyM3u8(downloader.download_file_if_not_exists())

    available_groups = sorted(my_m3u8.get_groups())

    selected_group = available_groups[show_menu_with_groups_availables(available_groups)]

    group_name = sanitize_group_name(selected_group.split('.')[1])

    save_filter_list(get_output_filename_for_group_name(group_name), my_m3u8.extract_group_from_list(selected_group))


def show_menu_with_groups_availables(groups: list) -> int:
    print("Grupos disponibles:")
    print("------------------------------------")
    for group in groups:
        print(group)

    group_selected = show_user_input()

    while group_selected < 0 or group_selected > len(groups):
        print("ERROR: no es un grupo válido")
        group_selected = show_user_input()

    return group_selected


def show_user_input() -> int:
    return int(input("Grupo para extraer: ")) - 1


def sanitize_group_name(group: str) -> str:
    return group.strip().replace(' ', '_')


def get_output_filename_for_group_name(group_name: str) -> str:
    return f"lists/{group_name}.m3u"


def save_filter_list(filename: str, groups: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(groups)


if __name__ == '__main__':
    main()
