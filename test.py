pseudopotentials = {'Ni': 'Ni.upf',
                    'Ag': 'Ag.upf'}
from ase.build import bulk, fcc100
from ase.calculators.espresso import Espresso
from ase.constraints import UnitCellFilter
from ase.optimize import BFGS
from ase.constraints import FixAtoms

vacuum=15
N_lay = 5

ecutwfc = 49*2
ecutrho = 12*ecutwfc
degauss = 2.2e-2
conv_thr = 3.2e-8
mixing_mode = 'local-TF'
beta = 0.4
input_data = {
    'verbosity': 'high',
    'system': 
        {
        'ecutwfc': ecutwfc,
        'ecutrho': ecutrho,
        'degauss': degauss,
        'occupations': 'smearing',
        'smearing': 'cold'
        },
    'electrons': 
        {
        #'mixing_mode': mixing_mode,
        #'mixing_beta': beta,
        'conv_thr': conv_thr,
        'electron_maxstep': 120
        }
    } 

input_data_slab = {
    'verbosity': 'high',
    'system': 
        {
        'ecutwfc': ecutwfc,
        'ecutrho': ecutrho,
        'degauss': degauss,
        'occupations': 'smearing',
        'smearing': 'cold'
        },
    'electrons': 
        {
        'mixing_mode': mixing_mode,
        #'mixing_beta': beta,
        'conv_thr': conv_thr,
        'electron_maxstep': 120
        }
    } 

a0 = 4.02
ag = bulk('Ag', crystalstructure='fcc', a=a0)
calc = Espresso(pseudopotentials=pseudopotentials,
                pseudo_dir='/home/user/qe-7.0-ReleasePack/qe-7.0/pseudo',
                tstress=True, tprnfor=True, kpts=(3, 3, 3), input_data=input_data)
ag.calc = calc

ucf = UnitCellFilter(ag)
opt = BFGS(ucf)
print('initial lat const:', (4*ag.get_volume()/len(ag))**(1.0/3.0))
opt.run(fmax=0.005)

# cubic lattic constant
a = (4*ag.get_volume()/len(ag))**(1.0/3.0)
print('final lat const:', a)
slab = fcc100('Ag', (4,4,N_lay), a=a, vacuum=vacuum)

mask = [atom.tag == N_lay for atom in slab]
slab.set_constraint(FixAtoms(mask=mask))

calc = Espresso(pseudopotentials=pseudopotentials,
                pseudo_dir='/home/user/qe-7.0-ReleasePack/qe-7.0/pseudo',
                tstress=True, tprnfor=True, kpts=(3, 3, 1), input_data=input_data_slab)
slab.calc = calc

dyn = BFGS(slab, trajectory='init_relax_restart.traj')
dyn.replay_trajectory('init_relax.traj')
dyn.run(fmax=0.005)
