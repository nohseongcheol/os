#!/usr/bin/env python3
"""Host libc 없이 연결한 English C 프로그램을 actualData ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from testUserNetwork import VirtualMachine

position = Path(__file__).resolve().parents[1]

def executeCommand():
    result = {}
    serverValue = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverValue.bind(('127.0.0.1', 0))
    serverValue.settimeout(0.1)
    portNumber = serverValue.getsockname()[1]
    receivedData = []
    terminationState = threading.Event()
    def echoReply():
        while not terminationState.is_set():
            try:
                data, address = serverValue.recvfrom(4096)
            except socket.timeout:
                continue
            receivedData.append(data)
            serverValue.sendto(data, address)
    workerValue = threading.Thread(target=echoReply, daemon=True)
    workerValue.start()
    try:
        for kindValue in ('elf', 'iso'):
            machine = VirtualMachine(position / ('build/kernel.' + kindValue), kindValue)
            try:
                for iterationValue in range(2):
                    machine.command('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    machine.command('run posixudp ' + str(portNumber), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                run = len(machine.logRecord)
                machine.serialValue.sendall(b'run posixinput\n')
                machine.waitState('POSIX INPUT READY', run)
                machine.serialValue.sendall(b'abcdef')
                Output = machine.waitState('jkoros> ', run)
                assert 'POSIX INPUT PASS' in Output and 'Exit: 0' in Output, Output
                machine.command('javac Hello.java', ['Exit: 0'])
                machine.command('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                machine.command('run hello recovered', ['arg: recovered', 'Exit: 0'])
                result[kindValue] = machine.logRecord.decode('utf-8', 'replace')
                print('PASS:', kindValue, 'POSIX file/공유 position/삭제 수명/address protectValue/UDP/표준 inputValue/기존 Java', flush=True)
            finally:
                machine.close()
        assert b'posix-udp' in receivedData and b'truncate' in receivedData and b'' in receivedData
    finally:
        terminationState.set(); workerValue.join(timeout=2); serverValue.close()
    result['host_datagrams'] = [data.decode() for data in receivedData]
    (position / 'build/ContractTest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    executeCommand()
