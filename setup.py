from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Geocoding',
    version='0.0.1',

    description='geocoding is an address search engine for France',
    long_description=long_description,

    url='https://github.com/DeVilhena-Paulo/Geocoding_Package',

    author='Paulo Emilio de Vilhena',
    author_email='pevilhena2@gmail.com',

    license='Apache Software License',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='Geocoder France',

    packages=['Geocoding'],

    py_modules=["Geocoding/search", "Geocoding/access", "Geocoding/utils"],

    install_requires=['numpy', 'Unidecode', 'KdQuery'],

    package_data={
        'Geocoding': ['database_dat/departement.dat',
                      'database_dat/commune.dat',
                      'database_dat/postal.dat',
                      'database_dat/postal_index.dat',
                      'database_dat/voie.dat',
                      'database_dat/localisation.dat',
                      'database_dat/kdtree.dat'],
    },
)
