#!/bin/bash

while getopts s:n:i: flag
do
    case "${flag}" in
        s) structure=${OPTARG};;
        n) name=${OPTARG};;
        i) input=${OPTARG};;
    esac
done


echo; echo "Starting LAMMPS procedure..."; echo;

cd scripts
lmp_omp_edited -in in.slice -var gbname $name -var input $input -var structure_name $structure
cd ..

