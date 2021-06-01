FROM fedora:31

RUN dnf -y install \
        ocaml \
        which \
        curl \
        git \
        make \
        redhat-rpm-config \
        glibc-static

RUN mkdir -p /build/source \
    && git clone https://github.com/bcpierce00/unison.git /build/source

RUN mkdir -p /build/output \
    && cd /build/source \
    && make UISTYLE=text NATIVE=true STATIC=true DEBUGGING=false \
    && ls -alsh src/unison src/unison-fsmonitor \
    && ldd -v src/unison || true \
    && ldd -v src/unison-fsmonitor || true \
    && cp -vf \
        src/unison \
        src/unison-fsmonitor \
            /build/output/
