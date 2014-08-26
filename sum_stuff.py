#!/usr/bin/env python

import sys

pool_stmts = []
pool_bb_edges = []
pool_bb_stmts = []

first_line = ''

for arg in sys.argv[:-1]:
	with open(arg,'r') as f:
		for line in f:

			if line[0] == '#':
				first_line = line

			if line[0] == '>':
				gstmt = line.split(':')
				for existing in pool_stmts:
					if gstmt[0] == existing[0]:
						existing[1]+=int(gstmt[1])
						break
				else:
					new_stmt = [gstmt[0], int(gstmt[1])]
					pool_stmts.append(new_stmt)

			if line[0] == '*':
				parts = line.split(';')
				bb_edges = [parts[0], int(parts[1].split(':')[1])]

				for existing in pool_bb_edges:
					if bb_edges[0] == existing[0]:
						existing[1]+=bb_edges[1]
						break
				else:
					pool_bb_edges.append(bb_edges)

			if line[0] == '+':
				parts = line.split(';')
				bb_stmts = [int(parts[0].split(':')[1]), int(parts[1].split(':')[1])]

				for existing in pool_bb_stmts:
					if bb_stmts[0] == existing[0]:
						existing[1]+=bb_stmts[1]
						break
				else:
					pool_bb_stmts.append(bb_stmts)

pool_stmts.sort()
pool_bb_edges.sort()
pool_bb_stmts.sort()

with open(sys.argv[-1],'w') as out:

	out.write(first_line)

	out.write("/"+50*"="+"\\" + "\n")

	for stmt in pool_stmts:
		out.write(stmt[0] + ": " + str(stmt[1]) + "\n")

	for bb_edges in pool_bb_edges:
		out.write(bb_edges[0] + "; Count: " + str(bb_edges[1]) + "\n")

	for bb_stmts in pool_bb_stmts:
		out.write("+ Basic blocks with this many statments: " +
				str(bb_stmts[0]) + ";" +
				" Count: " + str(bb_stmts[1]) + "\n")

	out.write("\\"+50*"="+"/" + "\n")
	