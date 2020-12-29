import os

import requests
from pyquery import PyQuery as pq


def get_download_url(movie_url):
    get_request = requests.get(movie_url)
    get_request_str = str(get_request.content, 'utf-8')

    pq_obj_items = pq(get_request_str)('div.download-list.d-hidden').eq(0)('div')('a').items()

    download_urls = []
    for pq_item in pq_obj_items:
        if '.mp4' in str(pq_item):
            download_url = pq_item('a').attr('href')
            download_urls.append(download_url)

    best_quality_download_url = download_urls[-1]
    download_movie(best_quality_download_url)


def download_movie(download_url):
    file_name = str(download_url).split(maxsplit=1)[1].replace('/', '')
    file_dir = 'videos/{}.mp4'.format(file_name)

    if not os.path.exists('videos'):
        os.mkdir('videos')

    get_video = requests.get(download_url, allow_redirects=True)
    with open(file_dir, "wb") as file_stream:
        video_content = get_video.content
        file_stream.write(video_content)

    return file_dir


url = 'http://asilmedia.net/11773-tepalikda-ajratish-olim-yaqin-emas-uzbek-tilida-2018-ozbekcha-tarjima-kino-hd.html'
get_download_url(url)
