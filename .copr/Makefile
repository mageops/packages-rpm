BUILD_DEPS = \
	rpm \
	rpm-libs \
	rpm-python \
	rpm-build \
	rpmdevtools \
	git \
	m4 \
	autoconf \
	automake \
	elfutils-libelf \
	logrotate \
	curl

.PHONY: prepare srpm rpm

basicdeps:
	# Install basic build dependencies
	dnf -y install $(BUILD_DEPS)

hooks: basicdeps
	# Run any package-specific setup hooks
	find . -maxdepth 1 -type f -executable -name '*.copr-hook.*' -exec {} \;

builddep: basicdeps
	# Make sure builddep is available
	(which yum 2>&1 >/dev/null && yum -y install yum-utils) || (which dnf 2>&1 >/dev/null && dnf -y install dnf-plugins-core-builddep)

	# Install build deps
	dnf builddep $(spec) -y

download:  basicdeps
	# Download sources
	spectool -g -R $(spec) -C "$(CURDIR)" -define '_sourcedir $(CURDIR)' --define '_specdir $(CURDIR)' --define '_srcrpmdir $(outdir)'

verify: download
	# Import source maintainer keys
	find $(CURDIR) -type f -name '*.key' -exec gpg --verbose --import {} \;

	# Verify downloaded signatures against maintainer keys
	find $(CURDIR) -type f -name '*.asc' -exec gpg --verbose --verify {} \;

prepare: basicdeps hooks builddep download verify

srpm: prepare
	rpmbuild -bs --define '_sourcedir $(CURDIR)' --define '_specdir $(CURDIR)' --define '_srcrpmdir $(outdir)' $(spec) --target x86_64

rpm: prepare
	rpmbuild -bb --define '_sourcedir $(CURDIR)' --define '_specdir $(CURDIR)' --define '_srcrpmdir $(outdir)' $(spec) --target x86_64