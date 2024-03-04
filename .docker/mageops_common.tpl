config_opts['plugin_conf']['tmpfs_enable'] = True
config_opts['plugin_conf']['tmpfs_opts'] = {}
config_opts['plugin_conf']['tmpfs_opts']['required_ram_mb'] = 16384
config_opts['plugin_conf']['tmpfs_opts']['max_fs_size'] = '15872m'
config_opts['plugin_conf']['tmpfs_opts']['mode'] = '0755'
config_opts['plugin_conf']['tmpfs_opts']['keep_mounted'] = False

config_opts['plugin_conf']['sign_enable'] = True
config_opts['plugin_conf']['sign_opts'] = {}
config_opts['plugin_conf']['sign_opts']['cmd'] = 'rpmsign'
config_opts['plugin_conf']['sign_opts']['opts'] = '--addsign %(rpms)s'

config_opts['rpmbuild_networking'] = True
config_opts['use_host_resolv'] = True

config_opts['nosync'] = True

# Do not generate repo, we do this afterwards
config_opts['createrepo_on_rpms'] = False

config_opts['yum.conf'] += """
[self]
name=self
baseurl=file:///home/builder/repo
repo_gpgcheck=0
gpgcheck=0
enabled=1
# needed for mock bootstrap, because bind isn't done there
skip_if_unavailable=1

[varnish60lts]
name=varnish60lts
baseurl=https://packagecloud.io/varnishcache/varnish60lts/el/$releasever/$basearch
repo_gpgcheck=0
gpgcheck=0
enabled=1
gpgkey=https://packagecloud.io/varnishcache/varnish60lts/gpgkey
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
"""


config_opts['macros']['%packager'] = 'creativestyle GmbH <https://creativestyle.de>'
config_opts['macros']['%_debugsource_packages'] = '1'
config_opts['macros']['%_debuginfo_subpackages'] = '1'

config_opts['plugin_conf']['bind_mount_enable'] = True
config_opts['plugin_conf']['bind_mount_opts']['dirs'].append(('/home/builder/repo', '/home/builder/repo' ))
