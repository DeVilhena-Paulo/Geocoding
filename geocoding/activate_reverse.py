import gc
import numpy as np

from kdquery import Tree

from .index import create_dat_file
from .datatypes import dtypes
from .datapaths import paths
from .utils import pre_order, degree_to_int
from .download import completion_bar


def node_to_tuple(node):
    left = node.left if node.left is not None else -1
    right = node.right if node.right is not None else -1

    return node.point + tuple(node.region[0]) + tuple(node.region[1]) + \
        (node.axis, left, right, node.data)


def create_kdtree():
    table = np.memmap(paths['localisation'], dtype=dtypes['localisation'])
    size = len(table)
    indices = np.argsort(table, order='longitude').astype('int32')

    limits = [[degree_to_int(-62), degree_to_int(55)],
              [degree_to_int(-22), degree_to_int(52)]]

    tree = Tree(2, size, limits)

    count, n_total = 0, size
    for i in pre_order(size):
        index = indices[i]
        loc = table[index]
        tree.insert((loc['longitude'], loc['latitude']), index)

        count += 1
        if count % 30000 == 0 or count == n_total:
            completion_bar('Loading kd-tree', (count / n_total))

    print('\nStoring ...')

    tuple_list = [node_to_tuple(node) for node in tree]

    del tree
    gc.collect()

    create_dat_file(tuple_list, paths['kdtree'], dtypes['kdtree'])

    return True
