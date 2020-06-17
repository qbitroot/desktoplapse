#!/bin/bash

fname=${2:-$(date +%s).mp4}
ffmpeg -framerate $1 -i cap/%06d.jpg -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p -s 1600x530 $fname
echo "Wrote output video to $fname";
du -sh $fname
