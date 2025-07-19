#stripped installer
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
import webbrowser
global community_2020
global community_2024

def get_top_level_folder(path):
    normalized_path = os.path.normpath(path)  # Normalizes slashes
    parts = normalized_path.split(os.sep)     # Splits by platform-specific separator
    return parts[0] if parts else None


def fetch_remote_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip().splitlines()
    except Exception as e:
        print(f"Failed to fetch remote file: {e}")
        return None


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



def get_last_index_containing(lines, substring):
    for i in reversed(range(len(lines))):
        if substring in lines[i]:
            return i
    return -1  # Not found

def get_first_index_containing(lines, substring):
    for i in range(len(lines)):
        if substring in lines[i]:
            return i
    return -1  # Not found


def checkmodulemethod(modulepath):
    with open(modulepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    indexex = get_first_index_containing(lines, "<!-- EX1UFILE = True -->")
    indexfa = get_first_index_containing(lines, "<!-- ASOBO FXA -->")
    if indexex == -1:
        if indexfa == -1:
            return("Norm")
        else:
            return("FXA")
    else:
        return("EX1")

def checkcustlayout(filepath):
    layout = None
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        if '<!-- CUSTOMLAYOUTPATH' in line:
            layout = line.strip().replace('<!-- CUSTOMLAYOUTPATH =', '').replace('-->', '').strip()
            return layout

    return None

def parse_ex1_metadata(modulepath):
    exurl = None
    expath = None
    newfile = None

    with open(modulepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        
        if '<!-- EXTERPTH' in line:
            expath = line.strip().replace('<!-- EXTERPTH =', '').replace('-->', '').strip()

        if '<!-- EXURL' in line:
            exurl = line.strip().replace('<!-- EXURL =', '').replace('-->', '').strip()
        
        if '<!-- NEWFILENAME' in line:
            newfile = line.strip().replace('<!-- NEWFILENAME =', '').replace('-->', '').strip()

    return exurl, expath, newfile



def quiet_uninstall(target_file, is_ex1 = False, impath = None):
    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    try:
        start = get_first_index_containing(lines, "TFX INSTALLED")
        end = get_last_index_containing(lines, "TFX END")
        del lines[start:end + 1]
        print(f"TFX update/reinstall completed successfully.")
    except ValueError:
        print(f"TFX installation completed successfully (no previous entry found).")

    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def uninstall_tfx(target_file):
    extfile = target_file
    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    method = checkmodulemethod(target_file)
    if method == "FXA":
        path = target_file
        path = Path(path).parent
        path = Path(path).parent
        removepath(path)
    else:
        try:
            start = lines.index('<!-- TFX INSTALLED -->\n')
            end = lines.index('<!-- TFX END -->\n')
            del lines[start:end + 1]
            print(r"TFX Uninstalled sucessfully.")
        except ValueError:
            file = rf"{Path(target_file).parent}\TFXinjbehavior.xml"
            if not os.path.isfile(file):
                print(r"TFX is not installed, uninstall skipped")
            else:
                impath, expath, addedfilename = parse_ex1_metadata(file)
                os.remove(file)
                os.remove(extfile)
                r = fetch_remote_file(r"https://raw.githubusercontent.com/TriTriTheCuber/TFX/refs/heads/main/ex1ini/oldexteriordefenitions/" + impath)
                r = "\n".join(r)
                with open(extfile, 'x', encoding='utf-8') as l:
                    l.write(r)
                print(r"TFX Uninstalled sucessfully.")
                return

        with open(target_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)



def loopinstall_tfx(filenames, insert_path, module_name, custom_tag):
    for fn in filenames:
        install_tfx(fn, insert_path, module_name, custom_tag)

def loopuninstall_tfx(target_files):
    for tf in target_files:
        uninstall_tfx(tf)



def install_tfx(filename, insert_path, module_name, custom_tag="</Behaviors>"):
    checkmodulemethod(insert_path)
    mmethod = checkmodulemethod(insert_path)
    if mmethod == "EX1":

        impath, expath, addedfilename = parse_ex1_metadata(insert_path)
        print(f"impath = '{impath}'\nexpath = '{expath}'\naddedfilename = '{addedfilename}'")
        remote = fetch_remote_file(r"https://raw.githubusercontent.com/TriTriTheCuber/tfx/main/ex1ini/newexteriordefinitions/" + impath)
        remote = "\n".join(remote)
        os.remove(filename)
        with open(filename, 'x', encoding='utf-8') as s:
            s.write(remote)
        addedfile = fr"{Path(filename).parent}\{addedfilename}"
        print (addedfile)
        with open(insert_path, 'r', encoding='utf-8') as f:
            insert = f.readlines()
        
        if os.path.isfile(addedfile):
            os.remove(addedfile)

        with open(addedfile, "x", encoding='utf-8') as i:
            insert = "".join(insert)
            i.write(insert)

        return
    
    if mmethod == "FXA":

        with open(insert_path, 'r', encoding='utf-8') as f:
            insert = f.readlines()
            insert = "".join(insert)
        if os.path.isfile(filename):
            path = filename
            path = Path(path).parent
            path = Path(path).parent
            removepath(path)
        os.makedirs(Path(filename).parent)
        with open(filename, 'x', encoding='utf-8') as s:
            s.write(insert)

        return



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
    if not installed:
        nfp = os.path.join(Path(file_path).parent, "TFXinjbehavior.xml")
        if not nfp == file_path:
            path, name, version, tag, installed = parse_tfx_metadata(nfp)
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
    lp = checkcustlayout(modulepath)
    if not lp:
        if simversion=="2020":
                spath = os.path.join(community_2020, get_top_level_folder(outpat[0]), "layout.json")
        else:
                spath = os.path.join(community_2024, get_top_level_folder(outpat[0]), "layout.json")
    else:
        if simversion=="2020":
                spath = os.path.join(community_2020, lp)
        else:
                spath = os.path.join(community_2024, lp)

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
    lp = checkcustlayout(modulepath)
    if not lp:
        if simversion=="2020":
                spath = os.path.join(community_2020, get_top_level_folder(outpat[0]), "layout.json")
        else:
                spath = os.path.join(community_2024, get_top_level_folder(outpat[0]), "layout.json")
    else:
        if simversion=="2020":
                spath = os.path.join(community_2020, lp)
        else:
                spath = os.path.join(community_2024, lp)

    regenlayout(spath)



def planebutton(sender, app_data, user_data):
    print(f"Clicked: {user_data[0]}")
    print(f"Sim version: {user_data[1]}")
    print(f"Action: '{user_data[2]}")
    action = user_data[2]
    if action == "--install":
        install_from_module(modulepath=user_data[0], simversion=user_data[1])
    if action == "--uninstall":
        uninstall_from_module(modulepath=user_data[0], simversion=user_data[1])
    if action == "--update":
        install_from_module(modulepath=user_data[0], simversion=user_data[1])


def regenlayout(path):
    subprocess.run(["MSFSLayoutGenerator.exe", path])




base_url = "https://raw.githubusercontent.com/TriTriTheCuber/TFX/main"

community_2020 = Path(sys.argv[2])
community_2024 = Path(sys.argv[2])
action = sys.argv[3]
file = Path(sys.argv[1])
simversion = sys.argv[4]
print(f"Community = {community_2020}, File = {file}, Action = {action}\nSimulator version: {simversion}")

planebutton(None, None, user_data=[file, simversion, action])

