# -*- coding: utf-8 -*-
"""Update the raw data used as the main source of information.

"""

import os
import zipfile
import requests

from references import raw_data, url, ban_zip


def get_ban_file():
    """Download the BAN files.
    """
    print('retrieving ban file : %s' % url)

    # Certifies the existence of the directory.
    if not os.path.exists(raw_data):
        os.mkdir(raw_data)

    if os.path.exists(ban_zip):
        os.remove(ban_zip)

    # Downloads the content and stores it at ban_zip.
    with open(ban_zip, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            raise Exception("Bad Response")

        for block in response.iter_content(1024):
            handle.write(block)

    print('download complete')


def unzip():
    print('unzip ban file at : %s' % ban_zip)

    # Certifies the existence of the subdirectory.
    if not os.path.exists(raw_data):
        os.mkdir(raw_data)

    # Uncompress each file within ban_zip
    with zipfile.ZipFile(ban_zip) as zf:
        for member in zf.infolist():
            zf.extract(member, path=raw_data)

    os.remove(ban_zip)
    print('unzip complete')


if __name__ == '__main__':
    print('UPDATING BAN FILE')

    get_ban_file()
    unzip()

    print("DONE")
