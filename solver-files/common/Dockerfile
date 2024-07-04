################### Init
FROM satcomp-infrastructure:common
USER root
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y --no-install-recommends install \
    build-essential \
    libopenmpi-dev \
    python3.8

# ##//linxi-test
# RUN apt-get -y --no-install-recommends install \
#     vim

# # ----------------
# # AriParti Builder Image
# # ----------------
# # >> Includes build files and test instances

COPY resources/AriParti /AriParti
RUN mkdir /AriParti/binary-files
RUN chmod +x /AriParti/AriParti.py

COPY resources/partitioner-src /partitioner
WORKDIR /partitioner
RUN python3 scripts/mk_make.py
WORKDIR /partitioner/build
RUN make -j
RUN cp /partitioner/build/z3 /AriParti/binary-files/partitioner-bin

COPY resources/z3pp-src /z3pp
WORKDIR /z3pp
RUN python3 scripts/mk_make.py
WORKDIR /z3pp/build
RUN make -j
RUN cp /z3pp/build/z3 /AriParti/binary-files/z3pp-at-smt-comp-2023-bin
