FROM python:3.6.1

ENV LD_LIBRARY_PATH /usr/local/lib:${LD_LIBRARY_PATH}
WORKDIR /app
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  git \
  sudo \
  unzip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && adduser --disabled-password --gecos '' docker \
  && adduser docker sudo \
  && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
  && echo 'Start Installing Mecab ......' \
  && git clone https://github.com/taku910/mecab.git \
  && cd mecab/mecab \
  && ./configure --with-charset=utf8 --enable-utf8-only \
  && make && make check \
  && make install \
  && echo 'Start Installing Neologd ......' \
  && cd /opt \
  && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
  && cd /opt/mecab-ipadic-neologd \
  && ./bin/install-mecab-ipadic-neologd -n -y \
  && pip install --upgrade pip
