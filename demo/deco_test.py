# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Mar 24, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import propro
import numpy as np

@propro.profile(sample_rate=0.1, fmt="txt")
def mem_hungry(size):
    a = []
    for i in range(size):
        a.append(np.random.random())
        
    b = []
    for i in range(size):
        t = []
        for j in range(size):
            t.append(i * a[j])
        b.append(t)

    b = np.array(b)
    
print("calling mem_hungry function")
mem_hungry(5000)
print("done")
