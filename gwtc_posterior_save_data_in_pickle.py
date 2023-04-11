# Here we download all files precisely Posteriors Estimation data release  (PE)
# from GWTC-2.1, GWTC-1 and GWTC-3

"""
- get PE for the events analyzed by the GWTC-2 rates and populations paper,
 which you can do by going to the GWTC-2.1 data release and downloading everything and
then removing events that are below the FAR threshold used in the GWTC-2  rates and populations paper
- do the same for GW190814, GW170817, GW190425 and the two NSBHs found in O3b.
The first three should be in the GWTC-2.1 data release,
but the NSBHs you'll need to get from the GWTC-3 data release 
or the data release that accompanied the NSBH paper
"""

## installation of environment
# The easy way is to install zenodo_get and download

# * pip install zenodo_get

# Download GWTC-2.1 vesrsion v2 by run the following command line

# * zenodo_get 6513631

# then GWTC-3 v1 by using this one, later
# you could use it to extract only the NSBH in ther

# *zenodo_get 5546663

# At the end GWTC-1 to just go here
# https://dcc.ligo.org/LIGO-P1800370/public and take

# * wget https://dcc.ligo.org/public/0157/P1800370/005/GWTC-1_sample_release.tar.gz
# then unzip it , or only download 'GW170817' data

##############################

# To read them , you need to,
# Install `pesummary<=0.9.1`, `seaborn<=0.10.1`

# to read and extract the data , in GWTC-2.1 and GWTC-3

# Note that  `pesummary<=0.9.1`, `seaborn<=0.10.1` is only to extract and save ,
# our PE in a pickle file to plot them in another environnement where seaborn version is recent,

# * p install seaborn==0.12.2

import os
import glob
import pickle
import numpy as np
from tqdm.auto import tqdm

import pesummary
from pesummary.io import read

print(pesummary.__version__)
import h5py

import warnings

warnings.filterwarnings("ignore")
from pesummary.utils.utils import logger
import logging

logger.setLevel(logging.CRITICAL)


# NSBH = ['GW191219', 'GW200105', 'GW200115', 'GW190917']
# BNS  =  ['GW170817', 'GW190425']
# =============================================================================
# returns each populations directory
# =============================================================================
BBH_path = f"{os.path.dirname(os.path.realpath('__file__'))}/GWTC-2.1/v2"

BNS_path = f"{os.path.dirname(os.path.realpath('__file__'))}/GWTC-1"

NSBH_path = f"{os.path.dirname(os.path.realpath('__file__'))}/GWTC-3"


print("===============================================")

# =============================================================================
# BBH populations, input the BBHs _cosmo.h5 files  in GWTC-2.1
# =============================================================================
bbh_filenames = glob.glob((BBH_path + "/**/*_cosmo.h5"), recursive=True)

bns_gw_names = []
nsbh_gw_names = []
bbh_gw_names = []

table_masses = {}

# Note that in GWTC-2.1 'GW190917' is classify as a NSBH

with tqdm(total=len(bbh_filenames)) as progress:
    for f in bbh_filenames:

        # name of GW event
        gw_name = f.split("/")[-1].split("-")[-1].split("_")[0]

        # Using pesummary to read GW data
        data = read(f)
        print("Found run labels:")
        print(data.labels)

        # Read data from 'C01:IMRPhenomXPHM'
        samples_dict = data.samples_dict

        try:
            posterior_samples = samples_dict["C01:IMRPhenomXPHM"]
            # posterior_samples = samples_dict['C01:Mixed']
            if gw_name in ["GW190425", "GW190814"]:
                bns_gw_names.append(gw_name)

            elif gw_name == "GW190917":
                nsbh_gw_names.append(gw_name)
            else:
                bbh_gw_names.append(gw_name)

        except KeyError:
            try:
                posterior_samples = samples_dict["C01:IMRPhenomNSBH:HighSpin"]

                if gw_name in ["GW190425", "GW190814"]:
                    bns_gw_names.append(gw_name)

                elif gw_name == "GW190917":
                    nsbh_gw_names.append(gw_name)
                else:
                    bbh_gw_names.append(gw_name)

            except KeyError:

                posterior_samples = samples_dict["C01:IMRPhenomPv2_NRTidal:HighSpin"]

                print("************************************************************")
                print(gw_name)

                print("====================================================")

                if gw_name in ["GW190425", "GW190814"]:
                    bns_gw_names.append(gw_name)

                elif gw_name == "GW190917":
                    nsbh_gw_names.append(gw_name)
                else:
                    bbh_gw_names.append(gw_name)

        table_masses[gw_name] = {}
        table_masses[gw_name]["mass1"] = list(posterior_samples["mass_1_source"])
        table_masses[gw_name]["mass2"] = list(posterior_samples["mass_2_source"])

        del samples_dict, posterior_samples, f, gw_name
        progress.update()


# =============================================================================
# NSBH populations in GWTC-3 and GWTC-2.1
# =============================================================================
## NSBH event from GWTC-3
# Note that in GWTC-2.1 'GW190917' is classify as a NSBH

# NSBHvents names
NSBH = ["GW191219", "GW200105", "GW200115"]

nsbh_filenames = glob.glob((NSBH_path + "/**/*_cosmo.h5"), recursive=True)

with tqdm(total=len(NSBH)) as progress:
    for file in nsbh_filenames:
        # name of GW event
        gw_name = file.split("/")[-1].split("-")[-1].split("_")[0]

        if gw_name in NSBH:
            # Add together NSBH populations in GWTC-3 and GWTC-2.1
            nsbh_gw_names.append(gw_name)

            # Using pesummary to read GW data
            data = read(file)
            print("Found run labels:")
            print(data.labels)

            # Read data from 'C01:IMRPhenomXPHM'
            samples_dict = data.samples_dict

            try:
                posterior_samples = samples_dict["C01:Mixed"]

            except KeyError:
                posterior_samples = samples_dict["C01:IMRPhenomNSBH:HighSpin"]

            table_masses[gw_name] = {}
            table_masses[gw_name]["mass1"] = list(posterior_samples["mass_1_source"])
            table_masses[gw_name]["mass2"] = list(posterior_samples["mass_2_source"])

            del samples_dict, posterior_samples, file, gw_name
            progress.update()


# =============================================================================
# BNS populations
# =============================================================================
## BNS event from GWTC-1
BNS = ["GW170817"]

with tqdm(total=len(BNS)) as progress:
    for gw_name in BNS:

        BNS_file = f"{BNS_path}/{gw_name}_GWTC-1.hdf5"

        # Add together BNS (GW170817) from GWTC-1 and to  BN (GW190425) in GWTC-2.1
        bns_gw_names.append(gw_name)

        posterior_samples = h5py.File(BNS_file, "r")
        print(posterior_samples.keys())

        table_masses[gw_name] = {}
        table_masses[gw_name]["mass1"] = list(
            posterior_samples["IMRPhenomPv2NRT_highSpin_posterior"][
                "m1_detector_frame_Msun"
            ]
        )
        table_masses[gw_name]["mass2"] = list(
            posterior_samples["IMRPhenomPv2NRT_highSpin_posterior"][
                "m2_detector_frame_Msun"
            ]
        )

        del BNS_file, posterior_samples, file, gw_name
        progress.update()


# Add GW names in table_masses,  dictionary
table_masses["bns_gw_names"] = bns_gw_names
table_masses["nsbh_gw_names"] = nsbh_gw_names
table_masses["bbh_gw_names"] = bbh_gw_names

# np.save('masses_file', table_masses)

# Save masses(table_mass) in a pickle file
try:
    with open("masses_file_IMRPhenom.pkl", "wb") as masses_file:
        pickle.dump(table_masses, masses_file, protocol=pickle.HIGHEST_PROTOCOL)

except:
    print("Unable to write to file")
