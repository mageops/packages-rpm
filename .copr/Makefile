#rpmbuild_src = $(shell rpmbuild --eval '%{_sourcedir}')

BUILD_DEPS = \
	rpm \
	rpm-libs \
	rpm-python \
	rpm-build \
	yum-utils \
	rpmdevtools \
	git \
	m4 \
	autoconf \
	automake \
	elfutils-libelf \
	logrotate

.PHONY: prepare srpm rpm

prepare:
	# Install build dependencies
	dnf -y install $(BUILD_DEPS)
	
	# Download sources
	spectool -g -R $(spec) -C "$(CURDIR)" -define '_sourcedir $(CURDIR)' --define '_specdir $(CURDIR)' --define '_srcrpmdir $(outdir)'

	# Install build deps
	yum-builddep $(spec) -y

	# Import source maintainer keys
	find $(CURDIR) -type f -name '*.key' -exec gpg --verbose --import {} \;

	# Verify downloaded signatures against maintainer keys
	find $(CURDIR) -type f -name '*.asc' -exec gpg --verbose --verify {} \;

srpm: prepare
	rpmbuild -bs --define '_sourcedir $(CURDIR)' --define '_specdir $(CURDIR)' --define '_srcrpmdir $(outdir)' $(spec) --target x86_64

rpm: prepare
	rpmbuild -bb --define '_sourcedir $(CURDIR)' --define '_specdir $(CURDIR)' --define '_srcrpmdir $(outdir)' $(spec) --target x86_64