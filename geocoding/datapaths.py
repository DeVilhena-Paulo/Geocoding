"""Path to the database files.

Attributes:
    here (str): Path to the package.
    database (str): Path to the database folder.
    tables (:obj:`list` of :obj:`str`): The name of each table in the database.
    paths (:obj:`list` of :obj:`str`): The path to each table of the database.
"""

import os

here = os.path.abspath(os.path.dirname(__file__))

database = os.path.join(here, 'database')

tables = ['departement', 'postal', 'commune', 'voie', 'localisation',
          'commune_index', 'postal_index', 'voie_index', 'kdtree']
paths = {table: os.path.join(database, table + '.dat') for table in tables}
