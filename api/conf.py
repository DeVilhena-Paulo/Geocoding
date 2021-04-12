with open('version.txt') as reader:
    VERSION = reader.read()

ADDRESS = 'address'
POSTAL_CODE = 'postal_code'
CITY = 'city'

QUALITY = {'1': 'Successful',
           '2': 'Precise number was not found',
           '3': 'Precise number was not found and there was no number in the input',
           '4': 'Street was not found',
           '5': 'Commune was not found',
           '6': 'Nothing was found',
           }
