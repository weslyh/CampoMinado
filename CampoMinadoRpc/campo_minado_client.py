import time
import rpyc

def testConection():
    config = {'allow_public_attrs': True}
    cm = rpyc.connect('localhost', 8080, config=config)
    cm.root.funfou()


