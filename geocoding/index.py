# -*- coding: utf-8 -*-
"""Processing of raw data.

This module creates an intermediary database in csv format. The goal of this
intermediate step is to easy the next step: the construction of the binary
files using tools from the package numpy.

"""

import os
import numpy as np
from collections import deque

from .references import raw_data
from .datatypes import dtypes
from .datapaths import paths, database
from .download import completion_bar
from . import ban_processing

file_names = ['departement', 'postal', 'commune', 'voie', 'localisation']
processed_files = {}


def process_files():
    for file in file_names:
        processed_files[file] = deque()

    ban_files = {}

    for (dirname, dirs, files) in os.walk(raw_data):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(dirname, filename)
                dpt_name = filename.split('_')[-1].split('.')[0]
                ban_files[dpt_name] = open(file_path, 'r', encoding='UTF-8')

    departements = list(ban_files.keys())
    departements.sort()

    for i, departement in enumerate(departements):
        ban_processing.update(departement, ban_files[departement],
                              processed_files)
        completion_bar('Processing files', (i + 1) / len(departements))

    print('')

    return True


def create_database():
    if not os.path.exists(database):
        os.mkdir(database)

    if not processed_files:
        return False

    add_index_tables()

    count, n_total = 0, len(processed_files)
    for table, processed_file in processed_files.items():
        create_dat_file(list(processed_file), paths[table], dtypes[table])

        count += 1
        completion_bar('Creating database', count / n_total)

    return True


def add_index_tables():
    index_tables = ['postal', 'commune', 'voie']
    for table in index_tables:
        processed_files[table + '_index'] = \
            sorted(range(len(processed_files[table])),
                   key=(lambda i: processed_files[table][i]))


def create_dat_file(lst, out_filename, dtype):
    """Write a list in a binary file as a numpy array.

    Args:
        lst: The list that will be written in the file.
        out_filename: The name of the binary file. It must be in the same
            directory.
        dtype: The type of the numpy array.

    """
    with open(out_filename, 'wb+') as out_file:
        dat_file = np.memmap(out_file, dtype=dtype, shape=(len(lst),))
        dat_file[:] = lst[:]
        dat_file.flush()


if __name__ == '__main__':
    process_files()
    create_database()
