# morph_index_docker

### Following river basin parameters are calculated:

| Parameter | Symbol | Calculation | Reference |
| --- | --- | ---| --- |
| Basin Area | A | GRASS Tool | |
| Basin Perimeter | P | GRASS Tool | |
| Main Channel Length | MCL | GRASS Tool | |
| Maximal Elevation | Hmax | GRASS Tool | |
| Minimal Elevation | Hmin | GRASS Tool | |
| Mean Elevation | Hmean | GRASS Tool | |
| Average Basin Slope | Sb | GRASS Tool | |
| Total Stream Length | Lu | GRASS Tool | |
| Bifurcation Ratio | Rb | GRASS Tool | |
| Average Mainstream Slope | Sms | GRASS Tool | |
| Circularity Ratio | Rc | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{4\pi*A}{P^2}) | |
| Elongation Ratio | Re | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{2*\sqrt{\frac{A}{\pi}}}{MCL}) | |
| Form Factor | Ff | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{A}{MCL^2}) | |
| Relative Relief | H | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}H_{max}-H_{min}) | |
| Relief Ratio | Rr | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{MCL}) | |
| Dissection Index | Di | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{H_{max}}) | |
| Hypsometric Integral | | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H_{mean}-H_{min}}{H}) | |
| Channel Gradient | Cg | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{\frac{\pi}{2}*\frac{\frac{Lu}{Lu-1}}{Rb}}) | |
| Slope Ratio | Rs| ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{S_{ms}}{S_{b}}) | |


__Copy files from Docker Container to Local__:
`docker cp <container-id>:/file/path/within/container /local/path`
The location of the output SHP-file will get printed after successful execution of the program. For instance, the output of the sample input dataset is stored at "/app/output/Hydrosheds_level8_centralVN_index" in the docker container; so the "/file/path/within/container" would be "/app/output/Hydrosheds_level8_centralVN_index"
