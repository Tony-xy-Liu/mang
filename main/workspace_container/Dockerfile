ARG CONDA_ENV=for_container

FROM condaforge/miniforge3
ENV DEBIAN_FRONTEND=noninteractive
# scope var from global
ARG CONDA_ENV

# I believe this is to avoid permission issues with 
# manipulating added files to places like /opt
RUN old_umask=`umask` \
    && umask 0000 \
    && umask $old_umask

# Singularity uses tini, but raises warnings
# we set it up here correctly for singularity
ADD ./lib/tini /tini
    
# singularity doesn't use the -s flag, and that causes warnings.
# -g kills process group on ctrl+C
ENTRYPOINT ["/tini", "-s", "-g", "--"]

# Avahi for named endpoint via multicast DNS
RUN apt-get update && apt-get install -y --no-install-recommends \
    avahi-daemon \
    libavahi-core7 \
    libnss-mdns \
    && rm -rf /var/lib/apt/lists/*

# https://mamba.readthedocs.io/en/latest/user_guide/mamba.html
# create conda env from yaml config
COPY ./lib/env.yml /opt/env.yml
# use an external cache for solved environments and install packages
RUN --mount=type=cache,target=/opt/conda/pkgs \
    mamba env create -n ${CONDA_ENV} -f /opt/env.yml
# alias p -> python
RUN echo "#!/bin/bash\npython \$@" >/bin/p && chmod +x /bin/p
# add bins to PATH so that the env appears "active"
ENV PATH /opt/conda/envs/${CONDA_ENV}/bin:/app:$PATH

COPY ./src /app
COPY ./src/avahi/avahi-daemon.conf /etc/avahi/avahi-daemon.conf
COPY ./src/avahi/nsswitch.conf /etc/nsswitch.conf


RUN mkdir -p /var/run/dbus


