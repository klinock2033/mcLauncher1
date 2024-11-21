from PyQt5.QtCore import Qt

accKey = {
    "AAA": "test",
    "AAA1": "test",
    "AAA2": "test",
    "AAA3": "test",
    "AAA4": "test",
}
class keytest:
    def __int__(self, parent):
        self.parent = parent
        self.lineEdit_key = parent.lineEdit_key
        self.pushButton_start = parent.pushButton_start
        self.label_16 = parent.label_16

    async def checkKey(self, key):
        if key in accKey:
            print(f"{key} exista in dictionar")
            self.label_16.setText("key accepted")
            self.label_16.setStyleSheet("color:green; font-size:20px;")
        else:
            print(f"{key} NU exista in dictionar")
            self.label_16.setText("Key error")
            self.label_16.setStyleSheet("color:red; font-size:20px;")