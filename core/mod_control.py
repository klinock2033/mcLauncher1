import asyncio
import sys
import os
import json
import hashlib
import yadisk
from colorama import Fore, Style
y = yadisk.YaDisk(token="y0_AgAAAAA8Bn3ZAAt3-QAAAAD-uFFGAADQQm_XPJpNlaMAsMmwQRNL6f6obA")

cloud_patch = "/minecraft_server/minecraft_launcher_mod/"

server_mod_list = {}
player_mod_list = {}
lista_moduri_nedorite = {}

project_mods_path = os.path.expanduser("~\\AppData\\Roaming\\.magmaDarck\\mods")

base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'

class FileControl:
    def __init__(self, parent):
        self.parent = parent
        self.textBrowser = parent.textBrowser
        self.progressBar = parent.progressBar

        self.setUp_fileControl()

    def setUp_fileControl(self):
        self.textBrowser.setText("")

    async def dev_Tool(self, text, msgType):
        ToolVersion = f"{Fore.CYAN}[Dev-tool-v1.0]:{Style.RESET_ALL}"
        ToolVersionHtml = "<font color='cyan'>[Dev-tool-v1.0]:</font>"
        color_map_console = {
            "simple": Style.RESET_ALL,
            "done": Fore.GREEN,
            "warn": Fore.YELLOW,
            "error": Fore.RED
        }
        if msgType == "simple":
            message = f"{ToolVersionHtml} <font color='white'>{text}</font>"
        elif msgType == "done":
            message = f"{ToolVersionHtml} <font color='green'>{text}</font>"
        elif msgType == "warn":
            message = f"{ToolVersionHtml} <font color='yellow'>{text}</font>"
        elif msgType == "error":
            message = f"{ToolVersionHtml} <font color='red'>{text}</font>"
        else:
            message = f"{ToolVersionHtml} <font color='red'>Dev tool error!</font>"
        colorConsole = color_map_console.get(msgType, Fore.RED)
        msg = message
        msgConsole = f"{ToolVersion} {colorConsole}{text}{Style.RESET_ALL}"
        print(msgConsole)
        self.textBrowser.append(message)


    async def cautam_directoriul_mods(self):
        if os.path.exists(project_mods_path):

            await self.dev_Tool("Mods directory exist", "done")
            asyncio.create_task(self.loadCloud_List())
        else:
            await self.dev_Tool("Mods directory don't exist", "warn")
            try:
                os.makedirs(project_mods_path)
                await self.dev_Tool("Create Mods Directory", "done")
                await self.loadCloud_List()
            except OSError as e:
                print(f"Eroare la crearea directorului '{project_mods_path}': {e}")
                raspuns_etapa = "Acces Dened!"

    async def loadCloud_List(self):
        await self.dev_Tool("load cloud list", "simple")
        extensii_permise = (".zip", ".rar", ".jar")
        try:
            """Primim lista de pe Yandex Disk"""
            for item in y.listdir(cloud_patch):
                if item['type'] == 'file' and item['name'].endswith(extensii_permise):
                    server_mod_list[item['name']] = {
                        "name": item['name'],
                        "md5": item['md5'],
                        "path": item['path'],
                    }

            """for debug"""
            for mod_name, mod_info in server_mod_list.items():
                print(mod_name)
                print(f"    MD5: {mod_info['md5']}")
                print(f" ")
            await self.loadLocalList()

        except yadisk.exceptions.PathNotFoundError:
            await self.dev_Tool(f"Directorul {cloud_patch} dont exist", "error")
            return {}
        except Exception as e:
            await self.dev_Tool(f"Eroare: {e}", "error")
            return {}

    async def loadLocalList(self):
        await self.dev_Tool(f"Load local mod list", "simple")
        extensii_permise = (".zip", ".rar", ".jar")

        try:
            for item in os.listdir(project_mods_path):
                cale_completa = os.path.join(project_mods_path, item)

                if os.path.isfile(cale_completa) and cale_completa.lower().endswith(extensii_permise):
                    # Calculăm MD5 pentru fișierul respectiv
                    with open(cale_completa, 'rb') as f:
                        sumaHash = hashlib.md5()
                        while chunk := f.read(8192):  # Citim fișierul pe bucăți pentru eficiență
                            sumaHash.update(chunk)
                        sumaHash = sumaHash.hexdigest()

                    # Adăugăm fișierul în lista player_mod_list
                    player_mod_list[item] = {
                        "name": item,
                        "md5": sumaHash,
                        "path": cale_completa,
                    }


            # Afișăm lista completă de moduri după ce toate fișierele au fost procesate
            print("[Player Mod List]:")
            for mod_name, mod_info in player_mod_list.items():
                print(mod_name)
                print(f"    MD5: {mod_info['md5']}")
                print(f" ")
            await self.compareModList()

        except OSError as e:
            await self.dev_Tool(f"Eroare: {e}", "error")

    async def compareModList(self):
        numar_moduri = len(server_mod_list)
        self.progressBar.setMaximum(numar_moduri)
        cur_mod_nr = 0
        for server_mod in server_mod_list:
            instal_mod = False
            cur_mod_nr = cur_mod_nr + 1
            await self.dev_Tool(f"-----------------------", "simple")
            await self.dev_Tool(f"Mods checked: {cur_mod_nr}/{numar_moduri}", "simple")
            self.progressBar.setValue(cur_mod_nr)
            await self.dev_Tool(f"cur mod: {server_mod}", "simple")
            for local_mod in player_mod_list:
                if str(local_mod) == str(server_mod):
                    await self.dev_Tool("Mode found", "done")
                    print(f"MD5: {player_mod_list[local_mod]['md5']}")
                    print(f"MD5: {server_mod_list[server_mod]['md5']}")
                    if player_mod_list[local_mod]['md5'] == server_mod_list[server_mod]['md5']:
                        instal_mod = True
                        await self.dev_Tool("VALID", "done")
                    else:
                        await self.dev_Tool("Unauthorized Mod", "error")
                        instal_mod = False
                        try:
                            cale_fisier = player_mod_list[local_mod]['path']
                            print(cale_fisier)
                            if os.path.exists(cale_fisier):
                                os.remove(cale_fisier)
                                await self.dev_Tool(f"delete mod: {local_mod}", "simple")
                            else:
                                await self.dev_Tool(f"Can't found mod: {local_mod}", "simple")
                        except Exception as e:
                            await self.dev_Tool(e, "error")

            if instal_mod == False:
                await self.dev_Tool("Mod not found", "warn")
                await self.dev_Tool("download mod...", "simple")
                await self.installMods(server_mod)

    def deleteMod(self, filename):
        pass

    async def installMods(self, mods):
        yadnex_drum = f"{cloud_patch}{str(mods)}"
        cale_fisier = os.path.join(project_mods_path, mods)
        try:
            await asyncio.to_thread(y.download, yadnex_drum, cale_fisier)
            await self.dev_Tool(f"download Compleat", "done")

        except Exception as e:
            await self.dev_Tool(f"Eroare: {e}", "error")
        pass
