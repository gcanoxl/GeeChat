from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QVBoxLayout, QTextEdit


class GeeChatClient(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GeeChat v0.1 -- by Cano XL')

        # UserList
        self.userList = QListWidget()
        self.userList.addItem("test")

        # Messages
        self.msgList = QTextEdit()
        self.msgList.setReadOnly(True)

        # InputMsgBox
        self.inputMsgBox = QTextEdit()

        # Layout
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.userList, 2)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.msgList, 8)
        self.vbox.addWidget(self.inputMsgBox, 2)

        self.hbox.addLayout(self.vbox, 8)
        self.setLayout(self.hbox)

        self.show()
