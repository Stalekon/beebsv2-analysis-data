#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
import numpy as np

#USAGE: You have to pass this script all *-combined.gimpdump files
#for all benchmarks as arguements.

#Like a template for the grouped data of each benchmark
gimple_types = [None]*8

gimple_types[0] = [["GimpleAssign Binary BitAndExpr",
"GimpleAssign Binary BitIorExpr", "GimpleAssign Binary BitXorExpr",
"GimpleAssign Unary BitNotExpr", "GimpleAssign Binary LshiftExpr",
"GimpleAssign Binary RshiftExpr", "GimpleAssign Binary RrotateExpr"],
"Logic and Shifts"]

gimple_types[1] = [["GimpleAssign Binary MinusExpr",
"GimpleAssign Binary PlusExpr", "GimpleAssign Binary PointerPlusExpr",
"GimpleAssign Binary MultExpr", "GimpleAssign Binary ExactDivExpr",
"GimpleAssign Binary RdivExpr", "GimpleAssign Binary TruncDivExpr",
"GimpleAssign Binary TruncModExpr", "GimpleAssign Unary AbsExpr",
"GimpleAssign Unary NegateExpr", "GimpleAssign Binary MaxExpr",
"GimpleAssign Binary MinExpr"],
"Regular Arithmetic"]

gimple_types[2] = [["GimpleAssign Constant IntegerCst",
"GimpleAssign Constant RealCst", "GimpleAssign Constant StringCst",
"GimpleAssign Declaration ParmDecl", "GimpleAssign Declaration VarDecl"],
"Assignments of value"]

gimple_types[3] = [["GimpleAssign Unary ConvertExpr",
"GimpleAssign Unary FloatExpr", "GimpleAssign Unary FixTruncExpr"],
"Type Conversions"]

gimple_types[4] = [["GimpleAssign Comparison EqExpr",
"GimpleAssign Comparison GeExpr" "GimpleAssign Comparison GtExpr",
"GimpleAssign Comparison LeExpr", "GimpleAssign Comparison LtExpr",
"GimpleAssign Comparison NeExpr", "GimpleCond Comparison EqExpr",
"GimpleCond Comparison GeExpr", "GimpleCond Comparison GtExpr",
"GimpleCond Comparison LeExpr", "GimpleCond Comparison LtExpr",
"GimpleCond Comparison NeExpr"],
"Comparisons"]

gimple_types[5] = [["GimpleCond Comparison EqExpr",
"GimpleCond Comparison GeExpr", "GimpleCond Comparison GtExpr",
"GimpleCond Comparison LeExpr", "GimpleCond Comparison LtExpr",
"GimpleCond Comparison NeExpr", "GimpleSwitch VlExp CallExpr",
"GimpleCall VlExp CallExpr", "GimpleReturn"],
"Branch"]

gimple_types[6] = [["GimpleAssign Expression AddrExpr",
"GimpleAssign Reference ArrayRef", "GimpleAssign Reference ComponentRef",
"GimpleAssign Reference MemRef"],
"Memory referencing"]

gimple_types[7] = [["GimpleAssign Tree Constructor"],
"Other"]

#To store the data about the bechmarks
#['name',types_dict,total_stmts_count,ignored_stmts_count]
bench_data = []

#
#Data retrieval
#

for arg in sys.argv[1:]:
	with open(arg,'r') as f:
		bench_name = arg.split('/')[-1].split('-')[:-1]
		bench_name = '-'.join(bench_name)

		#Dict to save data for curr benchmark
		curr_gimp_types = {}

		#Vars used to count total number of statements that were 
		#put in a category and statements that dont belong to any
		#and were ignored.
		total_stmts = 0
		ignored_stmts = 0

		for gt in gimple_types:
			curr_gimp_types[gt[1]] = 0

		for line in f:
			if line[0] == '>':
				ignored = True

				line = line[2:]
				data = line.split(':')

				for gt in gimple_types:
					if data[0] in gt[0]:
						curr_gimp_types[gt[1]] += int(data[1])
						total_stmts += int(data[1])
						ignored = False

				if ignored:
					ignored_stmts += int(data[1])

		bench_data.append([bench_name,curr_gimp_types,total_stmts,ignored_stmts])

#
#Plotting part
#

N = len(bench_data)
ind = np.arange(N)   # the x locations for the groups
layers_of_bars = [[] for x in xrange(len(gimple_types))]
width = 0.8       # the width of the bars: can also be len(x) sequence

legend_strings = []
bench_names = []

#The legend entries are the different type of statements
for gt in gimple_types:
	legend_strings.append(gt[1])

for bench in bench_data:
	bench_names.append(bench[0])

	for i, ls in enumerate(legend_strings):
		#This is the percentage of the gimple statements.
		#bench[1] is the dictionary with all counts of the
		#different types and bench[2] is the total count.
		layers_of_bars[i].append(bench[1][ls]*100/float(bench[2]))

#This var holds the height of all bars so far.
#Used to know where from to draw next layer of
#the bars
summ_of_botts = [0]*N

#The different colors used to color the bars
colors = ['#cc0000', '#cc3300', '#ffcc00', '#009900',
		  '#006666', '#0066ff', '#0000cc', '#663399']

#Stores all the bars. Used in legend generation
bars = []

#Size of the generated image in inches
plt.figure(figsize=(20.0, 10.0))

#Generates the bars on a layer per layer basis simultaneously.
for i,layer in enumerate(layers_of_bars):
	p = plt.bar(ind, layer, width, color=colors[i] , bottom=summ_of_botts)
	bars.append(p)
	summ_of_botts = [x+y for x,y in zip(summ_of_botts,layer)]

#Taking what we need from the bars. (No idea what,
#just following examples)
for b in bars:
	b = b[0]

#Various graph formating
plt.legend(bars , legend_strings, loc='center left', bbox_to_anchor=(1, 0.5),
	title="Groups of Statements")

plt.xticks(ind+width/2., bench_names, rotation=90)
plt.ylabel("Percentage of gimple statements")

plt.axis('tight')

#Adjusting some proportions. It's nice for the
#current figsize but might need adjusting if changed.
plt.subplots_adjust(left=0.04, bottom=0.20, right=0.84, top=0.97)

plt.savefig('gimple_analysis.png')

#plt.show()
