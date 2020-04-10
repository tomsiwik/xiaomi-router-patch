#!/bin/sh
set -e

printf "Enabling NVRAM ssh\n"
nvram set ssh_en=1
nvram commit
printf "--> Success\n\n"

# Want it secure? Go key-based and uncomment the lines below
# printf "Adding SSH pubkey\n"
# cp /tmp/id_rsa.pub /etc/dropbear/authorized_keys
# chmod 600 /etc/dropbear/authorized_keys
# printf "--> Success\n\n"

# Insecure method. Comment out if you choose the way above
# Meh.. this works fine too if you're changing the OS
echo -e "xiaomi4Life\nxiaomi4Life" | passwd
printf "Login password: xiaomi4Life\n"
printf "--> Success\n\n"

printf "Restarting dropbear\n"
/etc/init.d/dropbear stop
/etc/init.d/dropbear start
printf "--> Success"