from client import GeeChatClient
import sys
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    gcc = GeeChatClient()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
