__author__ = 'Joel Akeret'
__email__ = 'jakeret@phys.ethz.ch'
__version__ = '0.1.0'
__credits__ = 'ETH Zurich, Institute for Astronomy'

def format_date(date, fmt="%Y-%m-%d-%H:%M:%S"):
    return date.strftime(fmt)

from propro import *

try:
    from magic import *
except Exception: pass


