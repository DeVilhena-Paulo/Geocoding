=========
Geocoding
=========

Geocoding is an address search engine for France. Unlike other APIs, it uses a database provided by the french government (Base Adresse Nationale - BAN) as the main source of information and does not impose any limit to the number of queries. The main purpose of the project is to supply the needs of french data scientists that rely on geocoded data.

Getting Started
===============

Prerequisites
-------------

* Python version 3 installed locally
* Pip installed locally

For using purposes
------------------

You can download the package in the wheel format from this link:

`Geocoding.whl <https://drive.google.com/open?id=0B3GIkecVT8Q7YXNNbEkwX3l4cUE>`_.

and once the donwload is complete you execute the following command::

 pip install <path to whl file>/Geocoding-1.0.0-py3-none-any.whl

Or you can download the package in the source distribution format from this link:

`Geocoding.tar.gz <https://drive.google.com/open?id=0B3GIkecVT8Q7ejB5LVFJLWVmMUE>`_.

and once the donwload is complete you execute the following command::

 pip install <path to whl file>/Geocoding-1.0.0.tar.gz

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

Once it is done, you can build the package directly::

 python setup.py sdist

Or::

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
