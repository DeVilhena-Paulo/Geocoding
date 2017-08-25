import os
import sys
import numpy as np

from kdquery import Tree

from .index import create_dat_file
from .datatypes import dtypes
from .datapaths import paths
from .utils import pre_order, degree_to_int
from .download import completion_bar


def node_to_tuple(node):
    longitude, latitude = node.point

    limit_left = node.region[0][0]
    limit_right = node.region[0][1]
    limit_bottom = node.region[1][0]
    limit_top = node.region[1][1]

    left = node.left if node.left is not None else -1
    right = node.right if node.right is not None else -1

    return (longitude, latitude, limit_left, limit_right, limit_bottom,
            limit_top, node.axis, left, right, node.data)


def create_kdtree():
    table = np.memmap(paths['localisation'], dtype=dtypes['localisation'])
    indices = np.argsort(table, order='longitude').astype('int32')

    limits = [[degree_to_int(-62), degree_to_int(55)],
              [degree_to_int(-22), degree_to_int(52)]]

    tree = Tree(2, len(table), limits)

    count, n_total = 0, len(table)
    for i in pre_order(len(table)):
        index = indices[i]
        loc = table[index]
        tree.insert((loc['longitude'], loc['latitude']), index)

        count += 1
        completion_bar('Loading kd-tree', (count / n_total))

    print('\nStoring ...')
    tuple_list = [node_to_tuple(node) for node in tree]
    create_dat_file(tuple_list, paths['kdtree'], dtypes['kdtree'])
    print('Activation successfully')
    return True
