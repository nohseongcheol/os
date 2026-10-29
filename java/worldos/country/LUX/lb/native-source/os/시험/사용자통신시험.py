#!/usr/bin/env python3
"""aktuell_Daten ring 3 ELF/Host UDP 왕복/schützen_VALUE Feeler/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

positionéieren = Path(__file__).resolve().parents[1]


class virtuell_Computer:
    def __init__(self, Wee, 종류='elf', Reseau_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Verzeechnes_VALUE = Path(self.임시.name)
        self.LOG_Rei = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.Schierm_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, Schierm_Wee = Verzeechnes_VALUE / 'serial.sock', Verzeechnes_VALUE / 'monitor.sock'
        Befeel = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(Schierm_Wee) + ',server,nowait']
        Befeel += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Reseau_VALUE else ['-net', 'none']
        Befeel += ['-kernel', str(Wee)] if 종류 == 'elf' else ['-cdrom', str(Wee), '-boot', 'd']
        if 저장매체 is not None:
            Befeel += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Prozess_VALUE = subprocess.Popen(Befeel, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and Schierm_Wee.exists()):
                if self.Prozess_VALUE.poll() is not None:
                    raise AssertionError(self.Prozess_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Laf TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.Schierm_VALUE.connect(str(Schierm_Wee))
            self.직렬.setblocking(False)
            self.Schierm_VALUE.sendall(b'cont\n')
            self.Waart_Status('jkoros> ')
        except BaseException:
            self.Clôture()
            raise

    def Waart_Status(self, 문구, Laf=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_Rei[Laf:]:
                return self.LOG_Rei[Laf:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                Daten = self.직렬.recv(65536)
                if not Daten: break
                self.LOG_Rei.extend(Daten)
            if self.Prozess_VALUE.poll() is not None: break
        raise AssertionError('Waart_VALUE Feeler_VALUE: ' + 문구 + '\n' + self.LOG_Rei.decode('utf-8', 'replace'))

    def Befeel(self, Zeechefolleg_VALUE, 기대):
        Laf = len(self.LOG_Rei)
        self.직렬.sendall((Zeechefolleg_VALUE + '\n').encode())
        Mooss = self.Waart_Status('jkoros> ', Laf)
        for 문구 in 기대:
            assert 문구 in Mooss, (Zeechefolleg_VALUE, 문구, Mooss)
        assert 'PANIC' not in Mooss, Mooss
        return Mooss

    def Clôture(self):
        self.직렬.close()
        self.Schierm_VALUE.close()
        if self.Prozess_VALUE.poll() is None:
            self.Prozess_VALUE.terminate()
            try: self.Prozess_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Prozess_VALUE.kill()
                self.Prozess_VALUE.wait()
        self.Prozess_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(Verzeechnes_VALUE):
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
    항목들 = ['hello=' + str(positionéieren / 'build/apps/hello.elf')]
    for Numm, Inhalt_VALUE in 사례들.items():
        Quell = Verzeechnes_VALUE / (Numm + '.s')
        Quell.write_text('.code32\n.text\n.globl _start\n_start:\n' + Inhalt_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Verzeechnes_VALUE / (Numm + '.o')), str(Quell)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(positionéieren.parent / 'compiler/Benotzer_Link_Layout.ld'),
                        '-o', str(Verzeechnes_VALUE / (Numm + '.elf')), str(Verzeechnes_VALUE / (Numm + '.o'))], check=True)
        항목들.append(Numm + '=' + str(Verzeechnes_VALUE / (Numm + '.elf')))
    정상 = bytearray((positionéieren / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ongëlteg_Mooss = bytearray(정상); ongëlteg_Mooss[0] = 0; 변형들['badelf'] = ongëlteg_Mooss
    ongëlteg_Mooss = bytearray(정상); struct.pack_into('<I', ongëlteg_Mooss, 24, 0x00100000); 변형들['badentry'] = ongëlteg_Mooss
    ongëlteg_Mooss = bytearray(정상); struct.pack_into('<I', ongëlteg_Mooss, 28, 0x7fffffff); 변형들['badtable'] = ongëlteg_Mooss
    ongëlteg_Mooss = bytearray(정상); LOOKUP_Tabell = struct.unpack_from('<I', ongëlteg_Mooss, 28)[0]
    struct.pack_into('<I', ongëlteg_Mooss, LOOKUP_Tabell + 20, 0x7fffffff); 변형들['badsize'] = ongëlteg_Mooss
    for Numm, Daten in 변형들.items():
        Fichier = Verzeechnes_VALUE / (Numm + '.elf'); Fichier.write_bytes(Daten)
        항목들.append(Numm + '=' + str(Fichier))
    subprocess.run([sys.executable, str(positionéieren / 'Tools/묶기.py'), '-o', str(Verzeechnes_VALUE / 'apps.bin')] + 항목들, check=True)
    Quell = Verzeechnes_VALUE / 'apps.s'
    Quell.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Verzeechnes_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Verzeechnes_VALUE / 'apps.o'), str(Quell)], check=True)
    Kernel_VALUE = Verzeechnes_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(positionéieren / '부팅/Link_Layout.ld'), '-o', str(Kernel_VALUE),
                    str(positionéieren / 'build/boot.o'), str(positionéieren / 'build/java.o'), str(positionéieren / 'build/user.o'), str(Verzeechnes_VALUE / 'apps.o')], check=True)
    return Kernel_VALUE


def ausféieren_Befeel():
    Mooss = {}
    Server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Server_VALUE.bind(('127.0.0.1', 0))
    Server_VALUE.settimeout(0.1)
    Port_VALUE = Server_VALUE.getsockname()[1]
    RECEIVED_Element = []
    Schluss_App = threading.Event()
    def 되보내기():
        while not Schluss_App.is_set():
            try: Daten, Peer_VALUE = Server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_Element.append(Daten)
            if Daten != b'drop-me': Server_VALUE.sendto(Daten, Peer_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            Computer = virtuell_Computer(positionéieren / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                Computer.Befeel('apps', ['hello', 'udp', 'netcheck', 'stress'])
                Computer.Befeel('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                Computer.Befeel('run missing', ['Exit: -2'])
                Computer.Befeel('net', ['NET RTL8139'])
                Computer.Befeel('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Inhalt_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    Computer.Befeel('run udp 10.0.2.2 {} {}'.format(Port_VALUE, Inhalt_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Inhalt_VALUE.encode() in RECEIVED_Element, 'Host 서버에서 자료를 받지 못함'
                Computer.Befeel('run stress {}'.format(Port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                Computer.Befeel('run udp 10.0.2.2 {} drop-me'.format(Port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                Computer.Befeel('run hello recovered', ['arg: recovered', 'Exit: 0'])
                Mooss[종류] = Computer.LOG_Rei.decode('utf-8', 'replace')
                print('PASS: {} Benotzer ELF/ring 3/인수/UDP Host 왕복/TIME_VALUE 초과/Shell 복귀'.format(종류), flush=True)
            finally:
                try: Computer.Befeel('net', [])
                except Exception: pass
                (positionéieren / 'build/사용자통신-last.log').write_bytes(Computer.LOG_Rei)
                Computer.Clôture()
        Computer = virtuell_Computer(positionéieren / 'build/kernel.elf', Reseau_VALUE=False)
        try:
            Computer.Befeel('net', ['NET unavailable'])
            Computer.Befeel('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            Computer.Befeel('run hello', ['USER MODE ring 3', 'Exit: 0'])
            Mooss['no_nic'] = Computer.LOG_Rei.decode()
        finally: Computer.Clôture()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            Computer = virtuell_Computer(보호커널(Path(임시)), Reseau_VALUE=False)
            try:
                for Numm, Status_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    Computer.Befeel('run ' + Numm, ['Exit: ' + str(Status_VALUE)])
                    Computer.Befeel('run hello', ['USER MODE ring 3', 'Exit: 0'])
                Mooss['protection'] = Computer.LOG_Rei.decode()
                print('PASS: Benotzer Späicher_Daten/포트 격리, 잘못된 Uweiser/ELF, CPU 예외, 무한 Iteratioun_VALUE 제한', flush=True)
            finally:
                (positionéieren / 'build/보호시험-last.log').write_bytes(Computer.LOG_Rei)
                Computer.Clôture()
    finally:
        Schluss_App.set()
        일꾼.join(timeout=2)
        Server_VALUE.close()
    Mooss['host_udp_received'] = [{'length': len(Daten), 'sha256': hashlib.sha256(Daten).hexdigest()} for Daten in RECEIVED_Element]
    (positionéieren / 'build/사용자통신시험.json').write_text(json.dumps(Mooss, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ausféieren_Befeel()
