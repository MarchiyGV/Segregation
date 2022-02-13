#!/bin/bash

echo; echo "Starting LAMMPS procedure..."; echo;


lmp_omp_edited -in in.surface_thermal_relax -var T $1 -var initial_relaxation_steps $2

echo; echo "LAMMPS task done, plotting..."; echo

python plot_surface_thermal_relax.py

echo; echo "All done"; echo
