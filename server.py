import socket
from user import UserThread


class GeeChatServer(object):
    def __init__(self, host='127.0.0.1', port=54188):
        self.host = host
        self.port = port
        self.userlist = []

    def send_to_all(self, msg):
        print("send to all: %s" % msg)
        for u in self.userlist:
            u.send(msg)

    def get_userlist(self):
        userlist = []
        for u in self.userlist:
            print(u)
            userlist.append(u.username)
        return userlist

    def user_logout(self, user):
        if user in self.userlist:
            self.userlist.remove(user)

    def launchServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print('server started at %s:%s' % (self.host, self.port))
        while True:
            print('waiting for a new connection...')
            conn, addr = self.socket.accept()

            u = UserThread(conn, addr, self)
            u.start()
            self.userlist.append(u)


if __name__ == '__main__':
    gcs = GeeChatServer('127.0.0.1', 54188)
    gcs.launchServer()
