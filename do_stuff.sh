#!/bin/bash

for dir in ./*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	for file in $dir/*.static
	do
		mv $file $file.avr
	done
done
