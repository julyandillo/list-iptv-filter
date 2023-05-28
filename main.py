from downloader import Downloader
from config import Config

from mym3u8 import MyM3u8


def main():
    config = Config()
    downloader = Downloader(config)

    my_m3u8 = MyM3u8(downloader.download_file_if_not_exists())

    available_groups = sorted(my_m3u8.get_groups())

    selected_groups = get_selected_groups_from(available_groups)

    file_name = get_filename()

    save_filter_group(file_name, my_m3u8.extract_groups_from_list(selected_groups))


def get_selected_groups_from(available_groups):
    selected_groups = []
    more_gropups = True
    while more_gropups:
        selected_groups.append(available_groups[show_menu_with_groups_availables(available_groups)])
        input_more_gropups = str(input("¿Más grupos (S/N)?: ")).strip()
        more_gropups = input_more_gropups == 'S' or input_more_gropups == 's'
    return selected_groups


def get_filename():
    file_name = input('Nombre para el fichero: ')
    if not file_name.endswith('.m3u'):
        file_name += '.m3u'
    return file_name


def show_menu_with_groups_availables(groups: list) -> int:
    print("Grupos disponibles:")
    print("------------------------------------")
    for n, group in enumerate(groups):
        print(f"{n}. {group[group.find('.')+1:].strip()}")

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


def save_filter_group(filename: str, groups: list) -> None:
    path = f"lists/{filename}"
    with open(path, 'w', encoding='utf-8') as file:
        file.write("\n".join(groups))


if __name__ == '__main__':
    main()
