set term png
set out "volume.png"
set xrange[0:1000]
set yrange[0:0.15]
p "volume.dat"
