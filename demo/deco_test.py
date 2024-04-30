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

import numpy as np

import propro


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
