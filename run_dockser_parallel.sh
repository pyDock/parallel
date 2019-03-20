#!/bin/bash
# 0 < numProcs < 100
SCRIPT_PATH_R="`dirname \"$0\"`"              # relative
SCRIPT_PATH_A="`( cd \"$MY_PATH_R\" && pwd )`"  # absolutized and normalized

PYDOCK3_BIN=`which pydock3`
if [ $PYDOCK3_BIN ];then
	BASE_PATH=`dirname ${PYDOCK3_BIN}` 
else
	PYDOCK3_BIN=`dirname ${SCRIPT_PATH_R}`/pyDock3
	BASE_PATH=`dirname ${PYDOCK3_BIN}`
fi
export PYDOCK3_BIN
EXPECTED_ARGS=2
E_BADARGS=65

# Check for arguments
int='^[0-9]+$'
if [ $# -ne $EXPECTED_ARGS ];then
	echo "Usage: `basename $0` project_name num_cpus"
	exit $E_BADARGS
elif ! [[ $2 =~ $int ]];then
   	echo "The num_processors is incorrect"
   	exit $E_BADARGS
elif ! [ -f ${1}.ini ];then
   	echo "The project_name is incorrect, INI file not found"
   	exit $E_BADARGS
elif ! [ -f ${1}_rec.pdb ] || ! [ -f ${1}_lig.pdb ];then
   	echo "The setup module was not executed, please execute -> pydock $1 setup"
   	exit $E_BADARGS
elif ! [ -f ${1}.rot ];then
	echo "The ROT file not found, please execute the FTDock or ZDOCK and the correspondent rotftdock or rotzdock PyDock modules."
	exit $E_BADARGS
fi

case=$1
numProcs=$2
numRows=`wc $case.rot | cut -d ' ' -f 3`

# Calculate number of jobs
let rowsPerProc=$numRows/$numProcs
let modulus=$numRows%$numProcs
if [ $modulus -gt 0 ]; then
	let rowsPerProc=rowsPerProc+1
fi
echo "rowsPerProc=$rowsPerProc"

# Split in multiple files input rot file
split -l $rowsPerProc -d -a 2 $case.rot $case.rot.

# Execute in parallel mode
for ((i=0; i<numProcs; i++));do
	echo "PROC=$i"
	${SCRIPT_PATH_R}/run_dockser_parallel_aux.sh $case $i & 
done
# Wait for all children to finish
wait
wait

# Merge temporary files
echo "Merging energy files..."
sort -nk 5 tmp_pydock_*/*ene | grep -v "Conf\|\-\-" > $case.ene.merged
withRMSD=`grep "reference" $case.ini | wc -l`
if [[ $withRMSD == 1 ]];then
	cut -c1-72 $case.ene.merged > $case.ene.merged.tmp
else
  	cut -c1-60 $case.ene.merged > $case.ene.merged.tmp
fi
${SCRIPT_PATH_R}/addRank.pl $case.ene.merged.tmp > $case.ene.merged.withRank
head -n 2 tmp_pydock_00/*ene > header
cat header $case.ene.merged.withRank > $case.ene
echo "Done."

# Clean up the house
echo "Cleaning up the house..."
rm header $case.ene.merged*
rm -R tmp_pydock_*
echo "Done."
