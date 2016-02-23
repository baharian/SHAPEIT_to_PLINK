# SHAPEIT_to_PLINK
Convert phased genotype data from SHAPEIT2 format to PLINK format (plain text)
=======

Python scripts to convert phased genotype data from SHAPEIT2 format (`.haps`/`.sample`) to plain text PLINK format (`.ped`/`.map`) while
keeping the phasing information intact.
   1. The first step is to convert from SHAPEIT2 format (`.haps`/`.sample`) to IMPUTE2 format (`.haps`/`.legend`/`.sample`).
   2. The second step is to convert from IMPUTE2 format (`.haps`/`.legend`/`.sample`) to plain text PLINK format (`.ped`/`.map`).
   This step uses the SHAPEIT2 `.sample` file from the first step and the `cut` command in UNIX/Linux/Mac OS X.

The script to perform the first step, `convert_shapeit2_to_impute2.py`, is based on a script from PyPedia (available at
http://www.pypedia.com/index.php/convert_shapeit_reference_to_impute2). The second script, `convert_impute2_to_PEDMAP.py`, is written by me, because the one(s) from PyPedia (and other places) would start to use swap space for large datasets and would, therefore, become
excruciatingly slow; my script avoids using swap and performs the conversion in memory for any number of individuals.
