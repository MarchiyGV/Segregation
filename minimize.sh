#!/bin/bash

while getopts v:n:s:t: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        s) structure=${OPTARG};;
        t) type=${OPTARG};;
        *) echo "Unknonwn option ${flag}"; exit 1;;
    esac
done

echo; echo "Starting LAMMPS procedure..."; echo;

if [ $type == pure ]; then
    routine=in.minimize_0K_pure
elif [ $type == alloy ]; then
    routine=in.minimize_0K_alloy
fi

cd scripts
if [ $verbose = true ]; then
    lmp_omp_edited -in $routine -var gbname $name -var structure_name $structure
else
    $(lmp_omp_edited -in $routine -var gbname $name -var structure_name $structure)
fi
cd ..
echo; echo "All done"; echo
