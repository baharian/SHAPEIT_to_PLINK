"""
Copyright (c) 2012, 2013 The PyPedia Project, http://www.pypedia.com
<br>All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

http://www.opensource.org/licenses/BSD-2-Clause
"""

"""
Modified by Soheil Baharian on March 5, 2014
"""

import gzip
import sys

if (len(sys.argv) < 2 or len(sys.argv) > 6):
	print 'ERROR: invalid input parameters'
	print 'input files in SHAPEIT2 format: {SHAPEIT.haps} {SHAPEIT.sample}'
	print 'output files in IMPUTE2 format: {IMPUTE.haps} {IMPUTE.legend} {IMPUTE.sample}'
	print 'NOTE: input files can be uncompressed or gzip-compressed (.gz)'
	print 'USAGE: convert_shapeit2_to_impute2.py {SHAPEIT.haps} {SHAPEIT.sample} {IMPUTE.haps} {IMPUTE.legend} {IMPUTE.sample}'
	quit()

input_haps_filename = sys.argv[1]
input_sample_filename = sys.argv[2]
output_haps_filename = sys.argv[3]
output_legend_filename = sys.argv[4]
output_sample_filename = sys.argv[5]

print '\n'
print 'converting'
print '   ' + input_haps_filename
print '   ' + input_sample_filename
print 'from SHAPEIT2 format to'
print '   ' + output_haps_filename
print '   ' + output_legend_filename
print '   ' + output_sample_filename
print 'in IMPUTE2 format.'

# check for gzip-compressed .haps input file
if input_haps_filename.lower().endswith('.gz'):
	input_haps_file = gzip.open(input_haps_filename)
else:
	input_haps_file = open(input_haps_filename)
# check for gzip-compressed .haps input file
if input_sample_filename.lower().endswith('.gz'):
	input_sample_file = gzip.open(input_sample_filename)
else:
	input_sample_file = open(input_sample_filename)

output_haps_file = open(output_haps_filename, 'w')
output_legend_file = open(output_legend_filename, 'w')
output_sample_file = open(output_sample_filename, 'w')

# skip SHAPEIT sample first 2 lines
input_sample_header_1 = input_sample_file.readline().replace('\n', '').split()
input_sample_file.readline()
if 'sex' in input_sample_header_1:
	sex_index = input_sample_header_1.index('sex')
else:
	sex_index = None

input_sample = [x.replace('\n', '').split() for x in input_sample_file]

# write output sample file	
output_sample_file.write('sample sex\n')
output_sample_file.write('\n'.join([' '.join([input_sample[i][1], input_sample[i][sex_index] if sex_index else '-9']) for i in range(len(input_sample))]) + '\n')
#output_sample_file.write('sample population group sex\n')
#output_sample_file.write('\n'.join([' '.join(['SAMPLE_' + str(i+1), 'POPULATION', 'GROUP', input_sample[i][sex_index] if sex_index else '-9']) for i in range(len(input_sample))]) + '\n')

# write output legend header
output_legend_file.write('ID pos allele0 allele1\n')	

line_counter = 0	
for input_haps_line in input_haps_file:
	line_counter += 1
	if line_counter % 10000 == 0:
		print 'SNPs:', line_counter
	input_haps_s = input_haps_line.replace('\n', '').split()

	legend_to_print = [input_haps_s[1], input_haps_s[2], input_haps_s[3], input_haps_s[4]]
	haps_to_print = input_haps_s[5:]

	# save legend
	output_legend_file.write(' '.join(legend_to_print) + '\n')

	# save haps
	output_haps_file.write(' '.join(haps_to_print) + '\n')

output_sample_file.close()
output_haps_file.close()
output_legend_file.close()
input_haps_file.close()
input_sample_file.close()

print 'Output 1:', output_haps_filename
print 'Output 2:', output_legend_filename
print 'Output 3:', output_sample_filename
print '\n'
