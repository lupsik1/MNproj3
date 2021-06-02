import googlemaps
from API_Auth import api_auth
class HeighDataFromPath:

    def __init__(self, start, destination):
        self.gmaps = googlemaps.Client(key=api_auth['api-key'])


