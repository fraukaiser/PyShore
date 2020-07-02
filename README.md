# PyShore 

PyShore is a python based tool that allows you to detect changes in lake shorelines derived from satellite imagery. 

## Prerequisites

- Satellite imagery in GeoTIFF format
- Python 2.7+ with the following dependecies (via pip): gdal scikit-image numpy scipy matplotlib geopandas

## Workflow

The provided python scripts are doing the following:
- Smoothing_skimage_otsu_median_thresholding_v02_r00.py takes mutlitemporal images (you might need to do some manual pansharpening to enhance the spatial resolution of the data) and detects waterbodies using an adaptive threshold (Otsu) on the near infrared band. If your bands are not in the following order: B, G, R, NIR make sure to change line 35.
The binary information (water vs. non-water) is subsequently vectorized for usage in the second script.

- Plotting_shorelines.py uses the shapefile output from the first script as input and extracts the waterbodies. It removes infrastructure elements and filters for waterbodies > 0.1 ha.
In the subsequent nearest points analysis each shoreline vertex from one date to the nearest vertex of the following date is correlated. The distance and angle between correlated verttexes are calculated and saves as an attribute value for each point of the dataset. 
The resulting lakeID attribute table is saved to a .csv-file.

## Visualisation of the results

- BatchCSVtoSHP.py converts every lakeID.csv file to an ESRI Shapefile for visualisation. 

- batchloadcsv_qgs.py allows batch import to QGIS 2.18+


