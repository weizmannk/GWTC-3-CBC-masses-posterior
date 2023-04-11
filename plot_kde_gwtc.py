import numpy as np
import pandas as pd
import pickle
from tqdm.auto import tqdm

import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.patches as  mpatches

plt.style.use('seaborn-v0_8-darkgrid')

## fix color for GW envents
nsbh_color = 'olive'
GW190814_color ='darkviolet'
    
bns_color, color_1 , color_2, bbh_color= sns.color_palette('rocket', 4)

#read GWTC-2.1 data 
with open('masses_file_IMRPhenom.pkl', 'rb') as handle:
    table_masses = pickle.load(handle)

#GW events list names 
bns_gw_names  = table_masses['bns_gw_names']
nsbh_gw_names = table_masses['nsbh_gw_names']
bbh_gw_names  = table_masses['bbh_gw_names']

# Add all GW populations together
gw_names =  bns_gw_names + nsbh_gw_names + bbh_gw_names

# Set up the figure
f, ax = plt.subplots()
ax.set_aspect("equal")

with tqdm(total=len(gw_names)) as progress:
    for gw_name in gw_names:
        df = pd.DataFrame(data=table_masses[gw_name])
        
        if gw_name in bns_gw_names:
            if gw_name == 'GW190814':
                ax = sns.kdeplot(data=df, x='mass1', y='mass2',  color=GW190814_color, levels=1,  thresh=0.1)
            else :
                ax = sns.kdeplot(data=df, x='mass1', y='mass2',  color=bns_color, levels=1,  thresh=0.1)

        elif gw_name in nsbh_gw_names:
            ax = sns.kdeplot(data=df, x='mass1', y='mass2',  color=nsbh_color, levels=1,  thresh=0.1)
            
        else:
            if  gw_name in bbh_gw_names and gw_name not in bns_gw_names+nsbh_gw_names + ['GW190725']:
                ax = sns.kdeplot(data=df, x='mass1', y='mass2',  color=bbh_color, levels=1,  thresh=0.1)
            
        del gw_name, df
        progress.update()


ax.set(xscale='log', yscale='log')
        
#Plot Mass Gap

# MGapNS , m1 in [2.5, 5] and m2 in [1, 2.5[ 
ax.fill_between([2.5, 5], [2.5, 5], color='blue', linewidth=0, alpha=0.1)

#MGapBH, m1  in [5, 100[ and m2 in [2.5, 5[ 
ax.fill_between([5, 200],  5, 2.5, color='blue', linewidth=0, alpha=0.1)

## Remobe logscale values and reput the values in bellow.
ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax.set_xticks([1, 2, 3, 5, 10, 20, 30, 50, 100, 200, ])
ax.set_yticks([1, 2, 3, 5, 10, 20, 30, 50, 100, 200])


xlim = [1, 200]
ylim = [0.7, 150]

ax.set_xlim(xlim)
ax.set_ylim(ylim)

handles = [mpatches.Patch(facecolor=bns_color, label='BNS'), 
           mpatches.Patch(facecolor=nsbh_color, label='NSBH'),
           mpatches.Patch(facecolor=bbh_color, label='BBH'), 
          mpatches.Patch(facecolor=GW190814_color, label='GW190814')]

ax.text(60, 3.3, "Mass Gap",  color="navy", fontsize=14, fontweight="bold")

plt.legend(handles=handles, shadow=True, loc='upper left', bbox_to_anchor=(1.25, 0.5))

ax.set_xlabel(r'$m_1$ [$M_\odot$]', fontsize=14 ,fontweight="bold")
ax.set_ylabel(r'$m_2$ [$M_\odot$]', fontsize=14 ,fontweight="bold")

plt.gcf().set_size_inches(12, 6)
plt.subplots_adjust(left=0.1,
            bottom=0.1,
            right=0.9,
            top=0.9,
            wspace=0.4,
            hspace=0.4)

f.tight_layout()
plt.savefig(f'GWTC3_IMRPhenom_CIT.png')
plt.close()
