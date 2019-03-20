#!/bin/bash
case=$1
procID=$2
echo "INSIDE_AUX_PROC=$procID"
string_procID=`printf "%02d" $procID`
mkdir tmp_pydock_$string_procID
cp *pdb* tmp_pydock_$string_procID
cp *ini tmp_pydock_$string_procID
mv $case.rot.$string_procID tmp_pydock_$string_procID/$case.rot
cd tmp_pydock_$string_procID
$PYDOCK3_BIN $case dockser
echo "$procID FINI"
