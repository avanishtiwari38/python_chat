from threading import Thread
import Queue
import time
import logging
from Crypto import Random
import ast
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Util import randpool

import pickle
import socket
import ConfigParser
configs = ConfigParser.ConfigParser()
configs.read('socket_config.cfg')
configs.sections()

# generate the RSA key
blah = randpool.RandomPool()
RSAKey = RSA.generate(1024, blah.get_bytes)

RSAPubKey = RSAKey.publickey()

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)

BUFFER_SIZE = int(configs.get('Server','BUFFER_SIZE'))
commands_queue = Queue.PriorityQueue(BUFFER_SIZE)


class Command(object):
    def __init__(self, priority, data, conn):
        self.priority = priority
        self.data = data
        self.conn = conn

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)


class CommandsThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        Thread.__init__(self)
        self.target = target
        self.name = name

    def run(self):
        while True:
            try:
                if not commands_queue.empty():
                    command = commands_queue.get()
                    # get data from queue
                    logging.debug("Queueing data: " + command.data)
                    time.sleep(3)
                    logging.debug("Finshed queue: " + command.data)
                    command.conn.send("Data processing is done" + command.data)  # echo
            except socket.error as e:
                logging.debug("error while sending message after process")
            except Exception as e:
                logging.debug("General error while sending message")



# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    def __init__(self, conn, ip, port):
        Thread.__init__(self)
        self.conn, self.ip, self.port = conn, ip, port

    def run(self):
        while True:
            try:
                data = conn.recv(2048)
                encmessage = pickle.loads(data)
                data = RSAKey.decrypt(encmessage)
                if not commands_queue.full():
                    commands_queue.put(Command(2, data, self.conn))
                    # conn.send("Done: " + data)  # echo
            except EOFError as e:
                logging.exception("Exception raise %s" %e)
            except Exception as ex:
                logging.exception("General exception %s" %ex)




# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = str(configs.get('Server','TCP_IP'))
TCP_PORT = int(configs.get('Server','PORT'))


tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

c = CommandsThread(name='commands')
c.start()
threads.append(c)

while True:
    tcpServer.listen(int(configs.get('Server','MAX_CONNECTION')))
    print ("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip, port)) = tcpServer.accept()
    conn.send(pickle.dumps(RSAPubKey))

    newthread = ClientThread(conn, ip, port)
    newthread.start()
    threads.append(newthread)
