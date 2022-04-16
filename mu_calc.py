E_p_0 = -24782.3846293875 #final
E_p_1 = -24472.5535103112 #final

E_wfc110_p_0 = -24782.3612555626 #final
E_wfc110_p_1 = -24472.5256153101 #final

E_wfc110_a_0 = -24807.8136411687 #final
E_wfc110_a_1 = -24497.9705093705 #final
 
E_k3_p_0 = -24782.3766633464 #final
E_k3_p_1 = -24472.5431838997 #final

E_k2_p_0 = -24782.3604303399 #final
E_k2_p_1 = -24472.5248006393 #final

E_a_0 = -24807.83784225 #final
E_a_1 = -24497.9996853114 #final
E_a_2 = -24498.0073963742 #final
E_a_3 = -24498.0069078252 #final

E_15vac_a_0 = -24807.8378434103 #final
E_15vac_a_1 = -24497.9996862611 #final

E_15vac_k3_a_1 = -24497.9886084714 #final
E_15vac_k3_a_0 = -24807.8290838320 #final

E_15vac_k2_a_1 = -24497.9696908716 #final
E_15vac_k2_a_0 = -24807.8128121284 #final
      
DFT_mu_p_0 = (E_p_0 - E_p_1)*13.6056980659
DFT_mu_a_1 = (E_a_0 - E_a_1)*13.6056980659
DFT_mu_a_2 = (E_a_0 - E_a_2)*13.6056980659
DFT_mu_a_3 = (E_a_0 - E_a_3)*13.6056980659

DFT_mu_k3_p_0 = (E_k3_p_0 - E_k3_p_1)*13.6056980659
DFT_mu_k2_p_0 = (E_k2_p_0 - E_k2_p_1)*13.6056980659
DFT_mu_wfc110_p_0 = (E_wfc110_p_0 - E_wfc110_p_1)*13.6056980659

DFT_mu_15vac_a_1 = (E_15vac_a_0 - E_15vac_a_1)*13.6056980659
DFT_mu_15vac_k3_a_1 = (E_15vac_k3_a_0 - E_15vac_k3_a_1)*13.6056980659
DFT_mu_15vac_k2_a_1 = (E_15vac_k2_a_0 - E_15vac_k2_a_1)*13.6056980659
DFT_mu_wfc110_a_1 = (E_wfc110_a_0 - E_wfc110_a_1)*13.6056980659

DFT_dmu1 = (DFT_mu_a_1 - DFT_mu_p_0)
DFT_dmu2 = (DFT_mu_a_2 - DFT_mu_p_0)
DFT_dmu3 = (DFT_mu_a_3 - DFT_mu_p_0)

DFT_dmu_15vac_1 = (DFT_mu_15vac_a_1 - DFT_mu_p_0)
DFT_dmu_15vac_k3_1 = (DFT_mu_15vac_k3_a_1 - DFT_mu_k3_p_0)
DFT_dmu_15vac_k2_1 = (DFT_mu_15vac_k2_a_1 - DFT_mu_k2_p_0)

DFT_dmu_wfc110_1 = (DFT_mu_wfc110_a_1 - DFT_mu_wfc110_p_0)

print('DFT', DFT_dmu1, DFT_dmu2, DFT_dmu3)

mu_p = -3.48688943149

mu_a_1 = -3.58976608143999
mu_a_2 = -3.43710577076899
mu_a_3 = -3.47475040139599

MD_dmu1 = (mu_a_1 - mu_p)
MD_dmu2 = (mu_a_2 - mu_p)
MD_dmu3 = (mu_a_3 - mu_p)
print('MD', MD_dmu1, MD_dmu2, MD_dmu3)



from matplotlib import pyplot as plt
import numpy as np
x = np.array([1,2,3])
dft = np.array([DFT_dmu1, DFT_dmu2, DFT_dmu3])
md = np.array([MD_dmu1, MD_dmu2, MD_dmu3])
d = 0.3
w = 0.3
plt.bar(x-d/2, dft, width=w, label='DFT')
plt.bar(x+d/2, md, width=w, label='EAM')
#plt.bar(x[0:1]-(d+w)/2, [DFT_dmu_wfc110_1], width=w/3, label="k2 110wfc")
#plt.bar(x[0:1]-(d+w-2*w/3)/2, [DFT_dmu_15vac_k2_1], width=w/3, label='k2')
#plt.bar(x[0:1]-(d+w-4*w/3)/2, [DFT_dmu_15vac_k3_1], width=w/3, label='k3')
plt.xticks(x, x)
plt.gca().set_aspect('auto')
plt.xlabel('position')
plt.ylabel('$\Delta \mu, eV$')
plt.legend()
plt.gcf().tight_layout()
plt.show()