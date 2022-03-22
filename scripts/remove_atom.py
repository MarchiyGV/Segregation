    
def main(args):    
    from turtle import color
    import warnings
    warnings.filterwarnings('ignore', message='.*OVITO.*PyPI')
    from ovito.io import import_file, export_file
    from ovito import scene
    from ovito.modifiers import ColorCodingModifier
    from ovito.modifiers import ExpressionSelectionModifier as Selection
    from ovito.modifiers import DeleteSelectedModifier as DeleteSelected
    import sys
    from matplotlib import pyplot as plt
    import os
    import numpy as np
    from sklearn.cluster import DBSCAN
    from pathlib import Path

    lmp_input = args.postproc
    if not (os.path.abspath(os.getcwd()).split('/'))[-1]=='scripts':
        os.chdir('scripts')


    path = f"../GB_projects/{args.name}/slices/"
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
        z = data0.particles['Position'][:, 2]
        data = DBSCAN(eps=0.8, min_samples=10).fit(z.reshape(-1,1))
        clusters = data.fit_predict(z.reshape(-1,1))
        n = clusters[(list(z)).index(z.max())]
        if args.debug:
            for i, c in enumerate(clusters):
                if c==-1:
                    col='black'
                else:
                    col=(10*['red', 'blue', 'green', 'pink', 'yellow', 'orange'])[c]
                plt.plot([z[i]], [0.5], 'x', color=col)
            plt.show()
        ids = np.array(data0.particles['Particle Identifier'])[clusters==n]
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
        pipeline_i = import_file(file)
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
            log =  os.popen(f'lmp_omp_edited -in in.mu '+
                            f'-var gbname {args.name} '+
                            f'-var structure_name_1 slices/{args.src[0]} '+
                            f'-var structure_name_2 tmp/{outname} '+
                            f'-var input {lmp_input} '+
                            f'-pk omp {args.omp_jobs} -sf omp').read()
            for line in log.split('\n'):
                if '!' in line or args.debug:
                    print(line)
                    if 'mu' in line and '!' in line:
                        mu = float(line.split()[-1])
                        print(id, mu)
                        mus.append(mu)
                        out+=f'{id} {mu} {x[i]} {y[i]}\n'

    for i, id in enumerate(ids):
        do_stuff(i, id)

    if args.postproc:
        if args.contourplot:
            from scipy import interpolate
            interp = interpolate.interp2d(x, y, mus, bounds_error=False, fill_value=0)
            xs = np.linspace(x.min(), x.max())
            ys = np.linspace(y.min(), y.max())
            X, Y = np.meshgrid(xs, ys)
            MU=np.empty_like(X)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    MU[i, j]=interp(X[i,j], Y[i,j])
            plt.contourf(xs, ys, MU)
            plt.plot(x,y,'x')
            plt.colorbar()
            plt.show()
        if args.circleplot:
            from matplotlib import cm, colors
            xlen = data0.cell_[0,0]
            ylen = data0.cell_[1,1]
            fig = plt.figure(figsize=(6,6*ylen/xlen)) # give plots a rectangular frame
            ax = fig.add_subplot(111)
            mus = np.array(mus)
            x = np.array(x)
            y = np.array(y)
            cmap = cm.viridis
            for i in range(len(x)):
                c = (mus[i]-mus.min())/(mus.max()-mus.min())
                color = cmap(c)
                circle = plt.Circle((x[i], y[i]), 0.5, color=color)
                ax.add_artist(circle)
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
            if args.plot_ni:
                plt.plot(ni_x, ni_y, 'x')
            xmin = data0.cell_[0,3]
            xmax = xmin + xlen
            ymin = data0.cell_[1,3]
            ymax = ymin + ylen
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)
            ax.set_aspect('equal')
            norm = colors.Normalize(vmin=mus.min(), vmax=mus.max()) 
            plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
            plt.savefig(f'{impath}mu_{args.src[0]}.png')
            plt.show()
    print(out)
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