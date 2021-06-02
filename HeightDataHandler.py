import googlemaps
from API_Auth import api_auth
import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import numpy as np
class HeightDataFromPath:

    def __init__(self, start, destination):
        self.gmaps = googlemaps.Client(key=api_auth['api-key'])

        # setup data
        self.samples = 256
        self.draw_interval = 0.15
        # geo data

        self.start_geocode = self.gmaps.geocode(start)
        self.destination_geocode = self.gmaps.geocode(destination)

        self.start_coords = self.start_geocode[0]['geometry']['location']
        self.start_coords = (self.start_coords['lat'], self.start_coords['lng'])
        self.destination_coords = self.destination_geocode[0]['geometry']['location']
        self.destination_coords = (self.destination_coords['lat'], self.destination_coords['lng'])

        self.distance = geodesic(self.start_coords,self.destination_coords).kilometers
        self.elevation_df = self.get_elevation_data()

    def get_elevation_data(self):
        elevation = self.gmaps.elevation_along_path([self.start_coords, self.destination_coords], self.samples)
        elevation_dataframe = pd.DataFrame(elevation)
        return elevation_dataframe

    def draw_elevation(self):
        x = np.linspace()
        for sample in self.elevation_df['elevation']:
            print(sample)


