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

For using purposes
------------------

Download the built-package: |location_link1|

.. |location_link1| raw:: html

   <a href="https://drive.google.com/open?id=0B3GIkecVT8Q7YXNNbEkwX3l4cUE" target="_blank">Geocoding-1.0.0-py3-none-any.whl</a>

Once the donwload is complete, execute the following command::

 pip install <path to whl file>/Geocoding-1.0.0-py3-none-any.whl

Another option is to download the source distribution: |location_link2|

.. |location_link2| raw:: html

   <a href="https://drive.google.com/open?id=0B3GIkecVT8Q7ejB5LVFJLWVmMUE" target="_blank">Geocoding-1.0.0.tar.gz</a>

and once the donwload is complete, execute the following command::

 pip install <path to gztar file>/Geocoding-1.0.0.tar.gz

For development or testing purposes
-----------------------------------

Clone the project with git::

 git clone https://github.com/DeVilhena-Paulo/Geocoding.git

Change to the project's directory::

 cd Geocoding

Execute the following modules::

 python data/update.py
 python data/intermediate.py
 python data/index.py
 python data/activate_reverse.py

Once it is done, you can get the source distribution or the wheel of the package directly::

 python setup.py sdist
 python setup.py bdist_wheel

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
