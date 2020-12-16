# morph_index_docker

### Following river basin parameters are calculated:

| Parameter | Symbol | Calculation | Reference |
| --- | --- | ---| --- |
| Basin Area | A | GRASS Tool | |
| Basin Perimeter | P | GRASS Tool | |
| Circularity Ratio | Rc | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{4\pi*A}{P^2}) | |
| Main Channel Length | MCl | GRASS Tool | |
| Elongation Ratio | Re | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{2*\sqrt{A/\pi}}{MCL}) | |
| Form Factor | Ff | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{A}{MCL^2}) | |
| Maximal Elevation | Hmax | GRASS Tool | |
| Minimal Elevation | Hmin | GRASS Tool | |
| Relative Relief | H | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}Hmax-Hmin) | |
| Mean Elevation | Hmean | GRASS Tool | |
| Relief Ratio | Rr | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{MCL}) | |
| Dissection Index | Di | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{Hmax}) | |
| Hypsometric Integral | | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{Hmean-Hmin}{H}) | |
| Average Basin Slope | Sb | GRASS Tool | |
| Total Stream Length | Lu | GRASS Tool | |
| Bifurcation Ratio | Rb | GRASS Tool | |
| Channel Gradient | Cg | ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{H}{\frac{\pi}{2}*\frac{\frac{Lu}{Lu-1}}{Rb}}) | |
| Average Mainstream Slope | Sms | GRASS Tool | |
| Slope Ratio | Rs| ![equation](https://latex.codecogs.com/gif.latex?\dpi{150}\frac{Sms}{Sb} | |


__Copy files from Docker Container to host__:
docker cp <container-id>:/file/path/within/container /host/path
