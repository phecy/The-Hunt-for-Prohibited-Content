#!/usr/bin/env python

"convert data to VW format"

import csv
import sys
import pandas
from construct_line import *

input_file = sys.argv[1]
output_file = sys.argv[2]

print_counter_every = 1e5


#df = pandas.read_csv(input_file)

reader = csv.DictReader( open( input_file, 'rb' ), delimiter = '\t' )
o_f = open( output_file, 'wb' )
n = 0
for line in reader:
	
	new_line = construct_line( line )
	o_f.write( new_line )
	
	n += 1
	if n % print_counter_every == 0:
		print n	
	
