#!/bin/sh

while read item; do
    dir=~/"food_data/$item"
    mkdir -p $dir
    python scrapeImages.py --search "$item" --directory $dir
done <ingredients.txt

