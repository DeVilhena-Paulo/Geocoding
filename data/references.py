# -*- coding: utf-8 -*-
"""Main directory references as attributes and statement.

This module has all the the useful directory names and paths as attributes
and/or statements. It serves as a easy way to reference the directories
involved with the data manipulation.

"""

import os

here = os.path.abspath(os.path.dirname(__file__))

raw_data = os.path.join(here, 'raw')

processed_data = os.path.join(here, 'processed')

url = 'https://adresse.data.gouv.fr/data/BAN_licence_gratuite_repartage.zip'

ban_zip = os.path.join(raw_data, 'ban.zip')

tables = ['departement', 'commune', 'postal', 'voie', 'localisation']

csv_paths = {table: os.path.join(processed_data, table + '.csv')
             for table in tables}
