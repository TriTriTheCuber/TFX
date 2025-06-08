# resetlauncher.py
import time
import subprocess
import sys
import os


time.sleep(1)  # let the original app close
if os.path.isfile("tritrisim_installer.py"):
    subprocess.Popen([sys.executable, "tritrisim_installer.py"])
else:
    subprocess.Popen([sys.executable, "TriTriSim Installer.exe"])
