#!/bin/bash

echo; echo "Starting LAMMPS procedure..."; echo;


lmp_omp_edited -in in.segregation -var T $1 -var kappa $2 -var conc $3

#echo; echo "LAMMPS task done, plotting..."; echo

#python plot_thermal_relax.py

echo; echo "All done"; echo
