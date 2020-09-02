FROM python:3
ADD fuse.py /
ADD subtract.py /
RUN apt-get update -y
RUN apt-get install -y libgl1-mesa-glx
RUN pip install opencv-python pydicom numpy argparse Pillow glob2 progressbar
ENTRYPOINT [ "python" ]
