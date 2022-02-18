#!/bin/bash
verbose=false
mean_width=50
while getopts v:n:s:m: flag
do
    case "${flag}" in
        v) verbose=true;;
        n) name=${OPTARG};;
        s) structure=${OPTARG};;
        m) mean_width=${OPTARG};;
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
    lmp_omp_edited -in in.surface_thermal_relax -var gbname $name -var structure_name $structure
else
    $(lmp_omp_edited -in in.surface_thermal_relax -var gbname $name -var structure_name $structure)
fi

echo; echo "LAMMPS task done, plotting..."; echo

python plot_surface_thermal_relax.py $name $mean_width

cd ..
echo; echo "All done"; echo
