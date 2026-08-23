# %%
"""
Grand River Transit (GRT) Walkability Catchment Analysis
Author: Anas Aweis
Description: Evaluates 400m walking buffers around transit stops in Waterloo using GeoPandas.
"""

import geopandas as gpd
import matplotlib.pyplot as plt

def run_transit_analysis(input_file, municipality="Waterloo", buffer_dist=400):
    # 1. Load spatial dataset
    print(f"Loading data from {input_file}...")
    gdf = gpd.read_file(input_file)
    
    # 2. Filter by municipality & reproject to UTM Zone 17N (meters)
    stops = gdf[gdf['Municipality'] == municipality].copy()
    stops_utm = stops.to_crs(epsg=26917)
    print(f"Filtered to {len(stops_utm)} stops in {municipality}.")
    
    # 3. Create buffer and dissolve overlapping service areas
    buffers = stops_utm.copy()
    buffers['geometry'] = stops_utm.geometry.buffer(buffer_dist)
    merged_area = buffers.dissolve()
    
    # 4. Calculate total coverage in square kilometers
    area_km2 = merged_area.area.iloc[0] / 1_000_000
    print(f"Total {buffer_dist}m transit walking coverage: {area_km2:.2f} km²")
    
    # 5. Plot and export visualization
    fig, ax = plt.subplots(figsize=(10, 10))
    merged_area.plot(ax=ax, color='#b0d2f0', edgecolor='#2b5c8f', alpha=0.6, label=f'{buffer_dist}m Walk Buffer')
    stops_utm.plot(ax=ax, markersize=8, color='#002d62', label='Bus Stops')
    
    plt.title(f"City of {municipality} - GRT {buffer_dist}m Walkability Catchment", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("UTM Easting (m)")
    plt.ylabel("UTM Northing (m)")
    plt.grid(True, linestyle='--', alpha=0.4)
    
    output_img = f"{municipality.lower()}_transit_coverage.png"
    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    print(f"Map saved as '{output_img}'.")

if __name__ == "__main__":
    run_transit_analysis("GRT_Bus_Stops.geojson")


