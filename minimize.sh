#!/bin/bash

echo; echo "Starting LAMMPS procedure..."; echo;


lmp_omp_edited -in in.minimize_0K 


echo; echo "All done"; echo
