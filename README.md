# docker-fusion

To test the image fusion algorithm, run the following commands:

    git clone https://github.com/rvignav/docker-fusion.git
    cd docker-fusion

Add your two desired DICOM input images to the `docker-fusion` folder, then run:

    docker build -t fuse --build-arg i1=/path/to/image1.dcm --build-arg i2=/path/to/image2.dcm .
    docker run fuse /path/to/image1.dcm /path/to/image2.dcm
