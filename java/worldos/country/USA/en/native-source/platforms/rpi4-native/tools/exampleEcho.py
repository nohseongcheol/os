#!/usr/bin/env python3
"""English 네트워크 예제용 Host TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class EchoServers:
    def __init__(selfValue,tcpPort=0,udpPort=0):
        selfValue.hasReceived=[];selfValue.threads=[]
        hasReceived=selfValue.hasReceived
        class handleConnectionRequest(socketserver.BaseRequestHandler):
            def handle(selfValue):
                selfValue.request.settimeout(5);data=bytearray()
                while b'\n' not in data and len(data)<=512:
                    fragmentValue=selfValue.request.recv(512)
                    if not fragmentValue:return
                    data.extend(fragmentValue)
                hasReceived.append(('tcp',bytes(data)));selfValue.request.sendall(data)
        class datagramHandleRequest(socketserver.BaseRequestHandler):
            def handle(selfValue):
                data,socketValue=selfValue.request;hasReceived.append(('udp',data));socketValue.sendto(data,selfValue.client_address)
        selfValue.connectionControl=socketserver.ThreadingTCPServer(('127.0.0.1',tcpPort),handleConnectionRequest)
        try:selfValue.datagramControl=socketserver.ThreadingUDPServer(('127.0.0.1',udpPort),datagramHandleRequest)
        except Exception:selfValue.connectionControl.server_close();raise
        selfValue.connectionControl.daemon_threads=selfValue.datagramControl.daemon_threads=True
        selfValue.tcpPort=selfValue.connectionControl.server_address[1];selfValue.udpPort=selfValue.datagramControl.server_address[1]

    def __enter__(selfValue):
        for serverValue in (selfValue.connectionControl,selfValue.datagramControl):
            worker=threading.Thread(target=serverValue.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            worker.start();selfValue.threads.append(worker)
        return selfValue

    def __exit__(selfValue,*argumentArray):
        for serverValue in (selfValue.connectionControl,selfValue.datagramControl):serverValue.shutdown();serverValue.server_close()
        for worker in selfValue.threads:worker.join(timeout=1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tcp-port',type=int,default=9000);parser.add_argument('--udp-port',type=int,default=9001)
    argumentArray=parser.parse_args()
    with EchoServers(argumentArray.tcp_port,argumentArray.udp_port) as echoServerEntry:
        print('Host TCP {}, UDP {} prepare. 게스트 address: 10.0.2.2. exitProgram: Ctrl+C'.format(echoServerEntry.tcpPort,echoServerEntry.udpPort),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
