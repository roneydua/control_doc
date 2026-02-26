#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   graphics_atmos.py
@Time    :   2025/07/31 11:24:33
@Author  :   Roney D. Silva
@Contact :   roneyddasilva@gmail.com
'''

import numpy as np
import pandas as pd
import locale
import matplotlib.pyplot as plt
from python.atmosphere1976.atmosphere import Atmosphere1976
# from IPython.core.interactiveshell import InteractiveShell
# from ipywidgets import interactive, fixed
# InteractiveShell.ast_node_interactivity = "all"
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
# plt.style.use("default")
plt.style.use("eahc.mplstyle")
my_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
FIG_L = 6.29
FIG_A = (90.0) / 25.4

atmos_py = Atmosphere1976()
data = pd.read_csv('images/atmosfera_dados.csv')

# compute with atmos
atmos_py_data = []
for i in data["Altitude_km"]:
   atmos_py_data.append(atmos_py.get_properties(i))


atmos_df = pd.DataFrame(atmos_py_data)
atmos_df.keys()


if plt.fignum_exists("atmos"):
   plt.close("atmos")
fig, ax = plt.subplots(nrows=1, ncols=5, num="atmos" ,sharey=True, figsize=(FIG_L, FIG_A))

ax[0].plot(data["Temperatura_K"],data["Altitude_km"])
# ax[0].plot(atmos_df["temperature_K"],atmos_df["altitude_km"])
ax[1].plot(data["Pressao_Pa"],data["Altitude_km"])
# ax[1].plot(atmos_df["pressure_Pa"],atmos_df["altitude_km"])

ax[2].plot(data["Densidade_kgm3"],data["Altitude_km"])
# ax[2].plot(atmos_df["density_kg_m3"],atmos_df["altitude_km"])


ax[3].plot(data["VelocidadeSom_ms"],data["Altitude_km"])
# ax[3].plot(atmos_df["speed_of_sound_m_s"],atmos_df["altitude_km"])

ax[4].plot(data["Gravidade"],data["Altitude_km"])
# ax[4].plot(atmos_df["g_ratio_to_sea_level"]*atmos_py.GZERO,atmos_df["altitude_km"])

ax[0].set_xlabel(r"Temperature $\left[\si{\kelvin}\right]$")
ax[1].set_xlabel(r"Pressure $\left[\si{\pascal}\right]$")
ax[2].set_xlabel(r"Density $\left[\si{\kilo\gram\per\cubic\meter}\right]$")
ax[3].set_xlabel(r"Sound speed $\left[\si{\meter\per\second}\right]$")
ax[-1].set_xlabel(r"Gravitational \\ acceleration $\left[\si{\meter\per\squared\second}\right]$")
ax[0].set_ylabel(r"Altitude $\left[\si{\kilo\meter}\right]$")
ax[0].set_ylim(0, 400)
plt.savefig("images/environmentAtmos.pdf", format="pdf")
plt.close(fig="atmos")