import gzip
import os
import sys
import time

def Convert_impute2_to_PEDMAP(
	chromosome = None, 
	legend_file = None, 
	haplotypes_file = None, 
	sample_names = None,
	sample_names_filename = None,
	family_id = None,
	family_id_filename = None,
	p_id = None,
	p_id_filename = None,
	m_id = None,
	m_id_filename = None,
	gender = None,
	gender_filename = None,
	pheno = None,
	pheno_filename = None,
	output = None, 
	):

	if not output:
		output = os.path.splitext(legend_file)[0]
	map_filename = output + ".map"
	ped_filename = output + ".ped"

	# skip first line (header) of .legend file
	legend = [x.replace('\n', '').split() for x in open(legend_file, 'r').readlines()[1:]]
	SNPs = len(legend)

	# generating the .MAP file
	print "\nsaving .MAP file..."

	map_file = open(map_filename, 'w')

	for L in legend:
		map_file.write(str.join('\t', [str(chromosome), L[0], "0", L[1]]) + '\n')

	map_file.close()

	print "...done saving .MAP file"

	# generating the .PED file
	print "\nsaving .PED file..."

	haplotypes = open(haplotypes_file, 'r')
	totalIndivs = len(haplotypes.readline().replace('\n', '').split()) / 2
	haplotypes.seek(0)

	# generating the pedigree info from .sample file
	pedInfo = []
	currentIndiv = 0
	while currentIndiv < totalIndivs:
		pedInfo.append([family_id[currentIndiv], sample_names[currentIndiv], p_id[currentIndiv], m_id[currentIndiv], gender[currentIndiv], pheno[currentIndiv]]) 
		currentIndiv += 1

	# break the file into parts containing fieldsToRead columns, i.e., fieldsToRead/2 individuals
	fieldsToRead = 100

	if totalIndivs < (fieldsToRead / 2):	# if sample size is small...
		print "processing all individuals..."
		ped_file = open(ped_filename, 'w')

		H = haplotypes.readlines()
		haps = [x.replace('\n', '').split() for x in H]

		# map (0,1)'s -> (A, T, C, G)'s according to the .legend file, going SNP by SNP
		SNPIndex = 0
		while SNPIndex < SNPs:
			legendGeno = legend[SNPIndex][2:]	# determine the mapping

			# perform the conversion
			for index, value in enumerate(haps[SNPIndex]):
				if haps[SNPIndex][index] == "0":
					haps[SNPIndex][index] = legendGeno[0]
				else:
					haps[SNPIndex][index] = legendGeno[1]

			# shift to the next SNP
			SNPIndex += 1

		# transpose to get the .PED formatting
		haps_tr = []
		currentIndiv = 0
		while currentIndiv < totalIndivs:
			haps_tr.append([])	# make an empty list for each individual

			# populate the list by going through SNPs
			SNPIndex = 0
			while SNPIndex < SNPs:
				haps_tr[-1].extend(haps[SNPIndex][currentIndiv * 2 : currentIndiv * 2 + 2])

				# shift to the next SNP
				SNPIndex += 1

			currentIndiv += 1

		# write the .PED file
		currentIndiv = 0
		while currentIndiv < totalIndivs:
			# if sample size is small, the variable 'block' is effectively 1, so...
			#ped_file.write(str.join('\t', pedInfo[(block - 1) * (fieldsToRead / 2) + currentIndiv] + haps_tr[currentIndiv]) + '\n')
			ped_file.write(str.join('\t', pedInfo[currentIndiv] + haps_tr[currentIndiv]) + '\n')
			currentIndiv += 1

		haplotypes.close()
		ped_file.close()
	else:	# if sample size is large...
		ped_file = open(ped_filename, 'a')

		haplotypes.close()
		# assign a semi-random name to the temporary file to avoid collision with other processes doing the same conversion
		haplotypes_file_temp = "block" + str(chromosome) + time.strftime("%H%M%S") + ".haps"

		block = 1
		while block * (fieldsToRead / 2) < totalIndivs:
			print "processing individuals", ((block - 1) * (fieldsToRead / 2) + 1), "to", (block * (fieldsToRead / 2)), "..."
			os.system("cut -d' ' -f" + str((block - 1) * fieldsToRead + 1) + "-" + str(block * fieldsToRead) + " " + haplotypes_file + " > " + haplotypes_file_temp)

			haplotypes = open(haplotypes_file_temp, 'r')

			numIndivs = len(haplotypes.readline().replace('\n', '').split()) / 2
			haplotypes.seek(0)

			H = haplotypes.readlines()
			haps = [x.replace('\n', '').split() for x in H]

			# map (0,1)'s -> (A, T, C, G)'s according to the .legend file, going SNP by SNP
			SNPIndex = 0
			while SNPIndex < SNPs:
				legendGeno = legend[SNPIndex][2:]	# determine the mapping

				# perform the conversion
				for index, value in enumerate(haps[SNPIndex]):
					if haps[SNPIndex][index] == "0":
						haps[SNPIndex][index] = legendGeno[0]
					else:
						haps[SNPIndex][index] = legendGeno[1]

				# shift to the next SNP
				SNPIndex += 1

			# transpose to get the .PED formatting
			haps_tr = []
			currentIndiv = 0
			while currentIndiv < numIndivs:
				haps_tr.append([])	# make an empty list for each individual

				# populate the list by going through SNPs
				SNPIndex = 0
				while SNPIndex < SNPs:
					haps_tr[-1].extend(haps[SNPIndex][currentIndiv * 2 : currentIndiv * 2 + 2])

					# shift to the next SNP
					SNPIndex += 1

				currentIndiv += 1

			# write the .PED file
			currentIndiv = 0
			while currentIndiv < numIndivs:
				ped_file.write(str.join('\t', pedInfo[(block - 1) * (fieldsToRead / 2) + currentIndiv] + haps_tr[currentIndiv]) + '\n')
				currentIndiv += 1

			haplotypes.close()
			block += 1

		# check for the existence of any remaining non-processed individuals
		if ((block - 1) * (fieldsToRead / 2) + 1) < totalIndivs:
			print "processing the remaining individuals..."
			os.system("cut -d' ' -f" + str((block - 1) * fieldsToRead + 1) + "- " + haplotypes_file + " > " + haplotypes_file_temp)

			haplotypes = open(haplotypes_file_temp, 'r')

			numIndivs = len(haplotypes.readline().replace('\n', '').split()) / 2
			haplotypes.seek(0)

			H = haplotypes.readlines()
			haps = [x.replace('\n', '').split() for x in H]

			# map (0,1)'s -> (A, T, C, G)'s according to the .legend file, going SNP by SNP
			SNPIndex = 0
			while SNPIndex < SNPs:
				legendGeno = legend[SNPIndex][2:]	# determine the mapping

				# perform the conversion
				for index, value in enumerate(haps[SNPIndex]):
					if haps[SNPIndex][index] == "0":
						haps[SNPIndex][index] = legendGeno[0]
					else:
						haps[SNPIndex][index] = legendGeno[1]

				SNPIndex += 1

			# transpose to get the .PED formatting
			haps_tr = []
			currentIndiv = 0
			while currentIndiv < numIndivs:
				haps_tr.append([])	# make an empty list for each individual

				# populate the list by going through SNPs
				SNPIndex = 0
				while SNPIndex < SNPs:
					haps_tr[-1].extend(haps[SNPIndex][currentIndiv * 2 : currentIndiv * 2 + 2])

					# shift to the next SNP
					SNPIndex += 1

				currentIndiv += 1

			# write the .PED file
			currentIndiv = 0
			while currentIndiv < numIndivs:
				ped_file.write(str.join('\t', pedInfo[(block - 1) * (fieldsToRead / 2) + currentIndiv] + haps_tr[currentIndiv]) + '\n')
				currentIndiv += 1

			haplotypes.close()

		os.system("rm " + haplotypes_file_temp)	# deleting the temporary file
		ped_file.close()

	print "...done saving .PED file"

	return (ped_filename, map_filename)



# check for correct number of arguments 
if (len(sys.argv) < 2 or len(sys.argv) > 6):
	print 'ERROR: invalid input parameters'
	print 'input files in IMPUTE2 format: {IMPUTE.haps} {IMPUTE.legend}'
	print 'input files in SHAPEIT format: {SHAPEIT.sample}'
	print 'output files PED/MAP format: {PEDMAP}'
	print 'NOTE: input SHAPEIT file can be uncompressed (.sample) or gzip-compressed (.sample.gz)'
	print 'USAGE: convert_impute2_to_PEDMAP.py {IMPUTE.haps} {IMPUTE.legend} {SHAPEIT.sample} {PEDMAP} {chromosome#}'
	quit()

# read sample information from the original SHAPEIT2 .sample file
# (and check for gzip-compressed .sample input file)
if sys.argv[3].lower().endswith('.gz'):
	sample_info = [x.replace('\n', '').split() for x in gzip.open(sys.argv[3], 'r').readlines()[2:]]
else:
	sample_info = [x.replace('\n', '').split() for x in open(sys.argv[3], 'r').readlines()[2:]]

# parse the result into separate variables
sample_names = [x[1] for x in sample_info]
family_id = [x[0] for x in sample_info]
p_id = [x[3] for x in sample_info]
m_id = [x[4] for x in sample_info]
gender = [x[5] for x in sample_info]
pheno = [x[6] for x in sample_info]

returned = Convert_impute2_to_PEDMAP(
	sys.argv[5],	# chromosome number
	sys.argv[2],	# .legend file
	sys.argv[1],	# .haps file
	sample_names,
	None,
	family_id,
	None,
	p_id,
	None,
	m_id,
	None,
	gender,
	None,
	pheno,
	None,
	sys.argv[4]		# output file name
	)

if returned:
	print 'Method returned:'
	print str(returned)
