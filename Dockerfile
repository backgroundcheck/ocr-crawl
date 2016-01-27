FROM python:2.7.10
MAINTAINER Friedrich Lindenberg <friedrich@pudo.org>
ENV DEBIAN_FRONTEND noninteractive
ENV TESSDATA_PREFIX /usr/share/tesseract-ocr

RUN apt-get update -qq && apt-get install -y -q --no-install-recommends \
        curl git python-pip python-virtualenv build-essential python-dev \
        libxml2-dev libxslt1-dev libpq-dev apt-utils ca-certificates less \
        unrar-free unzip locales tesseract-ocr tesseract-ocr-bel \
        tesseract-ocr-aze tesseract-ocr-osd imagemagick-common imagemagick \
        libtesseract-dev tesseract-ocr-eng tesseract-ocr-rus \
        tesseract-ocr-ukr unrtf pstotext zlib1g-dev python-numpy \
  && apt-get clean

RUN pip install psycopg2 lxml numpy tesserwrap pdfminer==20140328 \
        chardet>=2.3.0 Pillow six thready
COPY . /crawl
WORKDIR /crawl
RUN pip install https://github.com/pudo/extractors/tarball/master
