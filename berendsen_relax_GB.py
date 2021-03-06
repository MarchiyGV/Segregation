from pathlib import Path
import argparse, os, sys
from subprocess import Popen, PIPE
import time, re, shutil
import numpy as np
sys.path.insert(1, f'{sys.path[0]}/scripts')
from set_lammps import lmp

def main(args):
    nonverbose = (not args.verbose)
    job = args.job
    name = args.name
    structure = args.structure
    if not structure:
        fname = f'GB_projects/{name}/conf.txt'
        flag=False
        with open(fname, 'r') as f :
            for line in f:
                if 'init' in line:
                    structure = line.split()[-1]
                    print(structure)
                    flag = True
        if not flag:
            raise ValueError(f'cannot find structure in conf.txt')

    print(name, '\n')

    print("Starting LAMMPS procedure...\n")

    print(os.getcwd())
    if (os.path.abspath(os.getcwd()).split('/'))[-1]!='scripts':
        os.chdir('scripts')
    print(os.getcwd())
    
    task = (f'{lmp} -in in.berendsen_relax ' +
            f'-var gbname {name} ' + 
            f'-var structure_name {structure} ' +
            f'-pk omp {job} ' +
            f'-sf omp')

    exitflag = False
    with Popen(task.split(), stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        time.sleep(0.1)
        print('\n')
        for line in p.stdout:
            if "All done" in  line:
                exitflag = True
            elif "dumpfile" in line:
                dumpfile = (line.replace('dumpfile ', '')).replace('\n', '')
                print(dumpfile)
            elif "datfile" in line:
                datfile = (line.replace('datfile ', '')).replace('\n', '')
                print(datfile)
            if nonverbose:
                if '!' in line:
                    print(line.replace('!', ''), end='')
            else:
                print(line, end='')             

    
    if exitflag:
        print("LAMMPS finish succesfully")
        if args.plot:
            impath = f'../GB_projects/{name}/images'
            Path(impath).mkdir(exist_ok=True)  
            from scripts.plot_thermal_relax import main as plot
            plot_args = parser.parse_args()
            plot_args.n = args.mean_width
            plot_args.inp = 'berendsen_relax'
            plot(plot_args)
        if args.ovito:
            os.popen(f'ovito {dumpfile}')
    else:
        print('\n!!!!!!!!!!!!!!!!!\n\nError occured in LAMMPS')
        raise ValueError('Error in LAMMPS, check input script and log file')
    
    fname = f'../GB_projects/{name}/conf.txt'
    output = ''
    flag=False
    with open(fname, 'r') as f :
        for line in f:
            if 'BR' in line:
                line = f'BR {datfile}\n'
                flag=True
                print(line)

            output += line
    if not flag:
        output += f'BR {datfile}\n'

    with open(fname, 'w') as f:
        f.write(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("-s", "--structure", required=False, default=None)
    parser.add_argument("-v", "--verbose", required=False, default=False, action='store_true',
                        help='show LAMMPS outpt')
    parser.add_argument("-j", "--job", required=False, default=1)
    parser.add_argument("-m", "--mean-width", dest='mean_width', required=False, default=50)
    parser.add_argument("-p", "--plot", required=False, default=False, action='store_true',
                        help='draw the thermodynamic plot')
    parser.add_argument("--ovito", required=False, default=False, action='store_true',
                        help='open the dump in ovito')
    args = parser.parse_args()
    main(args)




