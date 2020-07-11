# docker-fusion

To test the image fusion algorithm, run the following commands:

    git clone https://github.com/rvignav/docker-fusion.git
    cd docker-fusion

Add your two desired DICOM input images to the `docker-fusion` folder, then run:

    docker build -t fuse --build-arg i1=/path/to/image1.dcm --build-arg i2=/path/to/image2.dcm .
    docker run fuse /path/to/image1.dcm /path/to/image2.dcm

If you see `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`, run:
Windows:

    systemctl start docker

MacOS:

    brew cask install docker virtualbox
    brew install docker-machine
    docker-machine create --driver virtualbox default
    docker-machine restart
    eval "$(docker-machine env default)"
