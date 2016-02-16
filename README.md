# SHAPEIT_to_PLINK
convert phased genotype data from SHAPEIT2 format to PLINK (plain text) format

Python scripts to convert phased genotype data from SHAPEIT2 format (.haps/.sample) to plain text PLINK format (.ped/.map) while
keeping the phasing information intact.
1) The first step is to convert from SHAPEIT2 format (.haps/.sample) to IMPUTE2 format (.haps/.legend/.sample).
2) The second step is to convert from IMPUTE2 format (.haps/.legend/.sample) to plain text PLINK format (.ped/.map).
   This step uses the SHAPEIT2 .sample file from the first step and the 'cut' command in UNIX/Linux/Mac OS X.

The script to perform the first step (convert_shapeit2_to_impute2.py) is based on a script from PyPedia (available at
http://www.pypedia.com/index.php/convert_shapeit_reference_to_impute2). The second script (convert_impute2_to_PEDMAP.py) is written
entirely by me, because the one(s) from PyPedia (and anywhere else) would begin to use swap for large datasets and would become
excruciatingly slow.
