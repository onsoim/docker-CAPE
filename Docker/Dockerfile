FROM onsoim/python2

LABEL maintainer "https://github.com/onsoim"

ENV CUCKOO_VERSION 2.0.6

# Install Cuckoo Dependencies
RUN apk add --no-cache gcc \
	python-dev \
	musl-dev \
	libffi-dev \
	openssl-dev \
	bash \
	make \
	jpeg-dev \
	zlib-dev \
	py-pillow

# install cuckoo
RUN export PIP_NO_CACHE_DIR=off && \
	export PIP_DISABLE_PIP_VERSION_CHECK=on && \
	pip install cuckoo==$CUCKOO_VERSION && \
	cuckoo \
	cuckoo community