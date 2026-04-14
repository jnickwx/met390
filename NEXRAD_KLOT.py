#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:04:40 2026

@author: jnick
"""
# Weather radar using py-art 

import matplotlib.pyplot as plt
import pyart 
import cartopy.crs as ccrs
import glob
import os
    
# Read in radar data file into code
file_list = sorted(glob.glob('/Users/jnick/nexrad_KLOT_2026-03-26/*'))

for file_path in file_list:
    try:
        # If the files are still zipped, you'll need the extraction step
        radar = pyart.io.read(file_path)

        # Make the display 
        display = pyart.graph.RadarMapDisplay(radar)


        # Make figure 
        fig = plt.figure(figsize=[10, 8])


        # Plot reflectivity as a ppi map
        # sweep = 0 is the lowest elevation angle
        display.plot_ppi_map('reflectivity', 0, title='KLOT Reflectivity', 
             vmin= -32, vmax= 75, cmap='NWSRef',
             projection=ccrs.PlateCarree())
        
        # Range rings 
        display.plot_range_rings([50, 100, 150], col='black')
        display.plot_grid_lines()
        
        # Saving the figure
        output_filename = os.path.basename(file_path) + '.png'
        fig.savefig(output_filename, dpi=300)
        print(f"Successfully saved {output_filename}")
        plt.show() 
        
        # Close the figure to conserve memory
        plt.close(fig)
        
    except Exception as e:
        # Closes the try logic
        print(f"Skipping {file_path} due to error: {e}")
        
