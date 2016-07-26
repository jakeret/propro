# Copyright (C) 2016 ETH Zurich, Institute for Astronomy

# System imports
from __future__ import print_function, division, absolute_import, unicode_literals

import time
import psutil
import subprocess
import threading
import os
import traceback
import sys
from collections import namedtuple
from datetime import datetime
from propro import format_date

__all__ = ["profile", "profile_pid", "profile_cmd"]

ProfileResult = namedtuple("ProfileResult", ("time", "rss_mem", "vms_mem", "cpu_load", "threads"))

SLEEP_TIME = 0.5

PLOTTING_FMTS = ("pdf", "png")

class TimeoutError(Exception):
    pass

def _savetxt(filename, result):
    with open(filename, "w") as fp:
        for i in range(len(result.time)):
            fp.write("\t".join((str(col[i]) for col in result)))
            fp.write("\n")
            
def output(result, fmts, call, t0, baseline=None, save_fig=False):
    fig = None
    
    if baseline is not None:
        result = ProfileResult(result.time,
                               [tmp - baseline[0] for tmp in result.rss_mem],
                               [tmp - baseline[1] for tmp in result.vms_mem],
                               result.cpu_load,
                               [tmp - baseline[3] for tmp in result.threads])
    
    for fmt in set(fmts):
        if fmt in PLOTTING_FMTS:
            from propro import plotting
            fig = plotting.profile_plot(result, call, t0, fmt, save_fig)
            
        elif fmt == "txt":
            _savetxt("propro_%s_%s.%s"%(call, format_date(t0),fmt), result)
            
    return fig

def _measure(parent, interval=None):
    processes = parent.children(recursive=True)
    processes.append(parent)
    
    rss_mem=0
    vms_mem=0
    cpu_percent=0
    num_threads=0
    for process in processes:
        try:
            mem_info = process.memory_info()

            rss_mem += mem_info[0]
            vms_mem += mem_info[1]
            cpu_percent += parent.cpu_percent(interval=interval)
            num_threads += process.num_threads()
        except psutil.NoSuchProcess:
            pass
    return rss_mem, vms_mem, cpu_percent, num_threads


class Profiler(threading.Thread):
    
    def __init__(self, pid, sleep_time=None):
        if sleep_time is None:
            sleep_time = SLEEP_TIME
        self.sleep_time = sleep_time
        self.process = psutil.Process(pid)
        self._exception = None
        self._cancelled = False
        super(Profiler, self).__init__()

    def _active(self):
        return not self._cancelled and self.process.is_running()

    def _profile(self):
        times, rss_mems, vms_mems, cpu_percents, threads = [], [], [], [], []
        
        try:
            while self._active():
                rss_mem, vms_mem, cpu_percent, num_threads = _measure(self.process)
                times.append(time.time())
                rss_mems.append(rss_mem)
                vms_mems.append(vms_mem)
                cpu_percents.append(cpu_percent)
                threads.append(num_threads)
                time.sleep(self.sleep_time)
        except psutil.NoSuchProcess:
            self.cancel()
        except psutil.AccessDenied:
            self.cancel()
        
        return ProfileResult(times, rss_mems, vms_mems, cpu_percents, threads)
    
    def run(self):
        try:
            self._result = self._profile()
        except Exception:
            exc_info = sys.exc_info()
            self._exception = exc_info
            
    def cancel(self):
        self._cancelled = True

    def exception(self, timeout=None):
        self.join(timeout)
        if self.isAlive():
            raise TimeoutError("Call timed out after: "%timeout)
        return self._exception

    def result(self, timeout=None):
        self.join(timeout)
        if self.isAlive():
            raise TimeoutError("Call timed out after: "%timeout)
        return self._result

def profile_pid(pid, sample_rate=None, timeout=None):
    """
    Profile a specific process id 
    
    :param pid: The process id to profile
    :param sample_rate: (optional) Rate at which the process is being queried
    :param timeout: (optional) Maximal time the process is being profiled
    
    :returns ProfileResult: A `ProfileResult` namedtuple with the profiling result
    """
    if not psutil.pid_exists(pid):
        raise ValueError("Pid '%s' does not exist"%pid)
    
    profiler = Profiler(pid, sample_rate)
    profiler.start()
    ex = profiler.exception(timeout)
    if ex is not None:
        traceback.print_exception(*ex)
        raise ex
    
    return profiler.result()
    
def profile_cmd(cmd, sample_rate=None, timeout=None):
    """
    Profile a specific command 
    
    :param cmd: The command to profile 
    :param sample_rate: (optional) Rate at which the process is being queried
    :param timeout: (optional) Maximal time the process is being profiled
    
    :returns ProfileResult: A `ProfileResult` namedtuple with the profiling result
    """
    process = subprocess.Popen(cmd, shell=True)
    return profile_pid(process.pid, sample_rate, timeout)


class profile(object):
    """
    Decorator to profile a function or method. The profile result is automatically written to disk.  
    
    :param sample_rate: (optional) Rate at which the process is being queried
    :param timeout: (optional) Maximal time the process is being profiled
    :param fmt: (optional) The desired output format. Can also be a tuple of formats. Supported: txt and any matplotlib fmt
    :param callname: (optional) Name used for plot title and output file name
    """
    def __init__(self, sample_rate=None, timeout=None, fmt="txt", callname=None):

        self.sample_rate = sample_rate
        self.timeout = timeout
        
        if isinstance(fmt, basestring):
            fmt = [fmt]
        self.fmt = fmt
        self.save_fig=True
        self.callname = callname

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            pid = os.getpid()
            profiler = Profiler(pid, self.sample_rate)
            baseline = _measure(profiler.process)
            try:
                profiler.start()
                t0 = datetime.now()
                res = func(*args, **kwargs)
                profiler.cancel()
                ex = profiler.exception(self.timeout)
                if ex is not None:
                    raise ex
                prof_res = profiler.result(self.timeout)
                if self.callname is None:
                    self.callname = func.func_name
                self.fig = output(prof_res, self.fmt, self.callname, t0, baseline, self.save_fig)
                return res
            finally:
                profiler.cancel()
                
        return wrapper

