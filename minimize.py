from pathlib import Path
import argparse, os
from subprocess import Popen, PIPE
import time, re, shutil, sys
import numpy as np


def main(args):
    lmp = 'lmp_omp_edited'
    nonverbose = (not args.verbose)
    job = args.job
    name = args.name
    structure = args.structure

    print("Starting LAMMPS procedure...\n")

    print(os.getcwd())
    if (os.path.abspath(os.getcwd()).split('/'))[-1]!='scripts':
        os.chdir('scripts')
    print(os.getcwd())
    
    task = (f'{lmp} -in in.minimize_0K_alloy ' 
            f'-var gbname {name} ' + 
            f'-var structure_name {structure} ' +
            f'-pk omp {job} ' +
            f'-sf omp')

    print(task)

    exitflag = False
    with Popen(task.split(), stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        time.sleep(0.1)
        print('\n')
        for line in p.stdout:
            if "All done" in  line:
                exitflag = True
            elif "dumpfile" in line:
                dumpfile = (line.replace('dumpfile ', '')).replace('\n', '')
            elif "datfile" in line:
                datfile = (line.replace('datfile ', '')).replace('\n', '')
            if nonverbose:
                if '!' in line:
                    print(line.replace('!', ''), end='')
            else:
                print(line, end='')   


    
    if exitflag:
        print("LAMMPS finish succesfully")
        if args.ovito:
            os.popen(f'ovito {dumpfile}')
    else:
        print('\n!!!!!!!!!!!!!!!!!\n\nError occured in LAMMPS')
        raise ValueError('Error in LAMMPS, check input script and log file')

    file = datfile.replace("\n", "")
    fpath = f'../GB_projects/{name}/dat/{file}'  
    dest = f'../GB_projects/{name}/slices'
    Path(dest).mkdir(exist_ok=True)  
    shutil.copyfile(fpath, f'{dest}/{file}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("-s", "--structure", required=False, default=False)
    parser.add_argument("-v", "--verbose", required=False, default=False, action='store_true',
                        help='show LAMMPS outpt')
    parser.add_argument("-j", "--job", required=False, default=1)
    parser.add_argument("--ovito", required=False, default=False, action='store_true',
                        help='open the dump in ovito')
    args = parser.parse_args()
    main(args)



