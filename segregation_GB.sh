#!/bin/bash
verbose=false
mean_width=50
conc=-1
kappa=-1
job=7
while getopts v:n:s:m:c:k:j: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        s) structure=${OPTARG};;
        m) mean_width=${OPTARG};;
        c) conc=${OPTARG};;
        k) kappa=${OPTARG};;
        j) job=${OPTARG};;
        *) echo "Unknonwn option ${flag}"; exit 1;;
    esac
done
if [[ -n "$CONDA_PREFIX" ]]; then
    echo "Conda is active: $CONDA_PREFIX"
else
    read -p "Conda is not active, do you want to continue? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Ok"
    else
        exit 1
    fi
fi

echo; echo "Starting LAMMPS procedure..."; echo;

cd scripts
if [ $verbose = true ]; then
    lmp_omp_edited -in in.segregation -var gbname $name -var structure_name $structure -var conc_f $conc -var kappa_f $kappa -pk omp ${job} -sf omp
else
    $(lmp_omp_edited -in in.segregation -var gbname $name -var structure_name $structure -var conc_f $conc -var kappa_f $kappa -pk omp ${job} -sf omp)
fi

#echo; echo "LAMMPS task done, plotting..."; echo

#python plot_thermal_relax.py

echo; echo "All done"; echo
