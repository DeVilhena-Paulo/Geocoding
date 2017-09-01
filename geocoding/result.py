# -*- coding: utf-8 -*-
"""Creation of the output for the search methods.

Attributes:
    tables (:obj:`list` of :obj:`str`): The name of the tables containing
        useful information to include in the output.
    output_specs (:obj:`dict` of :obj:`list` of :obj:`str`): The fields of each
        table that we want to include in the output.

"""
from . import query
from .utils import int_to_degree

tables = ['departement', 'postal', 'commune', 'voie', 'localisation']
output_specs = {
    'departement': ['code'],
    'postal': ['code'],
    'commune': ['nom', 'code_insee'],
    'voie': ['nom'],
    'localisation': ['numero']
}


def get_table_ids(status):
    """Given the index of an element in one of the tables, it finds the index
    of all the referenced items in the other tables.

    Args:
        status (:obj:`tuple`): The first element is the name of a table and the
            second is the index of an element in this table.

    Returns:
        :obj:`dict`
        {
            'departement': (int): The index of the departement.
            'postal': (int): The index of the postal code.
            'commune': (int): The index of the city.
            'voie': (int): The index of the street.
            'localisation': (int): The index of the street number.
        }

    """
    table_ids = {}
    table, element_id = status
    table_ids[table] = element_id
    for i in range(tables.index(table), 0, -1):
        element_id = query.data[table]['ref_id'][element_id]
        table = tables[i - 1]
        table_ids[table] = element_id
    return table_ids


def get_output(status, quality):
    """Get the information required from each table to build the output.

    Args:
        status (:obj:`tuple`): The first element is the name of a table and the
            second is the index of an element in this table.
        quality (int): The quality of the search result.

    Returns:
        :obj:`dict`
        {
            'departement': {
                'code' (str): The code of the departement
            },
            'postal': {
                'code' (int): The postal code
            },
            'commune': {
                'nom' (str): The city name,
                'code_insee' (str): The code_insee of the city
            },
            'voie': {
                'nom' (str): The street name,
            },
            'localisation': {
                'numero' (str): The street number,
            },
            'longitude' (float): Longitude coordinate,
            'latitude' (float): Latitude coordinate,
            'quality' (int): The quality of the result
        }

    """
    output = {}
    for table in output_specs:
        output[table] = {field: None for field in output_specs[table]}
    output['longitude'] = None
    output['latitude'] = None
    output['quality'] = quality

    if status is None:
        return output

    # Get the index of the other tables
    table_ids = get_table_ids(status)
    table, element_id = status

    # Get the coordinates of the address in the right format
    if quality < 5:
        element = query.data[table][element_id]
        output['longitude'] = int_to_degree(element['longitude'])
        output['latitude'] = int_to_degree(element['latitude'])

    # Get the required information
    for table in output_specs:
        if table in table_ids:
            record = query.data[table][table_ids[table]]
            fields = output_specs[table]
            info = {field: record[field].item() for field in fields}
            output[table] = info

    output['quality'] = quality
    return output
