#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:53:51 2026

@author: jnick
"""



from goes2go import GOES
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs 

# Get an ABI Dataset 
G = GOES().latest()

#Make a figure for the single latest plot
fig_latest = plt.figure(figsize=(10,10))
ax = plt.subplot(projection=G.rgb.crs)
ax.imshow(G.rgb.TrueColor(), **G.rgb.imshow_kwargs)
ax.coastlines(color="white") #Added this to see easier
plt.title("Latest GOES TrueColor")

#Specific time for the GOES-19 data 
G19 = GOES(satellite=19).nearesttime("2026-03-26 00")

#List specific products to display 
products = ["NaturalColor", "DayCloudConvection", "AirMass"]

#Plot dimensions 
fig, axes = plt.subplots(1, 3, figsize=[15, 5], subplot_kw={'projection': G19.rgb.crs})
for product, ax in zip(products, axes.flatten()):
    nc = getattr(G19.rgb, product)()
    ax.imshow(nc, **G19.rgb.imshow_kwargs)
    ax.set_title(product)
    ax.axis("off")
    
plt.subplots_adjust(wspace=0.05)


#Processing for all avaiable RGB products 
rgb_products = [i for i in dir(G19.rgb) if i[0].isupper()][:5]

for product in rgb_products:
    fig = plt.figure(figsize=(8, 8))
    ax19 = fig.add_subplot(1, 1, 1, projection=G19.rgb.crs)
    
    #Make the RGB data
    RGB = getattr(G19.rgb, product)()
    
    ax19.imshow(RGB, **G19.rgb.imshow_kwargs)
    
    ax19.set_title(f"{G19.orbital_slot} {product}", loc="left", fontweight="bold")
    #Make the time formatting cleaner
    time_str = G19.t.dt.strftime('%H:%M UTC %d-%b-%Y').item()
    ax19.set_title(time_str, loc="right")
    ax19.coastlines(color="lightgray")

#Show the plots
plt.show() 

