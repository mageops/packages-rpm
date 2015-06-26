all: ngx_pagespeed-1.9.32.4.tar.gz psol-1.9.32.4.tar.gz

ngx_pagespeed-1.9.32.4.tar.gz:
	wget -O ngx_pagespeed-1.9.32.4.tar.gz https://github.com/pagespeed/ngx_pagespeed/archive/v1.9.32.4-beta.tar.gz

psol-1.9.32.4.tar.gz:
	wget -O psol-1.9.32.4.tar.gz https://dl.google.com/dl/page-speed/psol/1.9.32.4.tar.gz
