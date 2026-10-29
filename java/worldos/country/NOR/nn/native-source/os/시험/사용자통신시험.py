#!/usr/bin/env python3
"""faktisk_data ring 3 ELF/vert UDP 왕복/verne_VALUE FEIL/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

Posisjon = Path(__file__).resolve().parents[1]


class virtuell_maskin:
    def __init__(self, STIGE, 종류='elf', Nettverk_VALUE=True, Lagring_medium=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        katalog_VALUE = Path(self.임시.name)
        self.LOG_rad = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.skjerm_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, skjerm_bane = katalog_VALUE / 'serial.sock', katalog_VALUE / 'monitor.sock'
        Kommando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(skjerm_bane) + ',server,nowait']
        Kommando += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Nettverk_VALUE else ['-net', 'none']
        Kommando += ['-kernel', str(STIGE)] if 종류 == 'elf' else ['-cdrom', str(STIGE), '-boot', 'd']
        if Lagring_medium is not None:
            Kommando += ['-drive', 'file=' + str(Lagring_medium) + ',format=raw,if=ide,index=0']
        self.Prosess_VALUE = subprocess.Popen(Kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and skjerm_bane.exists()):
                if self.Prosess_VALUE.poll() is not None:
                    raise AssertionError(self.Prosess_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Køyr_2 TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.skjerm_VALUE.connect(str(skjerm_bane))
            self.직렬.setblocking(False)
            self.skjerm_VALUE.sendall(b'cont\n')
            self.vent_status('jkoros> ')
        except BaseException:
            self.Lukk()
            raise

    def vent_status(self, 문구, Køyr_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_rad[Køyr_2:]:
                return self.LOG_rad[Køyr_2:].decode('utf-8', 'replace')
            Les, _, _ = select.select([self.직렬], [], [], 0.1)
            if Les:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_rad.extend(data)
            if self.Prosess_VALUE.poll() is not None: break
        raise AssertionError('vent_VALUE feil_VALUE: ' + 문구 + '\n' + self.LOG_rad.decode('utf-8', 'replace'))

    def Kommando(self, streng_VALUE, 기대):
        Køyr_2 = len(self.LOG_rad)
        self.직렬.sendall((streng_VALUE + '\n').encode())
        forretningsmål = self.vent_status('jkoros> ', Køyr_2)
        for 문구 in 기대:
            assert 문구 in forretningsmål, (streng_VALUE, 문구, forretningsmål)
        assert 'PANIC' not in forretningsmål, forretningsmål
        return forretningsmål

    def Lukk(self):
        self.직렬.close()
        self.skjerm_VALUE.close()
        if self.Prosess_VALUE.poll() is None:
            self.Prosess_VALUE.terminate()
            try: self.Prosess_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Prosess_VALUE.kill()
                self.Prosess_VALUE.wait()
        self.Prosess_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(katalog_VALUE):
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
    항목들 = ['hello=' + str(Posisjon / 'build/apps/hello.elf')]
    for Namn, Innhald_VALUE in 사례들.items():
        KJELDE = katalog_VALUE / (Namn + '.s')
        KJELDE.write_text('.code32\n.text\n.globl _start\n_start:\n' + Innhald_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(katalog_VALUE / (Namn + '.o')), str(KJELDE)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisjon.parent / 'compiler/brukar_kople_Oppsett.ld'),
                        '-o', str(katalog_VALUE / (Namn + '.elf')), str(katalog_VALUE / (Namn + '.o'))], check=True)
        항목들.append(Namn + '=' + str(katalog_VALUE / (Namn + '.elf')))
    informasjonsteknologi_normal = bytearray((Posisjon / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ugyldig_forretningsmål = bytearray(informasjonsteknologi_normal); ugyldig_forretningsmål[0] = 0; 변형들['badelf'] = ugyldig_forretningsmål
    ugyldig_forretningsmål = bytearray(informasjonsteknologi_normal); struct.pack_into('<I', ugyldig_forretningsmål, 24, 0x00100000); 변형들['badentry'] = ugyldig_forretningsmål
    ugyldig_forretningsmål = bytearray(informasjonsteknologi_normal); struct.pack_into('<I', ugyldig_forretningsmål, 28, 0x7fffffff); 변형들['badtable'] = ugyldig_forretningsmål
    ugyldig_forretningsmål = bytearray(informasjonsteknologi_normal); LOOKUP_tabell = struct.unpack_from('<I', ugyldig_forretningsmål, 28)[0]
    struct.pack_into('<I', ugyldig_forretningsmål, LOOKUP_tabell + 20, 0x7fffffff); 변형들['badsize'] = ugyldig_forretningsmål
    for Namn, data in 변형들.items():
        Fil = katalog_VALUE / (Namn + '.elf'); Fil.write_bytes(data)
        항목들.append(Namn + '=' + str(Fil))
    subprocess.run([sys.executable, str(Posisjon / 'Verktøy/BIND_endepunkt.py'), '-o', str(katalog_VALUE / 'apps.bin')] + 항목들, check=True)
    KJELDE = katalog_VALUE / 'apps.s'
    KJELDE.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(katalog_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(katalog_VALUE / 'apps.o'), str(KJELDE)], check=True)
    kjerne_VALUE = katalog_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisjon / '부팅/kople_Oppsett.ld'), '-o', str(kjerne_VALUE),
                    str(Posisjon / 'build/boot.o'), str(Posisjon / 'build/java.o'), str(Posisjon / 'build/user.o'), str(katalog_VALUE / 'apps.o')], check=True)
    return kjerne_VALUE


def Utfør_kommando():
    forretningsmål = {}
    tenar_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tenar_VALUE.bind(('127.0.0.1', 0))
    tenar_VALUE.settimeout(0.1)
    port_VALUE = tenar_VALUE.getsockname()[1]
    RECEIVED_vare = []
    Utgang_app = threading.Event()
    def 되보내기():
        while not Utgang_app.is_set():
            try: data, node_VALUE_6a3b6fa7 = tenar_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_vare.append(data)
            if data != b'drop-me': tenar_VALUE.sendto(data, node_VALUE_6a3b6fa7)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            maskin = virtuell_maskin(Posisjon / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                maskin.Kommando('apps', ['hello', 'udp', 'netcheck', 'stress'])
                maskin.Kommando('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                maskin.Kommando('run missing', ['Exit: -2'])
                maskin.Kommando('net', ['NET RTL8139'])
                maskin.Kommando('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Innhald_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    maskin.Kommando('run udp 10.0.2.2 {} {}'.format(port_VALUE, Innhald_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Innhald_VALUE.encode() in RECEIVED_vare, 'vert 서버에서 자료를 받지 못함'
                maskin.Kommando('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                maskin.Kommando('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                maskin.Kommando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                forretningsmål[종류] = maskin.LOG_rad.decode('utf-8', 'replace')
                print('PASS: {} brukar ELF/ring 3/Argument/UDP vert 왕복/TIME_VALUE 초과/grensesnitt 복귀'.format(종류), flush=True)
            finally:
                try: maskin.Kommando('net', [])
                except Exception: pass
                (Posisjon / 'build/사용자통신-last.log').write_bytes(maskin.LOG_rad)
                maskin.Lukk()
        maskin = virtuell_maskin(Posisjon / 'build/kernel.elf', Nettverk_VALUE=False)
        try:
            maskin.Kommando('net', ['NET unavailable'])
            maskin.Kommando('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            maskin.Kommando('run hello', ['USER MODE ring 3', 'Exit: 0'])
            forretningsmål['no_nic'] = maskin.LOG_rad.decode()
        finally: maskin.Lukk()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            maskin = virtuell_maskin(보호커널(Path(임시)), Nettverk_VALUE=False)
            try:
                for Namn, status_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    maskin.Kommando('run ' + Namn, ['Exit: ' + str(status_VALUE)])
                    maskin.Kommando('run hello', ['USER MODE ring 3', 'Exit: 0'])
                forretningsmål['protection'] = maskin.LOG_rad.decode()
                print('PASS: brukar Minne_data/포트 격리, 잘못된 peikar/ELF, CPU unntak, 무한 gjentaking_VALUE 제한', flush=True)
            finally:
                (Posisjon / 'build/보호시험-last.log').write_bytes(maskin.LOG_rad)
                maskin.Lukk()
    finally:
        Utgang_app.set()
        일꾼.join(timeout=2)
        tenar_VALUE.close()
    forretningsmål['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in RECEIVED_vare]
    (Posisjon / 'build/사용자통신시험.json').write_text(json.dumps(forretningsmål, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Utfør_kommando()
