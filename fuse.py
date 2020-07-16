import cv2
import pydicom as dicom
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
import numpy as np
from numpy import linalg as LA
import argparse
from PIL import Image  
import tempfile
import datetime

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

print("Fused image saved to img.dcm")

file_meta = FileMetaDataset()
suffix = '.dcm'

ds = FileDataset('img.dcm', {},
                 file_meta=file_meta, preamble=b"\0" * 128)
ds.SOPInstanceUID = generate_uid()
ds.SeriesInstanceUID = generate_uid()
ds.SeriesDescription = 'Resulting image from fusing ' + ds1.SeriesDescription + ' with ' + ds2.SeriesDescription

ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian 
dt = datetime.datetime.now()
ds.ContentDate = dt.strftime('%Y%m%d')
timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
ds.ContentTime = timeStr

im_frame = Image.open('img.png')

if im_frame.mode == 'L':
    # (8-bit pixels, black and white)
    np_frame = np.array(im_frame.getdata(),dtype=np.uint8)
    ds.Rows = im_frame.height
    ds.Columns = im_frame.width
    ds.PhotometricInterpretation = "MONOCHROME1"
    ds.SamplesPerPixel = 1
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = np_frame.tobytes()
    ds.save_as('img.dcm')
elif im_frame.mode == 'RGBA':
    # RGBA (4x8-bit pixels, true colour with transparency mask)
    np_frame = np.array(im_frame.getdata(), dtype=np.uint8)[:,:3]
    ds.Rows = im_frame.height
    ds.Columns = im_frame.width
    ds.PhotometricInterpretation = "RGB"
    ds.SamplesPerPixel = 3
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = np_frame.tobytes()
    ds.save_as('img.dcm')
