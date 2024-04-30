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
Created on Mar 29, 2016

author: jakeret
'''

from datetime import datetime

import click

from propro.propro import profile_cmd, output


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option("--sample-rate", default=None, type=float, help="Rate at which the process is being queried")
@click.option("--timeout", default=None, type=float, help="Maximal time the process is being profiled")
@click.option("--fmt", default="txt", help="Output format")
@click.option("--name", default=None, help="Name of the output file. Default is the profiled command")
@click.argument("cmd", required=True, nargs=-1)
def run(sample_rate, timeout, fmt, name, cmd):
    if len(cmd) == 0:
        raise ValueError("Command is missing")

    cmd = " ".join(cmd)
    fmts = fmt.split(",")
    t0 = datetime.now()

    print("Going to profile '%s'" % cmd)

    prof_result = profile_cmd(cmd, sample_rate, timeout)

    if name is None:
        name = cmd.replace(" ", "_")

    print("Done. Output is written with prefix '%s' in format(s) '%s'" % (name, fmt))
    output(prof_result, fmts, name, t0, save_fig=True)
