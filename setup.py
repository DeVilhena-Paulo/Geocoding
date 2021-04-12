from setuptools import setup
import pandas as pd

with open('README.rst') as reader:
    readme = reader.read()

with open('version.txt') as reader:
    version = reader.read()

requirements = list(pd.read_csv('requirements.txt', header=None)[0])

setup(
    name='Geocoding',
    version=version,
    description='geocoding is an address search engine for France',
    long_description=readme,
    url='https://github.com/DeVilhena-Paulo/Geocoding',
    author='Paulo Emilio de Vilhena',
    author_email='pevilhena2@gmail.com',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='Geocoder.py France',
    packages=['geocoding'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'geocoding = geocoding.__main__:main'
        ]
    },
)
