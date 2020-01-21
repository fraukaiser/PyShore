# PyShore 

PyShore is a python based tool that allows you to detect changes in lake shorelines derived from satellite imagery. 

## Prerequisites

The provided python scripts are doing the following:
- noSmoothing_skimage_binary_threshold.py takes satellite imagery in GeoTIFF format (you might need to do some manual pansharpening to enhance the spatial resolution of the data) and detects waterbodies using an adaptive threshold (Otsu) on the near infrared band. If your bands are not in the following order: B, G, R, NIR make sure to change line 31. 

- noSmoothing_skimage_binary_threshold.py detects waterbodies using an user defined threshold (t value is to be set in line 30) on the NIR band. Again change line 31 if your NIR band is not at the fourth position or you want to use the thresholding on another band. 
