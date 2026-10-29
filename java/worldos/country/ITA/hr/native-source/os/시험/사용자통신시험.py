#!/usr/bin/env python3
"""stvaran_podaci ring 3 ELF/domaćin UDP 왕복/zaštititi_VALUE GREŠKA/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

Položaj = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, PUTANJA, 종류='elf', mreža_VALUE=True, Pohrana_medij=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        imenik_VALUE = Path(self.임시.name)
        self.LOG_zapis = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_put = imenik_VALUE / 'serial.sock', imenik_VALUE / 'monitor.sock'
        Naredba = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_put) + ',server,nowait']
        Naredba += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if mreža_VALUE else ['-net', 'none']
        Naredba += ['-kernel', str(PUTANJA)] if 종류 == 'elf' else ['-cdrom', str(PUTANJA), '-boot', 'd']
        if Pohrana_medij is not None:
            Naredba += ['-drive', 'file=' + str(Pohrana_medij) + ',format=raw,if=ide,index=0']
        self.Proces_VALUE = subprocess.Popen(Naredba, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_put.exists()):
                if self.Proces_VALUE.poll() is not None:
                    raise AssertionError(self.Proces_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Pokreni TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_put))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.stanje_čekanja('jkoros> ')
        except BaseException:
            self.Zatvori()
            raise

    def stanje_čekanja(self, 문구, Pokreni=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_zapis[Pokreni:]:
                return self.LOG_zapis[Pokreni:].decode('utf-8', 'replace')
            Čitaj, _, _ = select.select([self.직렬], [], [], 0.1)
            if Čitaj:
                podaci = self.직렬.recv(65536)
                if not podaci: break
                self.LOG_zapis.extend(podaci)
            if self.Proces_VALUE.poll() is not None: break
        raise AssertionError('čekaj_VALUE kvar_VALUE: ' + 문구 + '\n' + self.LOG_zapis.decode('utf-8', 'replace'))

    def Naredba(self, niz_VALUE, 기대):
        Pokreni = len(self.LOG_zapis)
        self.직렬.sendall((niz_VALUE + '\n').encode())
        REZULTAT = self.stanje_čekanja('jkoros> ', Pokreni)
        for 문구 in 기대:
            assert 문구 in REZULTAT, (niz_VALUE, 문구, REZULTAT)
        assert 'PANIC' not in REZULTAT, REZULTAT
        return REZULTAT

    def Zatvori(self):
        self.직렬.close()
        self.monitor_VALUE.close()
        if self.Proces_VALUE.poll() is None:
            self.Proces_VALUE.terminate()
            try: self.Proces_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proces_VALUE.kill()
                self.Proces_VALUE.wait()
        self.Proces_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(imenik_VALUE):
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
    항목들 = ['hello=' + str(Položaj / 'build/apps/hello.elf')]
    for Ime, Sadržaj_VALUE in 사례들.items():
        IZVOR = imenik_VALUE / (Ime + '.s')
        IZVOR.write_text('.code32\n.text\n.globl _start\n_start:\n' + Sadržaj_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(imenik_VALUE / (Ime + '.o')), str(IZVOR)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Položaj.parent / 'compiler/korisnik_veza_Raspored.ld'),
                        '-o', str(imenik_VALUE / (Ime + '.elf')), str(imenik_VALUE / (Ime + '.o'))], check=True)
        항목들.append(Ime + '=' + str(imenik_VALUE / (Ime + '.elf')))
    정상 = bytearray((Položaj / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    nevaljan_KR = bytearray(정상); nevaljan_KR[0] = 0; 변형들['badelf'] = nevaljan_KR
    nevaljan_KR = bytearray(정상); struct.pack_into('<I', nevaljan_KR, 24, 0x00100000); 변형들['badentry'] = nevaljan_KR
    nevaljan_KR = bytearray(정상); struct.pack_into('<I', nevaljan_KR, 28, 0x7fffffff); 변형들['badtable'] = nevaljan_KR
    nevaljan_KR = bytearray(정상); LOOKUP_tablica = struct.unpack_from('<I', nevaljan_KR, 28)[0]
    struct.pack_into('<I', nevaljan_KR, LOOKUP_tablica + 20, 0x7fffffff); 변형들['badsize'] = nevaljan_KR
    for Ime, podaci in 변형들.items():
        Datoteka = imenik_VALUE / (Ime + '.elf'); Datoteka.write_bytes(podaci)
        항목들.append(Ime + '=' + str(Datoteka))
    subprocess.run([sys.executable, str(Položaj / 'Alati/BIND_sudionik.py'), '-o', str(imenik_VALUE / 'apps.bin')] + 항목들, check=True)
    IZVOR = imenik_VALUE / 'apps.s'
    IZVOR.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(imenik_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(imenik_VALUE / 'apps.o'), str(IZVOR)], check=True)
    jezgra_sustava_VALUE = imenik_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Položaj / '부팅/veza_Raspored.ld'), '-o', str(jezgra_sustava_VALUE),
                    str(Položaj / 'build/boot.o'), str(Položaj / 'build/java.o'), str(Položaj / 'build/user.o'), str(imenik_VALUE / 'apps.o')], check=True)
    return jezgra_sustava_VALUE


def Izvrši_naredba():
    REZULTAT = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    prebaciti_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_artikl = []
    Izlaz_program = threading.Event()
    def eho_odgovor():
        while not Izlaz_program.is_set():
            try: podaci, ravnopravan_član_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_artikl.append(podaci)
            if podaci != b'drop-me': server_VALUE.sendto(podaci, ravnopravan_član_VALUE)
    일꾼 = threading.Thread(target=eho_odgovor, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            stroj = VM(Položaj / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                stroj.Naredba('apps', ['hello', 'udp', 'netcheck', 'stress'])
                stroj.Naredba('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                stroj.Naredba('run missing', ['Exit: -2'])
                stroj.Naredba('net', ['NET RTL8139'])
                stroj.Naredba('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Sadržaj_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    stroj.Naredba('run udp 10.0.2.2 {} {}'.format(prebaciti_VALUE, Sadržaj_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Sadržaj_VALUE.encode() in RECEIVED_artikl, 'domaćin 서버에서 자료를 받지 못함'
                stroj.Naredba('run stress {}'.format(prebaciti_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                stroj.Naredba('run udp 10.0.2.2 {} drop-me'.format(prebaciti_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                stroj.Naredba('run hello recovered', ['arg: recovered', 'Exit: 0'])
                REZULTAT[종류] = stroj.LOG_zapis.decode('utf-8', 'replace')
                print('PASS: {} korisnik ELF/ring 3/Argumenti/UDP domaćin 왕복/TIME_VALUE 초과/ljuska 복귀'.format(종류), flush=True)
            finally:
                try: stroj.Naredba('net', [])
                except Exception: pass
                (Položaj / 'build/사용자통신-last.log').write_bytes(stroj.LOG_zapis)
                stroj.Zatvori()
        stroj = VM(Položaj / 'build/kernel.elf', mreža_VALUE=False)
        try:
            stroj.Naredba('net', ['NET unavailable'])
            stroj.Naredba('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            stroj.Naredba('run hello', ['USER MODE ring 3', 'Exit: 0'])
            REZULTAT['no_nic'] = stroj.LOG_zapis.decode()
        finally: stroj.Zatvori()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            stroj = VM(보호커널(Path(임시)), mreža_VALUE=False)
            try:
                for Ime, Stanje_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    stroj.Naredba('run ' + Ime, ['Exit: ' + str(Stanje_VALUE)])
                    stroj.Naredba('run hello', ['USER MODE ring 3', 'Exit: 0'])
                REZULTAT['protection'] = stroj.LOG_zapis.decode()
                print('PASS: korisnik Memorija_podaci/포트 격리, 잘못된 pokazivač/ELF, CPU iznimka, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (Položaj / 'build/보호시험-last.log').write_bytes(stroj.LOG_zapis)
                stroj.Zatvori()
    finally:
        Izlaz_program.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    REZULTAT['host_udp_received'] = [{'length': len(podaci), 'sha256': hashlib.sha256(podaci).hexdigest()} for podaci in RECEIVED_artikl]
    (Položaj / 'build/사용자통신시험.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Izvrši_naredba()
