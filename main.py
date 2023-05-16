from pathlib import Path
import sys
import shutil
import os

IMAGES = ('.jpeg', '.png', '.jpg', '.svg')
VIDEO = ('.avi', '.mp4', '.mov', '.mkv')
DOCUMENTS = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
MUSIC = ('.mp3', '.ogg', '.wav', '.amr')
ARCHIVE = ('.zip', '.gz', '.tar',)

FOLDERS_NAMES = ('images', 'video', 'documents', 'music', 'archive', 'other_files')

CYRILLIC_SYMBOLS = r"абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_",  "_", "_", "_",
               "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",
               "_", "_", "_", "_", "_", "_", "_")
TRANSLIT_DICT = {}


def normalize(path):
    p = Path(path)

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANSLIT_DICT[ord(c)] = l
        TRANSLIT_DICT[ord(c.upper())] = l.upper()

    for name in p.iterdir():
        if name.is_file():
            name.rename(path + '/' + name.name[:name.name.index(name.suffix)].translate(TRANSLIT_DICT) + name.suffix)
        elif name.is_dir():
            if name.name not in FOLDERS_NAMES:
                name.rename(path + '/' + name.name.translate(TRANSLIT_DICT))


def sorted_files(path):
    path_to_dir = Path(path)
    images_list = []
    videos_list = []
    documents_list = []
    music_list = []
    archive_list = []

    for file in path_to_dir.iterdir():
        if file.suffix.lower() in IMAGES:
            images_list.append(file)
        elif file.suffix.lower() in VIDEO:
            videos_list.append(file)
        elif file.suffix.lower() in DOCUMENTS:
            documents_list.append(file)
        elif file.suffix.lower() in MUSIC:
            music_list.append(file)
        elif file.suffix.lower() in ARCHIVE:
            archive_list.append(file)

    return {
        'images': images_list,
        'video': videos_list,
        'documents': documents_list,
        'music': music_list,
        'archive': archive_list,
    }


def delete_empty_folder(path):
    p = Path(path)
    for folder in p.iterdir():
        if folder.is_dir() and not os.listdir(folder):
            folder.rmdir()


def replace_file(path):
    split_file = sorted_files(path)
    p = Path(path)
    folder_list = [item.name for item in p.iterdir() if item.is_dir()]
    for folder in FOLDERS_NAMES:
        if folder in split_file:
            if folder == 'archive':
                for file in split_file[folder]:
                    if folder not in folder_list:
                        os.mkdir(path + '/' + folder)
                        shutil.unpack_archive(file, path + '/' + folder + '/' + file.name.replace(file.suffix, ''))
                        shutil.move(file, path + '/' + folder)
                        folder_list.append(folder)
                    else:
                        shutil.unpack_archive(file, path + '/' + folder + '/' + file.name.replace(file.suffix, ''))
                        shutil.move(file, path + '/' + folder)

            else:
                for file in split_file[folder]:
                    if folder not in folder_list:
                        os.mkdir(path + '/' + folder)
                        shutil.move(file, path + '/' + folder)
                        folder_list.append(folder)
                    else:
                        shutil.move(file, path + '/' + folder)


def main(path):
    try:
        p = Path(path)
        delete_empty_folder(path)
        normalize(path)
        for dir_obj in p.iterdir():
            if dir_obj.is_file():
                replace_file(path)
            elif dir_obj.is_dir() and dir_obj.name not in FOLDERS_NAMES:
                main(path + '/' + dir_obj.name)
    except FileNotFoundError as e:
        print(f'{e}. Try to write correct path')


if __name__ == '__main__':
    try:
        path = sys.argv[1]
        main(path)
    except IndexError:
        print('Не бавтеся!! Введіть шлях до файлу, як аргумент командного рядка!!!')


