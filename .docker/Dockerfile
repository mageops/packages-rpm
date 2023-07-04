FROM fedora:36
# IMPORTANT!
# qemu-user-static MUST be also installed on host system outside docker!
RUN dnf install -y mock rpmdevtools rpm-sign nosync.i686 nosync.x86_64 qemu-user-static
RUN useradd -m builder && gpasswd -a builder mock
ADD mageops_common.tpl /etc/mock/templates/mageops_common.tpl
ADD epel-7-x86_64.cfg /etc/mock/epel-7-x86_64.cfg
ADD epel-7-aarch64.cfg /etc/mock/epel-7-aarch64.cfg
ADD ./build.sh /usr/local/bin/build-rpm
WORKDIR /home/builder
