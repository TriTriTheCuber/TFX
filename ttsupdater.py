import os
import sys
import requests
from pathlib import Path
import psutil

print(psutil.cpu_count())

global installertype
print(sys.argv)
if len(sys.argv) > 1:
    installertype = sys.argv[1]
    inpid = int(sys.argv[2])
else:
    installertype = None

def download(filename, base_url):
    url = f"{base_url}/{filename}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

print(installertype)
killproc = inpid
for p in psutil.process_iter():
    if p.pid == killproc:
        p.kill()  

if installertype == "exe":
    download("TriTriSim Installer.exe", "https://raw.githubusercontent.com/TriTriTheCuber/TFX/main")
else:
    download("tritrisim_installer.py", "https://raw.githubusercontent.com/TriTriTheCuber/TFX/main")