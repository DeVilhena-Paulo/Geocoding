# -*- coding: utf-8 -*-
"""Processing of raw data.

This module creates an intermediary database in csv format. The goal of this
intermediate step is to easy the next step: the construction of the binary
files using tools from the package numpy.

"""

import os
import numpy as np
from collections import deque

from .datatypes import dtypes
from .datapaths import paths, database
from .download import completion_bar, raw_data_folder_path
from . import ban_processing

file_names = ['departement', 'postal', 'commune', 'voie', 'localisation']
processed_files = {}


def process_files():
    for file in file_names:
        processed_files[file] = deque()

    ban_files = {}

    # Check if the folder with the data to process exists
    if not os.path.exists(raw_data_folder_path):
        print('Execute : geocoding download')
        return False

    # Open each csv file
    for (dirname, dirs, files) in os.walk(raw_data_folder_path):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(dirname, filename)
                dpt_name = filename.split('-')[-1].split('.')[0]
                ban_files[dpt_name] = open(file_path, 'r', encoding='UTF-8')

    # Check if the folder was not empty
    if not ban_files:
        print('Execute : geocoding decompress')
        return False

    departements = list(ban_files.keys())
    departements.sort()

    for i, departement in enumerate(departements):
        ban_processing.update(departement, ban_files[departement], processed_files)
        completion_bar('Processing BAN', (i + 1) / len(departements))

    return True


def create_database():
    if not os.path.exists(database):
        os.mkdir(database)

    if not processed_files:
        return False

    add_index_tables()

    count = 0
    for table, processed_file in processed_files.items():
        create_dat_file(list(processed_file), paths[table], dtypes[table])

        count += 1
        completion_bar('Storing data', count / len(processed_files))

    return True


def add_index_tables():
    index_tables = ['postal', 'commune', 'voie']

    # Index tables creation
    for i, table in enumerate(index_tables):
        sort_method = (lambda i: processed_files[table][i])

        # Sort table and add it to the module level dict processed_files
        processed_files[table + '_index'] = \
            sorted(range(len(processed_files[table])), key=sort_method)

        completion_bar('Indexing tables', (i + 1) / len(index_tables))


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
