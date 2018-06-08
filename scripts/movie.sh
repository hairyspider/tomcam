#!/bin/bash

rm /tmp/out.mp4

ffmpeg -framerate 20 -i /tmp/img%03d.jpg -c:v h264_omx -b:v 1500k /tmp/out.mp4

cp -rf /tmp/out.mp4 /var/www/html/img/
