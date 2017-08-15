# -*- coding: utf-8 -*-
"""Type of the elements in each table of the database.

The database is formed by numpy arrays and the type of the elements of each one
is specified in this module as a module level variable.

Attributes:
    departement_dtype (str): The definition of the numpy dtype for the
        elements of the departement table.
    postal_dtype (str): The definition of the numpy dtype for the elements of
        the postal table.
    commune_dtype (str): The definition of the numpy dtype for the elements of
        the commune table.
    voie_dtype (str): The definition of the numpy dtype for the elements of
        the voie table.
    localisation_dtype (str): The definition of the numpy dtype for the
        elements of the localisation table.
    kdtree_dtype (str): The definition of the numpy dtype for the elements of
        the kdtree table.
    dtypes (:obj:`dict` of :obj:`str`): A python dictionary to easily access
        the dtypes definitions.

"""

import numpy as np

departement_dtype = np.dtype([
    ('code', 'U3'),
    ('start', 'int32'),
    ('end', 'int32'),
])

postal_dtype = np.dtype([
    ('code', 'int32'),
    ('start', 'int32'),
    ('end', 'int32'),
    ('ref_id', 'int32'),
])

commune_dtype = np.dtype([
    ('normalise', 'U32'),
    ('nom', 'U32'),
    ('code_insee', 'U5'),
    ('longitude', 'int32'),
    ('latitude', 'int32'),
    ('start', 'int32'),
    ('end', 'int32'),
    ('ref_id', 'int32'),
])

voie_dtype = np.dtype([
    ('normalise', 'U47'),
    ('nom', 'U65'),
    ('longitude', 'int32'),
    ('latitude', 'int32'),
    ('start', 'int32'),
    ('end', 'int32'),
    ('ref_id', 'int32'),
])

localisation_dtype = np.dtype([
    ('numero', 'int16'),
    ('repetition', 'U3'),
    ('longitude', 'int32'),
    ('latitude', 'int32'),
    ('ref_id', 'int32'),
])

kdtree_dtype = np.dtype([
    ('longitude', 'int32'),
    ('latitude', 'int32'),
    ('limit_left', 'int32'),
    ('limit_right', 'int32'),
    ('limit_bottom', 'int32'),
    ('limit_top', 'int32'),
    ('dimension', 'int8'),
    ('left', 'int32'),
    ('right', 'int32'),
    ('ref_id', 'int32'),
])

dtypes = {
    'departement': departement_dtype,
    'postal': postal_dtype,
    'commune': commune_dtype,
    'voie': voie_dtype,
    'localisation': localisation_dtype,
    'commune_index': 'int32',
    'postal_index': 'int32',
    'voie_index': 'int32',
    'kdtree': kdtree_dtype
}
