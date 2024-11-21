import asyncio
import configparser
username = ""
accKey = {
    "AAA": "test",
    "AAA1": "test",
    "AAA2": "test",
    "AAA3": "test",
    "AAA4": "test",
}

setingPatch = 'setings/config.ini'
class Keytest:
    def __init__(self, parent):
        self.parent = parent
        self.lineEdit_key = parent.lineEdit_key
        self.pushButton_start = parent.pushButton_start
        self.label_16 = parent.label_16

        self.setUp_KeyLine()

    def setUp_KeyLine(self):
        self.lineEdit_key.setText(loadKey())

        #self.pushButton_start.clicked.connect(lambda: asyncio.create_task(self.checkKey(self.lineEdit_key.text())))

    def checkKey(self, cheaia):
        print("check key")

        if cheaia in accKey:
            print(f"{cheaia} exista in dictionar")
            self.label_16.setText(f"Welcome {accKey[cheaia]}")
            self.label_16.setStyleSheet("color:green; font-size:20px;")
            saveConfig(cheaia)
            username = accKey[cheaia]
            return True
        else:
            print(f"{cheaia} NU exista in dictionar")
            self.label_16.setText("Key error")
            self.label_16.setStyleSheet("color:red; font-size:20px;")
            return False


def saveConfig(key):
    config = configparser.ConfigParser()
    config.read(setingPatch)
    config['DEFAULT']['key'] = key
    with open(setingPatch, "w") as configfile:
        config.write(configfile)

def loadKey():
    config = configparser.ConfigParser()
    config.read(setingPatch)
    if "key" in config["DEFAULT"]:
        user_key = config["DEFAULT"]["key"]
        return user_key
    else:
        return ""