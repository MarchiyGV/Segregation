#!/bin/bash

while getopts v:n:s:f:i: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        s) structure_1=${OPTARG};;
        f) structure_2=${OPTARG};;
        i) input=${OPTARG};;
        *) echo "Unknonwn option ${flag}"; exit 1;;
    esac
done

echo; echo "Starting LAMMPS procedure..."; echo;

routine=in.mu

cd scripts
if [ $verbose = true ]; then
    lmp_omp_edited -in $routine -var gbname $name -var structure_name_1 $structure_1 -var structure_name_2 $structure_2 -var input $input
else
    $(lmp_omp_edited -in $routine -var gbname $name -var structure_name_1 $structure_1 -var structure_name_2 $structure_2 -var input $input)
fi
cd ..
echo; echo "All done"; echo
