#!/bin/bash

for dir in ./data2/*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	#echo $dir/*
	./sum_stuff.py $dir/*.gimpdump $dir/${name}-combined.gimpdump
done
