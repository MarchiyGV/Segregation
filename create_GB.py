from pathlib import Path
import argparse, os
from subprocess import Popen, PIPE
import time, re

def main(args):
    lmp = 'lmp_omp_edited'
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
                        ans = map(int, re.findall(r'\d+', line))
                        print('{:12d} {:12d} {:12d}'.format(*ans))
                    else:
                        print(line.replace('!', ''), end='')
            else:
                print(line, end='')             

    
    if exitflag:
        print("LAMMPS finish succesfully")
    else:
        print('\n!!!!!!!!!!!!!!!!!\n\nError occured in LAMMPS')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("v", "--verbose", required=False, default=False, action='store_true',
                        help='show LAMMPS outpt')
    parser.add_argument("-j", "--job", required=False, default=1)
    args = parser.parse_args()
    main(args)

