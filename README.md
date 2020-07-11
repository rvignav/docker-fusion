# docker-fusion

To test the image fusion algorithm, do the following:

    git clone https://github.com/rvignav/docker-fusion.git
    cd docker-fusion
    pip install opencv-python pydicom numpy argparse Pillow

Add your two desired DICOM input images to the `docker-fusion` folder.

    python3 fuse.py path/to/image1.dcm path/to/image2.dcm
