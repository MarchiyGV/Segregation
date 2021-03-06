    
# problem with many opened files (PMIX error out of resource) https://github.com/openpmix/openpmix/issues/1513
# closing avito instances https://www.ovito.org/forum/topic/how-to-remove-modifiers/#:~:text=you%20asked%20how%20to%20remove,element%20from%20a%20list%2C%20e.g.&text=deletes%20the%20first%20modifier%20from,to%20turn%20it%20off%2C%20e.g.

def main(args):  
    from turtle import color
    import warnings
    warnings.filterwarnings('ignore', message='.*OVITO.*PyPI')
    from ovito.io import import_file, export_file
    from ovito import scene
    from ovito.modifiers import ConstructSurfaceModifier, ColorCodingModifier
    from ovito.modifiers import ExpressionSelectionModifier as Selection
    from ovito.modifiers import DeleteSelectedModifier as DeleteSelected
    import sys
    from matplotlib import pyplot as plt
    import os
    import numpy as np
    from pathlib import Path
    sys.path.insert(1, f'{sys.path[0]}/scripts')
    from set_lammps import lmp
   
    lmp_input = args.postproc
    if not (os.path.abspath(os.getcwd()).split('/'))[-1]=='scripts':
        os.chdir('scripts')


    path = f"../GB_projects/{args.name}/samples_0K/"
    impath = f"../GB_projects/{args.name}/images/"
    Path(impath).mkdir(exist_ok=True)
    outpath = f"../GB_projects/{args.name}/output/"
    Path(outpath).mkdir(exist_ok=True)
    tmppath = f"../GB_projects/{args.name}/tmp/"
    Path(tmppath).mkdir(exist_ok=True)
    file = f"{path}{args.src[0]}"

    pipeline = import_file(file)
    data0 = pipeline.compute()

    if args.graphic:
        color_mod = ColorCodingModifier(
            property = 'c_eng',
            gradient = ColorCodingModifier.Viridis()
        )
        pipeline.modifiers.append(color_mod)
        data = pipeline.compute()
        pipeline.add_to_scene()
        scene.save('out.ovito')
        os.system('ovito out.ovito')
        os.system('rm out.ovito')

    if args.id:
        ids = args.id
    else:
        ids = int(input('ID of particle to remove: '))

    def find_surface_atoms():
        pipeline.modifiers.append(ConstructSurfaceModifier(radius = 2.4, select_surface_particles=True, compute_distances=True))
        data_surf = pipeline.compute()
        ids0 = data_surf.particles['Selection']==1
        ids1 = data_surf.particles['Particle Identifier'][ids0]
        z_0 = data_surf.particles['Position'][:, 2]
        z = data_surf.particles['Position'][ids0, 2]
        z_mean = z.mean()
        if args.debug:
            y = 0.5
            plt.plot(z_0, [y]*len(z_0), 'x')
            for zs in z:
                if zs>z_mean:
                    col = 'black'
                else:
                    col = 'red'
                plt.plot([zs], [y], 'x', color=col)
                plt.axvline(z_mean, linestyle='--', color='grey')
            plt.show()
        ids = ids1[z>z_mean]
        print(ids)
        return ids

    if ids[0] == 'all':
        ids = find_surface_atoms()

    if type(ids)==int:
        ids = [ids]
    global out
    if args.postproc:
        ind=[]
        for id in ids:
            id = int(id)
            ind.append(list(data0.particles['Particle Identifier']).index(id))
        ind = np.array(ind)
        x = np.array(data0.particles['Position'][:, 0])[ind]
        y = np.array(data0.particles['Position'][:, 1])[ind]
        xlen = data0.cell_[0,0]
        ylen = data0.cell_[1,1]
        xmin = data0.cell_[0,3]
        ymin = data0.cell_[1,3]
        print(xmin, ymin)
        out =  f'##mu for surface of {file}\n##xlen = {xlen}\n##ylen = {ylen}\n'
        out += f'##xmin = {xmin}\n##ymin = {ymin}\n##id mu x y\n'
        mus = []
    
    def do_stuff(i, id):
        global out
        pipeline_i.source.load(file)
        for mod in pipeline_i.modifiers:
            mod.enabled = False
        selection = Selection(expression=f'ParticleIdentifier=={id}')
        pipeline_i.modifiers.append(selection)

        delete = DeleteSelected()
        pipeline_i.modifiers.append(delete)

        data = pipeline_i.compute()
        if args.graphic:
            pipeline_i.add_to_scene()
            scene.save('out.ovito')
            os.system('ovito out.ovito')
            os.system('rm out.ovito')
        if args.outname:
            outname = f'{args.outname}_{id}'
        else:
            outname = f"{(args.src[0]).split('.')[0]}_removed_{id}"

        properties=["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z"]
        if args.src[1]=='dat':
            outtype="lammps/data"
            export_file(pipeline_i, f"{tmppath}{outname}", outtype)
        elif args.src[1]=='dump':
            outtype="lammps/dump"
            properties.append("c_eng")
            export_file(pipeline_i, f"{tmppath}{outname}", outtype, columns = properties)
        
        if args.postproc:            
            log =  os.popen(f'{lmp} -in in.mu '+
                            f'-var gbname {args.name} '+
                            f'-var structure_name_1 samples_0K/{args.src[0]} '+
                            f'-var structure_name_2 tmp/{outname} '+
                            f'-var input {lmp_input} '+
                            f'-pk omp {args.omp_jobs} -sf omp').read()
            exitflag = False
            for line in log.split('\n'):
                if "All done" in line:
                    exitflag = True
                if '!' in line or args.debug:
                    print(line)
                    if 'mu' in line and '!' in line:
                        mu = float(line.split()[-1])
                        print(id, mu)
                        mus.append(mu)
                        out+=f'{id} {mu} {x[i]} {y[i]}\n'
            if not exitflag:
                raise ValueError('Error in LAMMPS!')

    pipeline_i = import_file(file)
    for i, id in enumerate(ids):
        print(f'{i}/{len(ids)}: {round(100*i/len(ids))}%')
        do_stuff(i, id)

    ni_ind = []
    ni_x = []
    ni_y = []
    ni_z = []
    out+='## Ni positions: id, x, y, z\n'
    for i, tp in enumerate(data0.particles['Particle Type']):
        if tp==2:
            ni_ind.append(i)
            ni_x.append((data0.particles['Position'][:, 0])[i])
            ni_y.append((data0.particles['Position'][:, 1])[i])   
            ni_z.append((data0.particles['Position'][:, 2])[i])
            out+=f'#Ni {i} {ni_x[-1]} {ni_y[-1]} {ni_z[-1]}\n'
    
    with open(f'{outpath}mu_{args.src[0]}', 'w') as f:
        f.write(out)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-s", "--structure", required=True, dest='src', nargs=2, metavar=('STRUCTURE', 'TYPE'), 
                        help='structure from removing atom, type: "dat" or "dump"')
    parser.add_argument("-o", "--out-name", required=False, dest='outname', default=False, 
                        help='name of output structure file')
    parser.add_argument("-g", "--graphic", required=False, default=False, action='store_true',
                        help='show OVITO GUI when choosing ID to remove')
    parser.add_argument("--circleplot", required=False, default=False, action='store_true')
    parser.add_argument("--contourplot", required=False, default=False, action='store_true')
    parser.add_argument("--plot-ni", dest='plot_ni', required=False, default=False, action='store_true')
    parser.add_argument("-pp", "--post-proc", required=False, default=False, dest='postproc', 
                        metavar='ROUTINE_INPUT', help='evaluate mu')
    parser.add_argument("-d", "--debug", required=False, default=False, action='store_true', help='plot clustering')
    parser.add_argument("-j", "--omp-jobs", required=False, dest='omp_jobs', default=4)
    parser.add_argument("-i", "--id-to-remove", required=False, nargs='+', dest='id', default=False, 
                        help='list of integers or "all"')
    args = parser.parse_args()
    main(args)