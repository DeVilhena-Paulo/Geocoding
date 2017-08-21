import os
import sys
import numpy as np

from index import create_dat_file

from kdquery import Tree

import context
from geocoding.datatypes import dtypes
from geocoding.datapaths import paths
from geocoding.utils import pre_order, degree_to_int


def node_to_tuple(node):
    longitude = node.point[0]
    latitude = node.point[1]

    limit_left = node.region[0][0]
    limit_right = node.region[0][1]
    limit_bottom = node.region[1][0]
    limit_top = node.region[1][1]

    left = node.left if node.left is not None else -1
    right = node.right if node.right is not None else -1

    return (longitude, latitude, limit_left, limit_right, limit_bottom,
            limit_top, node.axis, left, right, node.data)


def create_kdtree_table():
    table = np.memmap(paths['localisation'], dtype=dtypes['localisation'])
    indices = np.argsort(table, order='longitude').astype('int32')

    limits = [[degree_to_int(-62), degree_to_int(55)],
              [degree_to_int(-22), degree_to_int(52)]]

    tree = Tree(2, len(table), limits)

    count = 0
    for i in pre_order(len(table)):
        index = indices[i]
        loc = table[index]
        tree.insert((loc['longitude'], loc['latitude']), index)
        count += 1
        if count % 1000000 == 0:
            print('tree size: %8d nodes' % count)

    tuple_list = [node_to_tuple(node) for node in tree]

    print('creating dat file')
    create_dat_file(tuple_list, paths['kdtree'], dtypes['kdtree'])


if __name__ == '__main__':
    print('ACTIVATING REVERSE FUNCTIONALITY')
    create_kdtree_table()
    print('DONE')
