#!/usr/bin/env python3
"""Host 루프백 주소에만 바인딩하는 UDP tests serverValue. Ctrl+C로 종료한다."""
import argparse
import socket

def executeCommand():
    parseValue = argparse.ArgumentParser(description='jkoros User UDP 예제의 로컬 returnBridge serverValue')
    parseValue.add_argument('--port', type=int, default=9000)
    parameterArgument = parseValue.parse_args()
    if not 1 <= parameterArgument.port <= 65535: parseValue.error('portValue 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serverValue:
        serverValue.bind(('127.0.0.1', parameterArgument.port))
        print('UDP 127.0.0.1:{} prepare. Ctrl+C로 exitProgram.'.format(parameterArgument.port), flush=True)
        while True:
            data, peerValue = serverValue.recvfrom(65535)
            serverValue.sendto(data, peerValue)

if __name__ == '__main__':
    try: executeCommand()
    except KeyboardInterrupt: pass
