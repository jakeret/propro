# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Mar 24, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

import matplotlib.pyplot as plt
try:
    import seaborn as sns
    sns.set_style("whitegrid")
except ImportError: pass

import numpy as np

from propro import format_date

MEM_UNITS = ["B", "KB", "MB", "GB"]

def profile_plot(result, title, t0, fmt, save=False):
    fig, ax = plt.subplots(3, 1, sharex=True, squeeze=True, figsize=(12,8))
    time = np.array(result.time)
    time -= time[0]
    
    rss_mem = np.array(result.rss_mem)
    for i in range(0, 4):
        if rss_mem.max() < 1024:
            break
        rss_mem = rss_mem / 1024
        
    unit = MEM_UNITS[i]
    ax[0].plot(time, rss_mem, 'k')
    ax[0].set_ylabel('RSS Memory [%s]'%unit)
    ax[0].set_ylim((0, None))
#     ax[1].plot(time, np.array(result.vms_mem)/factor, 'k')
#     ax[1].set_ylabel('VMS Memory [GB]')
    cpu_load = np.array(result.cpu_load)
    ax[1].plot(time, cpu_load, 'k')
    ax[1].set_ylabel('CPU [%]')
    ax[1].set_ylim((0, int(cpu_load.max() / 101 + 1) * 100 + 5))
    
    threads = np.array(result.threads)
    ax[2].plot(time, threads, 'k')
    ax[2].set_ylabel('Threads')
    ax[2].set_ylim((0, threads.max() * 1.1))
    
    ax[2].set_xlabel('Time [s]')
    fig.suptitle("Profiled '%s' at %s"%(title, format_date(t0)))
    
    if save:
        fig.savefig("propro_%s_%s.%s"%(title, format_date(t0), fmt))
        
    return fig