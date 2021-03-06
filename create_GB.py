from pathlib import Path
import argparse, os, sys
from subprocess import Popen, PIPE
import time, re, shutil
import numpy as np
import sys
sys.path.insert(1, f'{sys.path[0]}/scripts')
from set_lammps import lmp

def main(args):
    nonverbose = (not args.verbose)
    job = args.job
    name = args.name
    print(name, '\n')

    print("Starting LAMMPS procedure...\n")

    print(os.getcwd())
    if (os.path.abspath(os.getcwd()).split('/'))[-1]!='scripts':
        os.chdir('scripts')
    print(os.getcwd())

    task = (f'{lmp} -in in.GB_create_master ' +
            f'-var gbname {name} ' + 
            f'-pk omp {job} ' +
            f'-sf omp')

    
    exitflag = False
    files, E, N = [], [], []
    with Popen(task.split(), stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        time.sleep(0.1)
        print('\n')
        if nonverbose:
            headers = 'GB_energy Natoms Counter'.split()
            print('{0: <12} {1: <12} {2: <12}'.format(*headers))
        for line in p.stdout:
            if "All done" in  line:
                exitflag = True
            if nonverbose:
                if '!' in line:
                    if '.dat' in line:
                        files.append(line.replace('!', ''))
                        ans = list(map(int, re.findall(r'\d+', line)))
                        print('{:12d} {:12d} {:12d}'.format(*ans))
                        E.append(int(ans[0]))
                        N.append(int(ans[1]))
                    else:
                        print(line.replace('!', ''), end='')
            else:
                print(line, end='')             

    
    if exitflag:
        print("LAMMPS finish succesfully")
        E = np.array(E)
        N = np.array(N)
        print('E', E)
        print('N', N)
        inds = np.where(E == E.min())
        ind = (np.where(N == np.max(N[inds])))[0][0]
        print(f"\nMinimum energy {E[ind]} with maximum atoms {N[ind]} at:")
        print(files[ind])
        if args.ovito:
            os.popen(f'ovito ../GB_projects/{name}/0K_structures/{files[ind]}')
        while True:
            ans = input(f'Do you want to select this for futher steps? [y/n/<other_filename>]:').replace('\n', '')
            if ans=='y' or ans=='Y':
                file = files[ind]
                break
            elif ans=='n' or ans=='N':
                file = False
                break
            else:
                fpath = f'../GB_projects/{name}/0K_structures/{ans}'       
                if os.path.isfile(fpath):
                    file = ans
                else:
                    print('Pleas answer [Yy/Nn/<other_filename>]')
    else:
        print('\n!!!!!!!!!!!!!!!!!\n\nError occured in LAMMPS')

    if file:
        file = file.replace("\n", "")
        fpath = f'../GB_projects/{name}/0K_structures/{file}'  
        dest = f'../GB_projects/{name}/dat'
        Path(dest).mkdir(exist_ok=True)  
        shutil.copyfile(fpath, f'{dest}/initial.dat')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("-v", "--verbose", required=False, default=False, action='store_true',
                        help='show LAMMPS outpt')
    parser.add_argument("-j", "--job", required=False, default=1)
    parser.add_argument("--ovito", required=False, default=False, action='store_true',
                        help='open the final in ovito')
    args = parser.parse_args()
    main(args)

