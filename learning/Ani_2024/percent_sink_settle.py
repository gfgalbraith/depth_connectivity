# -*- coding: utf-8 -*-
"""

This script creates computes the percentage of sink sites and that of released particles that settle within the cluster

@author: Chinenye Ani, AIMS
"""

import networkx as nx
import numpy as np
import pandas as pd

connect_2d = pd.read_csv('/outputs/Moore_2015_d1transfer_probability_matrix_wide_2d.csv', header = None, skiprows=4)
connect_3d = pd.read_csv('/outputs/Moore_2015_d1transfer_probability_matrix_wide_3d.csv', header = None, skiprows=4)
sink_2d = np.where(connect_2d.sum(axis=0,numeric_only=True))[0]  # find sink sites
sink_3d = np.where(connect_3d.sum(axis=0,numeric_only=True))[0]
percent_2d = 100 * len(sink_2d) / 334  #calculate percentage of sinks
percent_3d = 100 * len(sink_3d) / 334
settle_2d = 100 * sum(connect_2d.sum(axis=1,numeric_only=True) * 61)/ 20374  # calculate the percentage of released particles that settle within the cluster
settle_3d = 100 * sum(connect_3d.sum(axis=1,numeric_only=True) * 61)/ 20374
print(percent_2d, percent_3d)