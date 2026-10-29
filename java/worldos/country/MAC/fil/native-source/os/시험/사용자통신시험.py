#!/usr/bin/env python3
"""totoo_data ring 3 ELF/host UDP 왕복/magprotekta_VALUE error/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

posisyon = Path(__file__).resolve().parents[1]


class virtual_machine:
    def __init__(self, path, 종류='elf', Network_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Directory_VALUE = Path(self.임시.name)
        self.LOG_hanay = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_path = Directory_VALUE / 'serial.sock', Directory_VALUE / 'monitor.sock'
        utos = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_path) + ',server,nowait']
        utos += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Network_VALUE else ['-net', 'none']
        utos += ['-kernel', str(path)] if 종류 == 'elf' else ['-cdrom', str(path), '-boot', 'd']
        if 저장매체 is not None:
            utos += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Proseso_VALUE = subprocess.Popen(utos, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_path.exists()):
                if self.Proseso_VALUE.poll() is not None:
                    raise AssertionError(self.Proseso_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU run TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_path))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.maghintay_katayuan('jkoros> ')
        except BaseException:
            self.isara()
            raise

    def maghintay_katayuan(self, 문구, run=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_hanay[run:]:
                return self.LOG_hanay[run:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_hanay.extend(data)
            if self.Proseso_VALUE.poll() is not None: break
        raise AssertionError('maghintay_VALUE pagpalya_VALUE: ' + 문구 + '\n' + self.LOG_hanay.decode('utf-8', 'replace'))

    def utos(self, string_VALUE, 기대):
        run = len(self.LOG_hanay)
        self.직렬.sendall((string_VALUE + '\n').encode())
        sukat = self.maghintay_katayuan('jkoros> ', run)
        for 문구 in 기대:
            assert 문구 in sukat, (string_VALUE, 문구, sukat)
        assert 'PANIC' not in sukat, sukat
        return sukat

    def isara(self):
        self.직렬.close()
        self.monitor_VALUE.close()
        if self.Proseso_VALUE.poll() is None:
            self.Proseso_VALUE.terminate()
            try: self.Proseso_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proseso_VALUE.kill()
                self.Proseso_VALUE.wait()
        self.Proseso_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(Directory_VALUE):
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
    항목들 = ['hello=' + str(posisyon / 'build/apps/hello.elf')]
    for pangalan, Nilalaman_VALUE in 사례들.items():
        pinagmulan = Directory_VALUE / (pangalan + '.s')
        pinagmulan.write_text('.code32\n.text\n.globl _start\n_start:\n' + Nilalaman_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Directory_VALUE / (pangalan + '.o')), str(pinagmulan)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posisyon.parent / 'compiler/gumagamit_Link_Layout.ld'),
                        '-o', str(Directory_VALUE / (pangalan + '.elf')), str(Directory_VALUE / (pangalan + '.o'))], check=True)
        항목들.append(pangalan + '=' + str(Directory_VALUE / (pangalan + '.elf')))
    정상 = bytearray((posisyon / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    hindi_tama_sukat = bytearray(정상); hindi_tama_sukat[0] = 0; 변형들['badelf'] = hindi_tama_sukat
    hindi_tama_sukat = bytearray(정상); struct.pack_into('<I', hindi_tama_sukat, 24, 0x00100000); 변형들['badentry'] = hindi_tama_sukat
    hindi_tama_sukat = bytearray(정상); struct.pack_into('<I', hindi_tama_sukat, 28, 0x7fffffff); 변형들['badtable'] = hindi_tama_sukat
    hindi_tama_sukat = bytearray(정상); LOOKUP_talahanayan = struct.unpack_from('<I', hindi_tama_sukat, 28)[0]
    struct.pack_into('<I', hindi_tama_sukat, LOOKUP_talahanayan + 20, 0x7fffffff); 변형들['badsize'] = hindi_tama_sukat
    for pangalan, data in 변형들.items():
        file = Directory_VALUE / (pangalan + '.elf'); file.write_bytes(data)
        항목들.append(pangalan + '=' + str(file))
    subprocess.run([sys.executable, str(posisyon / 'Mga_Tool/묶기.py'), '-o', str(Directory_VALUE / 'apps.bin')] + 항목들, check=True)
    pinagmulan = Directory_VALUE / 'apps.s'
    pinagmulan.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Directory_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Directory_VALUE / 'apps.o'), str(pinagmulan)], check=True)
    kernel_VALUE = Directory_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posisyon / '부팅/Link_Layout.ld'), '-o', str(kernel_VALUE),
                    str(posisyon / 'build/boot.o'), str(posisyon / 'build/java.o'), str(posisyon / 'build/user.o'), str(Directory_VALUE / 'apps.o')], check=True)
    return kernel_VALUE


def Mag_execute_utos():
    sukat = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_item = []
    Paglabas_app = threading.Event()
    def 되보내기():
        while not Paglabas_app.is_set():
            try: data, peer_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_item.append(data)
            if data != b'drop-me': server_VALUE.sendto(data, peer_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            machine = virtual_machine(posisyon / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                machine.utos('apps', ['hello', 'udp', 'netcheck', 'stress'])
                machine.utos('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                machine.utos('run missing', ['Exit: -2'])
                machine.utos('net', ['NET RTL8139'])
                machine.utos('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Nilalaman_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    machine.utos('run udp 10.0.2.2 {} {}'.format(port_VALUE, Nilalaman_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Nilalaman_VALUE.encode() in RECEIVED_item, 'host 서버에서 자료를 받지 못함'
                machine.utos('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                machine.utos('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                machine.utos('run hello recovered', ['arg: recovered', 'Exit: 0'])
                sukat[종류] = machine.LOG_hanay.decode('utf-8', 'replace')
                print('PASS: {} gumagamit ELF/ring 3/인수/UDP host 왕복/TIME_VALUE 초과/shell 복귀'.format(종류), flush=True)
            finally:
                try: machine.utos('net', [])
                except Exception: pass
                (posisyon / 'build/사용자통신-last.log').write_bytes(machine.LOG_hanay)
                machine.isara()
        machine = virtual_machine(posisyon / 'build/kernel.elf', Network_VALUE=False)
        try:
            machine.utos('net', ['NET unavailable'])
            machine.utos('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            machine.utos('run hello', ['USER MODE ring 3', 'Exit: 0'])
            sukat['no_nic'] = machine.LOG_hanay.decode()
        finally: machine.isara()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            machine = virtual_machine(보호커널(Path(임시)), Network_VALUE=False)
            try:
                for pangalan, katayuan_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    machine.utos('run ' + pangalan, ['Exit: ' + str(katayuan_VALUE)])
                    machine.utos('run hello', ['USER MODE ring 3', 'Exit: 0'])
                sukat['protection'] = machine.LOG_hanay.decode()
                print('PASS: gumagamit Memory_data/포트 격리, 잘못된 pointer/ELF, CPU pagbubukod, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (posisyon / 'build/보호시험-last.log').write_bytes(machine.LOG_hanay)
                machine.isara()
    finally:
        Paglabas_app.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    sukat['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in RECEIVED_item]
    (posisyon / 'build/사용자통신시험.json').write_text(json.dumps(sukat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Mag_execute_utos()
