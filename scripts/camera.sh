#!/bin/bash

python3 ~/infra-light.py ON

sleep 1

DATE=$(date +%Y-%m-%d"-"%H%M%S);

echo $DATE


raspistill -o /tmp/$DATE.jpg -ISO 800 -ex auto -awb auto -w 800 -h 600 -q 10 -a 12

python3 ~/infra-light.py OFF

cp /tmp/$DATE.jpg /var/www/html/current.jpg
mv /tmp/$DATE.jpg /var/www/html/img/

#remove old files
rm /tmp/img*.jpg

find /var/www/html/img/ -mtime +3 -type f -name '*.jpg' -execdir rm -- '{}' \;

#create new set of symbolic links
x=1; for i in $(ls -rt /var/www/html/img/*.jpg); do counter=$(printf %03d $x); ln -s "$i" /tmp/img"$counter".jpg; x=$(($x+1)); done


#create the movie
~/movie.sh
