# -*- coding: utf-8 -*-
"""Creation of the final database.

"""

import os
import numpy as np

from references import csv_paths

import context
from geocoding.datatypes import dtypes
from geocoding.datapaths import paths, database


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
    print_results(out_filename, dat_file)


def sort_table(in_filename, dtype, field):
    """Sort a numpy array stored in a file following a certain criteria.

    This method sorts a numpy array of objects stored in a binary file using a
    field of the object as the value to compare.

    Args:
        in_filename (str): The name of the file where the array is stored.
        dtype (np.dtype): The type of the objects in the array.
        field (str): The name of the field of the object to be used in the
            comparisons.

    """
    table = np.memmap(in_filename, dtype=dtype)
    table.sort(order=field)
    table.flush()

    print('sorted %s on %s' % (in_filename, field))


def csv_to_list(in_filename):
    in_file = open(in_filename, 'r+')
    tuple_list = [tuple(line.strip().split(';')) for line in in_file]
    tuple_length = max(len(tup) for tup in tuple_list)
    indices = []
    for i in range(len(tuple_list)):
        if len(tuple_list[i]) != tuple_length:
            indices.append(i)
    print(len(indices))
    for i in indices:
        del tuple_list[i]
    return tuple_list


def index_list(in_filename, dtype, column):
    """Return the indices of a sorted numpy array stored in a file.

    This method sorts a numpy array of objects stored in a binary file using a
    field of the object as the value to compare and returns the indices of this
    new array.

    Args:
        in_filename (str): The name of the file where the array is stored.
        dtype (np.dtype): The type of the objects in the array.
        field (str): The name of the field of the object to be used in the
            comparisons.

    Returns:
        list: The list of indices (int list).

    """
    table = np.memmap(in_filename, dtype=dtype)
    indexes_list = np.argsort(table, order=column).astype('int32')
    return indexes_list


def create_info_tables():
    for table in csv_paths:
        table_list = csv_to_list(csv_paths[table])
        create_dat_file(table_list, paths[table], dtypes[table])


def create_index_tables():
    def sort_and_store(table, table_index, column):
        indices = index_list(paths[table], dtypes[table], column)
        create_dat_file(indices, paths[table_index], 'int32')

    sort_and_store('postal', 'postal_index', 'code')
    sort_and_store('commune', 'commune_index', 'normalise')
    sort_and_store('voie', 'voie_index', 'normalise')


def print_results(filename, table):
    size = float(table.nbytes) / (1024 ** 2)
    print('written %s : %.3f MB' % (filename, size))


if __name__ == '__main__':
    print('CREATING DATABASE .dat')

    if not os.path.exists(database):
        os.mkdir(database)

    create_info_tables()
    create_index_tables()

    print('DONE')
