# -*- coding: utf-8 -*-

import os
from .datapaths import here

url = 'https://adresse.data.gouv.fr/data/BAN_licence_gratuite_repartage.zip'
raw_data = os.path.join(here, 'raw')
ban_zip = os.path.join(raw_data, 'ban.zip')
