# morph_index_docker

This program calculates selected hydromorphological parameters using Python3 and GRASS GIS running inside a Docker environment. It takes user-defined DEM <i>(in geotiff format)</i> and river basins <i>(in shp format)</i> as input and outputs a SHP-file with an attribute table containing all calculted parameters of each basin.

## Following river basin parameters are calculated:

| Parameter | Symbol | Calculation | Reference |
| --- | --- | ---| --- |
| Basin Area | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}A) | GRASS Tool | |
| Basin Perimeter | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}P) | GRASS Tool | |
| Main Channel Length | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}MCL) | GRASS Tool | |
| Maximum Relief or Absolute Relief | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Z/R_{a}) | GRASS Tool | |
| Minimum Relief | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}z) | GRASS Tool | |
| Mean Elevation | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}H_{mean}) | GRASS Tool | |
| Average Basin Slope | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}S_{b}) | GRASS Tool | |
| Total Stream Length | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}L_{u}) | GRASS Tool | |
| Bifurcation Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{b}) | GRASS Tool | |
| Average Mainstream Slope | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}S_{ms}) | GRASS Tool | |
| Circularity Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{c}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{4\pi*A}{P^2}) | <i>Mahala(2019)<sup>1</sup></i> |
| Elongation Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{e}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{2*\sqrt{\frac{A}{\pi}}}{MCL}) | <i>Pandi(2017)<sup>2</sup>, Schumm(1956)<sup>4</sup></i> |
| Form Factor | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}F_{f}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{A}{MCL^2}) | <i>Pandi(2017)<sup>2</sup>, Horton(1932)<sup>6</sup></i> |
| Relative Relief | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}H) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}Z-z) | <i>Mahala(2019)<sup>1</sup></i> |
| Relief Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{r}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{MCL}) | <i>Pandi(2017)<sup>2</sup>, Schumm(1956)<sup>4</sup></i> |
| Dissection Index | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}D_{i}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{Ra}) | <i>Mahala(2019)<sup>1</sup>, Rai(2017)<sup>3</sup></i> |
| Hypsometric Integral | | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H_{mean}-z}{H}) | <i>Strahler(1952)<sup>5</sup>??</i> |
| Channel Gradient | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}C_{g}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{\frac{\pi}{2}*Cl_{p}}) | <i>Rai(2017)<sup>3</sup></i> |
| Slope Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{s}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{S_{ms}}{S_{b}}) | ?? |

<p><i><sup>1</sup>Mahala, A. (2019). The significance of morphometric analysis to understand the hydrological and morphological characteristics in two different morpho-climatic settings. Applied Water Science, 10(1). doi:10.1007/s13201-019-1118-2</i></p>
<p><i><sup>2</sup>P. Dinagara Pandi, T. Thena, B. Nirmal, M. R. Aswathy, K. Saravanan & K.
Mohan (2017) Morphometric analyses of Neyyar River Basin, southern Kerala, India, Geology,
Ecology, and Landscapes, 1:4, 249-256, doi: 10.1080/24749508.2017.1389494</i></p>
<p><i><sup>3</sup>Rai, P.K., Chaubey, P.K., Mohan, K. et al. Geoinformatics for assessing the inferences of quantitative drainage morphometry of the Narmada Basin in India. Appl Geomat 9, 167–189 (2017). doi: 10.1007/s12518-017-0191-1</i></p>
<p><i><sup>4</sup>Schumm, S. A. (1956). Evolution of drainage systems & slopes in badlands at Perth Anboy, New Jersey. Geological Society of America Bulletin, 67, 597–646.</i></p>
<p><i><sup>5</sup>Strahler, A. N. (1952). Hypsometric analysis of erosional topography. Bulletin of the Geological Society of America, 63, 17–42.</i></p>
<p><i><sup>6</sup>Horton, R. E. (1932). Drainage-basin characteristics. Transactions, American Geophysical Union, 13, 350–361.</i></p>


## Usage
1. __Clone this repository to Local.__
<br>
2. __Place the input DEM and basin in the `/input` folder.__ (just like the attached sample DEM 'hydrosheds_90m.tif' and basin SHP-file 'Hydrosheds_level8_centralVN.shp')
<br>
3. __Let the input data be your own data.__ please replace the <b><i>line 758~760</i></b> of the python script `/script/morph_index.py` with the file names of your own input data and define the coordinate reference system (CRS) as well.

4. __Build Docker Image__:<br>
`(sudo) docker build --tag <image_tag>:<version> .`
<br><br>

5. __Run the program in Container__:<br>
`(sudo) docker runn --publish <host_port>:<container_port> --name <container_name> <image_tag>:<version>`
<br><br>

6. __Copy files from Docker Container to Local__:<br>
`(sudo) docker cp <container-id>:/file/path/within/container /local/path`
<br><br>
The location of the output SHP-file will get printed after successful execution of the program. For instance, the output of the sample input dataset is stored at **/app/output/Hydrosheds_level8_centralVN_index** in the docker container; so the 
`/file/path/within/container` 
would be **/app/output/Hydrosheds_level8_centralVN_index**
