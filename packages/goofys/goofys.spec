Name:             goofys
Version:          0.23.1
Release:          1%{?dist}

Summary:          A high-performance, POSIX-ish Amazon S3 file system written in Go
License:          Apache

Vendor:           Ka-Hing Cheung (kahing)
Packager:         creativestyle GmbH <https://creativestyle.de>
URL:              https://github.com/kahing/goofys/

Source:           https://github.com/kahing/goofys/releases/download/v%{version}/goofys

Requires:         fuse

%description
Goofys allows you to mount an S3 bucket as a filey system.

It's a Filey System instead of a File System because goofys strives 
for performance first and POSIX second. Particularly things that are 
difficult to support on S3 or would translate into more than one 
round-trip would either fail (random writes) or faked (no per-file permission). 
Goofys does not have an on disk data cache (checkout catfs), and consistency 
model is close-to-open.

%prep
%setup -q -c -T

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}/goofys

%files
%defattr(-,root,root,-)
%{_bindir}/goofys

%changelog
* Mon Jan 13 2020 Filip Sobalski <filip.sobalski@creativestyle.pl> - 0.23.1-1
- Initial version
