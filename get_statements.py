#!/usr/bin/env python

import sys

pool = []

for arg in sys.argv:
	with open(arg,'r') as f:
		for line in f:
			if line[0] == '>':
				data = line.split(':')
				if not (data[0] in pool):
					pool.append(data[0])

pool.sort()

for l in pool:
	print l
	