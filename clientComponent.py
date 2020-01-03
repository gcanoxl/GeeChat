from PyQt5.QtWidgets import QTextEdit, QListWidget, QToolBar
from PyQt5.QtCore import Qt


class GeeUserList(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GeeTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GeeContentBox(GeeTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAcceptRichText(True)
        self.setReadOnly(True)


class GeeInputMsgBox(GeeTextEdit):
    def __init__(self, window, *args, **kwargs):
        self.client = window
        super().__init__(*args, **kwargs)

        self.setReadOnly(False)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            self.client.sendMsg(self.toPlainText())
            self.clear()
        else:
            super().keyPressEvent(e)


class GeeToolBar(QToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
