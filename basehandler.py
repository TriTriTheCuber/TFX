#basehandler.py
import os
import sys
import requests
from pathlib import Path
import shutil
import zipfile
import tempfile

global community_2020
global community_2024






def handlepackages(simversion, action):
    global community_2020
    global community_2024
    if simversion == "2020":
        if action == "--downloadbase":
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2020.zip", community_path=community_2020)
        if action == "--removebase":
            remove_folder_from_community(folder_name="TFX-fxlib", community_path=community_2020)
        if action == "--updatebase":
            remove_folder_from_community(folder_name="TFX-fxlib", community_path=community_2020)
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2020.zip",community_path=community_2020)
        if action == "-materials":
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/materiallibs.zip",community_path=community_2020)
    else:
        if action == "--downloadbase":
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2024.zip",community_path=community_2024)
        if action == "--removebase":
            remove_folder_from_community(folder_name="TFX-fxlib", community_path=community_2024)
        if action == "--updatebase":
            remove_folder_from_community(folder_name="TFX-fxlib", community_path=community_2024)
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2024.zip",community_path=community_2024)
        if action == "--materials":
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/materiallibs.zip",community_path=community_2024)





def checkfiledifferences(remotelines, locallines, simver="2020"):
    if simver == "2020":
        if locallines[0] == None:
            return "Not installed"
        elif remotelines[1] == locallines[0]:
            return "Installed"
        else:
            return "Update"
    else:
        if locallines[0] == None:
            return "Not installed"
        elif remotelines[3] == locallines[0]:
            return "Installed"
        else:
            return "Update"


def fetch_remote_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip().splitlines()
    except Exception as e:
        print(f"Failed to fetch remote file: {e}")
        return None

def read_local_file(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip().splitlines()


def remove_folder_from_community(folder_name, community_path):
    target_path = os.path.join(community_path, folder_name)
    if os.path.isdir(target_path):
        shutil.rmtree(target_path)
        print(f"Removed folder: {target_path}")
        return True
    else:
        print(f"Folder not found: {target_path}")
        return False


def fetch_zip(zip_url, community_path):
    zip_temp = os.path.join(tempfile.gettempdir(), "_tfx_dl.zip")
    temp_unzip = os.path.join(tempfile.gettempdir(), "tfx_unzip")

    # Clean temp unzip folder if exists
    if os.path.exists(temp_unzip):
        shutil.rmtree(temp_unzip)
    os.makedirs(temp_unzip, exist_ok=True)

    print("\nDownloading zip...")
    try:
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()
        with open(zip_temp, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"Download failed: {e}")
        return False

    if not os.path.exists(zip_temp):
        print("Download failed.")
        return False

    print("Extracting zip...")
    try:
        with zipfile.ZipFile(zip_temp, 'r') as zip_ref:
            zip_ref.extractall(temp_unzip)
    except zipfile.BadZipFile:
        print("Extraction failed: Bad ZIP file.")
        return False

    # Find the first folder inside the zip
    zip_root = None
    for item in os.listdir(temp_unzip):
        item_path = os.path.join(temp_unzip, item)
        if os.path.isdir(item_path):
            zip_root = item_path
            break

    if not zip_root:
        print("No root folder found in zip.")
        return False

    print(f"Merging contents from {zip_root} to {community_path}")
    try:
        for root, dirs, files in os.walk(zip_root):
            rel_path = os.path.relpath(root, zip_root)
            target_dir = os.path.join(community_path, rel_path)
            os.makedirs(target_dir, exist_ok=True)

            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)
    except Exception as e:
        print(f"Error copying files: {e}")
        return False

    print("Cleaning up...")
    try:
        os.remove(zip_temp)
        shutil.rmtree(temp_unzip)
    except Exception as e:
        print(f"Cleanup failed: {e}")

    print("Download and extraction successful.")
    return True


def get_base_data(communityfolder):
    if os.path.exists(os.path.join(communityfolder, "TFX-fxlib")):
        baseinstalled = 1
        localversion = read_local_file(os.path.join(communityfolder, r"TFX-fxlib\tfx-base-version.txt"))
    else:
        baseinstalled = 0
        localversion = 0
    if os.path.exists(os.path.join(communityfolder, "gf-material-lib")):
        materialsinstalled = 1
    else:
        materialsinstalled = 0
    remoteversion = fetch_remote_file(r"https://raw.githubusercontent.com/TriTriTheCuber/tfx/main/versions.txt")
    remoteversion = remoteversion[3]
    return baseinstalled,localversion,remoteversion,materialsinstalled



base_url = "https://raw.githubusercontent.com/TriTriTheCuber/TFX/main"

community_2020 = Path(sys.argv[1])
community_2024 = Path(sys.argv[1])
action = sys.argv[2]
simversion = sys.argv[3]

handlepackages(simversion=simversion, action=action)
