#!/bin/bash
ARGS=$(getopt -a --options vs --long "verbose, structure" -- "$@")
eval set -- "$ARGS"
verbose="false"
structure="false"
while true; do
  case "$1" in
    -v|--verbose)
      verbose="true"
      shift;;
    -s|--structure)
      structure="true"
      shift;;
    --)
      break;;
     *)
      printf "Unknown option %s\n" "$1"
      exit 1;;
  esac
done

if [$structure = "true"]
then
    echo "Write structure file path:"
    read structure
else
    structure="STGB_210/STGB_210.GBE_659_80_125.dat"
    echo "default path was used: $structure"
fi

echo; echo "Starting LAMMPS procedure..."; echo;

if [ $verbose = "true" ]; then
    lmp_omp_edited -in in.thermal_relax -var structure $structure
else
    log=$(lmp_omp_edited -in in.thermal_relax -var structure $structure)
fi
echo $log > log_thermal_relax.txt 
echo; echo "LAMMPS task done, plotting..."; echo
python plot_thermal_relax.py

echo; echo "All done"; echo
