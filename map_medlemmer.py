import folium
import os
import geopandas as gpd
import pandas as pd
from collections import Counter
import json

def get_postnummer_mapping():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    postnumre_file = os.path.join(script_dir, 'postnumre-clipped-simplified.geojson')

    o = gpd.read_file(postnumre_file)
    o = o.rename(columns={'nr':'postalcode'})
    o['postalcode'] = o['postalcode'].astype('int64')
    o.crs = 4326
    return o

def make_map(users):
    postnummer_mapping = get_postnummer_mapping()
    counts = Counter([user.postnummer for user in users])
    counts_df = pd.DataFrame.from_dict(counts, orient='index', columns=['count']).reset_index().rename(columns={'index': 'postalcode'})
    merged_gdf = postnummer_mapping.merge(counts_df, on="postalcode", how="left")
    filtered_gdf = merged_gdf[merged_gdf["count"].notnull()]

    m = folium.Map(location=[56, 12], zoom_start=7)
    filtered_gdf = filtered_gdf[['postalcode','navn','geometry','count']]

    folium.GeoJson(
        filtered_gdf,
        name="Postal Codes",
        style_function=lambda feature: {
            "fillOpacity": feature['properties']["count"] / filtered_gdf["count"].max(),
            "weight": 1,
            "color": "black",
            "fillColor": "blue",
        },
        tooltip=folium.GeoJsonTooltip(fields=["postalcode",'navn', "count"]),
    ).add_to(m)
    
    return m