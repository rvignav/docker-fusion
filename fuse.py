import cv2
import pydicom as dicom
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
import numpy as np
from numpy import linalg as LA
import argparse
from PIL import Image  
import datetime
import glob
import sys
import os
import progressbar

parser = argparse.ArgumentParser(description='Fuse two images')
parser.add_argument('i1', type=str, help='Path to first series')
parser.add_argument('i2', type=str, help='Path to second series')

args = parser.parse_args()

series_path1 = args.i1
series_path2 = args.i2
studies = glob.glob('/home/series/PatientSeries/*')
paths = []
for study in studies:
    series_paths = glob.glob(study + '/*')
    for item in series_paths:
        paths.append(item)

i1 = ''
i2 = ''
for path in paths:
    if series_path1 in path:
        i1 = path
        break
for path in paths:
    if series_path2 in path:
        i2 = path
        break

def bubble_sort(series):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(series) - 1):
            if series[i].SliceLocation > series[i + 1].SliceLocation:
                # Swap the elements
                series[i], series[i + 1] = series[i + 1], series[i]
                swapped = True
    return series

print(i1)
print(i2)
series1DCM = glob.glob(str(i1) + "/*.dcm")
series2DCM = glob.glob(str(i2) + "/*.dcm")

if (len(series1DCM) != len(series2DCM)):
    print("ERROR: The two inputted DICOM series do not have the same number of slices.")
    exit(0)

bar = progressbar.ProgressBar(maxval=len(series1DCM)/5 + 1, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

one = dicom.read_file(series1DCM[0])
two = dicom.read_file(series2DCM[0])
image1 = one.pixel_array 
image2 = two.pixel_array
shape1 = image1.shape[::-1]
shape2 = image2.shape[::-1]
maxshape = ()
if shape1[0] > shape2[0]:
  maxshape = shape1
else:
  maxshape = shape2

# Sort lists
for i in range(len(series1DCM)):
  series1DCM[i] = dicom.read_file(series1DCM[i])  

for i in range(len(series2DCM)):
  series2DCM[i] = dicom.read_file(series2DCM[i])  

series1DCM = bubble_sort(series1DCM)
series2DCM = bubble_sort(series2DCM)

if not os.path.isdir('output'):
  os.mkdir('output')

def fuse(ds1, ds2, maxshape):
  im1 = ds1.pixel_array # np.asarray(cv2.imread(ds1.pixel_array, 0))
  im2 = ds2.pixel_array # np.asarray(cv2.imread(ds2.pixel_array, 0))
  im1 = cv2.resize(im1, maxshape)
  im2 = cv2.resize(im2, maxshape)

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
  return imf

def save(filename, imf, ds1, ds2):
  cv2.imwrite('img.png', imf)
  im_frame = Image.open('img.png')

  file_meta = FileMetaDataset()
  suffix = '.dcm'

  ds = FileDataset('output/' + str(filename), {},
                  file_meta=file_meta, preamble=b"\0" * 128)
  ds.SOPInstanceUID = generate_uid()
  ds.SeriesInstanceUID = generate_uid()
  ds.SeriesDescription = 'Fusion ' + ds1.SeriesDescription + ' ' + ds2.SeriesDescription
  ds.ContentCreatorName = 'ePAD'
  ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian 
  ds.ContentDate = datetime.datetime.now().strftime('%Y%m%d')
  ds.ContentTime = datetime.datetime.now().strftime('%H%M%S.%f')[:11]
  ds.ContentLabel = 'Fusion'
  ds.ImagePositionPatient = ds1.ImagePositionPatient
  ds.SliceLocation = ds1.SliceLocation

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
      ds.save_as('output/' + str(filename))
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
      ds.save_as('output/' + str(filename))

bar.start()
for i in range(len(series1DCM)):
  imf = fuse(series1DCM[i], series2DCM[i], maxshape)
  save('im'+str(i)+'.dcm', imf, series1DCM[i], series2DCM[i])
  if i % 5 == 0:
    # update progress
    bar.update(i/5 + 1)
bar.finish()

print("Fused images saved to the folder 'output'")
