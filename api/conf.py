with open('version.txt') as reader:
    VERSION = reader.read()

QUALITY = {'1': 'Successful',
           '2': 'Precise number was not found',
           '3': 'Precise number was not found and there was no number in the input',
           '4': 'Street was not found',
           '5': 'City was not found',
           '6': 'Nothing was found',
           }
