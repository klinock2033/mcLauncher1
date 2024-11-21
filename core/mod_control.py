import asyncio
import sys
import os
import json
import hashlib
import yadisk
from colorama import Fore, Style
y = yadisk.YaDisk(token="y0_AgAAAAA8Bn3ZAAt3-QAAAAD-uFFGAADQQm_XPJpNlaMAsMmwQRNL6f6obA")

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
        self.dev_Tool("intializare", "done")

    def dev_Tool(self, text, msgType):
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


    def cautam_directoriul_mods(self):
        if os.path.exists(project_mods_path):

            self.dev_Tool("Mods directory exist", "done")

        else:
            self.dev_Tool("Mods directory don't exist", "warn")
            try:
                os.makedirs(project_mods_path)
                self.dev_Tool("Create Mods Directory", "done")
            except OSError as e:
                print(f"Eroare la crearea directorului '{project_mods_path}': {e}")
                raspuns_etapa = "Acces Dened!"
