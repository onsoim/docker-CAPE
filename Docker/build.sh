# docker build -t onsoim/python2 .
docker build -t onsoim/cape .

echo "===== run docker test ====="

docker rmi -f $(docker images -f "dangling=true" -q)

# docker run --rm onsoim/python2 python --version
# docker run --rm -it onsoim/cuckoo /bin/bash

docker system df
docker volume ls
