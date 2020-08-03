# PyShore 

PyShore is a python based tool that allows you to detect changes in lake shorelines derived from satellite imagery. 

## Prerequisites

#### Technical

- Python 2.7+ with the following dependecies (via pip): gdal scikit-image numpy scipy matplotlib geopandas

#### Formal

Assemble your data in __one__ input folder. It should contain your

- (multi-temporal) satellite imagery in GeoTIFF format
- infrastructure data (e.g. OpenStreetMap) in Shapefile format
- study area image extent in Shapefile format

The file names of the satellite imagery must begin with the acquisition date, starting with the year, e.g. 16JUL22xxxx.TIF, 20060823xxxx.TIF. etc. Your folder should look similar to this:

>~/0_PyShore_Input$ tree .
>├── ORDER_SHAPE_32606.dbf 	# study area image extent to prevent NoData values.
>├── ORDER_SHAPE_32606.prj


`├── ORDER_SHAPE_32606.shp`
`├── ORDER_SHAPE_32606.shx`
`├── 06AUG15222517-M2AS-058878563040_01_P001_GS_pansharpened_cubic_0.5.TIF	# multi-temporal imagery`
`├── 10JUL09221426-M2AS-058878563030_01_P001_GS_pansharpened_cubic_0.5.TIF`
`├── 13JUL16225401-M2AS-058878563020_01_P001_GS_pansharpened_cubic_0.5.TIF`
`├── 16JUL10222531-M2AS-058878563010_01_P001_GS_pansharpened_cubic_0.5.TIF`
`├── gis_osm_buildings_a_free_1.cpg	# OSM infrastructure data, both line and polygon features`
`├── gis_osm_buildings_a_free_1.dbf`
`├── gis_osm_buildings_a_free_1.prj`
`├── gis_osm_buildings_a_free_1.shp`
`├── gis_osm_buildings_a_free_1.shx`
`├── gis_osm_landuse_a_free_1.cpg`
`├── gis_osm_landuse_a_free_1.dbf`
`├── gis_osm_landuse_a_free_1.prj`
`├── gis_osm_landuse_a_free_1.shp`
`├── gis_osm_landuse_a_free_1.shx`
`├── gis_osm_roads_free_1.cpg`
`├── gis_osm_roads_free_1.dbf`
`├── gis_osm_roads_free_1.prj`
`├── gis_osm_roads_free_1.shp`
`└── gis_osm_roads_free_1.shx`


## Workflow

The provided python scripts work as follows:


#### SmmothAndPlot.py 

Usage: `python SmoothAndPlot.py <path_in> <order-shape> <sitename>>` 

- `<path_in>` folder containing your OSM infrastructure Shapefiles and the ouput of Smoothing_skimage_otsu_median_thresholding.py

- `<order-shape>` path to your image extent Shapefile

- `<sitename>` user chosen string for naming the output files. 

The script accepts mutlitemporal images (you might need to do some manual pansharpening to enhance the spatial resolution of the data) stored in your input folder. The waterbody detection is based on an adaptive thresholding (Otsu) on the near infrared band. If your bands are not in the following order: B, G, R, NIR make sure to change line 74.
The binary information (water vs. non-water) is subsequently vectorized and saved to your input folder. 
After the extraction of waterbodies, infrastructure elements (from your infrastructure data in  and waterbodies < 0.1 ha (size can be changed in line 253) are removed. An intermediate output is stored in "1_PyShore_ProcData". 
Uses the shapefile output from the first script and the infrastructure data (both stored in path_in) as input and extracts the waterbodies. It removes infrastructure elements and filters for waterbodies > 0.1 ha. An intermediate output is stored in "1_PyShore_ProcData".

In the subsequent nearest points analysis each shoreline vertex from one date to the nearest vertex of the following date is correlated. The distance and angle between correlated vertexes are calculated and saved as an attribute value for each point of the dataset. 
The resulting lakeID attribute table is saved to a .csv-file (folder "2_PyShore_Output").

## Visualisation

#### BatchCSVtoSHP.py 
Converts every lakeID.csv file to an ESRI Shapefile for visualisation. 

#### batchloadcsv_qgs.py 
Allows batch import to QGIS 2.18+


