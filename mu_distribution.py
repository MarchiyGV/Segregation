from matplotlib import cm, colors
from matplotlib import pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
import argparse, os

def main(args):
    name = args.name
    print(os.getcwd())
    if (os.path.abspath(os.getcwd()).split('/'))[-1]=='scripts':
        os.chdir('..')
    print(os.getcwd())
    path = f'GB_projects/{name}/'
    impath = f"GB_projects/{name}/images/"
    Path(impath).mkdir(exist_ok=True)
    fig, ax = plt.subplots(1, 1, dpi=100)
    Ni=[2, 1, 0]
    for j, file in enumerate(args.file[::-1]):
        fpath = f'GB_projects/{name}/output/{file}'
        df = pd.read_csv(fpath, sep=' ', comment='#', names=['id', 'mu', 'x', 'y'])
        mu = np.array(df['mu'])
        #n, bins = np.histogram(mu, 25)    
        #ax.plot(bins[:-1], n
        
        n, bins, h = ax.hist(mu, 25, alpha = 0.7, label=f'{Ni[j]}% Ni', density=True)   
        ax.axvline(mu.max(), linestyle='--', color=h[0]._original_facecolor)
        ax.text(mu.max(), 10+j, round(mu.max(), 2), fontsize=7)
    
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
    try:
        args = parser.parse_args()
    except:
        args = parser.parse_args('-n STGB_210 -s mu_minimize_0K_pure.dat mu_minimize_0K_STGB_210_Ni_1_k_100.dat mu_minimize_0K_STGB_210_Ni_2_k_20.dat'.split())
    main(args)