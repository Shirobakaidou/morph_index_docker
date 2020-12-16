# morph_index_docker

### Following river basin parameters are calculated:

| Parameter | Symbol | Calculation | Reference |
| --- | --- | ---| --- |
| Basin Area | A | GRASS Tool | |
| Basin Perimeter | P | GRASS Tool | |
| Circularity Ratio | Rc | 4\pi*A/P^2| |
| Main Channel Length | MCl | GRASS Tool | |
| Elongation Ratio | Re | ![equation](https://latex.codecogs.com/gif.latex?\dpi{300}\frac{2*\sqrt{A/\pi}}{MCL}) | |
| Form Factor | Ff | \frac{A}{MCL^2} | |
| Maximal Elevation | Hmax | GRASS Tool | |
| Minimal Elevation | Hmin | GRASS Tool | |
| Relative Relief | H | Hmax - Hmin | |
| Mean Elevation | Hmean | GRASS Tool | |
| Relief Ratio | Rr | H/MCL | |
| Dissection Index | Di | H/Hmax | |
| Hypsometric Integral | | \frac{Hmean-Hmin}{H} | |
| Average Basin Slope | Sb | GRASS Tool | |
| Total Stream Length | Lu | GRASS Tool | |
| Bifurcation Ratio | Rb | GRASS Tool | |
| Channel Gradient | Cg | \frac{H}{\frac{\pi}{2}*\frac{\frac{Lu}{Lu-1}}{Rb}} | |
| Average Mainstream Slope | Sms | GRASS Tool | |
| Slope Ratio | Rs| Sms/Sb| |


__Copy files from Docker Container to host__:
docker cp <container-id>:/file/path/within/container /host/path
