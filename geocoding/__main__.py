#!/usr/bin/env python
import sys

from .download import get_ban_file, decompress
from .index import process_files, create_database
from .activate_reverse import create_kdtree


commands = {
    'download': [get_ban_file],
    'decompress': [decompress],
    'index': [process_files, create_database],
    'reverse': [create_kdtree],
    'update': [get_ban_file, decompress, process_files, create_database]
}


def main(args=None):
    command = sys.argv[1:]

    if not command or command[0] not in commands:
        print('usage: geocoding '
              '{update, download, decompress, index, reverse}')
        return

    for function in commands[command[0]]:
        success = function()
        if not success:
            return


if __name__ == "__main__":
    main()
