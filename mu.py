#/home/user/anaconda3/envs/ovito/bin/python
import argparse, glob, re
import scripts.remove_atom as remove_atom
import mu_plot, mu_distribution
import resource

_n = 20
resource.setrlimit(resource.RLIMIT_NOFILE, (2**_n, 2**_n))

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", required=True)
parser.add_argument("-s", "--structure", required=True,  metavar='STRUCTURE', 
                    help='structure from removing atom')
parser.add_argument("-pp", "--post-proc", default='mu', dest='postproc', 
                    metavar='ROUTINE_INPUT', help='evaluate mu with input ROUTINE_INPUT')
parser.add_argument("-d", "--debug", required=False, default=False, action='store_true', help='plot clustering')
parser.add_argument("-j", "--omp-jobs", required=False, dest='omp_jobs', default=4)
parser.add_argument("-f", "--force", required=False, default=False, action='store_true', help='recompute existing')
args = parser.parse_args()
args.outname = False
args.graphic = False
args.contourplot = False
args.circleplot = True
args.id = ['all']

with open(f"GB_projects/{args.name}/{args.postproc}.txt") as f:
    args.plot_ni = False
    for line in f:
        if ' type ' in line:
            if 'pure' in line:
                args.plot_ni = False
            elif 'alloy' in line:
                args.plot_ni = True
            else:
                print('type not defined,  Ni atoms wont be plotted')
        if 'agtype' in line:
            n = int(line.split(' ')[-1])
            if n>1:
                args.plot_ni = False
                break

structures = sorted(glob.glob(f'GB_projects/{args.name}/samples_0K/{args.structure}'))
outputs = glob.glob(f'GB_projects/{args.name}/output/mu_{args.structure}')
out_numbers = []
flist = []
for output in outputs:
    fname = output.split('/')[-1]
    number = int(re.findall(r'\d+', fname)[-1])
    out_numbers.append(number)

    
for i, structure_ in enumerate(structures):
    print(structure_)
    fname = structure_.split('/')[-1]
    number = int(re.findall(r'\d+', fname)[-1])
    flist.append(f'mu_{fname}')
    if number in out_numbers:
        if args.force:
            pass
        else:
            continue
    args.src = [fname, 'dat']
    remove_atom.main(args)
    

'''
args.file = [f'mu_{args.src[0]}']
args.norm = False
print(args.file)
mu_plot.main(args)
'''
args.file = flist
args.avg = True
mu_distribution.main(args)
