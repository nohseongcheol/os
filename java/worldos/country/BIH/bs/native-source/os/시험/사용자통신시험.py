#!/usr/bin/env python3
"""stvaran_podaci ring 3 ELF/organizator UDP 왕복/zaštititi_VALUE GRESKA/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

Pozicija = Path(__file__).resolve().parents[1]


class virtualno_mašina:
    def __init__(self, Putanja, 종류='elf', Mreža_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Direktorij_VALUE = Path(self.임시.name)
        self.LOG_red = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_put = Direktorij_VALUE / 'serial.sock', Direktorij_VALUE / 'monitor.sock'
        Naredba = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_put) + ',server,nowait']
        Naredba += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Mreža_VALUE else ['-net', 'none']
        Naredba += ['-kernel', str(Putanja)] if 종류 == 'elf' else ['-cdrom', str(Putanja), '-boot', 'd']
        if 저장매체 is not None:
            Naredba += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.proces_VALUE = subprocess.Popen(Naredba, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_put.exists()):
                if self.proces_VALUE.poll() is not None:
                    raise AssertionError(self.proces_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Pokreni TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_put))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.čekaj_stanje('jkoros> ')
        except BaseException:
            self.Zatvori()
            raise

    def čekaj_stanje(self, 문구, Pokreni=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_red[Pokreni:]:
                return self.LOG_red[Pokreni:].decode('utf-8', 'replace')
            Čitaj, _, _ = select.select([self.직렬], [], [], 0.1)
            if Čitaj:
                podaci = self.직렬.recv(65536)
                if not podaci: break
                self.LOG_red.extend(podaci)
            if self.proces_VALUE.poll() is not None: break
        raise AssertionError('čekaj_VALUE neuspjeh_VALUE: ' + 문구 + '\n' + self.LOG_red.decode('utf-8', 'replace'))

    def Naredba(self, string_VALUE, 기대):
        Pokreni = len(self.LOG_red)
        self.직렬.sendall((string_VALUE + '\n').encode())
        mjera = self.čekaj_stanje('jkoros> ', Pokreni)
        for 문구 in 기대:
            assert 문구 in mjera, (string_VALUE, 문구, mjera)
        assert 'PANIC' not in mjera, mjera
        return mjera

    def Zatvori(self):
        self.직렬.close()
        self.monitor_VALUE.close()
        if self.proces_VALUE.poll() is None:
            self.proces_VALUE.terminate()
            try: self.proces_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proces_VALUE.kill()
                self.proces_VALUE.wait()
        self.proces_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(Direktorij_VALUE):
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
    항목들 = ['hello=' + str(Pozicija / 'build/apps/hello.elf')]
    for Naziv, Sadržaj_VALUE in 사례들.items():
        IZVOR = Direktorij_VALUE / (Naziv + '.s')
        IZVOR.write_text('.code32\n.text\n.globl _start\n_start:\n' + Sadržaj_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Direktorij_VALUE / (Naziv + '.o')), str(IZVOR)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozicija.parent / 'compiler/korisnik_Veza_izgled.ld'),
                        '-o', str(Direktorij_VALUE / (Naziv + '.elf')), str(Direktorij_VALUE / (Naziv + '.o'))], check=True)
        항목들.append(Naziv + '=' + str(Direktorij_VALUE / (Naziv + '.elf')))
    정상 = bytearray((Pozicija / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    nevažeće_mjera = bytearray(정상); nevažeće_mjera[0] = 0; 변형들['badelf'] = nevažeće_mjera
    nevažeće_mjera = bytearray(정상); struct.pack_into('<I', nevažeće_mjera, 24, 0x00100000); 변형들['badentry'] = nevažeće_mjera
    nevažeće_mjera = bytearray(정상); struct.pack_into('<I', nevažeće_mjera, 28, 0x7fffffff); 변형들['badtable'] = nevažeće_mjera
    nevažeće_mjera = bytearray(정상); LOOKUP_tabela = struct.unpack_from('<I', nevažeće_mjera, 28)[0]
    struct.pack_into('<I', nevažeće_mjera, LOOKUP_tabela + 20, 0x7fffffff); 변형들['badsize'] = nevažeće_mjera
    for Naziv, podaci in 변형들.items():
        Fajl = Direktorij_VALUE / (Naziv + '.elf'); Fajl.write_bytes(podaci)
        항목들.append(Naziv + '=' + str(Fajl))
    subprocess.run([sys.executable, str(Pozicija / 'Alati/BIND_završna_tačka.py'), '-o', str(Direktorij_VALUE / 'apps.bin')] + 항목들, check=True)
    IZVOR = Direktorij_VALUE / 'apps.s'
    IZVOR.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Direktorij_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Direktorij_VALUE / 'apps.o'), str(IZVOR)], check=True)
    jezgro_VALUE = Direktorij_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozicija / '부팅/Veza_izgled.ld'), '-o', str(jezgro_VALUE),
                    str(Pozicija / 'build/boot.o'), str(Pozicija / 'build/java.o'), str(Pozicija / 'build/user.o'), str(Direktorij_VALUE / 'apps.o')], check=True)
    return jezgro_VALUE


def Izvrši_komanda():
    mjera = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_stavka = []
    izaći_program = threading.Event()
    def 되보내기():
        while not izaći_program.is_set():
            try: podaci, peer_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_stavka.append(podaci)
            if podaci != b'drop-me': server_VALUE.sendto(podaci, peer_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mašina = virtualno_mašina(Pozicija / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                mašina.Naredba('apps', ['hello', 'udp', 'netcheck', 'stress'])
                mašina.Naredba('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                mašina.Naredba('run missing', ['Exit: -2'])
                mašina.Naredba('net', ['NET RTL8139'])
                mašina.Naredba('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Sadržaj_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    mašina.Naredba('run udp 10.0.2.2 {} {}'.format(port_VALUE, Sadržaj_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Sadržaj_VALUE.encode() in RECEIVED_stavka, 'organizator 서버에서 자료를 받지 못함'
                mašina.Naredba('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                mašina.Naredba('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                mašina.Naredba('run hello recovered', ['arg: recovered', 'Exit: 0'])
                mjera[종류] = mašina.LOG_red.decode('utf-8', 'replace')
                print('PASS: {} korisnik ELF/ring 3/Argumenti/UDP organizator 왕복/TIME_VALUE 초과/ljuska 복귀'.format(종류), flush=True)
            finally:
                try: mašina.Naredba('net', [])
                except Exception: pass
                (Pozicija / 'build/사용자통신-last.log').write_bytes(mašina.LOG_red)
                mašina.Zatvori()
        mašina = virtualno_mašina(Pozicija / 'build/kernel.elf', Mreža_VALUE=False)
        try:
            mašina.Naredba('net', ['NET unavailable'])
            mašina.Naredba('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            mašina.Naredba('run hello', ['USER MODE ring 3', 'Exit: 0'])
            mjera['no_nic'] = mašina.LOG_red.decode()
        finally: mašina.Zatvori()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            mašina = virtualno_mašina(보호커널(Path(임시)), Mreža_VALUE=False)
            try:
                for Naziv, stanje_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    mašina.Naredba('run ' + Naziv, ['Exit: ' + str(stanje_VALUE)])
                    mašina.Naredba('run hello', ['USER MODE ring 3', 'Exit: 0'])
                mjera['protection'] = mašina.LOG_red.decode()
                print('PASS: korisnik Memorija_podaci/hardver_port 격리, 잘못된 pokazivač/ELF, CPU izuzetak, 무한 ponavljanje_VALUE 제한', flush=True)
            finally:
                (Pozicija / 'build/보호시험-last.log').write_bytes(mašina.LOG_red)
                mašina.Zatvori()
    finally:
        izaći_program.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    mjera['host_udp_received'] = [{'length': len(podaci), 'sha256': hashlib.sha256(podaci).hexdigest()} for podaci in RECEIVED_stavka]
    (Pozicija / 'build/사용자통신시험.json').write_text(json.dumps(mjera, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Izvrši_komanda()
