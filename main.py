import sys
from core.server import server_status
from core.sidebar import Sidebar
from core.header import Header
from core.keyList import Keytest
from core.setings import Setings
from core.mod_control import FileControl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
import asyncio
import resources_rc
from qasync import QEventLoop
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mcLauncher.ui", self)  # Încarcă fișierul .ui
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(388,603)
        self.label_3.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.label_select.move(0,0)
        self.label_19.setText("")
        self.label_18.setText("Connecting...")
        #Sidevbar init
        self.sidebar = Sidebar(self)
        QTimer.singleShot(0, self.init_async_tasks)
        #Heder init
        self.header = Header(self)
        #KEY accaunt init
        self.keyTest = Keytest(self)
        #Setings init
        self.lSetings = Setings(self)
        #fileControl init
        self.fileControl = FileControl(self)
        self.pushButton_start.clicked.connect(self.startBut)

    def startBut(self):
        response = self.keyTest.checkKey(self.lineEdit_key.text())
        print(response)
        if response:
            self.sidebar.setLoading()
            self.fileControl.cautam_directoriul_mods()
        else:
            print("invalid key")

    def init_async_tasks(self):
        print("Check server status")
        asyncio.create_task(self.check_server_status())
    async def check_server_status(self): # actualizăm funcția pentru a folosi noua logică
        ip = "193.233.80.168"
        port = 25565
        is_online, error = await server_status(ip, port)
        if is_online:
            self.label_18.setText("Online")
            self.label_18.setStyleSheet("color: green; font-size: 30px;")
        else:
            self.label_18.setText("Offline")
            self.label_18.setStyleSheet("color: red; font-size: 30px;")
            print(f"Error: {error}")
        QTimer.singleShot(3000, self.init_async_tasks)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()
