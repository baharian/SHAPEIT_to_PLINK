## Convert phased genotype data from SHAPEIT2 format to PLINK format (plain text)

### General info
Python scripts to convert phased genotype data from SHAPEIT2 format (`.haps`/`.sample`) to plain text PLINK format (`.ped`/`.map`) while
keeping the phasing information intact.
   1. The first step is to convert from SHAPEIT2 format (`.haps`/`.sample`) to IMPUTE2 format (`.haps`/`.legend`/`.sample`).
   2. The second step is to convert from IMPUTE2 format (`.haps`/`.legend`/`.sample`) to plain text PLINK format (`.ped`/`.map`).
   This step uses the SHAPEIT2 `.sample` file from the first step and the `cut` command in UNIX/Linux/Mac OS X.

The script to perform the first step, `convert_shapeit2_to_impute2.py`, is based on [a script](http://www.pypedia.com/index.php/convert_shapeit_reference_to_impute2) from PyPedia. The second script, `convert_impute2_to_PEDMAP.py`, is written by me, because the one(s) from PyPedia (and other places) would start to use swap space for large datasets and would, therefore, become
excruciatingly slow; my script avoids using swap and performs the conversion in memory for any number of individuals.

### Usage
Data has to be separated by chromosome; then, run a `for ((i = 1; i <= 22; i++)); do ...; done` loop and perform the following steps in the loop.
   1. `python convert_shapeit2_to_impute2.py chr${i}.haps chr${i}.sample temp${i}.haps temp${i}.legend temp${i}.sample`
   2. `python convert_impute2_to_PEDMAP.py temp${i}.haps temp${i}.legend chr${i}.sample chr${i} ${i}`
   3. `rm temp${i}.*`

You can comment out the third step if you would like to keep the output in IMPUTE2 format as well.
