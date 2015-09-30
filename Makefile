all: ngx_pagespeed-v1.9.32.6-beta.tar.gz psol-1.9.32.6.tar.gz

ngx_pagespeed-v1.9.32.6-beta.tar.gz:
	wget -O $@ https://github.com/pagespeed/ngx_pagespeed/archive/v1.9.32.6-beta.tar.gz

psol-1.9.32.6.tar.gz:
	wget -O $@ https://dl.google.com/dl/page-speed/psol/1.9.32.6.tar.gz
