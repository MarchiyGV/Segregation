# Segregation

This Molecular Dynamics (MD) code, based on LAMMPS package, performs creating bicrystal surface and modelling of solute segregation (alloying) in created structures with subsequet calculation of reulting chemical potential of surface atoms in order to investigate enhancing of corrosion resistance

## Usage

### Files

- Folder "GB_projects" should include projects with different Grain Boundary (GB) orientations (types) and different host or solute species, for example: "GB_projects/S3_210"
- Each project should include 3 files: "orientation.txt" - specify GB orientation, "input.txt" - all user defined simulation parameters, "segregation_plot.txt" - settings for plotting and cheking convergence of segregation simulation
- Also in root directory there is folder "potentials", which include potental files and LAMMPS settings needed for chosen potential (see example)

### Scripts

All scripts writed on <strong>Python</strong> with modules specified in <strong>"env_ovito.yml"</strong> conda enviroment file. 
LAMMPS is used as subroutine and its executable should be specfied in <strong>LMP</strong> emviroment variable (by default it is "lmp_serial"). For parallel execution OMP LAMMPS package was used.
User accessed scipts are placed in root folder, when files in script folder are only subroutines.

There are several steps of modelling implemented in scripts:

- <strong>create_GB.py</strong> - creating sequence of smallest polycrystall supercells "GB_projects/S3_210/0K_structures/GB_E659_N80_count1.dat", where E659 - means that GB energy is 659kJ/mole, N80 - structure consist of 80 atoms, count1 - id of structure.
User should choose optimal one from it (with minimum energy, but without defects). Chosen structure should be moved to "GB_projects/S3_210/dat" folder (it may be done automatically
with renaming to "initial.dat"). For convinience name of this structure (e.g. "initial.dat") is writed to "GB_projects/S3_210/conf.txt" file in format "init initial.dat", 
where "init" - name of step. It can be created manually or automatically. 
- <strong>berendsen_relax.py</strong> replicate and relax structure (with barostat and thermostat) to target temperature and zero pressure. 
- <strong>thermal_relax.py</strong> relax strucure with fixed volume at target temperature.
- <strong>surface_thermal_relax.py</strong> introduce surface and relax with fixed volume.
- <strong>segregation_GB</strong> simulate solute segregation (alloying) by VCSGC algoritm (https://vcsgc-lammps.materialsmodeling.org/) at target concentration, its variance, temperature and with fixed volume. 
This script also plot graphics in real time for checking covergence. Plotting and convergence settings can be changed in real time by changing the 
"GB_projects/S3_210/segregation_plot.txt" file.
After achiving of convergence this script sterts saving samples in "GB_projects/S3_210/samples" folder for subsequent calculation of chemical potential.
- <strong>minimize.py</strong> relax sampled structures to 0K state. Structures to relax can be defined via "-s structure_name1_n*.dat structure_name2_n*.dat ..." option, 
where "structure_name_n*.dat" should be in folder "GB_projects/S3_210/samples" ("*" - denotes any number). Resuls are saving to "GB_projects/S3_210/samples_0K".
- <strong>mu.py</strong> calculate chemical potential $\mu$ of surface atoms from relaxed structures from "samples_0K" folder specified via "-s structure_name1_n*.dat structure_name2_n*.dat ...". 
Results are saving to "GB_projects/S3_210/output" (in format of text files with .dat extention).
- <strong>mu_plot.py</strong> plot map of surface chemical potential.
- <strong>mu_distribution.py</strong> plot density of cumulative (CDF) distribution function of chamical potential

### Syntax

All scripts can be run by command:
"python script_name.py -n S3_210 [other args]", where -n specify project directory.

All scripts provide help by "-h" option.
