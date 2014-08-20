#!/usr/bin/env python

import sys

pool = []

for arg in sys.argv:
	f = open(arg,'r')
	for line in f:
		if line[0] == '>':
			data = line.split(':')
			if not (data[0] in pool):
				pool.append(data[0])
	f.close()

pool.sort()

for l in pool:
	print l
	