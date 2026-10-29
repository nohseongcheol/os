#!/usr/bin/env python3
"""attwali_data ring 3 ELF/host UDP 왕복/pproteġa_VALUE żball/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

pożizzjoni = Path(__file__).resolve().parents[1]


class virtwali_kompjuter:
    def __init__(self, mogħdija, 종류='elf', netwerk_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        direttorju_VALUE = Path(self.임시.name)
        self.LOG_RECORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.moniter_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, moniter_mogħdija = direttorju_VALUE / 'serial.sock', direttorju_VALUE / 'monitor.sock'
        kmand = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(moniter_mogħdija) + ',server,nowait']
        kmand += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if netwerk_VALUE else ['-net', 'none']
        kmand += ['-kernel', str(mogħdija)] if 종류 == 'elf' else ['-cdrom', str(mogħdija), '-boot', 'd']
        if 저장매체 is not None:
            kmand += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Proċess_VALUE = subprocess.Popen(kmand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and moniter_mogħdija.exists()):
                if self.Proċess_VALUE.poll() is not None:
                    raise AssertionError(self.Proċess_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU serje TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.moniter_VALUE.connect(str(moniter_mogħdija))
            self.직렬.setblocking(False)
            self.moniter_VALUE.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.agħlaq()
            raise

    def 기다림(self, 문구, serje=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_RECORD[serje:]:
                return self.LOG_RECORD[serje:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_RECORD.extend(data)
            if self.Proċess_VALUE.poll() is not None: break
        raise AssertionError('대기 żball_VALUE: ' + 문구 + '\n' + self.LOG_RECORD.decode('utf-8', 'replace'))

    def kmand(self, string_VALUE, 기대):
        serje = len(self.LOG_RECORD)
        self.직렬.sendall((string_VALUE + '\n').encode())
        miżura = self.기다림('jkoros> ', serje)
        for 문구 in 기대:
            assert 문구 in miżura, (string_VALUE, 문구, miżura)
        assert 'PANIC' not in miżura, miżura
        return miżura

    def agħlaq(self):
        self.직렬.close()
        self.moniter_VALUE.close()
        if self.Proċess_VALUE.poll() is None:
            self.Proċess_VALUE.terminate()
            try: self.Proċess_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proċess_VALUE.kill()
                self.Proċess_VALUE.wait()
        self.Proċess_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(direttorju_VALUE):
    사례들 = {
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
    항목들 = ['hello=' + str(pożizzjoni / 'build/apps/hello.elf')]
    for isem, Kontenut_VALUE in 사례들.items():
        sors = direttorju_VALUE / (isem + '.s')
        sors.write_text('.code32\n.text\n.globl _start\n_start:\n' + Kontenut_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(direttorju_VALUE / (isem + '.o')), str(sors)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pożizzjoni.parent / 'compiler/utent_Link_Tqassim.ld'),
                        '-o', str(direttorju_VALUE / (isem + '.elf')), str(direttorju_VALUE / (isem + '.o'))], check=True)
        항목들.append(isem + '=' + str(direttorju_VALUE / (isem + '.elf')))
    정상 = bytearray((pożizzjoni / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    invalidu_miżura = bytearray(정상); invalidu_miżura[0] = 0; 변형들['badelf'] = invalidu_miżura
    invalidu_miżura = bytearray(정상); struct.pack_into('<I', invalidu_miżura, 24, 0x00100000); 변형들['badentry'] = invalidu_miżura
    invalidu_miżura = bytearray(정상); struct.pack_into('<I', invalidu_miżura, 28, 0x7fffffff); 변형들['badtable'] = invalidu_miżura
    invalidu_miżura = bytearray(정상); LOOKUP_tabella = struct.unpack_from('<I', invalidu_miżura, 28)[0]
    struct.pack_into('<I', invalidu_miżura, LOOKUP_tabella + 20, 0x7fffffff); 변형들['badsize'] = invalidu_miżura
    for isem, data in 변형들.items():
        fajl = direttorju_VALUE / (isem + '.elf'); fajl.write_bytes(data)
        항목들.append(isem + '=' + str(fajl))
    subprocess.run([sys.executable, str(pożizzjoni / 'Għodod/묶기.py'), '-o', str(direttorju_VALUE / 'apps.bin')] + 항목들, check=True)
    sors = direttorju_VALUE / 'apps.s'
    sors.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(direttorju_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(direttorju_VALUE / 'apps.o'), str(sors)], check=True)
    kernel_VALUE = direttorju_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pożizzjoni / '부팅/Link_Tqassim.ld'), '-o', str(kernel_VALUE),
                    str(pożizzjoni / 'build/boot.o'), str(pożizzjoni / 'build/java.o'), str(pożizzjoni / 'build/user.o'), str(direttorju_VALUE / 'apps.o')], check=True)
    return kernel_VALUE


def eżegwixxa_kmand():
    miżura = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_element = []
    Ħruġ_programm = threading.Event()
    def 되보내기():
        while not Ħruġ_programm.is_set():
            try: data, peer_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_element.append(data)
            if data != b'drop-me': server_VALUE.sendto(data, peer_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            kompjuter = virtwali_kompjuter(pożizzjoni / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                kompjuter.kmand('apps', ['hello', 'udp', 'netcheck', 'stress'])
                kompjuter.kmand('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                kompjuter.kmand('run missing', ['Exit: -2'])
                kompjuter.kmand('net', ['NET RTL8139'])
                kompjuter.kmand('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Kontenut_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    kompjuter.kmand('run udp 10.0.2.2 {} {}'.format(port_VALUE, Kontenut_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Kontenut_VALUE.encode() in RECEIVED_element, 'host 서버에서 자료를 받지 못함'
                kompjuter.kmand('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                kompjuter.kmand('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                kompjuter.kmand('run hello recovered', ['arg: recovered', 'Exit: 0'])
                miżura[종류] = kompjuter.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS: {} utent ELF/ring 3/인수/UDP host 왕복/TIME_VALUE 초과/shell 복귀'.format(종류), flush=True)
            finally:
                try: kompjuter.kmand('net', [])
                except Exception: pass
                (pożizzjoni / 'build/사용자통신-last.log').write_bytes(kompjuter.LOG_RECORD)
                kompjuter.agħlaq()
        kompjuter = virtwali_kompjuter(pożizzjoni / 'build/kernel.elf', netwerk_VALUE=False)
        try:
            kompjuter.kmand('net', ['NET unavailable'])
            kompjuter.kmand('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            kompjuter.kmand('run hello', ['USER MODE ring 3', 'Exit: 0'])
            miżura['no_nic'] = kompjuter.LOG_RECORD.decode()
        finally: kompjuter.agħlaq()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            kompjuter = virtwali_kompjuter(보호커널(Path(임시)), netwerk_VALUE=False)
            try:
                for isem, stat_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    kompjuter.kmand('run ' + isem, ['Exit: ' + str(stat_VALUE)])
                    kompjuter.kmand('run hello', ['USER MODE ring 3', 'Exit: 0'])
                miżura['protection'] = kompjuter.LOG_RECORD.decode()
                print('PASS: utent Memorja_data/포트 격리, 잘못된 pointer/ELF, CPU 예외, 무한 iterazzjoni_VALUE 제한', flush=True)
            finally:
                (pożizzjoni / 'build/보호시험-last.log').write_bytes(kompjuter.LOG_RECORD)
                kompjuter.agħlaq()
    finally:
        Ħruġ_programm.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    miżura['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in RECEIVED_element]
    (pożizzjoni / 'build/사용자통신시험.json').write_text(json.dumps(miżura, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    eżegwixxa_kmand()
