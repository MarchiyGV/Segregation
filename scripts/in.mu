# INITIALIZATION
clear

units metal
atom_style atomic
boundary p p m
variable gbname index STGB_210 #should be selected by user
variable structure_name_1 index slice.dat #should be selected by user
variable structure_name_2 index slice.dat #should be selected by user
variable input index mu #[.txt] should be selected by user

variable self index mu

variable path index GB_projects
variable pot_path index potentials
variable home index scripts
variable thermo_output index thermo_output
variable dump index dump
variable structure_1 index ${path}/${gbname}/${structure_name_1}
variable structure_2 index ${path}/${gbname}/${structure_name_2}
variable gbpath index ${path}/${gbname}


shell mkdir ../${gbpath}/logs
log ../${gbpath}/logs/${self}.log
shell rm log.lammps

variable thermo_step_M equal 100
variable dump_step_M equal 500
include minimization_params.txt

print " "
print "%%%%%%%%%%%%%%%%%%%%%%%%%"
print "----------input----------"
include ../${gbpath}/${input}.txt
shell cat ../${gbpath}/${input}.txt
print " "
print "%%%%%%%%%%%%%%%%%%%%%%%%%"
print " "
variable dump_path index ${gbpath}/${dump}/${self}
shell mkdir ../${gbpath}/${dump}
shell mkdir ../${dump_path}
# ATOMS DEFINITION
read_data ../${structure_1}
######################################
# DEFINE INTERATOMIC POTENTIAL

shell cd ../${pot_path}
include ${potname_alloy}
shell cd ../${home}

######################################
# DEFINE THERMO AND OUTPUT

dump 1 all cfg ${dump_step_M} ../${dump_path}/dump_*.cfg mass type xs ys zs
dump_modify 1 element Ag ${element}


# ---------- Run Minimization --------------------- 
#reset_timestep 0
compute eng all pe/atom 
compute eatoms all reduce sum c_eng

run 0

variable file_tmp index ${self}_E.txt
fix tmp all print 1 "variable E0 equal $(c_eatoms)" file ${file_tmp} screen yes
run 0
variable z0 delete
include ${file_tmp}
unfix tmp
shell rm ${file_tmp}

delete_atoms group all compress yes
read_data ../${structure_2} add append

thermo ${thermo_step_M}
thermo_style custom step pe lx ly lz press pxx pyy pzz 
min_style cg
minimize ${etol} ${ftol} ${maxiter} ${maxeval} 

variable file_tmp index ${self}_E.txt
fix tmp all print 1 "variable E equal $(c_eatoms)" file ${file_tmp} screen yes
run 0
include ${file_tmp}
unfix tmp
shell rm ${file_tmp}


variable mu equal "v_E0-v_E"
print "!mu ${mu}" file ${self}_${input}.out screen yes
print "All done"