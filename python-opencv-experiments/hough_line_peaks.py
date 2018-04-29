# from https://git.sciunto.org/mirror/scikit-image/raw/0a7711b1bcdf5cdbdb730e937bedfe5d79329a7a/skimage/transform/hough_transform.py

import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.draw import line
img = np.zeros((15, 15), dtype=np.bool_)
rr, cc = line(0, 0, 14, 14)
img[rr, cc] = 1
rr, cc = line(0, 14, 14, 0)
img[cc, rr] = 1
hspace, angles, dists = hough_line(img)
hspace, angles, dists = hough_line_peaks(hspace, angles, dists)
len(angles)
