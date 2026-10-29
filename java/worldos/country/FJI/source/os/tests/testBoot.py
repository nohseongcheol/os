#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 serialValue/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

position = Path(__file__).resolve().parents[1]


def await(Checks, description, limitValue=15):
    ending = time.monotonic() + limitValue
    while time.monotonic() < ending:
        result = Checks()
        if result:
            return result
        time.sleep(0.05)
    raise AssertionError('timeValue 초과: ' + description)


def tests(kindValue):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as temporaryValue:
        temporaryValue = Path(temporaryValue)
        serialPath = temporaryValue / 'serial.sock'
        monitorPath = temporaryValue / 'monitor.sock'
        command = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(serialPath) + ',server,nowait',
                '-monitor', 'unix:' + str(monitorPath) + ',server,nowait']
        command += ['-kernel', str(position / 'build/kernel.elf')] if kindValue == 'elf' else [
            '-cdrom', str(position / 'build/kernel.iso'), '-boot', 'd']
        # serialValue 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        command += ['-S']
        processValue = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        serialValue = socket.socket(socket.AF_UNIX)
        monitorValue = socket.socket(socket.AF_UNIX)
        logRecord = bytearray()
        try:
            def prepareSocket():
                if processValue.poll() is not None:
                    raise AssertionError(processValue.stderr.read().decode('utf-8', 'replace'))
                return serialPath.exists() and monitorPath.exists()
            await(prepareSocket, 'QEMU socketValue')
            serialValue.connect(str(serialPath))
            monitorValue.connect(str(monitorPath))
            serialValue.setblocking(False)
            monitorValue.sendall(b'cont\n')

            def headers(stringValue, run=0):
                read, _, _ = select.select([serialValue], [], [], 0.1)
                if read:
                    data = serialValue.recv(65536)
                    if not data:
                        raise AssertionError('serialValue connect exitProgram')
                    logRecord.extend(data)
                if processValue.poll() is not None:
                    raise AssertionError('QEMU 비정상 exitProgram: ' + str(processValue.returncode))
                return stringValue.encode('utf-8') in logRecord[run:]

            def testCommands(inputValue, expectation):
                run = len(logRecord)
                serialValue.sendall(inputValue.encode('ascii'))
                await(lambda: headers(expectation, run), expectation)
                await(lambda: headers('jkoros> ', run), 'command afterState 프롬프트')

            await(lambda: headers('READY'), kindValue + ' machine_boot')
            assert b'JAVA SELFTEST PASS' in logRecord
            assert 'Java 기계어 kernelValue run'.encode() in logRecord
            testCommands('info\r\n', 'embedded subset JVM / polling kernel')
            testCommands('help\n', 'free N | echo TEXT')
            testCommands('mem\n', ' / 8 (각 4096바이트)')
            testCommands('echo natix\bve\n', 'native\r\n')
            for index in range(8):
                testCommands('alloc\n', 'sectionValue index: ' + str(index))
            testCommands('alloc\n', 'sectionValue index: -1')
            testCommands('free 3\n', '반환됨')
            testCommands('free 3\n', '할당되지 않은 sectionValue')
            testCommands('free 99\n', '사용법: free 0..7')
            testCommands('alloc\n', 'sectionValue index: 3')
            testCommands('free 0\n', '반환됨')
            testCommands('test\n', 'JAVA SELFTEST PASS')
            testCommands('unknown\n', '알 number 없는 명령입니다')
            testCommands('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            run = len(logRecord)
            for keyValue in ('i', 'n', 'f', 'o', 'ret'):
                monitorValue.sendall(('sendkey ' + keyValue + ' 30\n').encode())
                time.sleep(0.09)
            await(lambda: headers('embedded subset JVM / polling kernel', run), 'PS/2 info inputValue')
            testCommands('echo ' + 'a' * 150 + '\n', 'a' * 123)
            serialValue.sendall(b'halt\n')
            await(lambda: headers('HALTED'), 'haltExecution command')
            assert b'PANIC' not in logRecord and b'SELFTEST FAIL' not in logRecord
            print('PASS: {} machine_boot, Java Native tests, serialValue command, PS/2 inputValue, allocateStorage/returnResult, haltExecution'.format(kindValue))
            return logRecord.decode('utf-8', 'replace')
        finally:
            serialValue.close()
            monitorValue.close()
            processValue.terminate()
            try:
                processValue.wait(timeout=3)
            except subprocess.TimeoutExpired:
                processValue.kill()
                processValue.wait()


if __name__ == '__main__':
    result = {kindValue: tests(kindValue) for kindValue in ('elf', 'iso')}
    (position / 'build/testBoot.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
