import geopandas as gpd
from shapely.geometry import MultiLineString
import matplotlib.pyplot as plt

gdf = gpd.read_file("roads_final.gpkg", layer="roads_final")

keep = []
for idx, row in gdf.iterrows():
    # print(idx, row['real_world'])
    keep.append(row['real_world'])

gdf = gpd.read_file("roads_ini.gpkg", layer="roads_ini")


filtered_gdf = gdf[gdf['real_world'].isin(keep)]
filtered_gdf.to_file("roads_final_with_ini.gpkg", layer="roads_final_with_ini", driver="GPKG")

