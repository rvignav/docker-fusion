# docker-fusion

To test the image fusion algorithm, run the following commands:

    git clone https://github.com/rvignav/docker-fusion.git
    cd docker-fusion
    docker build -t fuse --build-arg i1=Series1 --build-arg i2=Series2 .
    docker run --name FUSE fuse Series1 Series2
    docker cp FUSE:/series ./series

The fused series is now stored in `docker-fusion/series` and can be opened and viewed.

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
