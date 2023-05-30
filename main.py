from pathlib import Path
import sys
import shutil
import os
from random import randint

IMAGES = ('.jpeg', '.png', '.jpg', '.svg')
VIDEO = ('.avi', '.mp4', '.mov', '.mkv')
DOCUMENTS = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
MUSIC = ('.mp3', '.ogg', '.wav', '.amr')
ARCHIVE = ('.zip', '.gz', '.tar',)

FOLDERS_NAMES = ('images', 'video', 'documents', 'music', 'archive')

CYRILLIC_SYMBOLS = r"абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_",
               "_",
               "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_",
               "_",
               "_", "_", "_", "_", "_", "_", "_")
TRANSLIT_DICT = {}

PATH = sys.argv[1]


def normalize(path):
    p = Path(path)

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANSLIT_DICT[ord(c)] = l
        TRANSLIT_DICT[ord(c.upper())] = l.upper()

    for name in p.iterdir():
        if name.is_file():
            name.rename(
                os.path.join(path, name.name[:name.name.index(name.suffix)].translate(TRANSLIT_DICT) + name.suffix))
        elif name.is_dir():
            if name.name not in FOLDERS_NAMES:
                name.rename(os.path.join(path, name.name.translate(TRANSLIT_DICT)))


def rename_same_file(path):
    path_to_dir = Path(path)
    file_names_list = [file.name for file in path_to_dir.glob('**/*')]
    for file in path_to_dir.glob('**/*'):
        if file_names_list.count(file.name) >= 2:
            new_name = file.with_name(str(randint(1000, 9999)) + '_' + file.name)
            file_names_list.append(new_name.name)
            file.replace(new_name)


def sorted_files(path):
    rename_same_file(path)
    path_to_dir = Path(path)
    images_list = []
    videos_list = []
    documents_list = []
    music_list = []
    archive_list = []
    other_files_list = []

    for file in path_to_dir.glob('**/*'):
        if file.suffix.lower() in IMAGES and path + '\\archive\\' not in str(file):
            images_list.append(file)
        elif file.suffix.lower() in VIDEO and path + '\\archive\\' not in str(file):
            videos_list.append(file)
        elif file.suffix.lower() in DOCUMENTS and path + '\\archive\\' not in str(file):
            documents_list.append(file)
        elif file.suffix.lower() in MUSIC and path + '\\archive\\' not in str(file):
            music_list.append(file)
        elif file.suffix.lower() in ARCHIVE:
            archive_list.append(file)
        elif file.is_file() and path + '\\archive\\' not in str(file):
            other_files_list.append(file)

    return {
        'images': images_list,
        'video': videos_list,
        'documents': documents_list,
        'music': music_list,
        'archive': archive_list,
        'other_files': other_files_list
    }


def delete_empty_folder(path):
    p = Path(path)
    for folder in p.iterdir():
        if folder.is_dir():
            if not os.listdir(folder):
                folder.rmdir()
            else:
                delete_empty_folder(folder)
                if not os.listdir(folder):
                    folder.rmdir()


def replace_file(path):
    split_file = sorted_files(path)
    p = Path(path)
    folder_list = [item.name for item in p.iterdir() if item.is_dir()]
    for folder_name, files_list in split_file.items():
        for file in files_list:
            if folder_name not in folder_list:
                os.mkdir(os.path.join(path, folder_name))
                shutil.move(file, os.path.join(path, folder_name))
                folder_list.append(folder_name)
            elif not Path(os.path.join(path, folder_name, file.name)).exists():
                shutil.move(file, os.path.join(path, folder_name))


def unpack_archive(path):
    if Path(os.path.join(path, 'archive')).exists():
        p = Path(os.path.join(path, 'archive'))
        for archives in p.iterdir():
            if not Path(os.path.join(path, 'archive', archives.name.replace(archives.suffix, ''))).exists():
                shutil.unpack_archive(archives,
                                      os.path.join(path, 'archive', archives.name.replace(archives.suffix, '')))


def clean_folder(path):
    try:
        replace_file(path)
        normalize(path)
        delete_empty_folder(path)
        unpack_archive(path)
    except FileNotFoundError as e:
        print(f'{e}. Try to write correct path')


def main():
    clean_folder(PATH)


if __name__ == '__main__':
    main()
