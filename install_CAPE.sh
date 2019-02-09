sudo apt-get install -y python-pip python3-pip libgeoip-dev libvirt-dev libfuzzy-dev

# python2: pefile2, geoip
# python3: else
pip install -r requirements-2.txt
pip3 install -r requirements-3.txt

python3 CAPE/cuckoo.py