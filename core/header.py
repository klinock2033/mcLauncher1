from PyQt5.QtCore import Qt


class Header:
    def __init__(self, parent):
        self.parent = parent
        self.label_title = parent.label_title
        self.label_butt_exit = parent.label_butt_exit

        self._is_moving = False
        self._start_pos = None

        self.setUp_header()

    def setUp_header(self):
        self.label_title.mousePressEvent = self.start_moving
        self.label_title.mouseMoveEvent = self.move_window
        self.label_title.mouseReleaseEvent = self.stop_moving
        self.label_butt_exit.mousePressEvent = self.closeApp

    def start_moving(self, event): #header start move window
        if event.button() == Qt.LeftButton:
            self._is_moving = True
            self._start_pos = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def move_window(self, event): #header move window
        if self._is_moving and event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self._start_pos)
            event.accept()

    def stop_moving(self, event): #header stop move window
        if event.button() == Qt.LeftButton:
            self._is_moving = False
            event.accept()

    def closeApp(self):
        self.parent.close()