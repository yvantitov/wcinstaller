# wc installer
# by yvan titov

import os
import json
import subprocess
import requests
import uuid

from lxml import html

version = "1.0.0"

print("WC temporary installer " + version + "\n ")

# download and install forge
print("Downloading Forge...")
forge_url = ("https://files.minecraftforge.net/maven/net/minecraftforge/"
             "forge/1.12.2-14.23.5.2847/forge-1.12.2-14.23.5.2847-installer.jar")
r = requests.get(forge_url)
open("forge.jar", "wb").write(r.content)
print("To continue, press OK to install the Forge client in your .minecraft folder")
cmd = ["java", "-jar", "forge.jar"]
installer_output: list = []
forge_installer_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
mc_path = ""
for line in forge_installer_process.stdout:
    line = str(line)
    i = line.find("libraries")
    if i != -1:
        line = line[15:i-2]
        for j in range(0, len(line)):
            char = line[j]
            if char == "\\":
                next_char = line[j+1]
                if next_char == "\\":
                    continue
            mc_path = mc_path + char
print("Done installing Forge...\n")

# create the game directory and folders
default_path = mc_path + "\\westeroscraft"
usr_ans = input("Where should WC client files be installed? Press ENTER for default (" + default_path + ") ")
wc_path = usr_ans if usr_ans != "" else default_path
os.makedirs(wc_path, exist_ok=True)
os.makedirs(wc_path + "\\mods", exist_ok=True)
os.makedirs(wc_path + "\\resourcepacks", exist_ok=True)
print("Created WesterosCraft game directory at " + wc_path + "\n")

# download and install mods
print("Downloading required mods...")
mods_path = wc_path + "\\mods\\"
of_url = "https://optifine.net/adloadx?f=OptiFine_1.12.2_HD_U_F5.jar"
wb_url = "http://mc.westeroscraft.com/WesterosCraftLauncher/prod-1.12.2/mods/WesterosBlocks.jar"
hc_url = "http://mc.westeroscraft.com/WesterosCraftLauncher/prod-1.12.2/mods/horse_colors.jar"
r = requests.get(of_url)
tree = html.fromstring(r.content)
of_anchor_elem = tree.xpath('//a[text()="OptiFine 1.12.2 HD U F5"]')
r = requests.get("http://optifine.net/" + of_anchor_elem[0].attrib['href'])
open(mods_path + "OptiFine_1.12.2_HD_U_F5.jar", "wb").write(r.content)
r = requests.get(wb_url)
open(mods_path + "WesterosBlocks.jar", "wb").write(r.content)
r = requests.get(hc_url)
open(mods_path + "horse_colors.jar", "wb").write(r.content)
print("All required mods have been installed\n")

# TODO: add support for automatically installing recommended mods

# get the resourcepack
print("Downloading the resourcepack...")
rp_path = wc_path + "\\resourcepacks\\"
rp_url = "http://mc.westeroscraft.com/WesterosCraftLauncher/prod-1.12.2/resourcepacks/WesterosCraft.zip"
r = requests.get(rp_url)
open(rp_path + "WesterosCraft.zip", "wb").write(r.content)
print("The resourcepack has been installed\n")

# add WC as an installation for the minecraft launcher
print("Setting up the minecraft launcher...")
with open(mc_path + "\\launcher_profiles.json") as f:
    profiles = json.load(f)
wc_profile_id = uuid.uuid4().hex
profiles["profiles"][wc_profile_id] = {
    "created": "1970-01-02T00:00:00.000Z",
    "gameDir": wc_path.replace("\\", "\\\\"),
    "icon": "Brick",
    "lastUsed": "1970-01-02T00:00:00.000Z",
    "lastVersionId": "1.12.2-forge1.12.2-14.23.5.2847",
    "name": "WesterosCraft 1.12.2",
    "type": "custom"
}
with open(mc_path + "\\launcher_profiles.json", "w") as f:
    json.dump(profiles, f)
print("Minecraft launcher installation created...\n")

print("Cleaning up...")
os.remove("forge.jar")
os.remove("forge.jar.log")
print("Cleaned up spare Forge files...\n")

print("Installation complete. Press ENTER to continue")
input()
