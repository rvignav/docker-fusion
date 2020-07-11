import cv2
import pydicom as dicom
import numpy as np
from numpy import linalg as LA
import argparse
from PIL import Image  

parser = argparse.ArgumentParser(description='Fuse two images')
parser.add_argument('i1', type=str, help='Path to first image')
parser.add_argument('i2', type=str, help='Path to second image')

args = parser.parse_args()

i1 = args.i1
i2 = args.i2

ds1 = dicom.read_file(i1)
ds2 = dicom.read_file(i2)
im1 = ds1.pixel_array; # np.asarray(cv2.imread(ds1.pixel_array, 0))
im2 = ds2.pixel_array; # np.asarray(cv2.imread(ds2.pixel_array, 0))
shape = im1.shape[::-1]
im2 = cv2.resize(im2, shape)

C = np.cov([im1.flatten('F'), im2.flatten('F')])
w, V = LA.eig(C)
a = []
b = []
D = np.diag(w)

for i in range(V.shape[0]):
  a.append(V[i][0])
  b.append(V[i][1])
if D[0][0] >= D[1][1]:
  pca = a/sum(a)
else:
  pca = b/sum(b)

imf = pca[0]*im1 + pca[1]*im2
cv2.imwrite("img.png", imf)

print("Fused image saved to img.png")

im = Image.open('img.png')
im.show()
