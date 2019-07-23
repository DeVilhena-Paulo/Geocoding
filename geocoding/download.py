# -*- coding: utf-8 -*-
"""Update the raw data used as the main source of information.

"""
import gzip
import os
import shutil
import sys
import requests
import hashlib

from .datapaths import here

raw_data_folder_path = os.path.join(here, 'raw')
ban_url = 'https://adresse.data.gouv.fr/data/ban/export-api-gestion/latest/ban/{}'
ban_dpt_gz_file_name = 'ban-{}.csv.gz'
ban_dpt_file_name = 'ban-{}.csv'
content_folder_path = os.path.join(here, 'content')
server_content_file_name = os.path.join(content_folder_path, 'server_content_v2.txt')
local_content_file_name = os.path.join(content_folder_path, 'local_content_v2.txt')
dpt_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "2A", "2B",
            "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
            "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
            "50", "51", "52", "53", "54", "55", "56", "57", "58", "59",
            "60", "61", "62", "63", "64", "65", "66", "67", "68", "69",
            "70", "71", "72", "73", "74", "75", "76", "77", "78", "79",
            "80", "81", "82", "83", "84", "85", "86", "87", "88", "89",
            "90", "91", "92", "93", "94", "95",
            "971", "972", "973", "974", "975", "976"]


def completion_bar(msg, fraction):
    percent = int(100 * fraction)
    size = int(50 * fraction)
    sys.stdout.write("\r%-16s: %3d%%[%s%s]" %
                     (msg, percent, '=' * size, ' ' * (50 - size)))
    sys.stdout.flush()

    # New line if bar is complete
    if fraction == 1.:
        print('')


def md5(fname):
    md5_hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def update_ban_file(url, file_name):
    r = requests.get(url)

    if r.status_code != 200:
        raise Exception('Unable to join BAN address website ({}). Status error code: {}'.format(url,
                                                                                                r.status_code))

    with open(file_name, 'w') as file:
        file.write(r.text)


def update_local_content_file():
    update_ban_file(ban_url.format(""), local_content_file_name)


def update_server_content_file():
    update_ban_file(ban_url.format(""), server_content_file_name)


def need_to_download():
    if not os.path.exists(local_content_file_name):
        return True
    else:
        update_server_content_file()

        if md5(server_content_file_name) == md5(local_content_file_name):
            print('BAN database is already up to date. No need to download it again.')
            os.remove(server_content_file_name)
            return False

        return True


def download_ban_dpt_file(ban_dpt_file_name):
    with open(os.path.join(raw_data_folder_path, ban_dpt_file_name), 'wb') as ban_dpt_file:
        response = requests.get(ban_url.format(ban_dpt_file_name), stream=True)

        if not response.ok:
            print('Download {} unsuccessful: bad response'.format(ban_dpt_file_name))
            return False

        done, total_size = 0, int(response.headers.get('content-length'))
        for block in response.iter_content(4096):
            ban_dpt_file.write(block)

            done += len(block)
            completion_bar('Downloading {}'.format(ban_dpt_file_name), done / total_size)

    if done != total_size:
        print('Download {} unsuccessful: incomplete'.format(ban_dpt_file_name))
        return False

    return True


def get_ban_file():
    if not os.path.exists(content_folder_path):
        os.mkdir(content_folder_path)

    if not need_to_download():
        return False

    print('A new version of BAN base is available.')

    update_local_content_file()

    if os.path.exists(raw_data_folder_path):
        shutil.rmtree(raw_data_folder_path)
    
    os.mkdir(raw_data_folder_path)

    for dpt in dpt_list:
        if not download_ban_dpt_file(ban_dpt_gz_file_name.format(dpt)):
            raise Exception('Impossible to download {}'.format(ban_dpt_gz_file_name.format(dpt)))

    return True


def decompress():
    for dpt in dpt_list:
        # Certifies the existence of the subdirectory.
        dpt_gz_file_path = os.path.join(raw_data_folder_path, ban_dpt_gz_file_name.format(dpt))
        if not os.path.isfile(dpt_gz_file_path):
            print('Decompression unsuccessful : inexistent file {}'.format(dpt_gz_file_path))
            return False

        # Decompress each file within gzip
        with gzip.open(dpt_gz_file_path, 'rb') as f_in:
            dpt_file_path = os.path.join(raw_data_folder_path, ban_dpt_file_name.format(dpt))
            print('Extracting file {}'.format(ban_dpt_gz_file_name.format(dpt)))
            with open(dpt_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    return True
