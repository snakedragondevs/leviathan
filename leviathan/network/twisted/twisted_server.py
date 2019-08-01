from __future__ import print_function
import threading
import time

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from leviathan.network.twisted.protocol.unconnected_ping import UnconnectedPing
from leviathan.network.twisted.protocol.unconnected_pong import UnconnectedPong


class HeartbeatSender(DatagramProtocol):

    def __init__(self, name, host, port):
        self.name = name
        self.loopObj = None
        self.host = host
        self.port = port

    def startProtocol(self):
        self.loopObj = LoopingCall(self.sendHeartBeat)
        self.loopObj.start(2, now=False)

    def stopProtocol(self):
        print("Called after all transport is teared down")
        pass

    def datagramReceived(self, data, address):
        print("received %r from %s:%d" % (data, address[0], address[1]))

    def sendHeartBeat(self):
        self.transport.write(self.name.encode(), (self.host, self.port))


class HeartbeatReceiver(DatagramProtocol):

    def __init__(self):
        pass

    def startProtocol(self):
        pass

    def stopProtocol(self):
        print("Called after all transport is teared down")

    def datagramReceived(self, data, address):
        now = time.localtime(time.time())
        timeStr = str(time.strftime("%y/%m/%d %H:%M:%S", now))
        print("%s received %r from %s:%d at %s" % ("receiver", data, address[0], address[1], timeStr))


class TwistedServer:

    def __init__(self):
        # heart_beat_sender_obj = HeartbeatSender("sender", "0.0.0.0", 19136)
        reactor.listenMulticast(19136, HeartbeatReceiver(), listenMultiple=True)
        # reactor.listenMulticast(19136, heart_beat_sender_obj, listenMultiple=True)
        reactor.run()
