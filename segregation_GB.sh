#!/bin/bash
verbose=false
mean_width=50
conc=-1
kappa=-1
job=7
restart=false
mu=false
while getopts v:n:s:w:c:k:j:r:m: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        s) structure=${OPTARG};;
        w) mean_width=${OPTARG};;
        c) conc=${OPTARG};;
        k) kappa=${OPTARG};;
        j) job=${OPTARG};;
        r) restart=true;;
        m) mu=${OPTARG};;
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
if [ $restart = true ]; then
    input="in.segregation_restart"
else
    input="in.segregation"
fi

if [ $mu = false ]; then
    mu_command=""
else
    mu_command="-var mu0 $mu"
fi

cd scripts
if [ $verbose = true ]; then
    lmp_omp_edited -in $input $mu_command -var gbname $name -var structure_name $structure -var conc_f $conc -var kappa_f $kappa -pk omp ${job} -sf omp
else
    $(lmp_omp_edited -in $input $mu_command -var gbname $name -var structure_name $structure -var conc_f $conc -var kappa_f $kappa -pk omp ${job} -sf omp)
fi



echo; echo "All done"; echo
