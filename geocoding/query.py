# -*- coding: utf-8 -*-
"""Interface to query for data.

This module defines the query methods for each table in the database.

Attributes:
    data (:obj:`dict` of :obj:`numpy.ndarray`): The database is formed by numpy
        arrays. Each of them is identified by a name and accessible by this
        dictionary with data[name].
    limits (:obj:`dict` of :obj:`tuple` of int): limits[table] stores the
        limits of the numpy array called table.

"""
import os
import numpy as np
import kdquery

from . import utils
from . import distance
from .similarity import Similarity
from .datatypes import dtypes
from .datapaths import paths

data = {}
limits = {}


def setup():
    """Initialize the module level variables.
    """
    if not data or not limits:
        for table in paths:
            if os.path.isfile(paths[table]):
                data[table] = np.memmap(paths[table], dtypes[table])
                limits[table] = (0, len(data[table]))


def select(table, column, start, end, element):
    """Search for a record on table with field column equals to element.

    Args:
        table (str): The name of the numpy array.
        column (str): The field to consider.
        start (int): The bottom limit index to look in the table.
        end (int): The top limit index to look in the table.
        element (str or int): The element to search for.

    Returns:
        (:obj:`tuple`)
        (pos (int): the position of the record in the table,
         found (bool): true if the search was succeeded)

    """
    # Binary search
    i, pos = utils.search(element, (start, end), data[table][column])
    found = (pos < end and data[table][column][pos] == element)
    return pos, found


def heuristics(table, column, narrow, wide, element):
    """Search record on table with field column the most similar to element.

    Args:
        table (str): The name of the numpy array.
        column (str): The field to consider.
        narrow (:obj:`tuple`): Tuple of length 3 with setting for the narrow
            search.
            first element (int): The bottom limit index to look in the table in
                the narrow search.
            second element (int): The top limit index to look in the table in
                the narrow search.
            third element (float): The threshold for the similarity score in
                the narrow search.
        wide (:obj:`tuple`): Tuple of length 3 with setting for the wide
            search (when the narrow is not successful).
            first element (int): The bottom limit index to look in the table in
                the wide search.
            second element (int): The top limit index to look in the table in
                the wide search.
            third element (float): The threshold for the similarity score in
                the wide search.
        element (str): The element to search for.

    Returns:
        (:obj:`tuple`)
        (element_id (int): the position of the record in the table,
         found (bool): true if the search was succeeded)

    """
    # Similarity function
    similarity = Similarity(element).score

    # Narrow search
    indices = range(narrow[0], narrow[1])
    score, rang, element_id = \
        utils.most_similar(indices, data[table][column], similarity)
    found = (score is not None and score >= narrow[2])

    # Wide search
    if not found and wide is not None:
        indices = range(wide[0], wide[1])
        score, rang, element_id = \
            utils.most_similar(indices, data[table][column], similarity)
        found = (score is not None and score >= wide[2])

    return element_id, found


def select_departement(dpt_code):
    """Select record on department table with field code equals to dpt_code.

    Args:
        dpt_code (str): The code of the department.

    Returns:
        dpt_id (int): The index of the record if the search was succeeded,
            None otherwise.

    """
    if dpt_code is None or len(dpt_code) != 2:
        return None
    start, end = limits['departement']
    dpt_id, found = select('departement', 'code', start, end, dpt_code)
    return dpt_id if found else None


def select_code_postal(code_postal):
    """Select record on postal table with field code equals to code_postal.

    Args:
        code_postal (int): The postal code.

    Returns:
        postal_id (int): The index of the record if the search was succeeded,
            None otherwise.

    """
    if code_postal is None:
        return None

    # Binary search with index list, because the postal table is not
    # entirely sorted.
    i, postal_id = utils.search(code_postal, data['postal_index'],
                                data['postal']['code'], sorted=False)
    start, end = limits['postal_index']
    found = (i < end and data['postal']['code'][postal_id] == code_postal)

    if not found:
        # Compute the difference to the nearest values from code_postal
        diff = [(abs(data['postal']['code'][j] - code_postal), j)
                for j in range(max(i - 1, start), min(i + 1, end))]
        min_value = min(diff)
        postal_id = min_value[1]
        found = (min_value[0] <= 5)

    return postal_id if found else None


def select_commune(postal_id, commune):
    """Select record on commune table with field normalize equals to commune or
    sufficiently similar.

    Args:
        postal_id (int): The index of the code postal that commune belongs to.
        commune (str): The city name.

    Returns:
        commune_id (int): The index of the record if the search was succeeded,
            None otherwise.

    """
    if postal_id is None or commune is None:
        return None

    # Binary search
    ref_element = data['postal'][postal_id]
    start, end = ref_element['start'], ref_element['end']
    commune_id, found = select('commune', 'normalise', start, end, commune)

    # Heuristics search with string similarity
    if not found:
        narrow = (max(start, commune_id - 2), min(end, commune_id + 2), 0.7)
        wide = (start, end, 0.5)
        commune_id, found = heuristics('commune', 'normalise', narrow, wide,
                                       commune)

    return commune_id if found else None


def complete_commune_selection(commune):
    """Select record on commune table with field normalize the most similar to
    commune.

    Search for commune in the entire commune table. This method is the
    option to find the commune once the method select_commune has failed.

    Args:
        commune (str): The city name.

    Returns:
        commune_id (int): The index of the record if the search was succeeded,
            None otherwise.

    """
    if commune is None:
        return None

    # Binary search with index list, because the commune table is not
    # entirely sorted.
    i, commune_id = utils.search(commune, data['commune_index'],
                                 data['commune']['normalise'],
                                 sorted=False)
    found = (data['commune']['normalise'][commune_id] == commune)

    # Heuristics
    if not found:
        start, end = limits['commune_index']
        similarity = Similarity(commune).score
        indices = data['commune_index'][max(start, i - 2): min(end, i + 2)]
        score, rang, commune_id = \
            utils.most_similar(indices, data['commune']['normalise'],
                               similarity)
        found = (score is not None and score >= 0.7)

    return commune_id if found else None


def select_voie(commune_id, voie, voie_type):
    """Select record on voie table with field normalize equals to voie or
    sufficiently similar.

    Args:
        commune_id (int): The index of the commune that the street belongs to.
        voie (str): The street name.

    Returns:
        voie_id (int): The index of the record if the search was succeeded,
            None otherwise.

    """
    if commune_id is None or voie is None:
        return None

    # Binary search
    ref_element = data['commune'][commune_id]
    start, end = ref_element['start'], ref_element['end']
    voie_id, found = select('voie', 'normalise', start, end, voie)

    # Heuristics
    if not found:
        start_type, end_type = voie_id - 1, voie_id
        if voie_type is not None:
            while data['voie']['normalise'][start_type].startswith(voie_type):
                start_type -= 1
            start_type += 1
            while data['voie']['normalise'][end_type].startswith(voie_type):
                end_type += 1

        if end_type - start_type > 1:
            narrow_start, narrow_end = start_type, end_type
        else:
            narrow_start = max(start, voie_id - 3)
            narrow_end = min(end, voie_id + 3)

        narrow = (narrow_start, narrow_end, 0.6)
        wide = (start, end, 0.4)

        voie_id, found = heuristics('voie', 'normalise', narrow, wide, voie)

    return voie_id if found else None


def complete_voie_selection(code_postal, commune, voie):
    """Select record on voie table with field normalise most similar to voie.

    Search for voie in the entire voie table. This method is the option to find
    the voie once the method select_voie has failed. It first tries to find the
    voie belonging to the commune the most similar to commune and if this step
    fails it will try to find the voie belonging to a postal code similar to
    code_postal.

    Args:
        commune (str): The city name.

    Returns:
        commune_id (int): The index of the record if the search was succeeded,
            None otherwise.

    """
    if voie is None:
        return None

    # Binary search
    i, voie_id = utils.search(voie, data['voie_index'],
                              data['voie']['normalise'],
                              sorted=False)

    # If the search was successful and there is no code_postal or commune
    # to continue, we finish.
    if code_postal is None and commune is None:
        return voie_id if data['voie']['normalise'][voie_id] == voie else None

    # Indices of voie table to consider in the heuristics step
    if data['voie']['normalise'][voie_id] == voie:
        # If the search was successful, find the greatest interval of equality
        j = i
        while data['voie']['normalise'][data['voie_index'][j]] == voie:
            j += 1
        voie_indices = data['voie_index'][i: j]
    else:
        # If the search wasn't successful, pick some near indices from the
        # search result
        start, end = limits['voie_index']
        voie_indices = data['voie_index'][max(start, i - 2): min(end, i + 2)]

    commune_indices = [data['voie']['ref_id'][index] for index in voie_indices]

    # First heuristics: apply similarity to commune
    if commune is not None:
        similarity = Similarity(commune).score
        score, rang, commune_id = \
            utils.most_similar(commune_indices, data['commune']['normalise'],
                               similarity)
        voie_id = voie_indices[rang]
        if score is not None and score >= 0.7:
            return voie_id

    # Second heuristics: consider the postal code
    if code_postal is not None:
        postal_indices = [data['commune']['ref_id'][commune_id]
                          for commune_id in commune_indices]
        first_algs = code_postal // 1000
        for i in range(len(postal_indices)):
            if first_algs == data['postal']['code'][postal_indices[i]] // 1000:
                return voie_indices[i]

    return None


def select_localisation(voie_id, numero):
    """Select record on localisation table with field numero equals to numero.

    Args:
        voie_id (int): The index of the street that the numero belongs to.
        numero (int): The street number.

    Returns:
        localisation_id (int): The index of the record if the search was
            succeeded, None otherwise.

    """
    if voie_id is None or numero is None:
        return None

    # Binary search
    ref_element = data['voie'][voie_id]
    start, end = ref_element['start'], ref_element['end']
    localisation_id, found = select('localisation', 'numero', start, end,
                                    numero)
    return localisation_id if found else None


def get_properties(node_id):
    """Auxiliary method to the nearest_point method from kdquery package.

    Args:
        node_id (int): Index of a node in the internal representation of the
            kd-tree using a numpy array.

    Returns:
        (:obj:`tuple`)
        (point (:obj:`tuple` of float): Longitude and latitude of the node,
         region (:ob:`list` of :obj:`list` of float): The region of the Earth`s
             surface that the node belongs to,
         dimension (int): The dimension of the surface divided by this node,
         active (bool): True if the node will be consider in the computation of
             the nearest point,
         left (int): Index to left child,
         right (int): Index to right child)

    """
    table_node = data['kdtree'][node_id]

    limit_left = utils.int_to_degree(table_node['limit_left'])
    limit_right = utils.int_to_degree(table_node['limit_left'])
    limit_bottom = utils.int_to_degree(table_node['limit_bottom'])
    limit_top = utils.int_to_degree(table_node['limit_top'])

    # The region of the space defined by the node
    region = [[limit_left, limit_right], [limit_bottom, limit_top]]

    # The position of the point in the space
    point = (utils.int_to_degree(table_node['longitude']),
             utils.int_to_degree(table_node['latitude']))

    # The dimension divided by this node
    dimension = table_node['dimension']

    # Indices to left and right children
    left = table_node['left'] if table_node['left'] != -1 else None
    right = table_node['right'] if table_node['right'] != -1 else None

    return point, region, dimension, True, left, right


def nearest_point_from(query):
    """Find the nearest node in the internal kd-tree to a given query.

    Args:
        query (:obj:`tuple` of float): Longitude and latitude of the position
            in this order.

    Returns:
        (:obj:`tuple`)
        (node_id (int): Index of the nearest node in the internal kd-tree,
         dist (float): The distance between the query and the nearest node)

    """
    return kdquery.nearest_point(query, 0, get_properties, distance.spherical)
