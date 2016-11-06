#!/usr/bin/env python3

import sys
import os
import datetime
import urllib.request
import re
import configparser

import vk
import progressbar

config = configparser.ConfigParser()
config.read('config.ini')
vk_token = config['DEFAULT']['access_token']

session = vk.Session(access_token=vk_token)
api = vk.API(session)


def timestamp_to_date(stamp):
    return datetime.datetime.fromtimestamp(int(stamp)).strftime('%Y%m%d')


def normalize(text):
    rep = {'"': '', ' ': '-'}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text).lower()


def get_max_res_photo(photo):
    """Return URL to photo with maximum resolution"""
    photo_sizes = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
    for i in range(len(photo_sizes)):
        try:
            url = (item for item in photo['sizes']
                   if item['type'] == photo_sizes[i]).__next__()
            break
        except:
            continue
    return url['src']


def download_all_albums(group):
    albums = api.photos.getAlbums(owner_id='-' + group)
    print("Albums: ", len(albums))
    for album in albums:
        album_name = timestamp_to_date(album['created']) + \
            '_' + normalize(album['title'])
        download_album_to_dir(group, album['aid'], album['size'], album_name)


def download_album(group, alb):
    album = api.photos.getAlbums(owner_id='-' + group, album_ids=alb)[0]
    album_name = timestamp_to_date(album['created']) + \
        '_' + normalize(album['title'])
    download_album_to_dir(group, alb, album['size'], album_name)


def download_album_to_dir(group, album, size, directory):
    print(directory + ' [album_id: ' + album + ']')
    if not os.path.exists(directory):
        os.makedirs(directory)
    counter = 1
    with progressbar.ProgressBar(max_value=size) as bar:
        for photo in api.photos.get(owner_id='-' + group,
                                    album_id=album, photo_sizes=1):
            url = get_max_res_photo(photo)
            out = os.path.join(directory, '{:04d}.jpg'.format(counter))
            urllib.request.urlretrieve(url, out)
            counter += 1
            bar.update(counter - 1)

if len(sys.argv) == 2:
    download_all_albums(sys.argv[1])
elif len(sys.argv) == 3:
    download_album(sys.argv[1], sys.argv[2])
else:
    print("Usage: vkbackup.py <group>")
    print("Usage: vkbackup.py <group> <album>")
    sys.exit()
