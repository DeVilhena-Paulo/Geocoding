# -*- coding: utf-8 -*-
"""Processing of raw data.

This module creates an intermediary database in csv format. The goal of this
intermediate step is to easy the next step: the construction of the binary
files using tools from the package numpy.

"""

import os

from references import csv_paths, raw_data, processed_data
from process_BAN import FileProcessor


def process_csv_files():
    if not os.path.exists(processed_data):
        os.mkdir(processed_data)

    with open(csv_paths['departement'], 'w', encoding='UTF-8') as dpt_file, \
            open(csv_paths['commune'], 'w', encoding='UTF-8') as commune_file,\
            open(csv_paths['postal'], 'w', encoding='UTF-8') as postal_file, \
            open(csv_paths['voie'], 'w', encoding='UTF-8') as voie_file, \
            open(csv_paths['localisation'], 'w', encoding='UTF-8') as \
            localisation_file:

        csv_files = {
            'departement': dpt_file,
            'commune': commune_file,
            'postal': postal_file,
            'voie': voie_file,
            'localisation': localisation_file
        }

        fileProc = FileProcessor(csv_files)

        for (dirname, dirs, files) in os.walk(raw_data):
            for filename in files:
                if filename.endswith('.csv'):
                    file_path = os.path.join(dirname, filename)
                    departement = filename.split('_')[-1].split('.')[0]

                    print('\nProcessing departement %s' % departement)

                    in_file = open(file_path, 'r', encoding='UTF-8')
                    fileProc.process(in_file, departement)


if __name__ == '__main__':
    print('PROCESSING BAN FILES')
    process_csv_files()
    print("DONE")
