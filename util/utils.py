from settings import *


def make_folder(folders=[setting_folder, output_folder, ts_files_folder, videos_folder, m3u8_contents_folder]):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
