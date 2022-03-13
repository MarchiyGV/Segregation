#!/bin/bash
verbose=false
while getopts v:n:h: flag
do
    case "${flag}" in
        h) help=true;;
        v) verbose=true;;
        n) name=${OPTARG};;
    esac
done

if [ $help ]; then
    echo "-n : name"
    echo "-v : verbose (print any key)"
    exit 0
fi

echo "$name"

echo; echo "Starting LAMMPS procedure..."; echo;

cd scripts
if [ $verbose = "true" ]; then
    lmp_omp_edited -in in.mono_create_master -var name $name 
else
    echo "non verb"
    $(lmp_omp_edited -in in.mono_create_master -var name $name )
fi
cd ..


echo; echo "All done"; echo
n=$(ls ./GB_projects/$name/0K_structures/ | wc -l)
echo "Created $n confiurations"
res=$(ls ./GB_projects/$name/0K_structures/ | sort -t'_' -n -k3 | head -1)
echo "minmum energy: $res"
echo "Cell size for minimum energy configuration:"
grep -e '[x,y,z]lo' ./GB_projects/$name/0K_structures/$res