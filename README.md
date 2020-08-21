# docker-fusion

Image fusion algorithm integrated into Stanford University's [ePAD Imaging Platform](https://epad.stanford.edu/). To test the image fusion algorithm, run the following commands:

    git clone https://github.com/rvignav/docker-fusion.git
    cd docker-fusion
    docker build -t fuse .
    docker run -v "local/files:/home/series/files" -v "local/patient/series:/home/series/PatientSeries" fuse "filename of series 1" "filename of series 2"

A possible command satisfying the bind and argument requirements is:

    docker run -v "$(pwd)/files:/home/series/files" -v "$(pwd)/SamplePatient:/home/series/PatientSeries" fuse "Series1" "Series2"

The fused series is now stored in the `output` folder of the Docker container and can be accessed by ePAD.

If you see `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`, run:

Windows:

    systemctl start docker

MacOS:

    brew cask install docker virtualbox
    brew install docker-machine
    docker-machine create --driver virtualbox default
    docker-machine restart
    eval "$(docker-machine env default)"

If you receive the error `docker: Error response from daemon: Conflict. The container name "/FUSE" is already in use`, run:

    docker ps -q -a | xargs docker rm
