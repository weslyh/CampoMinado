from random import randint

import rpyc
from rpyc.utils.server import ThreadedServer

class CampoMinadoRpyc(rpyc.Service):

    def exposed_funfou(self):
        print("test")

def server():
    thread = ThreadedServer(CampoMinadoRpyc, port=8080)
    thread.start()