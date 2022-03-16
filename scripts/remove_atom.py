import warnings
warnings.filterwarnings('ignore', message='.*OVITO.*PyPI')
from ovito.io import import_file, export_file
from ovito import scene
from ovito.modifiers import ColorCodingModifier
from ovito.modifiers import ExpressionSelectionModifier as Selection
from ovito.modifiers import DeleteSelectedModifier as DeleteSelected
import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", required=True)
parser.add_argument("-s", "--structure", required=True, dest='src')
parser.add_argument("-o", "--out-name", required=False, dest='outname', default=False)
parser.add_argument("-g", "--graphic", required=False, default=False, action='store_true')
parser.add_argument("-i", "--id-to-remove", required=False, dest='id', default=False)
args = parser.parse_args()



path = f"GB_projects/{args.name}/slices/"
file = f"{path}{args.src}"


pipeline = import_file(file)

data0 = pipeline.compute()


color_mod = ColorCodingModifier(
    property = 'c_eng',
    gradient = ColorCodingModifier.Viridis()
)
pipeline.modifiers.append(color_mod)

data = pipeline.compute()


if args.graphic:
    pipeline.add_to_scene()
    scene.save('out.ovito')
    os.system('ovito out.ovito')
    os.system('rm out.ovito')

if args.id:
    id = args.id
else:
    id = int(input('ID of particle to remove: '))

selection = Selection(expression=f'ParticleIdentifier=={id}')
pipeline.modifiers.append(selection)

delete = DeleteSelected()
pipeline.modifiers.append(delete)

data = pipeline.compute()

if args.graphic:
    pipeline.add_to_scene()
    scene.save('out.ovito')
    os.system('ovito out.ovito')
    os.system('rm out.ovito')
if args.outname:
    outname = args.outname
else:
    outname = f"{args.src.split('.')[0]}_removed_{id}"

export_file(pipeline, f"{path}{outname}", "lammps/dump", columns =
  ["Particle Identifier", "Particle Type", "Position.X", "Position.Y", "Position.Z", "c_eng"])
