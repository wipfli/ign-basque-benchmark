#!/bin/bash
osmium extract --bbox=-1.73430,43.2404848,-1.3204619,43.44051097 planet.osm.pbf -o basque.osm.pbf --progress
osmium tags-filter basque.osm.pbf -o basque-highway.osm.pbf --overwrite --progress w/highway=*
