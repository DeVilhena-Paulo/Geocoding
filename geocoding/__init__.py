from . import search
from geocoding import query

find = search.position
near = search.reverse

print('Loading geocoding data')
query.setup()
