from pathlib import Path
import argparse, os
from subprocess import Popen, PIPE
import time, re, shutil
import numpy as np
from scripts.plot_segregation import main as plot

def main(args):
    lmp = 'lmp_omp_edited'
    nonverbose = (not args.verbose)
    job = args.job
    name = args.name
    structure = args.structure
    N_loops = args.loops
    if not structure:
        fname = f'GB_projects/{name}/conf.txt'
        flag=False
        with open(fname, 'r') as f :
            for line in f:
                if 'STR' in line:
                    structure = line.split()[-1]
                    print(structure)
                    flag = True
        if not flag:
            raise ValueError(f'cannot find structure in conf.txt')
    if args.mu:
        mu_arg = f'-var mu0 {args.mu}'
    else:
        mu_arg = ''

    print(name, '\n')

    print("Starting LAMMPS procedure...\n")

    print(os.getcwd())
    if (os.path.abspath(os.getcwd()).split('/'))[-1]!='scripts':
        os.chdir('scripts')
    print(os.getcwd())
    
    task = (f'{lmp} -in in.segregation ' + mu_arg +
            f'-var gbname {name} ' + 
            f'-var structure_name {structure} ' +
            f'-var conc_f {args.conc} -var kappa_f {args.kappa} ' + 
            f'-pk omp {job} ' +
            f'-sf omp')

    print(task)

    exitflag = False
    counter = 0
    last_counter = 0
    with Popen(task.split(), stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        time.sleep(0.1)
        print('\n')
        for line in p.stdout:
            if 'thermo output file:' in line:
                src_path = line.split()[-1]
                src = src_path.split('/')[-1]
            if "All done" in  line:
                exitflag = True
            elif "dumpfile" in line:
                dumpfile = (line.replace('dumpfile ', '')).replace('\n', '')
            elif "datfile" in line:
                datfile = (line.replace('datfile ', '')).replace('\n', '')
            elif "vcsgc_loop" in line:
                counter += 1
                print('loop', counter)
            if nonverbose:
                if '!' in line:
                    print(line.replace('!', ''), end='')
            else:
                print(line, end='')   
            if (counter != last_counter) and (counter%N_loops == 0):
                last_counter = counter
                impath = f'../GB_projects/{name}/images'
                Path(impath).mkdir(exist_ok=True)  
                parser_ = argparse.ArgumentParser()
                plot_args = parser_.parse_args('')
                fname = f'../GB_projects/{name}/segregarion_plot.txt'
                flag1=False
                flag2=False
                flag3=False
                flag4=False
                flag5=False
                with open(fname, 'r') as f :
                    for line in f:
                        if 'slope width' in line:
                            plot_args.w = int(line.split()[-1])
                            flag1=True
                        if 'step' in line:
                            plot_args.st = int(line.split()[-1])
                            flag2=True
                        if 'rolling mean width' in line:
                            plot_args.num = int(line.split()[-1])
                            flag3=True
                        if 'offset' in line:
                            plot_args.s1 = int(line.split()[-1])
                            flag4=True
                        if 'converged slope' in line:
                            slope_conv = float(line.split()[-1])
                            flag5=True
                flag = (flag1 and flag2 and flag3 and flag4 and flag5)
                if not flag:
                    raise ValueError(f'incorrect segregarion_plot.txt')
                
                plot_args.name = args.name
                plot_args.src = src
                plot_args.hide = (not args.plot)
                slope = np.array(plot(plot_args))
                N_conv = np.sum(np.abs(slope)<slope_conv)
                print('convergence criteria achieved in', N_conv, 'points')


    
    if exitflag:
        print("LAMMPS finish succesfully")
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
            if 'STR' in line:
                line = f'STR {datfile}\n'
                flag=True
                print(line)

            output += line
    if not flag:
        output += f'STR {datfile}\n'

    with open(fname, 'w') as f:
        f.write(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("-s", "--structure", required=False, default=False)
    parser.add_argument("-v", "--verbose", required=False, default=False, action='store_true',
                        help='show LAMMPS outpt')
    parser.add_argument("-j", "--job", required=False, default=1)
    parser.add_argument("-m", "--mean-width", dest='mean_width', required=False, default=50)
    parser.add_argument("-c", "--conc", required=False, default=-1, type=float)
    parser.add_argument("--mu", required=False, default=None, type=float)
    parser.add_argument("-k", "--kappa", required=False, default=-1, type=float)
    parser.add_argument("-p", "--plot", required=False, default=False, action='store_true',
                        help='show the thermodynamic plot')
    parser.add_argument("--loops", required=False, default=100, type=int,
                        help='draw the thermodynamic plot each <N> loops')
    parser.add_argument("--ovito", required=False, default=False, action='store_true',
                        help='open the dump in ovito')
    args = parser.parse_args()
    main(args)



