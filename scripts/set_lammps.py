import os

if 'LMP' in os.environ:
    lmp = os.environ['LMP']
else:
    lmp = 'lmp_serial'

print(f'LAMMPS executable is assumed to be "{lmp}", this can be changed by setting enviromental variable "LMP"')