#!/bin/bash
set -e -x
# docker build . --tag magesuite/build-rpm:centos-7 --target=centos-7 --cache-from magesuite/build-rpm:centos-7
# docker push magesuite/build-rpm:centos-7
# docker run -it --entrypoint /bin/bash -v $(pwd):/root/rpmbuild magesuite/build-rpm:centos-7
#docker run -it -v $(pwd):/root/rpmbuild magesuite/build-rpm:centos-7


docker build . --tag magesuite/build-rpm:amazonlinux-1 --target=amazonlinux-1 --cache-from magesuite/build-rpm:amazonlinux-1
docker push magesuite/build-rpm:amazonlinux-1
#docker run -it --entrypoint /bin/bash -v $(pwd):/root/rpmbuild magesuite/build-rpm:amazonlinux-1
docker run -it -v $(pwd):/root/rpmbuild magesuite/build-rpm:amazonlinux-1