FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt install -y --no-install-recommends \
        bash bash-completion coreutils firefox-geckodriver git pkg-config python3 python3-pip \
        software-properties-common ssh sudo tzdata vim wget && \
    pip3 install --upgrade selenium selenium-wire pip && \
    sudo apt autoremove -y python3-pip && \
    ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime && \
    echo America/Los_Angeles > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

ARG NAME
ARG UID
ARG GID
RUN groupadd -g $GID $NAME && \
    useradd -u $UID -g $NAME --groups sudo --shell /bin/bash $NAME && \
    echo "$NAME ALL = NOPASSWD: ALL" > /etc/sudoers.d/$NAME && \
    mkdir /home/$NAME && chown -R $NAME:$NAME /home/$NAME

USER $NAME
WORKDIR /home/$NAME
