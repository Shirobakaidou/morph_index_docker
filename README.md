# morph_index_docker
<br>
### Following river basin parameters are calculated:
<br>
1. **Basin Area (A)** *(GRASS GIS Tool)*
2. **Basin Perimeter (P)** *(GRASS GIS Tool)*
3. **Circularity Ratio (Rc)** = 4\pi*A/P^2
4. **Main Channel Length (MCl)** *(GRASS GIS Tool)*
5. **Elongation Ratio (Re)** = \frac{2*\sqrt{A/\pi}}{MCL}
6. **Form Factor (Ff)** = \frac{A}{MCL^2}
7. **Maximal Elevation (Hmax)** *(GRASS GIS Tool)*
8. **Minimal Elevation (Hmin)** *(GRASS GIS Tool)*
9. **Relative Relief (H)** = Hmax - Hmin
10. **Mean Elevation (Hmean)** *(GRASS GIS Tool)*
11. **Relief Ratio (Rr)** = H/MCL
12. **Dissection Index (Di)** = H/Hmax
13. **Hypsometric Integral** = \frac{Hmean-Hmin}{H}
14. **Average Basin Slope (Sb)** *(GRASS GIS Tool)*
15. **Total Stream Length (Lu)** *(GRASS GIS Tool)*
16. **Bifurcation Ratio (Rb)** *(GRASS GIS Tool)*
17. **Channel Gradient (Cg)** = \frac{H}{\frac{\pi}{2}*\frac{\frac{Lu}{Lu-1}}{Rb}}
18. **Average Mainstream Slope (Sms)** *(GRASS r.basin module)*
19. **Slope Ratio (Rs)** = Sms/Sb


__Copy files from Docker Container to host__:
docker cp <container-id>:/file/path/within/container /host/path
