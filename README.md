# M3U8 Downloader
## 소개
m3u8을 다운로드 하고 ffmpeg로 .ts 파일을 합쳐서 완성된 영상을 만들어줍니다.
## 사용법
### ffmpeg 설치
ffmpeg이 있어야 실행이 가능합니다.
### 링크 가져오기
playlist.m3u8 또는 video.m3u8 링크를 찾습니다.

해당 링크는 주로 디버그 콘솔을 연뒤 네트워크 응답 중에서 m3u8 응답인 요청링크를 찾습니다.

어떤 사이트들은 playlist.m3u8, video.m3u8 형식으로 되어있습니다.(물론 사이트마다 다릅니다.)

m3u8은 주로 Master Playlist와 Media Plalist로 나누어져 있으며 Media Playlist 링크가 실제 .ts 파일들이 정의된 링크입니다.

Master Playlist는 Media Playlist 경로가 정의되어 있으며 `Master Playlist 경로(~~~.m3u8을 제외한 경로) + 목록에 정의된 경로`가 진짜 다운로드 가능한 링크입니다.

해당 링크를 열면 보통 내용은 아래와 같습니다.

playlist.m3u8는 최초 베이스 url로 비디오 정보가 담겨있습니다.

video.m3u8은 .ts 파일 목록을 표시해줍니다.

.ts 파일은 비디오가 쪼개진 패킷이며 해당 패킷이 있어야 다운로드가 가능합니다.

#### Master Playlist(playlist.m3u8)의 내용
```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=384000,AVERAGE-BANDWIDTH=434032,CODECS="avc1.66.21, mp4a.40.2",RESOLUTION=480x270,FRAME-RATE=29.97,CHANNELS="2"
content_384000.m3u8?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXT-X-STREAM-INF:BANDWIDTH=768000,AVERAGE-BANDWIDTH=836416,CODECS="avc1.66.30, mp4a.40.2",RESOLUTION=640x360,FRAME-RATE=29.97,CHANNELS="2"
content_768000.m3u8?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXT-X-STREAM-INF:BANDWIDTH=1024000,AVERAGE-BANDWIDTH=1106536,CODECS="avc1.77.31, mp4a.40.2",RESOLUTION=856x480,FRAME-RATE=29.97,CHANNELS="2"
content_1024000.m3u8?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXT-X-STREAM-INF:BANDWIDTH=2048000,AVERAGE-BANDWIDTH=2141704,CODECS="avc1.77.31, mp4a.40.2",RESOLUTION=1280x720,FRAME-RATE=29.97,CHANNELS="2"
content_2048000.m3u8?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXT-X-STREAM-INF:BANDWIDTH=5120000,AVERAGE-BANDWIDTH=5168360,CODECS="avc1.100.40, mp4a.40.2",RESOLUTION=1920x1080,FRAME-RATE=29.97,CHANNELS="2"
content_5120000.m3u8?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
```
#### Media Playlist(video.m3u8)의 내용
```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:11
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:10.077,
content_2048000_0.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_1.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_2.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_3.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_4.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_5.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_6.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_7.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_8.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:10.010,
content_2048000_9.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXTINF:7.289,
content_2048000_10.ts?solexpire=1705262771&solpathlen=189&soltoken=b2a21284e5046e3ab98309e64dfb837c&soltokenrule=c29sZXhwaXJlfHNvbHBhdGhsZW58c29sdXVpZA==&soluriver=2&soluuid=e2560257-3ade-43ca-b478-ac385c796428
#EXT-X-ENDLIST
```
### content.json 설정
메인프로젝트 아래에 settings 폴더를 만든뒤 아래에 `content.json`을 생성하고 다음과 같이 작성합니다.

```json
[
    {
        "name": "video_title",
        "m3u8_link": "aaa"
    }
]
```

### 기타 설정
- max_download_workers을 설정하면 ts파일을 동시에 다운로드 받는 수를 늘릴 수 있습니다.(**주의 워커 스레드가 많으면 프로그램이 멈출 수도 있습니다. 적당히 사용하세요**)