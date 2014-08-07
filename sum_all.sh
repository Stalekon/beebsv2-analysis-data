#!/bin/bash

for dir in ./*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	#echo $dir/*
	./sum_stuff.py $dir/* $dir/${name}-combined.gimpdump
done
