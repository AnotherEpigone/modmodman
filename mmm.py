import configparser
import distutils
import os
import shutil
import sys
from distutils import dir_util

def cliarg_fail():
    print("USAGE: python mmm.py [command] [mod folder]")
    print("Commands: deploy, revert")
    sys.exit(1)

def deployfolder(source, target):
    print(f"deploying folder {source}")
    distutils.dir_util.copy_tree(source, target)

def deploy(modfolder, basemodfolder, modmoddeployfolder):
    print(f"deploying modmod {os.path.basename(modfolder)}")
    for filename in os.listdir(modfolder):
        if filename != "mmm.ini":
            source = os.path.join(modfolder, filename)
            target = os.path.join(modmoddeployfolder, filename)
            if os.path.isfile(source):
                print(f"deploying file {filename}")
                shutil.copy(source, target)
                continue
            if os.path.isdir(source):
                deployfolder(source, target)

def revert(modfolder, basemodfolder, modmoddeployfolder):
    for filename in os.listdir(modfolder):
        if filename != "mmm.ini":
            source = os.path.join(basemodfolder, filename)
            target = os.path.join(modmoddeployfolder, filename)
            if os.path.isfile(source):
                print(f"reverting file {filename}")
                shutil.copy(source, target)
                continue
            if os.path.isdir(source):
                newmodfolder = os.path.join(modfolder, filename)
                revert(newmodfolder, source, target)

if len(sys.argv) < 3:
    cliarg_fail()

commandstring = sys.argv[1]
modfolder = sys.argv[2]

if commandstring == "deploy":
    command = deploy
elif commandstring == "revert":
    command = revert
else:
    cliarg_fail()

config = configparser.ConfigParser()
inipath = os.path.join(modfolder, "mmm.ini")
if not os.path.isfile(inipath):
    print(f"target mod ini not found \"{inipath}\"")
    sys.exit(1)

config.read(inipath)

basemodfolder = config["mmm"]["BaseModFolder"]
modmoddeployfolder = config["mmm"]["ModmodDeployFolder"]

command(modfolder, basemodfolder, modmoddeployfolder)