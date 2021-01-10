# morph_index_docker

### Following river basin parameters are calculated:

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
| Circularity Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{c}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{4\pi*A}{P^2}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Mahala(2019)^1) |
| Elongation Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{e}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{2*\sqrt{\frac{A}{\pi}}}{MCL}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Pandi(2017)^2,Schumm(1956)^4) |
| Form Factor | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}F_{f}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{A}{MCL^2}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Pandi(2017)^2,Horton(1932)^6) |
| Total Basin Relief | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}H) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}Z-z) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Pandi(2017)^2,Rai(2017)^3) |
| Relief Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{r}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{MCL}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Pandi(2017)^2,Schumm(1956)^4) |
| Dissection Index | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}D_{i}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{Ra}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Mahala(2019)^1,Rai(2017)^3) |
| Hypsometric Integral | | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H_{mean}-z}{H}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Strahler(1952)^5??) |
| Channel Gradient | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}C_{g}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{\frac{\pi}{2}*Cl_{p}}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Rai(2017)^3) |
| Slope Ratio | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}R_{s}) | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{S_{ms}}{S_{b}}) | ?? |

<p><i><sup>1</sup>Mahala, A. (2019). The significance of morphometric analysis to understand the hydrological and morphological characteristics in two different morpho-climatic settings. Applied Water Science, 10(1). doi:10.1007/s13201-019-1118-2</i></p>


__Copy files from Docker Container to Local__:<br>
`docker cp <container-id>:/file/path/within/container /local/path`
<br><br>
The location of the output SHP-file will get printed after successful execution of the program. For instance, the output of the sample input dataset is stored at **/app/output/Hydrosheds_level8_centralVN_index** in the docker container; so the 
`/file/path/within/container` 
would be **/app/output/Hydrosheds_level8_centralVN_index**
