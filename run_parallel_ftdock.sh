#!/bin/bash
E_BADARGS=65
SCRIPT_PATH_R="`dirname \"$0\"`"
echo "Searching FTDOCK MPI version"
FTDOCK_MPI=`grep -w '^FTDOCK=' ${SCRIPT_PATH_R}/../etc/pydock.conf | sed 's/FTDOCK=//g'`
type ${FTDOCK_MPI}/ftdock >/dev/null 2>&1 || { echo >&2 "FTDock not found check the PATH variable in ect/pydock.conf or install the program. Aborting."; exit ${E_BADARGS}; }
is_MPI=`${FTDOCK_MPI}/ftdock | grep "MPI" | wc -l`
if [ $is_MPI -eq 0 ]
    then
        echo "MPI version of FTdock not found.";
        exit ${E_BADARGS};
fi
if [ "$#" != "3" ] && [ "$#" != "2" ]; then
    echo "Wrong arguments";
    printf "Usage: `basename $0` project_name num_cpus noelec\nThe default setting of ftdock is perform the sampling with electrostatics to desactivate include the \"nonelec\" parameter.\n";
    exit ${E_BADARGS};
else
    int='^[0-9]+$'
    if ! [[ $2 =~ $int ]];then
            echo "Wrong arguments"
            echo "The num_processors is incorrect"
            exit ${E_BADARGS};
    fi
    if ! [ -f ${1}.ini ];then
            echo "Wrong arguments"
            echo "The project_name is incorrect, INI file not found"
            exit ${E_BADARGS};
    fi
    if [ "$3" != "noelec" ] && [ "$3" != "" ];then
            echo "Wrong arguments"
            echo "The electrostactic parameter is set incorectly"
            exit ${E_BADARGS};
    fi
fi

echo "pyDock TARGET name is: $1"
echo "Executing ftdock MPI version using $2 cpus"
if [ "$3" == "noelec" ];then
	echo "Executing ftdock MPI without electrostatic"
	mpirun -np $2 ${FTDOCK_MPI}/ftdock -static ${1}_rec.pdb -mobile ${1}_lig.pdb -calculate_grid 0.7 -angle_step 12 -internal -15 -surface 1.3 -keep 3 -noelec -out ${1}.ftdock
else
	echo "Executing ftdock MPI with electrostatic"
	mpirun -np $2 ${FTDOCK_MPI}/ftdock -static ${1}_rec.pdb -mobile ${1}_lig.pdb -calculate_grid 0.7 -angle_step 12 -internal -15 -surface 1.3 -keep 3 -out ${1}.ftdock
fi;
echo "Calculations finished, checking for results..."
calc_lines=`cat ${1}.ftdock | wc -l`
if [ "$calc_lines" == "10023" ]; then
    echo "${1}.ftdock is OK"
else
    echo "Error in ftdock output, please check log and errors above."
    exit 0;
fi
echo "Removing temporal data..."
rm -rf scratch_scores*.dat
echo "Done."
