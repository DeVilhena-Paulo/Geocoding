import uuid
import geocoding
import numpy as np

from datetime import datetime
from api.conf import *


class Geocoder:

    def __init__(self, data_to_geocode):
        self.errors = []
        self.geocoded = False
        self.uuid = str(uuid.uuid1())
        self.data = data_to_geocode
        self.geocoded_date_time = None
        self.check_data_to_geocode(data_to_geocode)

    def get_uuid(self):
        return self.uuid

    def get_errors(self):
        return self.errors

    def get_geocoded_date_time(self):
        return self.geocoded_date_time

    def get_geocoded_data(self):
        if self.is_geocoded():
            return self.data
        else:
            return None

    def check_data_to_geocode(self, data_to_geocode):
        errors = []
        for col_to_check in [ADDRESS, POSTAL_CODE, CITY]:
            if col_to_check not in data_to_geocode.columns:
                errors = errors + [f'Column {col_to_check} is missing.']
        if len(errors) > 0:
            self.errors = errors

    def has_errors(self):
        return len(self.errors) > 0

    def is_geocoded(self):
        return self.geocoded

    def geocode(self):
        if not self.geocoded and not self.has_errors():
            def find(args):
                if args[0] == '98000':
                    return np.nan, np.nan, np.nan
                else:
                    res = geocoding.find(*args)
                    return res.get('longitude', np.nan), res.get('latitude', np.nan), res.get('quality', np.nan)

            geocoded_fields = [find(args) for args in self.data[[POSTAL_CODE, CITY, ADDRESS]].fillna('').values]

            self.data['lon'], self.data['lat'], self.data['quality'] = zip(*geocoded_fields)
            self.geocoded_date_time = datetime.now()
            self.geocoded = True
