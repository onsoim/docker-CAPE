# docker build -t onsoim/python2 .
docker build -t onsoim/cuckoo .

echo "===== run docker test ====="

docker rmi -f $(docker images -f "dangling=true" -q)
docker run --rm onsoim/cuckoo cuckoo
