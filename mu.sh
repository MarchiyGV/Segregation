#!/bin/bash
job=4
while getopts v:n:s:f:i:j: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        s) structure_1=${OPTARG};;
        f) structure_2=${OPTARG};;
        i) input=${OPTARG};;
        j) job=${OPTARG};;
        *) echo "Unknonwn option ${flag}"; exit 1;;
    esac
done

echo; echo "Starting LAMMPS procedure..."; echo;

routine=in.mu

cd scripts
if [ $verbose = true ]; then
    lmp_omp_edited -in $routine -var gbname $name -var structure_name_1 $structure_1 -var structure_name_2 $structure_2 -var input $input -pk omp $job -sf omp 
else
    $(lmp_omp_edited -in $routine -var gbname $name -var structure_name_1 $structure_1 -var structure_name_2 $structure_2 -var input $input)
fi
cd ..
echo; echo "All done"; echo
