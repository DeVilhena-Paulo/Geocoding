from setuptools import setup

with open('README.rst') as reader:
    readme = reader.read()

setup(
    name='Geocoding',
    version='1.4.3',
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
    ],
    keywords='Geocoder France',
    packages=['geocoding'],
    install_requires=['numpy', 'Unidecode', 'KdQuery', 'sortedcontainers', 'requests'],
    entry_points={
        'console_scripts': [
            'geocoding = geocoding.__main__:main'
        ]
    },
)
