import subprocess
import minecraft_launcher_lib
import sys

current_max = 0
username = "Marter"
project_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace('minecraft', 'orizont')
forge_version = minecraft_launcher_lib.forge.find_forge_version("1.12.2")

def set_status(status: str):
    global inst_completed_final
    a = status
    if a == "Installation complete":
        inst_completed_final = 1
    else:
        inst_completed_final = 0

    print(status)
    return inst_completed_final


def set_progress(progress: int):
    global WorkProgres
    global Max_WorkProgres
    if current_max != 0:
        WorkProgres = int(progress)
        Max_WorkProgres = int(current_max)
        print(f"{progress}/{current_max}")
    return WorkProgres



def set_max(new_max: int):
    global current_max
    current_max = new_max
    print("FINAL PROGRESS SET TO :"+str(current_max))

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

def run_minecraft():
    minecraft_launcher_lib.forge.find_forge_version("1.12.2")
    options = {
        'username': username,
        'uuid:': '',
        'token': ''
    }
    subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version="1.12.2-forge-14.23.5.2860", minecraft_directory=project_directory, options=options))


def instal_minecraft():
    minecraft_launcher_lib.forge.install_forge_version(forge_version, project_directory, callback=callback)
    print(str(callback))