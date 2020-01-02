import threading
import json


class UserThread(threading.Thread):
    def __init__(self, conn, addr, server):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.username = addr[0]
        self.server = server

    def _sendMsg(self, msg):
        print("send: %s to %s" % (msg, self.username))
        self.conn.send(msg.encode())

    def send(self, msg):
        self._sendMsg(msg)

    def _recvMsg(self):
        with self.conn:
            while True:
                msg = self.conn.recv(1024).decode()
                if msg == '':
                    print('Disconnected!')
                    self.logout()
                    break
                print("recv: %s from %s" % (msg, self.username))
                self.parseMsg(msg)

    def _send_action(self, action, **param):
        jsonmsg = {'action': action,
                   'param': param}
        self.server.send_to_all(json.dumps(jsonmsg))

    def login(self, username, **param):
        self.username = username
        self._send_action('login', username=self.username,
                          userlist=self.server.get_userlist())

    def logout(self):
        self.server.user_logout(self)
        self._send_action('logout', username=self.username,
                          userlist=self.server.get_userlist())

    def parseMsg(self, msg):
        json_msg = json.loads(msg)
        action = json_msg['action']
        param = json_msg['param']

        if action == 'login':
            self.login(**param)
        elif action == 'logout':
            self.logout()
        elif action == 'send_to_all':
            print('send')

    def run(self):
        self._recvMsg()
