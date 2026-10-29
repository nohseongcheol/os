#!/usr/bin/env python3
"""faktisk_data ring 3 ELF/vert UDP 왕복/beskytte_VERDI feil/TID_VERDI 제한/잘못된 ELF를 검증한다."""
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


class VM:
    def __init__(self, Sti, 종류='elf', nettverk_VERDI=True, lager_medium=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        katalog_VERDI = Path(self.임시.name)
        self.LOG_POST = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.skjerm_VERDI = socket.socket(socket.AF_UNIX)
        직렬경로, skjerm_bane = katalog_VERDI / 'serial.sock', katalog_VERDI / 'monitor.sock'
        Kommando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(skjerm_bane) + ',server,nowait']
        Kommando += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if nettverk_VERDI else ['-net', 'none']
        Kommando += ['-kernel', str(Sti)] if 종류 == 'elf' else ['-cdrom', str(Sti), '-boot', 'd']
        if lager_medium is not None:
            Kommando += ['-drive', 'file=' + str(lager_medium) + ',format=raw,if=ide,index=0']
        self.Prosess_VERDI = subprocess.Popen(Kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and skjerm_bane.exists()):
                if self.Prosess_VERDI.poll() is not None:
                    raise AssertionError(self.Prosess_VERDI.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Kjør_2 TID_VERDI 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.skjerm_VERDI.connect(str(skjerm_bane))
            self.직렬.setblocking(False)
            self.skjerm_VERDI.sendall(b'cont\n')
            self.ventende_tilstand('jkoros> ')
        except BaseException:
            self.Lukk()
            raise

    def ventende_tilstand(self, 문구, Kjør_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_POST[Kjør_2:]:
                return self.LOG_POST[Kjør_2:].decode('utf-8', 'replace')
            Les, _, _ = select.select([self.직렬], [], [], 0.1)
            if Les:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_POST.extend(data)
            if self.Prosess_VERDI.poll() is not None: break
        raise AssertionError('vent_VERDI feil_VERDI: ' + 문구 + '\n' + self.LOG_POST.decode('utf-8', 'replace'))

    def Kommando(self, streng_VERDI, 기대):
        Kjør_2 = len(self.LOG_POST)
        self.직렬.sendall((streng_VERDI + '\n').encode())
        KR = self.ventende_tilstand('jkoros> ', Kjør_2)
        for 문구 in 기대:
            assert 문구 in KR, (streng_VERDI, 문구, KR)
        assert 'PANIC' not in KR, KR
        return KR

    def Lukk(self):
        self.직렬.close()
        self.skjerm_VERDI.close()
        if self.Prosess_VERDI.poll() is None:
            self.Prosess_VERDI.terminate()
            try: self.Prosess_VERDI.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Prosess_VERDI.kill()
                self.Prosess_VERDI.wait()
        self.Prosess_VERDI.communicate()
        self.임시.cleanup()


def 보호커널(katalog_VERDI):
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
    for Navn, Innhold_VERDI in 사례들.items():
        KILDE = katalog_VERDI / (Navn + '.s')
        KILDE.write_text('.code32\n.text\n.globl _start\n_start:\n' + Innhold_VERDI +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(katalog_VERDI / (Navn + '.o')), str(KILDE)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisjon.parent / 'compiler/bruker_koble_Oppsett.ld'),
                        '-o', str(katalog_VERDI / (Navn + '.elf')), str(katalog_VERDI / (Navn + '.o'))], check=True)
        항목들.append(Navn + '=' + str(katalog_VERDI / (Navn + '.elf')))
    informasjonssystemer_normal = bytearray((Posisjon / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ugyldig_KR = bytearray(informasjonssystemer_normal); ugyldig_KR[0] = 0; 변형들['badelf'] = ugyldig_KR
    ugyldig_KR = bytearray(informasjonssystemer_normal); struct.pack_into('<I', ugyldig_KR, 24, 0x00100000); 변형들['badentry'] = ugyldig_KR
    ugyldig_KR = bytearray(informasjonssystemer_normal); struct.pack_into('<I', ugyldig_KR, 28, 0x7fffffff); 변형들['badtable'] = ugyldig_KR
    ugyldig_KR = bytearray(informasjonssystemer_normal); oppslagstabell = struct.unpack_from('<I', ugyldig_KR, 28)[0]
    struct.pack_into('<I', ugyldig_KR, oppslagstabell + 20, 0x7fffffff); 변형들['badsize'] = ugyldig_KR
    for Navn, data in 변형들.items():
        Fil = katalog_VERDI / (Navn + '.elf'); Fil.write_bytes(data)
        항목들.append(Navn + '=' + str(Fil))
    subprocess.run([sys.executable, str(Posisjon / 'Verktøy/BIND_deltaker.py'), '-o', str(katalog_VERDI / 'apps.bin')] + 항목들, check=True)
    KILDE = katalog_VERDI / 'apps.s'
    KILDE.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(katalog_VERDI / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(katalog_VERDI / 'apps.o'), str(KILDE)], check=True)
    kjerne_VERDI = katalog_VERDI / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posisjon / '부팅/koble_Oppsett.ld'), '-o', str(kjerne_VERDI),
                    str(Posisjon / 'build/boot.o'), str(Posisjon / 'build/java.o'), str(Posisjon / 'build/user.o'), str(katalog_VERDI / 'apps.o')], check=True)
    return kjerne_VERDI


def Utfør_kommando():
    KR = {}
    server_VERDI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VERDI.bind(('127.0.0.1', 0))
    server_VERDI.settimeout(0.1)
    port_VERDI = server_VERDI.getsockname()[1]
    MOTTATT_AVKAST_vare = []
    Utgang_app = threading.Event()
    def oppdatere_skjerm_svar():
        while not Utgang_app.is_set():
            try: data, node_VERDI_6a3b6fa7 = server_VERDI.recvfrom(4096)
            except socket.timeout: continue
            MOTTATT_AVKAST_vare.append(data)
            if data != b'drop-me': server_VERDI.sendto(data, node_VERDI_6a3b6fa7)
    arbeider_VERDI = threading.Thread(target=oppdatere_skjerm_svar, daemon=True)
    arbeider_VERDI.start()
    try:
        for 종류 in ('elf', 'iso'):
            maskin = VM(Posisjon / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                maskin.Kommando('apps', ['hello', 'udp', 'netcheck', 'stress'])
                maskin.Kommando('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                maskin.Kommando('run missing', ['Exit: -2'])
                maskin.Kommando('net', ['NET RTL8139'])
                maskin.Kommando('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Innhold_VERDI in ('hello-network', 'odd', 'even', 'repeat-123'):
                    maskin.Kommando('run udp 10.0.2.2 {} {}'.format(port_VERDI, Innhold_VERDI), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Innhold_VERDI.encode() in MOTTATT_AVKAST_vare, 'vert 서버에서 자료를 받지 못함'
                maskin.Kommando('run stress {}'.format(port_VERDI), ['UDP STRESS PASS', 'Exit: 0'])
                maskin.Kommando('run udp 10.0.2.2 {} drop-me'.format(port_VERDI), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                maskin.Kommando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = maskin.LOG_POST.decode('utf-8', 'replace')
                print('PASS: {} bruker ELF/ring 3/Argumenter/UDP vert 왕복/TID_VERDI 초과/Shell 복귀'.format(종류), flush=True)
            finally:
                try: maskin.Kommando('net', [])
                except Exception: pass
                (Posisjon / 'build/사용자통신-last.log').write_bytes(maskin.LOG_POST)
                maskin.Lukk()
        maskin = VM(Posisjon / 'build/kernel.elf', nettverk_VERDI=False)
        try:
            maskin.Kommando('net', ['NET unavailable'])
            maskin.Kommando('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            maskin.Kommando('run hello', ['USER MODE ring 3', 'Exit: 0'])
            KR['no_nic'] = maskin.LOG_POST.decode()
        finally: maskin.Lukk()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            maskin = VM(보호커널(Path(임시)), nettverk_VERDI=False)
            try:
                for Navn, status_VERDI in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    maskin.Kommando('run ' + Navn, ['Exit: ' + str(status_VERDI)])
                    maskin.Kommando('run hello', ['USER MODE ring 3', 'Exit: 0'])
                KR['protection'] = maskin.LOG_POST.decode()
                print('PASS: bruker Minne_data/maskinvare_port 격리, 잘못된 peker/ELF, CPU unntak, 무한 sprint_VERDI 제한', flush=True)
            finally:
                (Posisjon / 'build/Beskyttelse_test-last.log').write_bytes(maskin.LOG_POST)
                maskin.Lukk()
    finally:
        Utgang_app.set()
        arbeider_VERDI.join(timeout=2)
        server_VERDI.close()
    KR['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in MOTTATT_AVKAST_vare]
    (Posisjon / 'build/test_bruker_nettverk.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Utfør_kommando()
