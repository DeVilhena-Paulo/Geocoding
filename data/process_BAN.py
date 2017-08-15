# -*- coding: utf-8 -*-
import numpy as np

import context
from geocoding.utils import degree_to_int
from geocoding import normalize as norm


line_specs = {
    "nom_voie": 1,
    "numero": 3,
    "repetition": 4,
    "code_insee": 5,
    "code_postal": 6,
    "nom_ld": 8,
    "nom_afnor": 9,
    "acheminement": 10,
    "longitude": 13,
    "latitude": 14,
    "nom_commune": 15
}

limits = {
    "code_postal": 5,
    "code_insee": 5,
    "nom_ld": 50,
    "nom_afnor": 50,
    "nom_voie": 50,
    "acheminement": 45
}
limits = {}

types = {
    "numero": int,
    "code_postal": int,
    "longitude": float,
    "latitude": float
}

n_fields = 16

skip_count = {'lines': 0, 'streets': 0, 'cities': 0}


class LineProcessor:

    def __init__(self):
        self.fields = {}
        self.size = 0

    def update(self, line):
        splited_line = norm.uniform(line).split(';')
        self.size = len(splited_line)
        if self.size == n_fields:
            for spec in line_specs:
                self.fields[spec] = splited_line[line_specs[spec]]

    def test(self):
        """Test the coherence of a line from a departement csv file.
        """
        def limit_test(word, limit):
            return len(word) <= limit

        def type_test(word, typ):
            try:
                typ(word)
                return True
            except ValueError:
                return False

        result = (self.size == n_fields)
        for field in limits:
            result &= limit_test(self.fields[field], limits[field])
        for field in types:
            result &= type_test(self.fields[field], types[field])
        return result


class FileProcessor:

    def __init__(self, files):
        self.lineProc = LineProcessor()
        self.files = files
        self.line = {file: 0 for file in files}

    def update_dictionary(self, dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = value
            return True
        return False

    def process(self, in_file, departement):
        self.dictionary = {}
        self.departement = departement

        for key in skip_count:
            skip_count[key] = 0

        next(in_file)
        for line in in_file:
            self.lineProc.update(line)

            if not self.lineProc.test():
                skip_count['lines'] += 1
                continue

            self.process_line()

        self.write_departement()

        for key, value in skip_count.items():
            print("number of skkiped %s: %d" % (key, value))

    def get_voie(self):
        nom_voie = norm.uniform_adresse(self.lineProc.fields['nom_voie'])
        nom_ld = norm.uniform_adresse(self.lineProc.fields['nom_ld'])
        nom_afnor = norm.uniform_adresse(self.lineProc.fields['nom_afnor'])

        voie, voie_norm = None, None
        if len(nom_afnor) > 0 and len(nom_afnor) <= 47:
            voie = norm.remove_separators(self.lineProc.fields['nom_afnor'])
            voie_norm = nom_afnor
        elif len(nom_voie) > 0 and len(nom_voie) <= 47:
            voie = norm.remove_separators(self.lineProc.fields['nom_voie'])
            voie_norm = nom_voie
        elif len(nom_ld) > 0 and len(nom_ld) <= 47:
            voie = norm.remove_separators(self.lineProc.fields['nom_ld'])
            voie_norm = nom_ld

        return voie, voie_norm

    def get_commune(self):
        acheminement = \
            norm.uniform_commune(self.lineProc.fields['acheminement'])
        nom_commune = norm.uniform_commune(self.lineProc.fields['nom_commune'])

        comm, comm_norm = None, None
        if len(acheminement) > 0:
            comm = norm.remove_separators(self.lineProc.fields['acheminement'])
            comm_norm = acheminement
        elif len(nom_commune) > 0:
            comm = norm.remove_separators(self.lineProc.fields['nom_commune'])
            comm_norm = nom_commune

        return comm, comm_norm

    def get_localisation(self):
        numero = int(self.lineProc.fields['numero'])
        repetition = self.lineProc.fields['repetition'].replace('"', '')
        lon = degree_to_int(self.lineProc.fields['longitude'])
        lat = degree_to_int(self.lineProc.fields['latitude'])

        return numero, repetition, lon, lat

    def process_line(self):
        code_insee = self.lineProc.fields['code_insee']
        code_postal = int(self.lineProc.fields['code_postal'])

        commune, commune_norm = self.get_commune()
        voie, voie_norm = self.get_voie()
        numero, repetition, lon, lat = self.get_localisation()

        postal_key = (code_postal, )
        postal_dict = self.dictionary
        if postal_key not in postal_dict:
            postal_dict[postal_key] = dict()

        if commune is None:
            skip_count['cities'] += 1
            return

        commune_key = (commune_norm, commune, code_insee)
        commune_dict = postal_dict[postal_key]
        if commune_key not in commune_dict:
            commune_dict[commune_key] = dict()

        if voie is None:
            skip_count['streets'] += 1
            return

        voie_key = (voie_norm, voie)
        voie_dict = commune_dict[commune_key]
        if voie_key not in voie_dict:
            voie_dict[voie_key] = list()

        voie_dict[voie_key].append((numero, repetition, lon, lat))

    def write_line(self, table, tuple_value):
        line = ';'.join([str(value) for value in tuple_value]) + '\n'
        self.files[table].write(line)
        self.line[table] += 1

    def write_departement(self):
        current_id = self.line['departement']

        start = self.line['postal']
        self.write_postal(current_id, self.dictionary)
        end = self.line['postal']

        # write departement
        self.write_line('departement', (self.departement, start, end))

    def write_postal(self, id_ref, dictionary):
        sorted_keys = list(dictionary.keys())
        if not sorted_keys:
            return

        sorted_keys.sort()
        for key in sorted_keys:
            current_id = self.line['postal']

            start = self.line['commune']
            self.write_commune(current_id, dictionary[key])
            end = self.line['commune']

            # write line
            tuple_value = key + (start, end, id_ref)
            self.write_line('postal', tuple_value)

    def write_commune(self, id_ref, dictionary):
        sorted_keys = list(dictionary.keys())
        if not sorted_keys:
            return

        sorted_keys.sort()
        for key in sorted_keys:
            current_id = self.line['commune']

            start = self.line['voie']
            self.write_voie(current_id, dictionary[key])
            end = self.line['voie']

            localisation_list = [value for k, value in dictionary[key].items()]
            lon = self.compute_mean(localisation_list, 0)
            lat = self.compute_mean(localisation_list, 1)

            # write line
            tuple_value = key + (lon, lat, start, end, id_ref)
            self.write_line('commune', tuple_value)

    def write_voie(self, id_ref, dictionary):
        sorted_keys = list(dictionary.keys())
        if not sorted_keys:
            return

        sorted_keys.sort()
        for key in sorted_keys:
            current_id = self.line['voie']

            start = self.line['localisation']
            self.write_localisation(current_id, dictionary[key])
            lon = self.compute_mean(dictionary[key], 2)
            lat = self.compute_mean(dictionary[key], 3)

            end = self.line['localisation']

            # write line
            tuple_value = key + (lon, lat, start, end, id_ref)
            self.write_line('voie', tuple_value)

            dictionary[key] = (lon, lat)

    def write_localisation(self, id_ref, lst):
        lst.sort()
        for key in lst:
            # write tuple
            self.write_line('localisation', key + (id_ref, ))

    def compute_mean(self, lst, index):
        return int(np.mean([int(tuple_value[index]) for tuple_value in lst]))
