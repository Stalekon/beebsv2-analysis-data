#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
import numpy as np

#USAGE: You have to pass this script all *-combined.gimpdump files
#for all benchmarks as arguments.

#To store the data about the bechmarks
#['name',types_dict,total_stmts_count,ignored_stmts_count]
bench_data = []

#The legend entries are the different type counts of edges
instr_legend = ["ALU operations",
			    "Data movement",
			    "Memory operations",
			    "Control Flow",
			    "Miscellaneous"]

instr_groups = [['ALU operations', instr_legend[0]],
			    ['Data movement', instr_legend[1]],
			    ['Memory', instr_legend[2]],
			    ['Control Flow', instr_legend[3]],
			    ['Miscellaneous', instr_legend[4]]]

#
#Data retrieval
#

for arg in sys.argv[1:]:
	with open(arg,'r') as f:
		bench_name = arg.split('/')[-1].split('.')[0]

		#Dict to save data for curr benchmark
		dict_counts = {}

		total_instr = 0

		for it in instr_legend:
			dict_counts[it] = 0

		for line in f:
			if line[0] == '>':

				line = line[2:]
				data = line.split(':')

				for it in instr_groups:
					if data[0] == it[0]:
						dict_counts[it[1]] += int(data[1])
						total_instr += int(data[1])

		bench_data.append([bench_name,dict_counts,total_instr])

#
#Plotting part
#

N = len(bench_data)
ind = np.arange(N)   # the x locations for the groups
layers_of_bars = [[] for x in xrange(len(instr_groups))]
width = 0.8       # the width of the bars: can also be len(x) sequence

#List holding names of diff benchmarks used in plotting
bench_names = []

for bench in bench_data:
	bench_names.append(bench[0])

	for i, it in enumerate(instr_legend):
		#This is the percentage of the diff counts.
		#bench[1] is the dictionary with all counts of the
		#different types and bench[2] is the total count.
		layers_of_bars[i].append(bench[1][it]*100/float(bench[2]))

#This var holds the height of all bars so far.
#Used to know where from to draw next layer of
#the bars
summ_of_botts = [0]*N

#The different colors used to color the bars
colors = ['#cc0000', '#ffcc00', '#009900', '#0066ff', '#663399']

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
plt.legend(bars , instr_legend, loc='center left', bbox_to_anchor=(1, 0.5),
	title="Groups of Instructions")

plt.xticks(ind+width/2., bench_names, rotation=90)
plt.ylabel("Percentage of instructions")

plt.axis('tight')

#Adjusting some proportions. It's nice for the
#current figsize but might need adjusting if changed.
plt.subplots_adjust(left=0.04, bottom=0.20, right=0.84, top=0.97)

plt.savefig('avr_static_analysis.png')

#plt.show()
