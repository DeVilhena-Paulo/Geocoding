#!/usr/bin/env python
import os
import sys
import shutil
import zipfile
import requests

from .datapaths import database

url = "https://dl.dropboxusercontent.com/s/vp3x2j8xlt63gkm/database.zip?dl=0"

here = os.path.abspath(os.path.dirname(__file__))
file = os.path.join(here, 'data.zip')


def completion_bar(msg, fraction):
    percent = int(100 * fraction)
    size = int(50 * fraction)
    sys.stdout.write("\r%s : %3d%%[%s%s]" %
                     (msg, percent, '=' * size, ' ' * (50 - size)))
    sys.stdout.flush()


def get_uploaded_data():
    """Donwload uploaded database.
    """
    with open(file, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            raise Exception("Bad Response")

        done_length = 0
        total_length = int(response.headers.get('content-length'))

        for block in response.iter_content(4096):
            handle.write(block)

            # Print completion bar
            done_length += len(block)
            completion_bar('Retrieving database', done_length / total_length)

        print('')


def unzip():

    if os.path.exists(database):
        shutil.rmtree(database)

    os.mkdir(database)

    # Uncompress each file within file
    with zipfile.ZipFile(file) as zf:
        zipped_files = len(zf.infolist())
        unzipped_files = 0

        for member in zf.infolist():
            zf.extract(member, path=database)

            # Print completion bar
            unzipped_files += 1
            completion_bar('Uncompressing files',
                           unzipped_files / zipped_files)

    print('\nGeocoding is ready to use!')


def main(args=None):
    args = sys.argv[1:]
    commands = {
        'download': get_uploaded_data,
        'unzip': unzip,
        'update': (lambda: (get_uploaded_data(), unzip()))
    }

    if not args or args[0] not in commands:
        print("usage: geocoding {download, unzip, update}")
        return

    commands[args[0]]()


if __name__ == "__main__":
    main()
