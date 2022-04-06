#!/bin/bash
verbose=false
job=1
while getopts v:n:j: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        j) job=${OPTARG};;
    esac
done

echo "$name"

echo; echo "Starting LAMMPS procedure..."; echo;

cd scripts
if [ $verbose = "true" ]; then
    lmp_omp_edited -in in.GB_create_master -var gbname $name -pk omp ${job} -sf omp
else
    echo "non verb"
    $(lmp_omp_edited -in in.GB_create_master -var gbname $name -pk omp ${job} -sf omp)
fi
cd ..


echo; echo "All done"; echo
n=$(ls ./GB_projects/$name/0K_structures/ | wc -l)
echo "Created $n confiurations"
res=$(ls ./GB_projects/$name/0K_structures/ | sort -t'_' -n -k3 | head -1)
echo "minmum energy: $res"
echo "Cell size for minimum energy configuration:"
grep -e '[x,y,z]lo' ./GB_projects/$name/0K_structures/$res