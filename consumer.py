import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


class ApiConsumer:

    def __init__(self,get_url, post_url, delete_url):
        self._get_url = get_url
        self._post_url = post_url
        self._delete_url = delete_url

    @property
    def delete_url(self):
        return self._delete_url

    @delete_url.setter
    def delete_url(self, url):
        self._delete_url = url

    @property
    def get_url(self):
        return self._get_url

    @get_url.setter
    def get_url(self, url):
        self._get_url = url

    @property
    def post_url(self):
        return self._post_url

    @post_url.setter
    def post_url(self, url):
        self._post_url = url

    def create_dataframe(self):
        response = requests.get(self.get_url)
        return pd.json_normalize(response.json())

    def visualize(self):
        df = self.create_dataframe()
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        ax = world.plot(color='white', edgecolor='black', figsize=(16, 24))
        gdf.plot(ax=ax, color='red')
        plt.show()

    def post_json(self,json):
        requests.post(self.post_url, json=json)

    def delete_by_country(self, country):
        requests.delete(f'{self.delete_url}?country={country}')