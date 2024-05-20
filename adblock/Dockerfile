FROM mitmproxy/mitmproxy
RUN apt-get update && apt-get upgrade -y
RUN apt-get install wget git build-essential gcc ninja-build pybind11-dev libre2-dev cython3 cmake libpq-dev python3-dev python3-pip python3-wheel -y
RUN git clone https://github.com/epitron/mitm-adblock.git
WORKDIR /mitm-adblock
RUN pip install --upgrade pip
RUN pip install 'Cython>=0.29.19,<1.0'
WORKDIR /
RUN git clone https://github.com/andreasvc/pyre2.git
WORKDIR /pyre2
RUN make install
WORKDIR /mitm-adblock
RUN pip install --no-cache-dir mitmproxy adblockparser
RUN ./update-blocklists
EXPOSE 8118
CMD [ "./go" ] 
