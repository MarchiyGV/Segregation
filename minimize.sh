#!/bin/bash

while getopts v:n:s: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        s) structure=${OPTARG};;
        *) echo "Unknonwn option ${flag}"; exit 1;;
    esac
done

echo; echo "Starting LAMMPS procedure..."; echo;



cd scripts
if [ $verbose = true ]; then
    lmp_omp_edited -in in.minimize_0K -var gbname $name -var structure_name $structure
else
    $(lmp_omp_edited -in in.minimize_0K -var gbname $name -var structure_name $structure)
fi
cd ..
echo; echo "All done"; echo
