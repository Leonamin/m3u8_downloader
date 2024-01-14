import os
from typing import Tuple
import requests

from settings import m3u8_contents_folder

# m3u8 파일을 다운로드 받아서 저장하는 함수
# 반환으로는 base_url과 media_playlist_content를 반환


def get_m3u8_content(url: str, filename: str) -> Tuple[str, str]:
    media_playlist_response: requests.Response = requests.get(url)
    m3u8_content: str = media_playlist_response.text

    _is_master_playlist: bool = is_master_playlist(m3u8_content)

    media_playlist_content: str = None
    base_url: str = url.rsplit('/', 1)[0] + '/'

    print('is_master_playlist: ', _is_master_playlist)

    if _is_master_playlist:
        highest_quality_media_playlist_url: str = get_highest_quality_media_playlist_url(
            m3u8_content, base_url)
        media_playlist_response = requests.get(
            highest_quality_media_playlist_url)
        media_playlist_content = media_playlist_response.text
        base_url = highest_quality_media_playlist_url.rsplit('/', 1)[0] + '/'

        print('Master Playlist Content: \n')
        print(m3u8_content)
        print('new base_url: ', base_url)
    else:
        media_playlist_content = m3u8_content
        base_url = url.rsplit('/', 1)[0] + '/'

    print('Media Playlist Content: \n')
    print(media_playlist_content)

    save_media_playlist_content(media_playlist_content, filename)

    return base_url, media_playlist_content


def is_master_playlist(m3u8_content):
    return "#EXT-X-STREAM-INF" in m3u8_content


def get_highest_quality_media_playlist_url(m3u8_content, base_url):
    lines = m3u8_content.split('\n')
    highest_quality_stream_url = None
    for line in lines:
        if line.startswith('#EXT-X-STREAM-INF'):
            highest_quality_stream_url = None  # 다음 스트림 URL을 확인하기 위해 초기화
        elif line and not line.startswith('#') and not highest_quality_stream_url:
            # 스트림 URL을 저장 (가장 마지막에 나온 URL을 최종적으로 사용)
            highest_quality_stream_url = base_url + line
    return highest_quality_stream_url


def save_media_playlist_content(m3u8_content, file_name):
    file_path = os.path.join(m3u8_contents_folder, f'{
                             file_name}_m3u8_content.txt')
    counter = 2
    while os.path.exists(file_path):
        file_path = os.path.join(m3u8_contents_folder, f'{
                                 file_name}_m3u8_content_{counter}.txt')
        counter += 1
    with open(file_path, 'w') as file:
        file.write(m3u8_content)


if __name__ == '__main__':
    m3u8_url = 'https://rosedebt.com/f3ad4377-b55d-4e6e-a0de-83de7fd82600/playlist.m3u8'
    base_url = m3u8_url.rsplit('/', 1)[0] + '/'
    response = requests.get(m3u8_url)
    m3u8_content = response.text
    print(m3u8_content)
    print(get_highest_quality_media_playlist_url(m3u8_content, base_url))
    pass
