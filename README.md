# morph_index_docker

### Following river basin parameters are calculated:

| Parameter | Symbol | Calculation | Reference |
| --- | --- | ---| --- |
| Basin Area | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}A) | GRASS Tool | |
| Basin Perimeter | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}P) | GRASS Tool | |
| Main Channel Length | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}MCL) | GRASS Tool | |
| Maximum Relief or Absolute Relief | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Z or R_{a}) | GRASS Tool | |
| Minimum Relief | z | GRASS Tool | |
| Mean Elevation | Hmean | GRASS Tool | |
| Average Basin Slope | Sb | GRASS Tool | |
| Total Stream Length | Lu | GRASS Tool | |
| Bifurcation Ratio | Rb | GRASS Tool | |
| Average Mainstream Slope | Sms | GRASS Tool | |
| Circularity Ratio | Rc | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{4\pi*A}{P^2}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Mahala(2019)^1) |
| Elongation Ratio | Re | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{2*\sqrt{\frac{A}{\pi}}}{MCL}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Schumm(1956)^4) |
| Form Factor | Ff | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{A}{MCL^2}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Horton(1932)^6) |
| Total Basin Relief | H | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}Z-z) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Rai(2017)^2,Pandi(2017)^3) |
| Relief Ratio | Rr | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{MCL}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Schumm(1956)^4) |
| Dissection Index | Di | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{Ra}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Mahala(2019)^1,Rai(2017)^2) |
| Hypsometric Integral | | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H_{mean}-z}{H}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Strahler(1952)^5) |
| Channel Gradient | Cg | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{\frac{\pi}{2}*\frac{\frac{Lu}{Lu-1}}{Rb}}) | ![text](https://latex.codecogs.com/gif.latex?\dpi{150}Rai(2017)^2,Pandi(2017)^3) |
| Slope Ratio | Rs| ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{S_{ms}}{S_{b}}) | ?? |


__Copy files from Docker Container to Local__:<br>
`docker cp <container-id>:/file/path/within/container /local/path`
<br><br>
The location of the output SHP-file will get printed after successful execution of the program. For instance, the output of the sample input dataset is stored at **/app/output/Hydrosheds_level8_centralVN_index** in the docker container; so the 
`/file/path/within/container` 
would be **/app/output/Hydrosheds_level8_centralVN_index**
