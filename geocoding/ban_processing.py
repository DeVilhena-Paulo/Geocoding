# -*- coding: utf-8 -*-
import numpy as np
from sortedcontainers import SortedDict, SortedSet

from .utils import degree_to_int
from . import normalize as norm


line_specs = {
    "nom_voie": 7,
    "numero": 5,
    "repetition": 6,
    "code_insee": 10,
    "code_postal": 8,
    "longitude": 14,
    "latitude": 15,
    "nom_commune": 9,
    "nom_complementaire": 11
}

types = {
    "code_postal": int,
    "numero": int,
    "longitude": float,
    "latitude": float
}

voie_fields = ['nom_voie']

commune_fields = ['nom_complementaire', 'nom_commune']

fields_length = 19


def test(fields):
    if len(fields) != fields_length:
        return False

    for field in types:
        try:
            types[field](fields[line_specs[field]])
        except ValueError:
            return False
    return True


def get_field(field_name, fields, normalization_method, size_limit=None):
    text = fields[line_specs[field_name]].replace('"', '')
    normalise = normalization_method(text)
    if len(normalise) > 0:
        nom = norm.remove_separators(norm.uniform(text))
        if size_limit is None or len(nom) <= size_limit:
            return nom, normalise
    return None, None


def get_voie(fields):
    for field_name in voie_fields:
        voie_nom, voie_normalise = get_field(field_name, fields,
                                             norm.uniform_adresse, 47)
        if voie_nom is not None:
            return voie_nom, voie_normalise
    return None, None


def get_commune(fields):
    for field_name in commune_fields:
        commune_nom, commune_normalise = get_field(field_name, fields, norm.uniform_commune)
        if commune_nom is not None:
            return commune_nom, commune_normalise
    return None, None


def get_attributes(fields):
    if not test(fields):
        return None

    commune_nom, commune_normalise = get_commune(fields)
    if commune_nom is None:
        return None

    voie_nom, voie_normalise = get_voie(fields)
    if voie_nom is None:
        return None

    code_insee = fields[line_specs['code_insee']]
    code_postal = int(fields[line_specs['code_postal']])

    numero = int(fields[line_specs['numero']])
    repetition = fields[line_specs['repetition']].replace('"', '')
    lon = degree_to_int(fields[line_specs['longitude']])
    lat = degree_to_int(fields[line_specs['latitude']])

    return (code_postal, commune_normalise, commune_nom, code_insee,
            voie_normalise, voie_nom, numero, repetition, lon, lat)


def update(dpt_nom, csv_file, processed_files):
    postal_dict = SortedDict()

    next(csv_file)
    for line in csv_file:
        attributes = get_attributes(line.strip().split(';'))
        if attributes is None:
            continue
        postal_key = attributes[:1]
        commune_key = attributes[1: 4]
        voie_key = attributes[4: 6]
        localisation = attributes[6:]

        if postal_key not in postal_dict:
            postal_dict[postal_key] = SortedDict()

        commune_dict = postal_dict[postal_key]
        if commune_key not in commune_dict:
            commune_dict[commune_key] = SortedDict()

        voie_dict = commune_dict[commune_key]
        if voie_key not in voie_dict:
            voie_dict[voie_key] = SortedSet()

        voie_dict[voie_key].add(localisation)

    update_departement(dpt_nom, processed_files, postal_dict)


def update_departement(dpt_nom, processed_files, postal_dict):
    current_id = len(processed_files['departement'])

    start = len(processed_files['postal'])
    update_postal(current_id, processed_files, postal_dict)
    end = len(processed_files['postal'])

    processed_files['departement'].append((dpt_nom, start, end))


def update_postal(id_ref, processed_files, postal_dict):
    for key in postal_dict.keys():
        current_id = len(processed_files['postal'])

        start = len(processed_files['commune'])
        update_commune(current_id, processed_files, postal_dict[key])
        end = len(processed_files['commune'])

        tuple_value = key + (start, end, id_ref)
        processed_files['postal'].append(tuple_value)


def update_commune(id_ref, processed_files, commune_dict):
    for key in commune_dict.keys():
        current_id = len(processed_files['commune'])

        start = len(processed_files['voie'])
        update_voie(current_id, processed_files, commune_dict[key])
        end = len(processed_files['voie'])

        localisation_list = [value for k, value in commune_dict[key].items()]
        lon, lat = tuple_list_mean(localisation_list, range(2))

        tuple_value = key + (lon, lat, start, end, id_ref)
        processed_files['commune'].append(tuple_value)


def update_voie(id_ref, processed_files, voie_dict):
    for key in voie_dict.keys():
        current_id = len(processed_files['voie'])

        start = len(processed_files['localisation'])
        update_localisation(current_id, processed_files, voie_dict[key])
        lon, lat = tuple_list_mean(voie_dict[key], range(2, 4))

        end = len(processed_files['localisation'])

        tuple_value = key + (lon, lat, start, end, id_ref)
        processed_files['voie'].append(tuple_value)

        # Gambiarra - não me orgulho disso
        voie_dict[key] = (lon, lat)


def update_localisation(id_ref, processed_files, localisation_set):
    for localisation in localisation_set:
        tuple_value = localisation + (id_ref, )
        processed_files['localisation'].append(tuple_value)


def tuple_list_mean(tuple_list, indices):
    return (int(np.mean([int(value[index]) for value in tuple_list]))
            for index in indices)
