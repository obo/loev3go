#!/usr/bin/env python3
import numpy as np
import sys

# get angle from arg 0
# positive numbers mean counter-clockwise
if len(sys.argv) > 1:
  a=int(sys.argv[1])
else:
  a=None

# load data from stdin
d=np.loadtxt("/dev/stdin")

# construct rotation matrix
c=np.cos(np.radians(a))
s=np.sin(np.radians(a))
m=np.array([[c,-s],[s,c]])

# apply the rotation
r=np.transpose(np.matmul(m, np.transpose(d)))

# save the rotated
np.savetxt("/dev/stdout", r, delimiter="\t")

