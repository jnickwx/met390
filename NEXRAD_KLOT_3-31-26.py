#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:59:40 2026

@author: jnick
"""

import os
import glob
import concurrent.futures
from tqdm import tqdm
from PIL import Image # <-- The library that stitches the GIF together

# HEADLESS MODE: Run Matplotlib in the background
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pyart 
import cartopy.crs as ccrs

# --- SETTINGS ---
OUTPUT_FOLDER = '/Users/jnick/intercollegiate/radar_output_images_3/31/26'
GIF_SPEED = 400 # Milliseconds per frame (Lower = Faster animation. 400ms is standard)

def process_radar_file(file_path):
    """This function handles a single radar file."""
    if "MDM" in file_path:
        return None 
        
    try:
        radar = pyart.io.read(file_path)
        
        fig = plt.figure(figsize=[10, 8])
        display = pyart.graph.RadarMapDisplay(radar)
        
        # --- FILTER SETUP ---
        gatefilter = pyart.filters.GateFilter(radar)
        gatefilter.exclude_below('reflectivity', 20)
        try:
            gatefilter.exclude_below('cross_correlation_ratio', 0.95)
        except KeyError:
            pass 
        
        # --- PLOTTING ---
        display.plot_ppi_map('reflectivity', 0, title='KLOT Reflectivity', 
             vmin=0, vmax=75, cmap='NWSRef',
             projection=ccrs.PlateCarree(),
             gatefilter=gatefilter)
        
        display.plot_range_rings([50, 100, 150], col='black')
        display.plot_grid_lines()
        
        # --- SAVING TO FOLDER ---
        filename = os.path.basename(file_path) + '.png'
        save_path = os.path.join(OUTPUT_FOLDER, filename)
        
        # dpi=120 creates a great looking GIF without making the file size massive
        fig.savefig(save_path, dpi=120, bbox_inches='tight')
        plt.close(fig)
        
        return "Success"
        
    except Exception as e:
        return f"Skipping {os.path.basename(file_path)} due to error: {e}"


# --- MAIN EXECUTION BLOCK ---
if __name__ == '__main__':
    # 1. Get the list of raw files
    file_list = sorted(glob.glob('/Users/jnick/intercollegiate/nexrad_KLOT_2026-03-31/*'))
    
    # 2. Create the output folder
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # 3. CPU Safeguards
    total_cores = os.cpu_count() or 4 
    safe_cores = max(1, total_cores - 2) 
    
    print(f"Found {len(file_list)} files. Outputting to: {OUTPUT_FOLDER}")
    print(f"Using {safe_cores} CPU cores...\n")
    
    # 4. Generate the PNGs
    with concurrent.futures.ProcessPoolExecutor(max_workers=safe_cores) as executor:
        results = list(tqdm(
            executor.map(process_radar_file, file_list), 
            total=len(file_list), 
            desc="Generating Maps", 
            unit="file",
            dynamic_ncols=True
        ))
        
    # Print out any errors
    errors_found = False
    for result in results:
        if result and "Skipping" in result:
            print(result)
            errors_found = True
            
    if not errors_found:
        print("\nAll sweeps processed successfully!")

    # --- NEW: GIF ANIMATION GENERATOR ---
    print("\nStitching images into an animated GIF...")
    
    # Find all the newly created PNGs in our output folder
    png_files = sorted(glob.glob(os.path.join(OUTPUT_FOLDER, '*.png')))
    
    if len(png_files) > 1:
        # Load the images into Pillow
        frames = [Image.open(image) for image in png_files]
        
        # Define where to save the GIF
        gif_path = os.path.join(OUTPUT_FOLDER, 'radar_loop_3-31-26.gif')
        
        # Save the GIF (loop=0 means it loops infinitely)
        frames[0].save(
            gif_path, 
            format='GIF', 
            append_images=frames[1:],
            save_all=True, 
            duration=GIF_SPEED, 
            loop=0
        )
        print(f"SUCCESS! Animation saved to: {gif_path}")
    else:
        print("Not enough images generated to create a GIF.")