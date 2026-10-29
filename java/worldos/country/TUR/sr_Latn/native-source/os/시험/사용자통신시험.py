#!/usr/bin/env python3
"""stvarni_podaci ring 3 ELF/host UDP 왕복/zaštititi_VALUE greška/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

pozicija = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, putanja, 종류='elf', Mreža_VALUE=True, Skladište_Srednja=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Imenik_VALUE = Path(self.임시.name)
        self.LOG_snimi = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_putanja = Imenik_VALUE / 'serial.sock', Imenik_VALUE / 'monitor.sock'
        komanda = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_putanja) + ',server,nowait']
        komanda += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Mreža_VALUE else ['-net', 'none']
        komanda += ['-kernel', str(putanja)] if 종류 == 'elf' else ['-cdrom', str(putanja), '-boot', 'd']
        if Skladište_Srednja is not None:
            komanda += ['-drive', 'file=' + str(Skladište_Srednja) + ',format=raw,if=ide,index=0']
        self.Proces_VALUE = subprocess.Popen(komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_putanja.exists()):
                if self.Proces_VALUE.poll() is not None:
                    raise AssertionError(self.Proces_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU koristiti TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_putanja))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.stanje_čekanja('jkoros> ')
        except BaseException:
            self.Zatvori()
            raise

    def stanje_čekanja(self, 문구, koristiti=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_snimi[koristiti:]:
                return self.LOG_snimi[koristiti:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                podaci = self.직렬.recv(65536)
                if not podaci: break
                self.LOG_snimi.extend(podaci)
            if self.Proces_VALUE.poll() is not None: break
        raise AssertionError('čekaj_VALUE otkazivanje_VALUE: ' + 문구 + '\n' + self.LOG_snimi.decode('utf-8', 'replace'))

    def komanda(self, niska_VALUE, 기대):
        koristiti = len(self.LOG_snimi)
        self.직렬.sendall((niska_VALUE + '\n').encode())
        KR = self.stanje_čekanja('jkoros> ', koristiti)
        for 문구 in 기대:
            assert 문구 in KR, (niska_VALUE, 문구, KR)
        assert 'PANIC' not in KR, KR
        return KR

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


def 보호커널(Imenik_VALUE):
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
    항목들 = ['hello=' + str(pozicija / 'build/apps/hello.elf')]
    for ime, Sadržaj_VALUE in 사례들.items():
        izvor = Imenik_VALUE / (ime + '.s')
        izvor.write_text('.code32\n.text\n.globl _start\n_start:\n' + Sadržaj_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Imenik_VALUE / (ime + '.o')), str(izvor)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozicija.parent / 'compiler/korisnik_Veza_Raspored.ld'),
                        '-o', str(Imenik_VALUE / (ime + '.elf')), str(Imenik_VALUE / (ime + '.o'))], check=True)
        항목들.append(ime + '=' + str(Imenik_VALUE / (ime + '.elf')))
    정상 = bytearray((pozicija / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    nevažeći_KR = bytearray(정상); nevažeći_KR[0] = 0; 변형들['badelf'] = nevažeći_KR
    nevažeći_KR = bytearray(정상); struct.pack_into('<I', nevažeći_KR, 24, 0x00100000); 변형들['badentry'] = nevažeći_KR
    nevažeći_KR = bytearray(정상); struct.pack_into('<I', nevažeći_KR, 28, 0x7fffffff); 변형들['badtable'] = nevažeći_KR
    nevažeći_KR = bytearray(정상); LOOKUP_tabela = struct.unpack_from('<I', nevažeći_KR, 28)[0]
    struct.pack_into('<I', nevažeći_KR, LOOKUP_tabela + 20, 0x7fffffff); 변형들['badsize'] = nevažeći_KR
    for ime, podaci in 변형들.items():
        Datoteka = Imenik_VALUE / (ime + '.elf'); Datoteka.write_bytes(podaci)
        항목들.append(ime + '=' + str(Datoteka))
    subprocess.run([sys.executable, str(pozicija / 'Alatke/povezati_učesnik.py'), '-o', str(Imenik_VALUE / 'apps.bin')] + 항목들, check=True)
    izvor = Imenik_VALUE / 'apps.s'
    izvor.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Imenik_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Imenik_VALUE / 'apps.o'), str(izvor)], check=True)
    jezgro_VALUE = Imenik_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozicija / '부팅/Veza_Raspored.ld'), '-o', str(jezgro_VALUE),
                    str(pozicija / 'build/boot.o'), str(pozicija / 'build/java.o'), str(pozicija / 'build/user.o'), str(Imenik_VALUE / 'apps.o')], check=True)
    return jezgro_VALUE


def Izvrši_komanda():
    KR = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_stavka = []
    Izađi_program = threading.Event()
    def eho_odgovor():
        while not Izađi_program.is_set():
            try: podaci, ravnopravni_uređaj_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_stavka.append(podaci)
            if podaci != b'drop-me': server_VALUE.sendto(podaci, ravnopravni_uređaj_VALUE)
    일꾼 = threading.Thread(target=eho_odgovor, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            računar = VM(pozicija / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                računar.komanda('apps', ['hello', 'udp', 'netcheck', 'stress'])
                računar.komanda('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                računar.komanda('run missing', ['Exit: -2'])
                računar.komanda('net', ['NET RTL8139'])
                računar.komanda('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Sadržaj_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    računar.komanda('run udp 10.0.2.2 {} {}'.format(port_VALUE, Sadržaj_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Sadržaj_VALUE.encode() in RECEIVED_stavka, 'host 서버에서 자료를 받지 못함'
                računar.komanda('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                računar.komanda('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                računar.komanda('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = računar.LOG_snimi.decode('utf-8', 'replace')
                print('PASS: {} korisnik ELF/ring 3/인수/UDP host 왕복/TIME_VALUE 초과/ljuska 복귀'.format(종류), flush=True)
            finally:
                try: računar.komanda('net', [])
                except Exception: pass
                (pozicija / 'build/사용자통신-last.log').write_bytes(računar.LOG_snimi)
                računar.Zatvori()
        računar = VM(pozicija / 'build/kernel.elf', Mreža_VALUE=False)
        try:
            računar.komanda('net', ['NET unavailable'])
            računar.komanda('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            računar.komanda('run hello', ['USER MODE ring 3', 'Exit: 0'])
            KR['no_nic'] = računar.LOG_snimi.decode()
        finally: računar.Zatvori()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            računar = VM(보호커널(Path(임시)), Mreža_VALUE=False)
            try:
                for ime, Status_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    računar.komanda('run ' + ime, ['Exit: ' + str(Status_VALUE)])
                    računar.komanda('run hello', ['USER MODE ring 3', 'Exit: 0'])
                KR['protection'] = računar.LOG_snimi.decode()
                print('PASS: korisnik Memorija_podaci/포트 격리, 잘못된 pokazivač/ELF, CPU izuzetak, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (pozicija / 'build/보호시험-last.log').write_bytes(računar.LOG_snimi)
                računar.Zatvori()
    finally:
        Izađi_program.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    KR['host_udp_received'] = [{'length': len(podaci), 'sha256': hashlib.sha256(podaci).hexdigest()} for podaci in RECEIVED_stavka]
    (pozicija / 'build/사용자통신시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Izvrši_komanda()
