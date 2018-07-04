#!/usr/bin/env python3

# python print to stderr (most portable and flexible)
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

import numpy as np
import scipy.optimize
import sys

# get angle from arg 0
# positive numbers mean counter-clockwise
if len(sys.argv) > 1:
  a=float(sys.argv[1])
else:
  a=None

# load data from stdin
d=np.loadtxt("/dev/stdin")

def rotated_data(a):
  # construct rotation matrix
  c=np.cos(np.radians(a))
  s=np.sin(np.radians(a))
  m=np.array([[c,-s],[s,c]])
  # apply the rotation
  r=np.transpose(np.matmul(m, np.transpose(d)))
  return r

if a is None:
  # optimizing
  def f(a):
    rd=rotated_data(a)
    slic=rd[:,1]
    l=np.min(slic)
    h=np.max(slic)
    cost=(h-l)**2
    return cost
  res=scipy.optimize.minimize_scalar(f)
  assert res.success
  eprint('Found best rotation angle:', res.x)
  a=res.x

# save the rotated
np.savetxt("/dev/stdout", rotated_data(a), delimiter="\t")

