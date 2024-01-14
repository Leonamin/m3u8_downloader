import json
import os
import requests
import subprocess
import concurrent.futures

from settings import *
from util.utils import make_folder


def download_m3u8_content(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


def read_m3u8_link_list():
    with open(os.path.join(setting_folder, 'content.json'), 'r') as file:
        return json.load(file)


def save_m3u8_content(m3u8_content, file_name):
    file_path = os.path.join(m3u8_contents_folder, f'{
                             file_name}_m3u8_content.txt')
    counter = 2
    while os.path.exists(file_path):
        file_path = os.path.join(m3u8_contents_folder, f'{
                                 file_name}_m3u8_content_{counter}.txt')
        counter += 1
    with open(file_path, 'w') as file:
        file.write(m3u8_content)


def extract_ts_urls(m3u8_content, base_url):
    lines = m3u8_content.split('\n')
    ts_urls = []
    for i in range(len(lines)):
        if lines[i].endswith('.ts'):
            ts_urls.append(base_url + lines[i])
    return ts_urls


def download_ts_files_parallel(ts_urls, output_dir):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_download_workers) as executor:
        futures = [executor.submit(download_m3u8_content, url, os.path.join(
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
    try:
        # m3u8 내용 다운로드 및 저장
        m3u8_response = requests.get(item['m3u8_link'])
        m3u8_content = m3u8_response.text
        save_m3u8_content(m3u8_content, item['name'])

        #  ts 파일 URL 생성을 위한 기본 URL 설정
        # ts_url = item['ts_base_link']
        # if len(ts_url) == 0:
        #     ts_url = item['m3u8_link'].rsplit('/', 1)[0] + '/'

        ts_url = item['m3u8_link'].rsplit('/', 1)[0] + '/'

        # ts 파일 URL 생성
        ts_urls = extract_ts_urls(m3u8_content, ts_url)

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
    except Exception as e:
        print(f"Error processing {item['name']}: {e}")


if __name__ == '__main__':
    make_folder()

    content_list = read_m3u8_link_list()
    for content in content_list:
        process_content(content)
