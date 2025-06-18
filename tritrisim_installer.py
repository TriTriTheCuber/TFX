#tritrisim_installer.py
import dearpygui.dearpygui as dpg
import time as Time
import os
import sys
import requests
import subprocess
from pathlib import Path
import ctypes
import ctypes.wintypes
import re
import shutil
import zipfile
import tempfile
import threading
import base64
import math
clear = lambda: os.system('cls')
global goodlogin
goodlogin = 0
# Validation

keyform = [5,5,5]
choices = ["1","2","3","4","5","6","7","8","9","0","A","B","C","D","E","F"]
worth = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

def calculateworth(code):
    worthout = 0
    a = list(code)
    for b in a:
        if not b == "-":
            worthout = worthout + worth[choices.index(b)]
    return worthout

def calculatepin(worth, size = 100000):
    pinout = worth
    for f in range(pinout):
        pinout = pinout + worth * pinout/(15*(f+1))
    pinout = pinout / worth
    pinout = math.cos(pinout) + 1
    pinout = (pinout * size * 0.4) + size * 0.1
    pinout = round(pinout)
    return pinout
        
def getformat(key):
    kel = list(key)
    form = []
    formcount = 0
    for a in kel:
        if a == "-":
            form.append(formcount)
            formcount = 0
            continue
        formcount = formcount + 1
    form.append(formcount)
    return form

def showformat(form):
    outt = []
    for a in form:
        for b in range(a):
            outt.append("x")
        outt.append("-")
    outt.reverse()
    outt.remove("-")
    outt.reverse()
    out = "".join(outt)
    return out



# Important stuff



def resetapplication():
    pass
#    removepath("InstallerInserts")
#    removepath("InstallerInserts2024")
#    removefile("MSFSLayoutGenerator.exe")
#    removefile("state.txt")
#    sys.exit(0)
#Not reliable


def restart_app():
    dpg.delete_item("main_panel")
    mainwindow()


def specialbuttoncallback(sender, appdata, user_data):
    simversion = user_data[0]
    action = user_data[1]
    print (user_data)
    print (simversion)
    print (action)
    pass
    if simversion == "2020":
        if action == "bdown":
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2020.zip", community_path=community_2020)
        if action == "br":
            remove_folder_from_community(folder_name="TFX-fxlib", community_path=community_2020)
        if action == "u":
            remove_folder_from_community(folder_name="TFX-fxlib", community_path=community_2020)
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2020.zip",community_path=community_2020)
        if action == "mat":
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/materiallibs.zip",community_path=community_2020)
    else:
        if action == "bdown":
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2024.zip",community_path=community_2024)
        if action == "br":
            remove_folder_from_community(folder_name="TFX-fxlib", community_path=community_2024)
        if action == "u":
            remove_folder_from_community(folder_name="TFX-fxlib", community_path=community_2024)
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/TFX.2024.zip",community_path=community_2024)
        if action == "mat":
            fetch_zip(zip_url=r"https://github.com/TriTriTheCuber/TFX/releases/download/openbeta/materiallibs.zip",community_path=community_2024)
    restart_app()


def createspecialbuttons(buttontag="2020tab", simversion="2020"):
    user_data = []
    if simversion == "2020":
        remotelines = fetch_remote_file(r"https://raw.githubusercontent.com/TriTriTheCuber/tfx/main/tfxbaseversions.txt")
        locallines = read_local_file(os.path.join(community_2020, r"TFX-fxlib\tfx-base-version.txt"))
        if locallines == None:
            if os.path.exists(os.path.join(community_2020, r"TFX-fxlib")):
                locallines = [1,1,1,1]
            else:
                locallines = [None]
        status = checkfiledifferences(remotelines, locallines, "2020")
        if status == "Not installed":
            buttonlabel1 = "Install Base Package"
            action1 = "bdown"
        if status == "Installed":
            buttonlabel1 = "Uninstall Base Package"
            action1 = "br"
        if status == "Update":
            buttonlabel1 = rf"Update Base Package (v{locallines[0]} -> v{remotelines[1]})"
            action1 = "u"
        enabled2 = True
        if os.path.exists(os.path.join(community_2020, "gf-material-lib")):
            buttonlabel2 = "Materiallibs already installed"
            action2 = None
            enabled2 = False
        else:
            buttonlabel2 = "Install Materiallibs"
            action2 = "mat"
        dpg.add_button(label=buttonlabel1, tag="2020basebutton", user_data=[simversion, action1], callback=specialbuttoncallback, parent=buttontag)
        dpg.add_button(label=buttonlabel2, tag="2020matbutton", user_data=[simversion, action2], callback=specialbuttoncallback, parent=buttontag, enabled=enabled2)
    else:
        remotelines = fetch_remote_file(r"https://raw.githubusercontent.com/TriTriTheCuber/tfx/main/tfxbaseversions.txt")
        locallines = read_local_file(os.path.join(community_2024, r"TFX-fxlib\tfx-base-version.txt"))
        if locallines == None:
            if os.path.exists(os.path.join(community_2024, r"TFX-fxlib")):
                locallines = [1,1,1,1]
            else:
                locallines = [None]
        status = checkfiledifferences(remotelines, locallines, "2024")
        if status == "Not installed":
            buttonlabel1 = "Install Base Package"
            action1 = "bdown"
        if status == "Installed":
            buttonlabel1 = "Uninstall Base Package"
            action1 = "br"
        if status == "Update":
            buttonlabel1 = rf"Update Base Package (v{locallines[0]} -> v{remotelines[1]})"
            action1 = "u"
        enabled2 = True
        if os.path.exists(os.path.join(community_2024, "gf-material-lib")):
            buttonlabel2 = "Materiallibs already installed"
            action2 = None
            enabled2 = False
        else:
            buttonlabel2 = "Install Materiallibs"
            action2 = "mat"
        dpg.add_button(label=buttonlabel1, tag="2024basebutton", callback=specialbuttoncallback, user_data = [simversion, action1], parent=buttontag)
        dpg.add_button(label=buttonlabel2, tag="2024matbutton", callback=specialbuttoncallback, user_data = [simversion, action2], parent=buttontag, enabled=enabled2)


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
        print("Local file does not exist.")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read().strip().splitlines()


def get_top_level_folder(path):
    normalized_path = os.path.normpath(path)  # Normalizes slashes
    parts = normalized_path.split(os.sep)     # Splits by platform-specific separator
    return parts[0] if parts else None


def removepath(folder_name):
    target_path = Path(folder_name)
    if os.path.isdir(target_path):
        shutil.rmtree(target_path)
        print(f"Removed folder: {target_path}")
        return True
    else:
        print(f"Folder not found: {target_path}")
        return False

def removefile(file_name):
    target_path = Path(file_name)
    if os.path.isfile(target_path):
        os.remove(target_path)
        print(f"Removed file: {target_path}")
        return True
    else:
        print(f"File not found: {target_path}")
        return False

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


def line_exists_flexible(filepath, target_line):
    target_line = target_line.strip().lower()
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            if target_line in line.strip().lower():
                return True
    return False


def fetch_and_download_files(owner, repo, folder_path, destination, branch="main"):
    # GitHub API URL to list folder contents
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder_path}?ref={branch}"
    
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch folder contents: {response.status_code} - {response.text}")
        return

    os.makedirs(destination, exist_ok=True)  # make destination if missing

    for item in response.json():
        if item['type'] == 'file':
            file_name = item['name']
            download_url = item['download_url']
            local_path = os.path.join(destination, file_name)

            try:
                print(f"⬇️ Downloading {file_name}...")
                file_data = requests.get(download_url)
                file_data.raise_for_status()

                with open(local_path, 'wb') as f:
                    f.write(file_data.content)

                print(f"✅ Saved to {local_path}")
            except Exception as e:
                print(f"❌ Error downloading {file_name}: {e}")


def get_usercfg_paths():
    appdata = os.getenv("APPDATA")
    if not appdata:
        print("❌ APPDATA environment variable not found.")
        return []
    return [
        os.path.join(appdata, "Microsoft Flight Simulator", "UserCfg.opt"),
        os.path.join(appdata, "Microsoft Flight Simulator 2024", "UserCfg.opt")
    ]

def get_community_folder_from_usercfg(cfg_path):
    if not os.path.isfile(cfg_path):
        return None

    with open(cfg_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip().startswith("InstalledPackagesPath"):
            # Extract path inside quotes
            parts = line.split('"')
            if len(parts) >= 2:
                base_path = parts[1]
                community_path = os.path.join(base_path, "Community")
                if os.path.isdir(community_path):
                    return community_path
    return None


def find_msfs_community_folders():
    community_folders = []
    cfg_paths = get_usercfg_paths()

    for cfg_path in cfg_paths:
        community = get_community_folder_from_usercfg(cfg_path)
        if community:
            community_folders.append((cfg_path, community))

    return community_folders


def check_plane(filepath, simversion="2020"):
    if simversion == "2020":
        selpath = os.path.join(community_2020, filepath)
    else:
        selpath = os.path.join(community_2024, filepath)
    with open(selpath, "r") as file:
        lines=file.readlines()
    return (parse_tfx_metadata(file_path=selpath))


def check_plane_from_file(file, simv="2020"):
    pathv, namev, versionv, tagv, inv = parse_tfx_metadata(file_path=file)
    return (check_plane(filepath=pathv, simversion=simv))

def planebutton(sender, app_data, user_data):
    print(f"Clicked: {user_data[0]}")
    print(f"Sim version: {user_data[1]}")
    print(f"Action: '{user_data[2]}")
    action = user_data[2]
    if action == "Install":
        install_from_module(modulepath=user_data[0], simversion=user_data[1])
    if action == "Uninstall":
        uninstall_from_module(modulepath=user_data[0], simversion=user_data[1])
    if action == "Update":
        install_from_module(modulepath=user_data[0], simversion=user_data[1])
    restart_app()


def generate_file_buttons(folder_path, buttontag=None, simversion="2020", extraprefix=None):

    if not os.path.exists(folder_path):
        print(f"[!] Folder '{folder_path}' not found!")
        return

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        # Only include files (optional: filter types here)
        if os.path.isfile(full_path):
            # Create a unique name for each button
            pathv, namev, versionv, tagv, inv = parse_tfx_metadata(file_path=full_path)
            pathnv = []
            for index in range(len(pathv)):
                if simversion=="2020":
                    pathnv.append(os.path.join(community_2020, pathv[index]))
                else:
                    pathnv.append(os.path.join(community_2024, pathv[index]))
            opathnv = pathnv[0]
            opathv = pathv[0]
            try:
                install = check_plane(pathv[0], simversion)[4]
            except:
                install = False
            planeinstalled = os.path.isfile(pathnv[0])
            action = None
            if planeinstalled:
                if not install:
                    button_label = rf"Install {namev}"
                    action = "Install"
                else:
                    inver = check_plane(pathv[0], simversion)[2]
                    if inver == versionv:
                        button_label = rf"Uninstall {namev}"
                        action = "Uninstall"
                    else:
                        button_label = rf"Update {namev}"
                        action = "Update"
            else:
                button_label = rf"{namev}... aircraft not installed"

            if not buttontag: buttontag = "</Behaviors>"
            if extraprefix:
                button_label = extraprefix + button_label
            dpg.add_button(label=button_label, callback=planebutton, user_data = [full_path, simversion, action], parent=buttontag, enabled=planeinstalled, tag=f"button.{full_path}.{simversion}")



def get_last_index_containing(lines, substring):
    for i in reversed(range(len(lines))):
        if substring in lines[i]:
            return i
    return -1  # Not found


def quiet_uninstall(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    try:
        start = lines.index('<!-- TFX INSTALLED -->\n')
        end = get_last_index_containing(lines, "TFX END")
        del lines[start:end + 1]
        print(f"TFX update/reinstall completed successfully.")
    except ValueError:
        print(f"TFX installation completed successfully (no previous entry found).")

    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def uninstall_tfx(target_file):
    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    try:
        start = lines.index('<!-- TFX INSTALLED -->\n')
        end = lines.index('<!-- TFX END -->\n')
        del lines[start:end + 1]
        print(r"TFX Uninstalled sucessfully.")
    except ValueError:
        print(r"TFX is not installed, uninstall skipped")

    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)



def loopinstall_tfx(filenames, insert_path, module_name, custom_tag):
    for fn in filenames:
        install_tfx(fn, insert_path, module_name, custom_tag)

def loopuninstall_tfx(target_files):
    for tf in target_files:
        uninstall_tfx(tf)


def install_tfx(filename, insert_path, module_name, custom_tag="</Behaviors>"):
    target_file = Path(filename)
    insert_content = Path(insert_path).read_text(encoding='utf-8').splitlines(keepends=True)

    quiet_uninstall(target_file)

    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if custom_tag is not None:
        print(f"Using tag {custom_tag}")
        index = next((i for i, line in enumerate(lines) if f'{custom_tag}' in line), -1)
        if index == -1:
            print(f"Critical error: '{custom_tag}' tag not found!")
            return
        new_lines = lines[:index] + insert_content + lines[index:]
    else:
        index = next((i for i, line in enumerate(lines) if '</Behaviors>' in line), -1)
        if index == -1:
            print("Critical error: '</Behaviors>' tag not found!")
            return
        new_lines = lines[:index] + insert_content + lines[index:]

    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"TFX installed successfully into {module_name}.")

def deleteitem(sender):
    dpg.delete_item(sender)
    global goodlogin


def createloginfile(key,pin):
    with open("alphakey.txt", "x") as l:
        pile = f"{key}{pin}"
        encoded=base64.b64encode(pile.encode('utf-8'))
        l.write(encoded.decode())


def svalidatedetails(pekey, pepin):
    global goodlogin
    reqpin = calculatepin(calculateworth(pekey), 10000000000)
    format = showformat(getformat(pekey))
    if format == "xxxxx-xxxxx-xxxxx":
        reqpin = f"{reqpin}"
        if pepin == reqpin:
            goodlogin = 1
        else:
            goodlogin = 0
    else:
        goodlogin = 0



def validatedetails(pekey, pepin):
    global goodlogin
    reqpin = calculatepin(calculateworth(pekey), 10000000000)
    format = showformat(getformat(pekey))
    if format == "xxxxx-xxxxx-xxxxx":
        reqpin = f"{reqpin}"
        if pepin == reqpin:
            goodlogin = 1
            createloginfile(pekey, pepin)
        else:
            print ("Sorry, nope.")
            goodlogin = 0
    else:
        goodlogin = 0
    deleteitem("alwin")
    restart_app()



def alphalogin():
    with dpg.window(modal=True, label="Alpha testing login", tag="alwin", width=300, height=200, on_close=lambda: deleteitem("alwin")):
        dpg.add_text("Please enter your credentials.")
        dpg.add_input_text(label="Key", tag="keybox",hint="xxxxx-xxxxx-xxxxx")
        dpg.add_input_text(label="Pin", tag="pinbox",hint="xxxxxxxxxx")
        with dpg.group(horizontal=True):
            dpg.add_button(label="Submit", callback=lambda: validatedetails(dpg.get_value("keybox"), dpg.get_value("pinbox")))
            dpg.add_button(label="Cancel", callback=lambda: deleteitem("alwin"))




def domenu(sender):
    if sender=="alphalog":
        alphalogin()
    if sender=="alphalogo":
        removefile("alphakey.txt")
        print("Opting out of alpha testing...")
        restart_app()
    if sender=="cfu":
        print ("Fetching files...")
        fetch_and_download_files(owner="TriTriTheCuber", repo="TFX", folder_path="2020", destination="InstallerInserts", branch="main")
        fetch_and_download_files(owner="TriTriTheCuber", repo="TFX", folder_path="2024", destination="InstallerInserts2024", branch="main")
        restart_app()
    if sender=="cfua":
        print ("Fetching alpha files...")
        fetch_and_download_files(owner="TriTriTheCuber", repo="TFX", folder_path=r"alpha/2020", destination=r"alpha\2020", branch="main")
        fetch_and_download_files(owner="TriTriTheCuber", repo="TFX", folder_path=r"alpha/2024", destination=r"alpha\2024", branch="main")
        restart_app()



def verify_and_download(filename, base_url):
    if not os.path.exists(filename):
        url = f"{base_url}/{filename}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}")


def parse_tfx_metadata(file_path):
    installed = False
    path = []
    name = None
    tag = None
    version = None
    start_line = None
    end_line = None

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        
        if '<!-- TFX INSTALLED -->' in line:
            installed = True
            start_line = line

        # PATH or PATH1, PATH2, etc
        if line.startswith("<!-- PATH"):
            match = re.search(r'PATH\d*\s*=\s*(.+?)\s*-->', line)
            if match:
                path.append(match.group(1))
        
        elif '<!-- NAME =' in line:
            name = line.strip().replace('<!-- NAME =', '').replace('-->', '').strip()

        elif '<!-- TAG =' in line:
            tag = line.strip().replace('<!-- TAG =', '').replace('-->', '').strip()

        elif '<!-- TFX VERSION' in line:
            version = line.strip().replace('<!-- TFX VERSION', '').replace('-->', '').strip()

        elif '<!-- TFX END -->' in line:
            end_line = line
            break

    return path, name, version, tag, installed


def uninstall_from_module(modulepath,simversion):
    outpat, outname, outver, outtag, outinstall = parse_tfx_metadata(modulepath)
    outpath = []
    for index in range(len(outpat)):
        if simversion=="2020":
            outpath.append(os.path.join(community_2020, outpat[index]))
        else:
            outpath.append(os.path.join(community_2024, outpat[index]))
    
    print (f"Outpath -> '{outpath[0]}' \nOutname -> '{outname}' \nOutver -> '{outver}' \nOuttag -> '{outtag}'")
    target_file = []
    for index in range(len(outpath)):
        target_file.append(Path(outpath[index]))
    loopuninstall_tfx(target_file)
    if simversion=="2020":
            spath = os.path.join(community_2020, get_top_level_folder(outpat[0]), "layout.json")
    else:
            spath = os.path.join(community_2024, get_top_level_folder(outpat[0]), "layout.json")
    print (spath)
    regenlayout(spath)

def install_from_module(modulepath, simversion):
    outpat, outname, outver, outtag, outinstall = parse_tfx_metadata(modulepath)
    outpath = []
    for index in range(len(outpat)):
        if simversion=="2020":
            outpath.append(os.path.join(community_2020, outpat[index]))
        else:
            outpath.append(os.path.join(community_2024, outpat[index]))
    
    print (f"Outpath -> '{outpath[0]}' \nOutname -> '{outname}' \nOutver -> '{outver}' \nOuttag -> '{outtag}'")
    loopinstall_tfx(filenames=outpath,insert_path=modulepath, module_name=outname, custom_tag=outtag)
    if simversion=="2020":
            spath = os.path.join(community_2020, get_top_level_folder(outpat[0]), "layout.json")
    else:
            spath = os.path.join(community_2024, get_top_level_folder(outpat[0]), "layout.json")
    print (spath)
    regenlayout(spath)



def on_window_close():
    print("Window closed. Shutting down.")
    dpg.stop_dearpygui()


def regenlayout(path):
    subprocess.run(["MSFSLayoutGenerator.exe", path])

def set_state(value):
    with open("state.txt", "w", encoding="utf-8") as f:
        f.write(str(value) + "\n")

if not os.path.isfile("state.txt"):
    with open("state.txt", 'x') as state:
        state.write("0")


def get_state():
    try:
        with open("state.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None  # or default to "0"


def devtoggle():
    current = get_state()
    new_value = "1" if current == "0" else "0"
    set_state(new_value)
    print (rf"New devmode = {new_value}")
    restart_app()


def mainwindow():
    global alpha
    global alphareg
    alpha, alphareg = getalphastatus()
    devmode = get_state()
    if devmode == "1":
        devmodet = True
    else:
        devmodet = False
    with dpg.window(tag="main_panel", width=500, height=400, pos=[0,0],label="TriTriSim Installer",on_close=on_window_close):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Check for updates", tag="cfu", callback=domenu)
                if alpha == 1:
                    dpg.add_menu_item(label="Check for updates (Alpha)", tag="cfua", callback=domenu)
                dpg.add_menu_item(label="Restart Installer", callback=lambda: restart_app())
            with dpg.menu(label="Settings"):
                dpg.add_checkbox(label="Devmode", tag="devtoggle", default_value=devmodet, callback=devtoggle)
            with dpg.menu(label="Programs"):
                if alpha == 0:
                    dpg.add_menu_item(label="Alpha testing login", tag="alphalog", callback=domenu)
                else:
                    dpg.add_menu_item(label="Opt out of alpha testing", tag="alphalogo", callback=domenu)
            if devmode=="1":
                with dpg.menu(label="Devmode"):
                    dpg.add_menu_item(label="Reset installer", callback=resetapplication)
            
        dpg.add_text("Welcome to the TriTriSim installer. \nPlease select an installer:")
        exist_2020 = community_2020 and not community_2020 == " "
        exist_2024 = community_2024 and not community_2024 == " "
        with dpg.tab_bar(label="tab bar"):
            if exist_2020:
                with dpg.tab(label="2020",tag="2020tab"):
                    with dpg.group(horizontal=True, tag="2020sg"):
                        createspecialbuttons(buttontag="2020sg", simversion="2020")
                    generate_file_buttons(folder_path="InstallerInserts", buttontag="2020tab", simversion="2020")
            if exist_2024:
                with dpg.tab(label="2024",tag="2024tab"):
                    with dpg.group(horizontal=True, tag="2024sg"):
                        createspecialbuttons(buttontag="2024sg", simversion="2024")
                    generate_file_buttons(folder_path="InstallerInserts2024", buttontag="2024tab", simversion="2024")
            if alpha == 1:
                with dpg.tab(label="Alpha",tag="altab"):
                    generate_file_buttons(folder_path=r"alpha\2020", buttontag="altab", simversion="2020", extraprefix="(2020) ")
                    generate_file_buttons(folder_path=r"alpha\2024", buttontag="altab", simversion="2024", extraprefix="(2024) ")

            




def none2020():
    global community_2020
    community_2020 = " "

def none2024():
    global community_2024
    community_2024 = " "


def fileset2020(sender, appdata):
    global community_2020
    community_2020 = appdata['file_path_name']

def fileset2024(sender, appdata):
    global community_2024
    community_2024 = appdata['file_path_name']

def getcommunity():
    community_2020f = None
    community_2024f = None
    found = find_msfs_community_folders()
    if not found:
        print("❌ No Community folders found from UserCfg.opt files.")
    else:
        for origin, path in found:
            if "2024" in origin:
                print(f"Found MSFS 2024 Community folder:\n{path}")
                community_2024f = path
            else:
                print(f"Found MSFS 2020 Community folder:\n{path}")
                community_2020f = path
    if not community_2020f:
        community_2020f = " "
    if not community_2024f:
        community_2024f = " "
    return community_2020f, community_2024f


# End of important stuff
community_2020 = None
community_2024 = None

devmode = get_state()
if devmode == "1":
    devmodet = True
else:
    devmodet = False

def getalphastatus():
    global goodlogin
    if os.path.isfile("alphakey.txt"):
        with open("alphakey.txt", "r") as al:
            lines = al.readlines()
            delines = base64.b64decode(lines[0]).decode('utf-8')
        key = delines[:17]
        pin = delines[-10:]
        print (f"Key is {key}, pin is {pin}")
        svalidatedetails(key,pin)
        if goodlogin == 1:
            ar = [key,pin]
            a = 1
            print(f"Login was sucessful")
        else:
            a = 0
            ar = []
            print(f"Login was unsucessful. File deleting.")
            print("Reason: Invalid credentials")
            removefile("alphakey.txt")
    else:
        a = 0
        ar = []
    return a, ar




global alpha
global alphareg



if not os.path.exists("InstallerInserts"):
    os.makedirs("InstallerInserts")
if not os.path.exists("InstallerInserts2024"):
    os.makedirs("InstallerInserts2024")


if not devmode=="1":
    fetch_and_download_files(owner="TriTriTheCuber", repo="TFX", folder_path="2020", destination="InstallerInserts", branch="main")
    fetch_and_download_files(owner="TriTriTheCuber", repo="TFX", folder_path="2024", destination="InstallerInserts2024", branch="main")

currentver = 1
base_url = "https://raw.githubusercontent.com/TriTriTheCuber/TFX/main"
required_files = ["MSFSLayoutGenerator.exe"]

for file in required_files:
    verify_and_download(file, base_url)

dpg.create_context()



dpg.create_viewport(clear_color=[0,0,0,0], title="TriTriSim Installer_87498378")

if not os.path.isfile("community.txt"):
    community_2020, community_2024 = getcommunity()
    if community_2020 == " ":
        community_2020 = None
    if community_2024 == " ":
        community_2024 = None
    if community_2020 == None:
        dpg.add_file_dialog(directory_selector=True, show=True, callback=fileset2020, cancel_callback=none2020, tag="2020filedialogue", width=700, height=400, label="Please select your 2020 community folder, it was not detected. If you do not have MSFS 2020 installed, please press 'cancel'.")
    if community_2024 == None:
        dpg.add_file_dialog(directory_selector=True, show=True, callback=fileset2024, cancel_callback=none2024, tag="2024filedialogue", width=700, height=400, label="Please select your 2024 community folder, it was not detected. If you do not have MSFS 2024 installed, please press 'cancel'.")
else:
    with open("community.txt", "r") as c:
        communitylines = c.readlines()
        community_2020 = communitylines[0].strip()
        community_2024 = communitylines[1].strip()

print (f"{community_2020}\n{community_2024}")



with dpg.theme() as disabled_theme:
    with dpg.theme_component(dpg.mvButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (30, 30, 30, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (30, 30, 30, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (30, 30, 30, 255))

dpg.bind_theme(disabled_theme)


#init main window
mainwindow()
if alpha == 1:
    if not os.path.exists("alpha"):
        os.makedirs("alpha")
    if not os.path.exists(r"alpha\2020"):
        os.makedirs(r"alpha\2020")
    if not os.path.exists(r"alpha\2024"):
        os.makedirs(r"alpha\2024")






dpg.setup_dearpygui()
dpg.show_viewport()



dpg.toggle_viewport_fullscreen()

# Get native HWND handle
hwnd = ctypes.windll.user32.FindWindowW(None, "TriTriSim Installer_87498378")
# Set window style to layered (NOT transparent to input)
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
# Apply the style
style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
style |= WS_EX_LAYERED
ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
# Enable transparency with color key (pure black = transparent)
ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0x000000, 0, 0x01)

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    if community_2020 and community_2024:
        if not os.path.isfile("community.txt"):
            with open("community.txt", 'x') as community:
                community.write(community_2020)
                community.write("\n")
                community.write(community_2024)
                restart_app()

dpg.start_dearpygui()
dpg.destroy_context()