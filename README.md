# Xiami Router Patch

_Tested on:_

- [Xiaomi Mi Wi-Fi Router 3G (R3G)](https://openwrt.org/toh/xiaomi/mir3g)
- I'm sure this workaround can work on newer/others too

I screwed up. I bought too many Xiaomi Routers: nano, mini and some other monster I don't remember.
While all of them were a pleasure to setup with OpenWrt, Xiami decided to make it a hassle to do so
with their newer devices. And here is where my problems began: the bully Xiaomi Router 3 (R3G) was on
lock-down. You need to register this device on miwifi.com and override your router with a custom
`miwifi_ssh.bin` that only allows YOU with the listed password on miwifi's website to access ssh.
If that's not enough, everything is chinese.

Unlucky me the website wouldn't let me download this image because I had another device registered (Nano).
So game over I thought. And then I discovered CVE-2019-18370 and created this useful script to cirvumvent
the (paranoid) process and do it the friendly way so you guys can install your router os of choice (OpenWRT ftw).

## Prerequisite

- [x] Python / Python3
- [x] Pip with packages: requests, tarfile
- [x] Installed Xiaomi firmwares that have this vuln:
  - [Dev firmware 2.25.122](http://bigota.miwifi.com/xiaoqiang/rom/r3g/miwifi_r3g_firmware_c2175_2.25.122.bin)
  - [Dev firmware 2.25.124](http://bigota.miwifi.com/xiaoqiang/rom/r3g/miwifi_r3g_firmware_12f97_2.25.124.bin)
- [ ] (optional) `ssh-keygen` if you choose key-based auth

## Getting Started

By default SSH is deactivated and the root password unknown (or determined from miwifi.com, I don't know how).
BUT fear not! We're going to access the router through a known vulnerability (CVE-2019-18370) and change it
to `xiaomi4Life` as well as start/activate dropbear (SSH).

Make sure your router is running and connected via ethernet.

```sh
# Did you read the prerequisites? If not, uncomment the lines below 
# and make sure you have python v3 installed
# pip install requests
# pip install tarfile

# Make sure your router is connected (eth) & ready
# This will activate ssh and set the root password to 'xiaomi4Life'
python3 install.py
```

## Enabling SSH & Key-Based Authentication (optional)

In `bootstrap/setup.sh` you can uncomment the key-file setup and add a `id_rsa.pub` file into the `bootstrap/` folder.
And voila... the setup will work too and add your key to `authorized_keys` of dropbear.

## New firmware

Download the newest version from: https://openwrt.org/toh/xiaomi/mir3g
For me this is a `openwrt-*.kernel1.bin` and `openwrt-*.rootfs0.bin` (\* omitted for brevity). Or build your own version if you're brave.

```sh
# Copy both binaries to the tmp folder
scp openwrt*.bin root@192.168.31.1:/tmp

# Log into the router
ssh root@192.168.31.1

# Install images
cd /tmp
mtd write openwrt.kernel1.bin kernel1
mtd write openwrt.rootfs0.bin rootfs0
nvram set flag_try_sys1_failed=1
nvram commit
reboot

# And after some time your router is accessible with
# and the openwrt banner will greet you
ssh root@192.168.1.1
```
