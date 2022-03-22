import googlemaps
from API_Auth import api_auth
import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import numpy as np
from Interpolation import interpolate_using_lagrange, interpolate_using_splines
import itertools


class HeightDataFromPath:
    def __init__(self, start, destination, title, res,fname):
        self.title = title
        self.gmaps = googlemaps.Client(key=api_auth['api-key'])

        self.n_id = fname+"_"+str(res)+"samples"
        # setup data
        self.samples = 3 * round(float(res) / 3)  # uses closes multiple of 3 due to the spline implementation
        self.draw_interval = 0.0001
        self.next_plot_interval = 1
        self.interpolation_resolution_scale = 20

        # geo data
        self.start_geocode = self.gmaps.geocode(start)
        self.destination_geocode = self.gmaps.geocode(destination)

        self.start_coords = self.start_geocode[0]['geometry']['location']
        self.start_coords = (self.start_coords['lat'], self.start_coords['lng'])
        self.destination_coords = self.destination_geocode[0]['geometry']['location']
        self.destination_coords = (self.destination_coords['lat'], self.destination_coords['lng'])

        self.distance = geodesic(self.start_coords, self.destination_coords).meters
        self.elevation_df = self.get_elevation_data()

        # final x y data for height
        self.x = np.linspace(0, self.distance, num=self.samples)
        self.y = self.elevation_df['elevation']

    def get_elevation_data(self):
        elevation = self.gmaps.elevation_along_path([self.start_coords, self.destination_coords], self.samples)
        elevation_dataframe = pd.DataFrame(elevation)
        return elevation_dataframe

    def draw_elevation(self):
        i = 0
        max_h = self.y.max()
        min_h = self.y.min()
        colorspace = np.linspace((0, 0, 1), (1, 0, 0), 102)
        colors = list()
        plt.figure(figsize=(10, 6), dpi=120)
        # map colors for scatter plot
        for i in range(0, self.samples):
            curr_value = self.y[i]
            color = colorspace[int((curr_value - min_h) / (max_h - min_h) * 100) + 1]
            colors.append(color)

        # draw scatter plot step by step

        for i in range(0, self.samples + 1):
            plt.cla()
            plt.xlim([-10, self.distance + 10])
            plt.ylim([min_h - 30, max_h + 30])
            plt.title(self.title)
            plt.xlabel("Odległość od początku trasy[m]")
            plt.ylabel("Wysokość nad poziomem morza[m]")
            plt.scatter(self.x[0:i], self.y[0:i], c=colors[0:i], s=10, marker='o', label="Punkty pomiarowe")
            plt.legend()
            plt.pause(self.draw_interval)

        # draw interpolated values
        plt.pause(self.next_plot_interval)
        xp = np.linspace(0, self.distance, self.interpolation_resolution_scale * self.samples)
        yp_lagrange = interpolate_using_lagrange(self.x, self.y, self.interpolation_resolution_scale * self.samples)
        plt.plot(xp, yp_lagrange, 'b', label="Interpolacja, wielomian Lagrange'a")
        plt.legend()
        plt.pause(self.next_plot_interval)

        xp_splines, yp_splines = interpolate_using_splines(self.x, self.y, self.interpolation_resolution_scale)

        plt.plot(xp_splines, yp_splines, 'r', label="Interpolacja, funkcja sklejana stopnia 3")
        plt.legend()
        plt.pause(self.next_plot_interval)
        fname = "plot"+str(self.n_id)+".png"
        plt.savefig(fname)
        plt.close()
