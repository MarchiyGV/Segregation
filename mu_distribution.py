from matplotlib import cm, colors
from matplotlib import pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
import argparse, os
import glob, re


def main(args):
    name = args.name
    print(os.getcwd())
    if (os.path.abspath(os.getcwd()).split('/'))[-1]=='scripts':
        os.chdir('..')
    print(os.getcwd())
    path = f'GB_projects/{name}/'
    impath = f"GB_projects/{name}/images/"
    Path(impath).mkdir(exist_ok=True)
    fig, ax = plt.subplots(1, 1, dpi=500)
    
    files = []
    mus = []
    for e in args.file:
        files.append(glob.glob(f'GB_projects/{name}/output/{e}'))
    
    conc = []

    for j, file in enumerate(files):
        mu_avg = []
        fname = file[0].split('/')[-1]
        conc.append(float(re.findall(r'\d+\.*\d*', fname)[1]))
        for fpath in file:
            df = pd.read_csv(fpath, sep=' ', comment='#', names=['id', 'mu', 'x', 'y'])
            mu = np.array(df['mu'])
            mu_avg += list(mu)
            if args.avg:
                pass
                #ax.axvline(mu.max(), linestyle='--')
            else:
                n, bins, h = ax.hist(mu, 25, alpha = 0.7, density=True, label=fpath.split('_')[-1])   
                ax.axvline(mu.max(), linestyle='--', color=h[0]._original_facecolor)
            #ax.text(mu.max(), 10+j, round(mu.max(), 2), fontsize=7)
    
        if args.avg:
            ax.hist(mu_avg, 250, density=True, label=f'$ c = {conc[-1]}$', alpha=0.7)
    plt.xlim((np.min(mu_avg), np.max(mu_avg)))
    plt.xlabel('$\mu, eV$')
    plt.ylabel('density')
    plt.legend()
    plt.savefig(f'{impath}mu_distribution.png')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help='for example STGB_210')
    parser.add_argument("-s", "--structure", required=True, dest='file', metavar='OUTPUT', nargs='+',
                        help='output of mu.py, for example "mu_minimize_0K_STGB_210_Ni_2_k_20.dat"')
    parser.add_argument("--avg", required=False, help='plot average distribution', action='store_true', default=False)                  
    args = parser.parse_args()
    main(args)