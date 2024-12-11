#!/bin/bash
while read -r url filename; do
    wget -c "$url" -O "./musics/$filename"
done < links.txt
