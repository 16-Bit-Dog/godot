import os
import shutil
import sys
import urllib.request
from methods import print_error, print_warning
import os
from typing import TYPE_CHECKING
from misc.utility.scons_hints import *

if TYPE_CHECKING:
    from SCons.Script.SConscript import SConsEnvironment

def get_godot_base_dependencies_path():
    # Base Godot dependencies path
    deps_folder = "thirdparty/"
    if(not os.path.exists(deps_folder)):
        print("Not running scons from root godot folder, Slang will not download as expected")

    return deps_folder

def get_slang_folder_path():
    return get_godot_base_dependencies_path()+"slang/"

def get_slang_version():
    return "2025.8"

def get_slang_archive_name(slang_platform_name, slang_arch_name):
    return "slang-"+get_slang_version()+"-"+slang_platform_name+"-"+slang_arch_name+".zip"

def get_slang_archive_path(slang_platform_name, slang_arch_name):
    return os.path.join(get_slang_folder_path(), get_slang_archive_name(slang_platform_name, slang_arch_name))

def fetch_slang(slang_platform_name, slang_arch_name):
    #https://github.com/shader-slang/slang/releases/download/v2025.1/slang-2025.1-windows-x86_64.zip
    slang_folder = get_slang_folder_path()

    # Create dependencies folder
    mustClean = True
    if not os.path.exists(slang_folder):
        print("Making Dirs: "+slang_folder)
        os.makedirs(slang_folder)
        mustClean = False
        
    slang_version = get_slang_version()
    slang_archive_name = get_slang_archive_name(slang_platform_name, slang_arch_name)
    slang_folder_path = get_slang_folder_path()
    slang_archive_path = get_slang_archive_path(slang_platform_name, slang_arch_name)

    # remove all but the zip since we do not know if these files are up-to-date, only can trust the zip-name
    if mustClean:
        print("Cleaning previously installed Slang")
        for i in os.listdir(slang_folder_path):
            if(not i.endswith(".zip")):
                ipath = slang_folder_path+str(i)
                if(os.path.isdir(ipath)):
                    shutil.rmtree(ipath)
                else:
                    os.remove(ipath)

    if not os.path.isfile(slang_archive_path):
        url = f"https://github.com/shader-slang/slang/releases/download/v{slang_version}/{slang_archive_name}"
        print(f"Downloading Slang {slang_archive_name} from {url} ...")
        urllib.request.urlretrieve(
            url,
            slang_archive_path,
        )
    
    print(f"Extracting Slang {slang_archive_path} to {slang_folder_path} ...")
    shutil.unpack_archive(slang_archive_path, slang_folder_path)
    print(f"Installed Slang at {slang_folder_path}")    

# if unsupported `platformName`/`archName` is specified, the program will exit
def install_slang(env: "SConsEnvironment", platformName, archName):
    platform_name_to_slang_platform_name = {
        "Android": "linux",
        "iOS": "macos",
        "LinuxBSD": "linux",
        "macOS" : "macos",
        "Windows" : "windows"
    }
    arch_name_to_slang_arch_name = {
        "x86_64": "x86_64",
        "arm64": "aarch64",
    }
    
    slang_platform_name = platform_name_to_slang_platform_name.get(platformName)
    slang_arch_name = arch_name_to_slang_arch_name.get(archName)

    if slang_platform_name == None: 
        print_error("slang does not support the platform: "+platformName)
        sys.exit(255)
    if slang_arch_name == None: 
        print_error("slang does not support the arch: "+archName)
        sys.exit(255)
        
    fetch_slang(slang_platform_name, slang_arch_name)

    env["slang_path"] = get_slang_folder_path()
    env.AppendUnique(CPPDEFINES=["SLANG_ENABLED"])
    env.Append(LIBPATH=[os.path.realpath(os.path.join(env["slang_path"], "lib"))])
    if env.msvc:
        env.Append(LINKFLAGS=["slang.lib"])
    else:
        env.Append(LIBS=["slang"])
    slang_include_dir = os.path.relpath(os.path.join(env["slang_path"], "bin"))
    if not env.msvc:
        env.Append(CPPFLAGS=["-isystem", Dir(slang_include_dir).path])
    else:
        env.Prepend(CPPPATH=[slang_include_dir])