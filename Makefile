RPM:=nginx-1.9.5-1.el7.ngx.src.rpm
FILES=logrotate nginx.init nginx.sysconf nginx.conf nginx.vh.default.conf nginx.suse.init nginx.service nginx.upgrade.sh nginx.suse.logrotate

sources: ngx_pagespeed-v1.9.32.6-beta.tar.gz psol-1.9.32.6.tar.gz ${FILES}

ngx_pagespeed-v1.9.32.6-beta.tar.gz:
	wget -O $@ https://github.com/pagespeed/ngx_pagespeed/archive/v1.9.32.6-beta.tar.gz

psol-1.9.32.6.tar.gz:
	wget -O $@ https://dl.google.com/dl/page-speed/psol/1.9.32.6.tar.gz

${RPM}:
	wget -O $@ http://nginx.org/packages/mainline/centos/7/SRPMS/$@

${FILES}: ${RPM}
	bash -c "rpm2cpio.pl $< | cpio -i -E <(echo $@)"

.PHONY: sources
