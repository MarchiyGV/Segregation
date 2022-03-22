#!/bin/bash
job=8
while getopts v:n:s:t:j: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        s) structure=${OPTARG};;
        t) type=${OPTARG};;
        j) job=${OPTARG};;
        *) echo "Unknonwn option ${flag}"; exit 1;;
    esac
done

echo; echo "Starting LAMMPS procedure..."; echo;

if [ $type == pure ]; then
    routine=in.minimize_0K_pure
elif [ $type == alloy ]; then
    routine=in.minimize_0K_alloy
fi

postfix="-pk omp $job -sf omp"

cd scripts
if [ $verbose = true ]; then
    lmp_omp_edited -in $routine -var gbname $name -var structure_name $structure $postfix
else
    $(lmp_omp_edited -in $routine -var gbname $name -var structure_name $structure $postfix)
fi
cd ..
echo; echo "All done"; echo
