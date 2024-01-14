import json
import os
import requests
import subprocess
import concurrent.futures

from settings import *
from util.utils import make_folder
from util.m3u8_utils import get_m3u8_content


def read_m3u8_link_list():
    with open(os.path.join(setting_folder, 'content.json'), 'r') as file:
        return json.load(file)


def download_ts_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


def extract_ts_urls(m3u8_content, base_url):
    lines = m3u8_content.split('\n')
    ts_urls = []
    for i in range(len(lines)):
        if lines[i].endswith('.ts'):
            ts_urls.append(base_url + lines[i])
    return ts_urls


def download_ts_files_parallel(ts_urls, output_dir):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_download_workers) as executor:
        futures = [executor.submit(download_ts_file, url, os.path.join(
            output_dir, url.split('/')[-1])) for url in ts_urls]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def merge_ts_files_to_mp4(input_dir, output_file):
    ts_files = sorted([os.path.join(input_dir, f)
                      for f in os.listdir(input_dir) if f.endswith('.ts')])
    with open('file_list.txt', 'w') as f:
        for file in ts_files:
            f.write(f"file '{file}'\n")
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0',
                   '-i', 'file_list.txt', '-c', 'copy', output_file])
    os.remove('file_list.txt')


def process_content(item):
    succeedList = []
    failedList = []
    try:
        # m3u8 내용 다운로드 및 저장
        base_url, media_playlist = get_m3u8_content(
            item['m3u8_link'], item['name'])

        ts_urls = extract_ts_urls(media_playlist, base_url)

        # ts 파일 다운로드 폴더 생성 및 다운로드
        ts_output_dir = os.path.join(ts_files_folder, item['name'])
        if not os.path.exists(ts_output_dir):
            os.makedirs(ts_output_dir)
        download_ts_files_parallel(ts_urls, ts_output_dir)

        # 파일 병합
        output_video_file = os.path.join(videos_folder, f"{item['name']}.mp4")
        merge_ts_files_to_mp4(ts_output_dir, output_video_file)

        # 다운로드한 ts 파일 삭제
        for ts_file in os.listdir(ts_output_dir):
            os.remove(os.path.join(ts_output_dir, ts_file))
        os.rmdir(ts_output_dir)
        succeedList.append(item['name'])
    except Exception as e:
        print(f"Error processing {item['name']}: {e}")
        failedList.append(item['name'])

    print(f"Succeed: {succeedList}")

    print(f"Failed: {failedList}")


if __name__ == '__main__':
    make_folder()
    content_list = read_m3u8_link_list()
    for content in content_list:
        process_content(content)
