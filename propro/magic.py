# propro is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# propro is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with propro.  If not, see <http://www.gnu.org/licenses/>.


'''
Created on Mar 24, 2016

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from IPython.core.magic import Magics
from IPython.core.magic import line_cell_magic
from IPython.core.magic import magics_class
from IPython.utils.ipstruct import Struct
import propro


@magics_class
class ProfileMagic(Magics):
    
    @line_cell_magic("propro")
    def execute(self, parameter_s="", cell=None):
        opts_def = Struct(r=None, t=None, f="png")
        opts, arg_str = self.parse_options(parameter_s, 'r:t:f', posix=False)
        opts.merge(opts_def)
        
        if cell is not None:
            arg_str += '\n' + cell
        code = self.shell.input_splitter.transform_cell(arg_str)
        
        def wrapper():
            ns = {}
            exec(code, self.shell.user_ns, ns)
        
        kwargs = dict(sample_rate= float(opts.r) if opts.r is not None else None,
                      timeout= float(opts.t) if opts.t is not None else None,
                      fmt= opts.f.split(","),)

        prof_dec = propro.profile(**kwargs)
        prof_dec.save_fig = False
        prof_dec.fmt.append("png")
        prof_dec.callname = "IPython cell"
        dec_func = prof_dec(wrapper)
        dec_func()
        
def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(ProfileMagic)
