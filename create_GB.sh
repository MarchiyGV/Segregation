#!/bin/bash
verbose=false
while getopts v:n: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
    esac
done

echo "$name"

echo; echo "Starting LAMMPS procedure..."; echo;

cd scripts
if [ $verbose = "true" ]; then
    lmp_omp_edited -in in.GB_create_master -var gbname $name 
else
    echo "non verb"
    $(lmp_omp_edited -in in.GB_create_master -var gbname $name)
fi
cd ..


echo; echo "All done"; echo
n=$(ls ./GB_projects/$name/0K_stuctures/ | wc -l)
echo "Created $n confiurations"
res=$(ls ./GB_projects/$name/0K_stuctures/ | sort -t'_' -n -k3 | head -1)
echo "minmum energy: $res"
echo "Cell size for minimum energy configuration:"
grep -e '[x,y,z]lo' ./GB_projects/$name/0K_stuctures/$res