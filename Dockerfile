FROM python:3
ADD fuse.py /
ARG i1
ADD $i1 ./
ARG i2
ADD $i2 ./
RUN pip install opencv-python pydicom numpy argparse Pillow
ENTRYPOINT [ "python", "./fuse.py" ]
