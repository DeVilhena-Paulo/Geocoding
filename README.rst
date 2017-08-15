=========
Geocoding
=========

Geocoding is an address search engine for France. Unlike other APIs, it uses a database provided by the french government (Base Adresse Nationale - BAN) as the main source of information and does not impose any limit to the number of queries. The main purpose of the project is to supply the needs of french data scientists that rely on geocoded data.

Getting Started
===============

Prerequisites
-------------

* Python version 3.6 installed locally
* Pip installed locally

Usage
=====

The search engine
-----------------

.. code-block:: python

    import geocoding


    # -*- Complete search -*-
    output = geocoding.find('91120', 'Palaiseau', '12, Bd des Maréchaux')
    print(output['longitude'], output['latitude'])  # 2.2099342 48.7099138


    # -*- Incomplete search -*-
    output = geocoding.find('91120', None, '12, Bd des Maréchaux')
    print(output['quality'])  # 1 -> It means that the search was successful

    output = geocoding.find('91120', None, 'Bd des Maréchaux')
    print(output['quality'])  # 3 -> It means that the number was not found

    output = geocoding.find('91120', 'Palaiseau', None)
    print(output['quality'])  # 4 -> It means that the street was not found

    output = geocoding.find(None, 'Palaiseau', '12, Bd des Maréchaux')
    print(output['quality'])  # 1

    output = geocoding.find(None, None, '12, Bd des Maréchaux')
    print(output['postal']['code'])  # 35800
    print(output['commune']['nom'])  # DINARD
    print(output['voie']['nom'])  # BOULEVARD DES MARECHAUX


    # -*- Search with typos -*-
    geocoding.find('91120', 'Palaiseau', '12, Bd des Maréchx')['quality']  # 1
    geocoding.find('91120', 'Palaiau', '12, Bd des Maréchx')['quality']  # 1
    geocoding.find('91189', 'Palaiseau', '12, Bd des Maréchx')['quality']  # 1
    geocoding.find('91189', None, '12, Bd des Maréchx')['quality']  # 1


    # -*- Flexible syntax -*-
    geocoding.find('91120', 'Palaiseau')['quality']  # 4
    geocoding.find(commune='Palaiseau')['quality']  # 4
    geocoding.find('91120')['quality']  # 5

    args = {
        'code_postal': '91120',
        'commune': 'Palaiseau',
        'adresse': '12, Bd Marechaux'
    }
    geocoding.find(**args)
