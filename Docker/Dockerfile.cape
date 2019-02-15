FROM onsoim/cuckoo

LABEL maintainer "https://github.com/onsoim"

RUN echo " ===> Install CAPE Dependencies..." && \
	apk add --no-cache freetype-dev \
	libvirt-dev \
	geoip-dev \
	lapack-dev \
	gfortran \
	g++ \
	libxslt-dev \
	libxml2-dev && \
	wget -P /usr/share/GeoIP/ https://github.com/maxmind/geoip-api-c/blob/master/data/GeoIP.dat && \
	echo " ===> Install pydeep Dependencies..." && \
	wget http://sourceforge.net/projects/ssdeep/files/ssdeep-2.13/ssdeep-2.13.tar.gz && \
	tar -xvf ssdeep-2.13.tar.gz && \
	cd ssdeep-2.13 && \
	./configure && \
	make && \
	make install && \
	cd ../ && \
	rm -rf ssdeep*

RUN echo " ===> Install CAPE..." && \
	apk add --no-cache git && \
	git clone https://github.com/ctxis/cape && \
	cd cape && \
	BUILD_LIB=1 pip install -r requirements.txt
