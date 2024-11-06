import geopandas as gpd
from shapely.geometry import MultiLineString
import matplotlib.pyplot as plt

gdf = gpd.read_file("osm-clipped.gpkg", layer="osm-clipped")

clipped_lengths = {}
for idx, row in gdf.iterrows():
    geometry = row.geometry
    if isinstance(geometry, MultiLineString):
        total_length = sum(line.length for line in geometry.geoms)  # Sum the lengths of LineStrings
        # print(f"osm_id: {row['osm_id']}, Total Length of Lines: {total_length}")
        if row['osm_id'] in clipped_lengths:
            clipped_lengths[row['osm_id']] += total_length
        else:
            clipped_lengths[row['osm_id']] = total_length
    else:
        print(f"osm_id: {row['osm_id']} has a different geometry type: {type(geometry)}")


gdf = gpd.read_file("osm.gpkg", layer="osm")

lengths = {}
for idx, row in gdf.iterrows():
    geometry = row.geometry
    # print(geometry.length)
    if row['osm_id'] in lengths:
        lengths[row['osm_id']] += geometry.length
    else:
        lengths[row['osm_id']] = geometry.length

# # Plot the histogram
# plt.hist(lengths.values(), bins=10, range=(0.0, 0.001), edgecolor='black')

# # Labeling the plot
# plt.xlabel('lengths')
# plt.ylabel('Frequency')
# plt.title('Histogram of Ratios')

# # Display the histogram
# plt.show()

keep = []
min_length = 0.0005
for clipped_key in clipped_lengths:
    ratio = clipped_lengths[clipped_key] / lengths[clipped_key]
    if ratio > 0.2 and lengths[clipped_key] > min_length:
        keep.append(clipped_key)

# Filter the GeoDataFrame to include only features with matching osm_ids
filtered_gdf = gdf[gdf['osm_id'].isin(keep)]

# Save the filtered GeoDataFrame to a new GeoPackage file
filtered_gdf.to_file("filtered_output.gpkg", layer="osm", driver="GPKG")
