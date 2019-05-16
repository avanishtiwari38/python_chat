# !/usr/bin/env python
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import pickle
import socket
import ConfigParser
configs = ConfigParser.ConfigParser()
configs.read('socket_config.cfg')

random_generator = Random.new().read
key = RSA.generate(1024, random_generator) #generate pub and priv key

publickey = key.publickey() # pub key export for exchange
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = configs.get('Client','HOST')
port = int(configs.get('Client','PORT'))
sock.connect((host,port))

# this should loop around until a delimeter is read
# or something similar
rcstring = sock.recv(2048)

# this object is of type RSAobj_c, which only has public key
# encryption is possible, but not decryption
publickey = pickle.loads(rcstring)

while True:
    # read data from meassage file
    message_file = open(configs.get('Client','message_file'), 'r')
    for messages in message_file:
        secretText = publickey.encrypt(messages, 32)
        sock.sendall(pickle.dumps(secretText))
        while True:
            print("response: ", sock.recv(1024))
