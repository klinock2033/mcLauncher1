import sys
import resources_rc
import socket
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
import asyncio
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
        #Bara de scroll
        self.label_title.mousePressEvent = self.start_moving
        self.label_title.mouseMoveEvent = self.move_window
        self.label_title.mouseReleaseEvent = self.stop_moving
        #SideBar schimbam taburile
        self.l_but_accaunt.mousePressEvent = lambda event: self.changeSideBarTab(event, "user")
        self.l_but_sellect.mousePressEvent = lambda event: self.changeSideBarTab(event, "setings")

        self._is_moving = False  # Variabilă pentru a determina dacă se mută fereastra

        #butonul close
        self.label_butt_exit.mousePressEvent = self.closeApp
        #SideBar repozition
        self.sidBarPosition("open")
        # Amânăm inițializarea task-ului
        QTimer.singleShot(0, self.init_async_tasks)

    def init_async_tasks(self):
        """Inițializează task-urile asincrone după ce aplicația este gata."""
        print("first chek server status")
        asyncio.create_task(self.check_server_status())
    def closeApp(self): #exit app
        self.close()
    def start_moving(self, event): #TopBar start move window
        if event.button() == Qt.LeftButton:
            self._is_moving = True
            self._start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def move_window(self, event): #TopBar move window
        if self._is_moving and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._start_pos)
            event.accept()

    def stop_moving(self, event): #TopBar stop move window
        if event.button() == Qt.LeftButton:
            self._is_moving = False
            event.accept()

    def sidBarPosition(self,status): #SideBar active inactive
        if status == "open":
            self.widget_SideBar.move(0,36)

        elif status == "close":
            self.widget_SideBar.move(420, 50)

    def changeSideBarTab(self, event, tabName):
        if event.button() == Qt.LeftButton:
            if tabName == "user":
                self.label_select.move(0, 0)
                #User tab
                self.tabWidget.setCurrentWidget(self.tab)
            elif tabName == "setings":
                self.label_select.move(0, 83)
                # setings tab
                self.tabWidget.setCurrentWidget(self.tab_2)
            else:
                print("error sellect tab")
            event.accept()
#Tab 1
    async def check_server_status(self): #controlam daca serveru e online
        ip = "193.233.80.168"
        port = 25565
        print("Check server status")
        try:
            reader, writer = await asyncio.open_connection(ip, port)
            self.label_18.setText("Online")
            QTimer.singleShot(3000, self.init_async_tasks)
            self.label_18.setStyleSheet("color: green; font-size: 30px;")
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            self.label_18.setText("Offline")
            self.label_18.setStyleSheet("color: red; font-size: 30px;")
            QTimer.singleShot(3000, self.init_async_tasks)
            print(f"Eroare: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()
