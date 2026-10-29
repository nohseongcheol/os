#!/usr/bin/env python3
"""actualData ring 3 ELF/Host UDP 왕복/protectValue error/timeValue limitValue/잘못된 ELF를 검증한다."""
import json
import hashlib
from pathlib import Path
import select
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time

position = Path(__file__).resolve().parents[1]


class VirtualMachine:
    def __init__(self, path, kindValue='elf', networkValue=True, storageMedium=None):
        self.temporaryValue = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        directoryValue = Path(self.temporaryValue.name)
        self.logRecord = bytearray()
        self.serialValue = socket.socket(socket.AF_UNIX)
        self.monitorValue = socket.socket(socket.AF_UNIX)
        serialPath, monitorPath = directoryValue / 'serial.sock', directoryValue / 'monitor.sock'
        command = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(serialPath) + ',server,nowait',
                '-monitor', 'unix:' + str(monitorPath) + ',server,nowait']
        command += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if networkValue else ['-net', 'none']
        command += ['-kernel', str(path)] if kindValue == 'elf' else ['-cdrom', str(path), '-boot', 'd']
        if storageMedium is not None:
            command += ['-drive', 'file=' + str(storageMedium) + ',format=raw,if=ide,index=0']
        self.processValue = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            ending = time.monotonic() + 10
            while not (serialPath.exists() and monitorPath.exists()):
                if self.processValue.poll() is not None:
                    raise AssertionError(self.processValue.stderr.read().decode())
                if time.monotonic() > ending: raise AssertionError('QEMU run timeValue 초과')
                time.sleep(0.03)
            self.serialValue.connect(str(serialPath))
            self.monitorValue.connect(str(monitorPath))
            self.serialValue.setblocking(False)
            self.monitorValue.sendall(b'cont\n')
            self.waitState('jkoros> ')
        except BaseException:
            self.close()
            raise

    def waitState(self, phraseValue, run=0, limitValue=15):
        ending = time.monotonic() + limitValue
        while time.monotonic() < ending:
            if phraseValue.encode() in self.logRecord[run:]:
                return self.logRecord[run:].decode('utf-8', 'replace')
            read, _, _ = select.select([self.serialValue], [], [], 0.1)
            if read:
                data = self.serialValue.recv(65536)
                if not data: break
                self.logRecord.extend(data)
            if self.processValue.poll() is not None: break
        raise AssertionError('waitValue failureValue: ' + phraseValue + '\n' + self.logRecord.decode('utf-8', 'replace'))

    def command(self, stringValue, expectation):
        run = len(self.logRecord)
        self.serialValue.sendall((stringValue + '\n').encode())
        result = self.waitState('jkoros> ', run)
        for phraseValue in expectation:
            assert phraseValue in result, (stringValue, phraseValue, result)
        assert 'PANIC' not in result, result
        return result

    def close(self):
        self.serialValue.close()
        self.monitorValue.close()
        if self.processValue.poll() is None:
            self.processValue.terminate()
            try: self.processValue.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.processValue.kill()
                self.processValue.wait()
        self.processValue.communicate()
        self.temporaryValue.cleanup()


def protectedKernel(directoryValue):
    casesList = {
        'badmem': 'movl $7, 0x00100000',
        'badport': 'movw $0x3f8, %dx\noutb %al, %dx',
        'spin': '1: jmp 1b',
        'badptr': 'movl $1,%eax\nmovl $0x00100000,%ebx\nint $0x80\ncmpl $-14,%eax\njne fail\n'
                  'movl $999,%eax\nint $0x80\ncmpl $-38,%eax\njne fail\n'
                  'xorl %ebx,%ebx\nxorl %eax,%eax\nint $0x80\nfail: movl $1,%ebx\nxorl %eax,%eax\nint $0x80',
        'fault': 'ud2',
        'badfile': '''
            movl $20,%eax
            movl $0x00100000,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $20,%eax
            movl $name,%ebx
            movl $0x00100000,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $negative,%ecx
            xorl %edx,%edx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $empty,%ecx
            movl $1,%edx
            int $0x80
            cmpl $-22,%eax
            jne fail
            movl $20,%eax
            movl $empty,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-22,%eax
            jne fail
            xorl %eax,%eax
            xorl %ebx,%ebx
            int $0x80
        fail:
            xorl %eax,%eax
            movl $1,%ebx
            int $0x80
        .balign 4
        name: .long 1,88
        empty: .long 0
        negative: .long -1
        ''',
    }
    entriesList = ['hello=' + str(position / 'build/apps/hello.elf')]
    for name, contentValue in casesList.items():
        source = directoryValue / (name + '.s')
        source.write_text('.code32\n.text\n.globl _start\n_start:\n' + contentValue +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(directoryValue / (name + '.o')), str(source)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position.parent / 'compiler/userLinkLayout.ld'),
                        '-o', str(directoryValue / (name + '.elf')), str(directoryValue / (name + '.o'))], check=True)
        entriesList.append(name + '=' + str(directoryValue / (name + '.elf')))
    isNormal = bytearray((position / 'build/apps/hello.elf').read_bytes())
    variantsList = {}
    invalidResult = bytearray(isNormal); invalidResult[0] = 0; variantsList['badelf'] = invalidResult
    invalidResult = bytearray(isNormal); struct.pack_into('<I', invalidResult, 24, 0x00100000); variantsList['badentry'] = invalidResult
    invalidResult = bytearray(isNormal); struct.pack_into('<I', invalidResult, 28, 0x7fffffff); variantsList['badtable'] = invalidResult
    invalidResult = bytearray(isNormal); lookupTable = struct.unpack_from('<I', invalidResult, 28)[0]
    struct.pack_into('<I', invalidResult, lookupTable + 20, 0x7fffffff); variantsList['badsize'] = invalidResult
    for name, data in variantsList.items():
        file = directoryValue / (name + '.elf'); file.write_bytes(data)
        entriesList.append(name + '=' + str(file))
    subprocess.run([sys.executable, str(position / 'tools/bindEndpoint.py'), '-o', str(directoryValue / 'apps.bin')] + entriesList, check=True)
    source = directoryValue / 'apps.s'
    source.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(directoryValue / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(directoryValue / 'apps.o'), str(source)], check=True)
    kernelValue = directoryValue / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position / 'machine_boot/link_layout.ld'), '-o', str(kernelValue),
                    str(position / 'build/boot.o'), str(position / 'build/java.o'), str(position / 'build/user.o'), str(directoryValue / 'apps.o')], check=True)
    return kernelValue


def executeCommand():
    result = {}
    serverValue = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverValue.bind(('127.0.0.1', 0))
    serverValue.settimeout(0.1)
    portValue = serverValue.getsockname()[1]
    receivedItem = []
    exitProgram = threading.Event()
    def echoReply():
        while not exitProgram.is_set():
            try: data, peerValue = serverValue.recvfrom(4096)
            except socket.timeout: continue
            receivedItem.append(data)
            if data != b'drop-me': serverValue.sendto(data, peerValue)
    workerValue = threading.Thread(target=echoReply, daemon=True)
    workerValue.start()
    try:
        for kindValue in ('elf', 'iso'):
            machine = VirtualMachine(position / ('build/kernel.elf' if kindValue == 'elf' else 'build/kernel.iso'), kindValue)
            try:
                machine.command('apps', ['hello', 'udp', 'netcheck', 'stress'])
                machine.command('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                machine.command('run missing', ['Exit: -2'])
                machine.command('net', ['NET RTL8139'])
                machine.command('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for contentValue in ('hello-network', 'odd', 'even', 'repeat-123'):
                    machine.command('run udp 10.0.2.2 {} {}'.format(portValue, contentValue), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert contentValue.encode() in receivedItem, 'Host 서버에서 자료를 받지 못함'
                machine.command('run stress {}'.format(portValue), ['UDP STRESS PASS', 'Exit: 0'])
                machine.command('run udp 10.0.2.2 {} drop-me'.format(portValue), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                machine.command('run hello recovered', ['arg: recovered', 'Exit: 0'])
                result[kindValue] = machine.logRecord.decode('utf-8', 'replace')
                print('PASS: {} User ELF/ring 3/arguments/UDP Host 왕복/timeValue 초과/shell 복귀'.format(kindValue), flush=True)
            finally:
                try: machine.command('net', [])
                except Exception: pass
                (position / 'build/사용자통신-last.log').write_bytes(machine.logRecord)
                machine.close()
        machine = VirtualMachine(position / 'build/kernel.elf', networkValue=False)
        try:
            machine.command('net', ['NET unavailable'])
            machine.command('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            machine.command('run hello', ['USER MODE ring 3', 'Exit: 0'])
            result['no_nic'] = machine.logRecord.decode()
        finally: machine.close()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as temporaryValue:
            machine = VirtualMachine(protectedKernel(Path(temporaryValue)), networkValue=False)
            try:
                for name, stateValue in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    machine.command('run ' + name, ['Exit: ' + str(stateValue)])
                    machine.command('run hello', ['USER MODE ring 3', 'Exit: 0'])
                result['protection'] = machine.logRecord.decode()
                print('PASS: User memoryData/hardwarePort 격리, 잘못된 pointer/ELF, CPU exception, 무한 iterationValue limitValue', flush=True)
            finally:
                (position / 'build/ProtectionTest-last.log').write_bytes(machine.logRecord)
                machine.close()
    finally:
        exitProgram.set()
        workerValue.join(timeout=2)
        serverValue.close()
    result['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in receivedItem]
    (position / 'build/testUserNetwork.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    executeCommand()
