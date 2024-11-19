from PyQt5.QtCore import Qt
import asyncio


class Sidebar:
    def __init__(self, parent):
        self.parent = parent
        self.widget_SideBar = parent.widget_SideBar
        self.label_select = parent.label_select
        self.tabWidget = parent.tabWidget

        self.setup_sidebar()

    def setup_sidebar(self):
        """ initializarea sidebar """
        self.parent.l_but_accaunt.mousePressEvent = lambda event: self.changeSideBarTab(event, "user")
        self.parent.l_but_sellect.mousePressEvent = lambda event: self.changeSideBarTab(event, "setings")
        self.set_sidebar_position("open")


    def init_async_tasks(self):
        print("Check server status")
        asyncio.create_task(self.parent.check_server_status())

    def set_sidebar_position(self, status):
        """activam dezactivam sidebar"""
        if status == "open":
            self.widget_SideBar.move(0, 36)
        elif status == "close":
            self.widget_SideBar.move(420, 50)

    def changeSideBarTab(self, event, tabName):
        """ schimba tab """
        if event.button() == Qt.LeftButton:
            if tabName == "user":
                self.label_select.move(0, 0)
                # Schimbă la tab-ul user
                self.tabWidget.setCurrentWidget(self.parent.tab)
            elif tabName == "setings":
                self.label_select.move(0, 83)
                # Schimbă la tab-ul de setări
                self.tabWidget.setCurrentWidget(self.parent.tab_2)
            else:
                print("Error: Tab selection failed.")
            event.accept()
