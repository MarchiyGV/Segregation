from pathlib import Path
import argparse, os
from subprocess import Popen, PIPE
import time, re, shutil, sys, glob
import numpy as np

errors = []
def main(args):
    lmp = 'lmp_omp_edited'
    nonverbose = (not args.verbose)
    job = args.job
    name = args.name
    if not args.pure:
        script = 'in.minimize_0K_alloy'
    else:
        script = 'in.minimize_0K_pure'

    if not args.force_size:
        fname = f'GB_projects/{name}/conf.txt'
        flag=False
        with open(fname, 'r') as f :
            for line in f:
                if 'init' in line:
                    init = line.split()[-1]
                    print(init)
                    flag = True
        if not flag:
            raise ValueError(f'cannot find init structure in conf.txt in order to use 0K size, lease write it manually in input script and use --fore-size flag' )
        flag_x = False
        flag_y = False
        with open(f'GB_projects/{name}/dat/{init}', 'r') as f:
            for line in f:
                if 'xlo xhi' in line:
                    _args = line.split()
                    xlo = float(_args[0])
                    xhi = float(_args[1])
                    dx = xhi - xlo
                    flag_x = True
                if 'ylo yhi' in line:
                    _args = line.split()
                    ylo = float(_args[0])
                    yhi = float(_args[1])
                    dy = yhi - ylo
                    flag_y = True
        if flag_x and flag_y:
            lst = []
            with open(f'GB_projects/{name}/input.txt' ,'r') as f:
                a = ['lx_0K_i ', 'ly_0K_i ']
                for line in f:
                    for word in a:
                        if word in line:
                            _args = line.split()
                            if 'lx_0K_i' in _args[1]:
                                dksi = dx
                            else:
                                dksi = dy

                            line = f'{_args[0]} {_args[1]} {_args[2]} {dksi}\n'
                    lst.append(line)
            with open(f'GB_projects/{name}/input.txt','w') as f:
                for line in lst:
                    f.write(line)
        else:
            raise ValueError('cannot read init structure file (xlo xhi, ylo yhi)')
            

    structures = sorted(glob.glob(f'GB_projects/{name}/samples/{args.structure}'))
    for structure_ in structures:
        structure = structure_.split('/')[-1]
        print(structure)
        number = int(re.findall(r'\d+', structure)[-1])
        if number<args.start:
            print('already done, pass...')
            continue
        print("Starting LAMMPS procedure...\n")

        print(os.getcwd())
        if (os.path.abspath(os.getcwd()).split('/'))[-1]!='scripts':
            os.chdir('scripts')
        print(os.getcwd())
        
        task = (f'{lmp} -in {script} ' 
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
            file = datfile.replace("\n", "")
            fpath = f'../GB_projects/{name}/dat/{file}'  
            dest = f'../GB_projects/{name}/samples_0K'
            Path(dest).mkdir(exist_ok=True)  
            shutil.move(fpath, f'{dest}/{file}')
        else:
            print('\n!!!!!!!!!!!!!!!!!\n\nError occured in LAMMPS')
            #raise ValueError('Error in LAMMPS, check input script and log file')
            errors.append(structure)

        
    print('All done!')
    if len(errors)>0:
        print(len(errors))
        for error in errors:
            print('error in', error)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("-s", "--structure", required=False, default=False)
    parser.add_argument("-v", "--verbose", required=False, default=False, action='store_true',
                        help='show LAMMPS outpt')
    parser.add_argument("--pure", required=False, default=False, action='store_true')
    parser.add_argument("-j", "--job", required=False, default=1)
    parser.add_argument("--start", required=False, default=0, type=int)
    parser.add_argument("--ovito", required=False, default=False, action='store_true',
                        help='open the dump in ovito')
    parser.add_argument("--force-size", dest='force_size', required=False, default=False, action='store_true',
                        help='do not rewrite 0K size in input file')
    args = parser.parse_args()
    main(args)




