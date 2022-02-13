#!/bin/bash
ARGS=$(getopt -a --options vn --long "verbose, name" -- "$@")
eval set -- "$ARGS"
verbose="false"
name="false"
while true; do
  case "$1" in
    -v|--verbose)
      verbose="true"
      shift;;
    -n|--name)
      name="true"
      shift;;
    --)
      break;;
     *)
      printf "Unknown option %s\n" "$1"
      exit 1;;
  esac
done

if [$name = "true"]
then
    echo "Write GB name:"
    read name
else
    name="STGB_210"
    echo "default name was used: $name"
fi

echo; echo "Starting LAMMPS procedure..."; echo;

if [ $verbose = "true" ]; then
    lmp_omp_edited -in in.GB_create_master -var gbname $name -var oriname $name".txt"
else
    log=$(lmp_omp_edited -in in.GB_create_master -var gbname $name -var oriname $name".txt")
fi
echo $log > log.txt 
echo; echo "All done"; echo
n=$(ls ./$name/ | wc -l)
echo "Created $n confiurations"
res=$(ls ./$name/ | sort -t'_' -n -k3 | head -1)
echo "minmum energy: $res"
echo "Cell size for minimum energy configuration:"
grep -e '[x,y,z]lo' ./$name/$res