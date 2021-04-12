=========
Geocoding
=========

Geocoding is an address search engine for France. Unlike other APIs, it uses a database provided by the french government (Base Adresse Nationale - BAN) as the main source of information and does not impose any limit to the number of queries. The purpose of the project is to supply the needs of french data scientists that rely on geocoded data.

Getting Started
===============

Prerequisites
-------------

* Python version 3 installed locally
* Pip installed locally
* Docker (for geocoding API use)

Using API with Docker
---------------------

Build the API server locally

  docker build --build-arg app_port=8088 --progress=plain -t geocoding-api .

Docker requirements for building

* Memory 12Gb
* Disk image size 50Gb

Use it

  docker run -p 8088:8088 geocoding-api

The API is available through:

* In your browser:

  * http://localhost:8088
  * http://localhost:8088/use
  * http://localhost:8088/geocode/<address>/<postal_code>/<city>

* With Curl:

  curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"address": [], "postal_code": [], "city": []}' \
  http://localhost:8088/geocode_file

Exemples:

  http://localhost:8088/geocode/12, Bd des Maréchaux/91120/Palaiseau

  curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"address": "12, Bd des Maréchaux", "postal_code": "91120", "city": "Palaiseau"}' \
  http://localhost:8088/geocode_file


For using purposes
------------------

The package can easily be installed via pip::

  pip install geocoding

Before the first use, you need to download the BAN database and process its files to unlock the functionalities of the package. All of this can be done with the following command (the whole process should take 30 minutes)::

  geocoding update

Alternatively, you can do it step by step with the following commands::

  geocoding download
  geocoding decompress
  geocoding index
  geocoding remove_non_necessary_files

To unlock the reverse search, execute the following command::

  geocoding reverse

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

The reverse functionality
-------------------------

.. code-block:: python

    import geocoding

    # longitude and latitude
    query = (2.2099, 48.7099)
    output = geocoding.near(query)
    output['commune']['nom']  # PALAISEAU
    output['voie']['nom']  # BOULEVARD DES MARECHAUX

Benchmarks
---------------

.. code-block:: python

    import geocoding

    begin = time.time()
    for _ in range(2000):
        geocoding.find('91130', 'PALISEAU', '12 BD DES MARECHUX')
    print(time.time() - begin, 'seconds')  # 1.063 seconds

    begin = time.time()
    for _ in range(10000):
        geocoding.find('91120', 'PALAISEAU', '12 BD DES MARECHAUX')
    print(time.time() - begin, 'seconds')  # 1.407 seconds

    begin = time.time()
    for _ in range(10000):
        geocoding.find('75015', 'PARIS', '1 RUE SAINT CHARLES')
    print(time.time() - begin, 'seconds')  # 1.525 seconds

    begin = time.time()
    for _ in range(1000):
        geocoding.near((2, 48))
    print(time.time() - begin, 'seconds')  # 0.922 seconds
