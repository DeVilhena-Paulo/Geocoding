# -*- coding: utf-8 -*-
"""Normalization methods the database and the input of the search.

Attributes:
    dicitionary (dict of str): Dictionary of common abbreviations in French
        search queries.
    voie_type_1 (set of str): Set of common types of street with one word in
        France.
    voie_type_2 (set of str): Set of common types of street with two word in
        France.
    meanless_words (set of str): Set of words in French that does not contain
        information to distinguish one address from another.

"""
import re
from unidecode import unidecode


dictionary = {
    "ALL": "ALLEE",
    "AV": "AVENUE",
    "BD": "BOULEVARD",
    "CH": "CHEMIN",
    "CHE": "CHEMIN",
    "CRS": "COURS",
    "CTRE": "CENTRE",
    "DOM": "DOMAINE",
    "HAM": "HAMEAU",
    "IMP": "IMPASSE",
    "LD": "LIEUDIT",
    "LOT": "LOTISSEMENT",
    "LT": "LIEUTENANT",
    "PAS": "PASSAGE",
    "PDT": "PRESIDENT",
    "PL": "PLACE",
    "QU": "QUAI",
    "QUA": "QUARTIER",
    "RLE": "RUELLE",
    "RES": "RESIDENCE",
    "RPT": "RONDPOINT",
    "RTE": "ROUTE",
    "SQ": "SQUARE",
    "ST": "SAINT",
    "STE": "SAINTE",
    "TRA": "TRAVERSE",
    "VLGE": "VILLAGE"
}

voie_type_1 = set(["ALLEE", "AVENUE", "BOULEVARD", "CITE", "CHEMIN", "CENTRE",
                   "CLOS", "COURS", "DOMAINE", "GALERIE", "HAMEAU", "HLM",
                   "IMPASSE", "LIEUDIT", "LOTISSEMENT", "MAIL", "QUAI",
                   "QUARTIER", "PASSAGE", "PLACE", "RONDPOINT",
                   "ROUTE", "RUE", "RUELLE", "SQUARE", "TRAVERSE", "VOIE",
                   "VILLAGE", "ZONE"])

voie_type_2 = set([("CHEF", "LIEU"), ("LIEU", "DIT"), ("GRANDE", "RUE"),
                   ("GRAND", "RUE"), ("GRANDE", "PLACE"), ("ROND", "POINT")])

meanless_words = set(["DE", "DES", "DU", "D", "LE", "LES", "LA", "L",
                      "A", "AU", "AUX", "ET", "EN", "SUR", "SOUS", "CEDEX"])


def uniform(text):
    """Return the upper-case text converted to ascii.
    """
    return unidecode(text.strip()).upper()


def remove_separators(text):
    """Remove some separator symbols that doesn't make sense in an address.

    Remove the parenthesis and everything inside if there is, otherwise search
    for a slash or a vertical slash and return the everything at the its left.
    """
    # Remove parenthesis
    text = re.sub(r'[(].*[)]', '', text)
    # The slash
    if re.findall(r'/', text):
        return text.split('/')[0]
    # The vertical slash
    elif re.findall(r'[|]', text):
        return text.split('|')[0]
    return text


def uniform_words(text):
    """Return a normalized list of words from text.

    Split the normalized text in words and select those that aren't in the
    module level variable meanless_words set.
    """
    text = uniform(remove_separators(text))

    text = text.replace(",", ' ')
    text = text.replace("'", ' ')
    text = text.replace('"', '')
    text = text.replace('-', ' ')

    return [word for word in translate(text) if word not in meanless_words]


def translate(text):
    """Translate the abbreviations to their long form using the module level
    variable dictionary.
    """
    words = text.split()
    for i in range(len(words)):
        if words[i] in dictionary:
            words[i] = dictionary[words[i]]
    return words


def uniform_adresse(text):
    """Normalization of the address.
    """
    return ''.join(uniform_words(text))


def uniform_commune(text):
    """Normalization of the city name.
    """
    return re.sub(r'[0-9]', '', ''.join(uniform_words(text))).strip()


def find_voie_type(words):
    """Find the type of the street using the module level variables voie_type_1
    and voie_type_2.
    """
    voie_type_index = None
    for i in range(len(words) - 2, -1, -1):
        if words[i] in voie_type_1 or (words[i], words[i + 1]) in voie_type_2:
            voie_type_index = i
            return i

    return voie_type_index


def mine(text):
    """Retrieve the useful information from the address.

    Extract the street's name, type and number from an address description.

    Args:
        text (str): The address.

    Returns:
        tuple:
        (numero (int); The number, voie (str): The name,
         voie_type (str): The type)

    """
    words = uniform_words(text)

    # If the text has no words, return None
    if not len(words) or len(text) == 0:
        return None, None, None

    voie_type_index = find_voie_type(words)

    # The index of the last word to consider in the search for the number
    numero_limit = voie_type_index if voie_type_index is not None \
        else (len(words) - 1)

    # Search for the number
    numero, numero_index = None, None
    for i, word in reversed(list(enumerate(words[:numero_limit]))):
        matches = re.findall(r'[0-9]+', word)
        if matches:
            numero, numero_index = int(matches[0]), i
            break

    # In the case that the word describing the type of the street wasn't found
    if voie_type_index is None and numero_index is not None:
        voie_type_index = numero_index + 1
    elif voie_type_index is None:
        voie_type_index = 0

    voie = ''.join(words[voie_type_index:])
    voie_type = words[voie_type_index]
    return numero, voie, voie_type
