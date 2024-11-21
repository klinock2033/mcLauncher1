import configparser
import os

config = configparser.ConfigParser()
setingPatch = 'setings/config.ini'

class Setings:
    def __init__(self, parent):
        self.parent = parent
        self.comboBox_ram = parent.comboBox_ram
        self.label_19 = parent.label_19
        self.pushButton_save = parent.pushButton_save

        self.SetUp_setings()
        self.configRed()

    def configRed(self):
        memory_ram = checkConfigExist()
        self.comboBox_ram.setCurrentText(memory_ram)

    def SetUp_setings(self):

        self.pushButton_save.clicked.connect(lambda: saveConfig(self.comboBox_ram.currentText()))

def checkConfigExist():
    if os.path.isfile(setingPatch):

        config.read(setingPatch)
        memory_ram = config['DEFAULT']['memory_ram']
        print(f"setarile au fost gasite {memory_ram}")
        return memory_ram
    else:
        print("setarile nu au fost gasite")
        config['DEFAULT'] = {'memory_ram': '4G'}
        with open(setingPatch, "w") as configfile:
            config.write(configfile)

        return "4G"
def saveConfig(ram_x):
    config['DEFAULT'] = {'memory_ram': ram_x}
    with open(setingPatch, "w") as configfile:
        config.write(configfile)