#!/usr/bin/env python

import sys

pool = []

first_line = ''

for arg in sys.argv[:-1]:
	f = open(arg,'r')
	for line in f:

		if line[0] == '#':
			first_line = line

		if line[0] == '>':
			data = line.split(':')
			for existing in pool:
				if data[0] == existing[0]:
					existing[1]+=int(data[1])
					break
			else:
				new_stmt = [data[0], int(data[1])]
				pool.append(new_stmt)
	f.close()

pool.sort()

out = open(sys.argv[-1],'w')

out.write(first_line)

out.write("/"+50*"="+"\\" + "\n")

for stmt in pool:
	out.write(stmt[0] + ": " + str(stmt[1]) + "\n")

out.write("\\"+50*"="+"/" + "\n")
out.close
	