from pathlib import Path
import sys
import shutil
import os

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


# PATH = sys.argv[1]


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


def sorted_files(path):
    path_to_dir = Path(path)
    images_list = []
    videos_list = []
    documents_list = []
    music_list = []
    archive_list = []
    other_files_list = []

    for file in path_to_dir.glob('**/*'):
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
        elif file.is_file():
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
        if folder_name == 'archive':
            for file in files_list:
                if folder_name not in folder_list:
                    os.mkdir(os.path.join(path, folder_name))
                    shutil.move(file, os.path.join(path, folder_name))
                    folder_list.append(folder_name)
                elif not Path(os.path.join(path, folder_name, file.name)).exists():
                    shutil.move(file, os.path.join(path, folder_name))

        else:
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
                shutil.unpack_archive(archives, os.path.join(path, 'archive', archives.name.replace(archives.suffix, '')))


def clean_folder(path):
    try:
        replace_file(path)
        normalize(path)
        delete_empty_folder(path)
        unpack_archive(path)
    except FileNotFoundError as e:
        print(f'{e}. Try to write correct path')


clean_folder(r'C:\Users\sadBOY\Desktop\Green1')

# def main():
#     clean_folder(PATH)


# if __name__ == '__main__':
#     main()
