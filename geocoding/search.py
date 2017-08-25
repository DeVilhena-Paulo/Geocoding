# -*- coding: utf-8 -*-
"""Definition of the search methods.

This module defines the logic of the two most relevant methods of this package:
the position method and the reverse method.
"""
from . import normalize
from . import query
from . import result


def preprocessing(code_postal, commune, adresse):
    """First processing of the input from the position method.

    Convert postal code to int, normalize the city name and separate number
    and street from adresse.

    Args:
        code_postal (str): The postal code.
        commune (str): The city name.
        adresse(str): Address with number and street name.

    Returns:
        (:obj:`tuple`)
        (code_postal (int): The postal code,
         commune (str): The city name normalized,
         numero (int): The street number,
         voie (str): The street name)

    """
    # Try to convert postal code to int.
    if isinstance(code_postal, str):
        try:
            code_postal = int(code_postal)
        except ValueError:
            code_postal = None
    else:
        code_postal = None

    # Normalize city.
    if isinstance(commune, str):
        commune = normalize.uniform_commune(commune)
    else:
        commune = None

    # Retrieve the number and street from address and normalize street name.
    numero, voie, voie_type = None, None, None
    if isinstance(adresse, str):
        numero, voie, voie_type = normalize.mine(adresse)

    return code_postal, commune, numero, voie, voie_type


def position(code_postal=None, commune=None, adresse=None):
    """Find the position over the surface of the Earth of the given address.

    Args:
        code_postal (str): The postal code.
        commune (str): The city name.
        adresse(str): Address with number and street name.

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

    Example:
        >>> from geocoding import search
        >>> search.position('91120', 'Palaiseau', '12, Bd des Maréchaux')

    """
    query.setup()

    # Input preprocessing.
    code_postal, commune, numero, voie, voie_type = \
        preprocessing(code_postal, commune, adresse)

    # Try to find postal code.
    postal_id = query.select_code_postal(code_postal)

    # Try to find city.
    commune_id = query.select_commune(postal_id, commune)
    if commune_id is None:
        commune_id = query.complete_commune_selection(commune)

    # Try to find street.
    voie_id = query.select_voie(commune_id, voie, voie_type)
    if voie_id is None:
        voie_id = query.complete_voie_selection(code_postal, commune, voie)

    # Try to find number.
    localisation_id = query.select_localisation(voie_id, numero)

    # Prepare the output.
    if localisation_id is not None:
        # Quality = 1 -> The search was successful.
        status, quality = ('localisation', localisation_id), 1

    elif voie_id is not None:
        status = ('voie', voie_id)
        # Quality = 2 -> The precise number was not found.
        # Quality = 3 -> The precise number was not found and there was no
        #                number in the input.
        quality = 3 if numero is None else 2

    elif commune_id is not None:
        # Quality = 4 -> The street was not found.
        status, quality = ('commune', commune_id), 4

    elif postal_id is not None:
        # Quality = 5 -> The commune was not found.
        status, quality = ('postal', postal_id), 5

    else:
        # Quality = 6 -> Nothing was found.
        status, quality = None, 6

    return result.get_output(status, quality)


def reverse(position):
    """Finds the nearest address in France to a given position over the Earth.

    Args:
        position (:obj:`tuple` of float): Longitude and latitude of the in this
            order.

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

    Example:
        >>> from geocoding import search
        >>> search.reverse((2.21, 48))

    """
    query.setup()

    if position is None:
        return result.get_output(None, 6)
    node_id, dist = query.nearest_point_from(position)

    # Get the reference id for the address.
    localisation_id = query.data['kdtree']['ref_id'][node_id]
    return result.get_output(('localisation', localisation_id), 1)
