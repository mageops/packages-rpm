yum -y install gnupg
gpg --import --dry-run --with-colons /root/rpm-gpg-key.pub.asc 
gpg --import --dry-run --with-colons /root/rpm-gpg-key.pub.asc 
gpg --init
gpg -help
mkdir -p /root/.gnupg
gpg --import --dry-run --with-colons /root/rpm-gpg-key.pub.asc 
gpg --import --dry-run --with-colons /root/rpm-gpg-key.sec.asc
gpg --with-fingerprint /root/rpm-gpg-key.sec.asc
gpg --with-colons --with-fingerprint /root/rpm-gpg-key.sec.asc
gpg --with-colons /root/rpm-gpg-key.sec.asc
gpg --help
gpg --with-colons --with-key-data /root/rpm-gpg-key.sec.asc
gpg --with-colons --with-key-data --with-fingerprint /root/rpm-gpg-key.sec.asc
gpg --list-keys
gpg --import *.asc
gpg --import /root/*.asc
gpg --list-keys
gpg --list-secret-keys
gpg --with-key-data --with-fingerprint /root/rpm-gpg-key.sec.asc
gpg --with-key-data --with-fingerprint /root/rpm-gpg-key.sec.asc | grep 2AA
gpg --with-key-data --with-fingerprint /root/rpm-gpg-key.sec.asc | grep --color 2AA
gpg --with-colons /root/rpm-gpg-key.sec.asc 
function gpg_key_show()     {       gpg --with-colons "$1" 2>&1;                                                }
function gpg_key_user()     {       gpg_key_show "$1" | awk -F: '/^(sec|pub):/{ print $10 }';                                                                        }
function gpg_key_id()       {       gpg_key_show "$1" | awk -F: '/^(sec|pub):/ { print $5 }';                                                                   }
gpg_key_user /root/rpm-gpg-key.pub.asc 
gpg_key_id /root/rpm-gpg-key.pub.asc 
