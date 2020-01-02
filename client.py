from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QInputDialog
from clientComponent import GeeUserList, GeeContentBox, GeeInputMsgBox
import socket
import json
import _thread


class GeeChatClient(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.userlist = []

        self.connect('127.0.0.1', 54188)
        self.login()

    def initUI(self):
        self.setWindowTitle('GeeChat v0.1 -- by Cano XL')

        # UserList
        self.userList = GeeUserList()
        # Messages
        self.contentBox = GeeContentBox()
        # InputMsgBox
        self.inputMsgBox = GeeInputMsgBox(self)

        # Layout
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.userList, 2)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.contentBox, 8)
        self.vbox.addWidget(self.inputMsgBox, 2)

        self.hbox.addLayout(self.vbox, 8)
        self.setLayout(self.hbox)

        self.show()

    def _sendMsg(self, msg):
        self.socket.send(msg.encode())

    def _recvMsg(self):
        while True:
            msg = self.socket.recv(1024).decode()
            self.parseMsg(msg)

    def _send_action(self, action, **param):
        jsonmsg = {'action': action,
                   'param': param}
        self._sendMsg(json.dumps(jsonmsg))

    def parseMsg(self, msg):
        json_msg = json.loads(msg)
        action = json_msg['action']
        param = json_msg['param']

        if action == 'login':
            self.login_msg(param['username'])
            self.update_userlist(param['userlist'])
        elif action == 'logout':
            self.logout_msg(param['username'])
            self.update_userlist(param['userlist'])

    def login(self):
        self.username = QInputDialog().getText(
            self, 'Login', 'Enter your username')[0]
        self._send_action('login', username=self.username)

    def logout(self):
        self._send_action('logout')

    def login_msg(self, username):
        html = '''
        <strong><font color=green>%s</font> logined!<br/></strong>
        ''' % username
        self.contentBox.insertHtml(html)

    def logout_msg(self, username):
        html = '''
        <strong><font color=red>%s</font> logout!<br/></strong>
        ''' % username
        self.contentBox.insertHtml(html)

    def update_userlist(self, userlist):
        self.userList.clear()
        for u in userlist:
            self.userList.addItem(u)

    def connect(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        _thread.start_new_thread(self._recvMsg, ())

    def sendMsg(self, msg):
        self._send_action('send_to_all', msg=msg)

    def closeEvent(self, e):
        self.logout()
        _thread.exit()
        self.socket.close()
