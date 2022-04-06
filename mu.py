#/home/user/anaconda3/envs/ovito/bin/python
import argparse
import scripts.remove_atom as remove_atom
import mu_plot

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", required=True)
parser.add_argument("-s", "--structure", required=True, dest='src', metavar='STRUCTURE', 
                    help='structure from removing atom')
parser.add_argument("-pp", "--post-proc", required=True, default=True, dest='postproc', 
                    metavar='ROUTINE_INPUT', help='evaluate mu with input ROUTINE_INPUT')
parser.add_argument("-d", "--debug", required=False, default=False, action='store_true', help='plot clustering')
parser.add_argument("-j", "--omp-jobs", required=False, dest='omp_jobs', default=4)
args = parser.parse_args()
args.outname = False
args.graphic = False
args.contourplot = False
args.circleplot = True
args.id = ['all']
args.src = [args.src, 'dat']

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

remove_atom.main(args)
args.file = f'mu_{args.src}'
mu_plot(args)