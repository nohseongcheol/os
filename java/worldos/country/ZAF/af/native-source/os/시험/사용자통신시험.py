#!/usr/bin/env python3
"""werklik_data ring 3 ELF/hou UDP 왕복/beskerm_VALUE Fout/tyd_VALUE 제한/잘못된 ELF를 검증한다."""
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

Posisie = Path(__file__).resolve().parents[1]


class virtueel_masjien:
    def __init__(self, Pad, 종류='elf', Netwerk_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        gids_VALUE = Path(self.임시.name)
        self.LOG_ry = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_pad = gids_VALUE / 'serial.sock', gids_VALUE / 'monitor.sock'
        Opdrag = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_pad) + ',server,nowait']
        Opdrag += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Netwerk_VALUE else ['-net', 'none']
        Opdrag += ['-kernel', str(Pad)] if 종류 == 'elf' else ['-cdrom', str(Pad), '-boot', 'd']
        if 저장매체 is not None:
            Opdrag += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Proses_VALUE = subprocess.Popen(Opdrag, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_pad.exists()):
                if self.Proses_VALUE.poll() is not None:
                    raise AssertionError(self.Proses_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Loop tyd_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_pad))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.wag_stand('jkoros> ')
        except BaseException:
            self.Sluit()
            raise

    def wag_stand(self, 문구, Loop=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_ry[Loop:]:
                return self.LOG_ry[Loop:].decode('utf-8', 'replace')
            Lees, _, _ = select.select([self.직렬], [], [], 0.1)
            if Lees:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_ry.extend(data)
            if self.Proses_VALUE.poll() is not None: break
        raise AssertionError('wag_VALUE faling_VALUE: ' + 문구 + '\n' + self.LOG_ry.decode('utf-8', 'replace'))

    def Opdrag(self, string_VALUE, 기대):
        Loop = len(self.LOG_ry)
        self.직렬.sendall((string_VALUE + '\n').encode())
        maatreël = self.wag_stand('jkoros> ', Loop)
        for 문구 in 기대:
            assert 문구 in maatreël, (string_VALUE, 문구, maatreël)
        assert 'PANIC' not in maatreël, maatreël
        return maatreël

    def Sluit(self):
        self.직렬.close()
        self.monitor_VALUE.close()
        if self.Proses_VALUE.poll() is None:
            self.Proses_VALUE.terminate()
            try: self.Proses_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proses_VALUE.kill()
                self.Proses_VALUE.wait()
        self.Proses_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(gids_VALUE):
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
    항목들 = ['hello=' + str(Posisie / 'build/apps/hello.elf')]
    for Naam, Inhoud_VALUE in 사례들.items():
        Bron = gids_VALUE / (Naam + '.s')
        Bron.write_text('.code32\n.text\n.globl _start\n_start:\n' + Inhoud_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(gids_VALUE / (Naam + '.o')), str(Bron)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisie.parent / 'compiler/gebruiker_Skakel_Uitleg.ld'),
                        '-o', str(gids_VALUE / (Naam + '.elf')), str(gids_VALUE / (Naam + '.o'))], check=True)
        항목들.append(Naam + '=' + str(gids_VALUE / (Naam + '.elf')))
    정상 = bytearray((Posisie / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ongeldig_maatreël = bytearray(정상); ongeldig_maatreël[0] = 0; 변형들['badelf'] = ongeldig_maatreël
    ongeldig_maatreël = bytearray(정상); struct.pack_into('<I', ongeldig_maatreël, 24, 0x00100000); 변형들['badentry'] = ongeldig_maatreël
    ongeldig_maatreël = bytearray(정상); struct.pack_into('<I', ongeldig_maatreël, 28, 0x7fffffff); 변형들['badtable'] = ongeldig_maatreël
    ongeldig_maatreël = bytearray(정상); LOOKUP_tabel = struct.unpack_from('<I', ongeldig_maatreël, 28)[0]
    struct.pack_into('<I', ongeldig_maatreël, LOOKUP_tabel + 20, 0x7fffffff); 변형들['badsize'] = ongeldig_maatreël
    for Naam, data in 변형들.items():
        Lêer = gids_VALUE / (Naam + '.elf'); Lêer.write_bytes(data)
        항목들.append(Naam + '=' + str(Lêer))
    subprocess.run([sys.executable, str(Posisie / 'Nutsmiddels/묶기.py'), '-o', str(gids_VALUE / 'apps.bin')] + 항목들, check=True)
    Bron = gids_VALUE / 'apps.s'
    Bron.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(gids_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(gids_VALUE / 'apps.o'), str(Bron)], check=True)
    kern_VALUE = gids_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisie / '부팅/Skakel_Uitleg.ld'), '-o', str(kern_VALUE),
                    str(Posisie / 'build/boot.o'), str(Posisie / 'build/java.o'), str(Posisie / 'build/user.o'), str(gids_VALUE / 'apps.o')], check=True)
    return kern_VALUE


def uitvoer_bevel():
    maatreël = {}
    bediener_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bediener_VALUE.bind(('127.0.0.1', 0))
    bediener_VALUE.settimeout(0.1)
    ombou_VALUE = bediener_VALUE.getsockname()[1]
    RECEIVED_item = []
    Verlaat_program = threading.Event()
    def 되보내기():
        while not Verlaat_program.is_set():
            try: data, portuur_VALUE = bediener_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_item.append(data)
            if data != b'drop-me': bediener_VALUE.sendto(data, portuur_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            masjien = virtueel_masjien(Posisie / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                masjien.Opdrag('apps', ['hello', 'udp', 'netcheck', 'stress'])
                masjien.Opdrag('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                masjien.Opdrag('run missing', ['Exit: -2'])
                masjien.Opdrag('net', ['NET RTL8139'])
                masjien.Opdrag('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Inhoud_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    masjien.Opdrag('run udp 10.0.2.2 {} {}'.format(ombou_VALUE, Inhoud_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Inhoud_VALUE.encode() in RECEIVED_item, 'hou 서버에서 자료를 받지 못함'
                masjien.Opdrag('run stress {}'.format(ombou_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                masjien.Opdrag('run udp 10.0.2.2 {} drop-me'.format(ombou_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                masjien.Opdrag('run hello recovered', ['arg: recovered', 'Exit: 0'])
                maatreël[종류] = masjien.LOG_ry.decode('utf-8', 'replace')
                print('PASS: {} gebruiker ELF/ring 3/인수/UDP hou 왕복/tyd_VALUE 초과/dop 복귀'.format(종류), flush=True)
            finally:
                try: masjien.Opdrag('net', [])
                except Exception: pass
                (Posisie / 'build/사용자통신-last.log').write_bytes(masjien.LOG_ry)
                masjien.Sluit()
        masjien = virtueel_masjien(Posisie / 'build/kernel.elf', Netwerk_VALUE=False)
        try:
            masjien.Opdrag('net', ['NET unavailable'])
            masjien.Opdrag('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            masjien.Opdrag('run hello', ['USER MODE ring 3', 'Exit: 0'])
            maatreël['no_nic'] = masjien.LOG_ry.decode()
        finally: masjien.Sluit()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            masjien = virtueel_masjien(보호커널(Path(임시)), Netwerk_VALUE=False)
            try:
                for Naam, stand_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    masjien.Opdrag('run ' + Naam, ['Exit: ' + str(stand_VALUE)])
                    masjien.Opdrag('run hello', ['USER MODE ring 3', 'Exit: 0'])
                maatreël['protection'] = masjien.LOG_ry.decode()
                print('PASS: gebruiker Geheue_data/hardeware_ombou 격리, 잘못된 wyser/ELF, CPU uitsondering, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (Posisie / 'build/보호시험-last.log').write_bytes(masjien.LOG_ry)
                masjien.Sluit()
    finally:
        Verlaat_program.set()
        일꾼.join(timeout=2)
        bediener_VALUE.close()
    maatreël['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in RECEIVED_item]
    (Posisie / 'build/사용자통신시험.json').write_text(json.dumps(maatreël, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    uitvoer_bevel()
