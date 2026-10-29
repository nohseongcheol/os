#!/usr/bin/env python3
"""todellinen_data ring 3 ELF/isäntä UDP 왕복/suojata_ARVO VIRHE/AIKA_ARVO 제한/잘못된 ELF를 검증한다."""
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

paikka = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, polku_2, 종류='elf', verkko_ARVO=True, Tallennus_väline=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Directory_ARVO = Path(self.임시.name)
        self.LOG_TIETUE = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.näyttö_ARVO = socket.socket(socket.AF_UNIX)
        직렬경로, näyttö_polku = Directory_ARVO / 'serial.sock', Directory_ARVO / 'monitor.sock'
        komento = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(näyttö_polku) + ',server,nowait']
        komento += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if verkko_ARVO else ['-net', 'none']
        komento += ['-kernel', str(polku_2)] if 종류 == 'elf' else ['-cdrom', str(polku_2), '-boot', 'd']
        if Tallennus_väline is not None:
            komento += ['-drive', 'file=' + str(Tallennus_väline) + ',format=raw,if=ide,index=0']
        self.prosessi_ARVO = subprocess.Popen(komento, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and näyttö_polku.exists()):
                if self.prosessi_ARVO.poll() is not None:
                    raise AssertionError(self.prosessi_ARVO.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Suorita_2 AIKA_ARVO 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.näyttö_ARVO.connect(str(näyttö_polku))
            self.직렬.setblocking(False)
            self.näyttö_ARVO.sendall(b'cont\n')
            self.odotustila('jkoros> ')
        except BaseException:
            self.Sulje()
            raise

    def odotustila(self, 문구, Suorita_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_TIETUE[Suorita_2:]:
                return self.LOG_TIETUE[Suorita_2:].decode('utf-8', 'replace')
            Luku, _, _ = select.select([self.직렬], [], [], 0.1)
            if Luku:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_TIETUE.extend(data)
            if self.prosessi_ARVO.poll() is not None: break
        raise AssertionError('odottaa_ARVO virhe_ARVO: ' + 문구 + '\n' + self.LOG_TIETUE.decode('utf-8', 'replace'))

    def komento(self, merkkijono_ARVO, 기대):
        Suorita_2 = len(self.LOG_TIETUE)
        self.직렬.sendall((merkkijono_ARVO + '\n').encode())
        TULOS = self.odotustila('jkoros> ', Suorita_2)
        for 문구 in 기대:
            assert 문구 in TULOS, (merkkijono_ARVO, 문구, TULOS)
        assert 'PANIC' not in TULOS, TULOS
        return TULOS

    def Sulje(self):
        self.직렬.close()
        self.näyttö_ARVO.close()
        if self.prosessi_ARVO.poll() is None:
            self.prosessi_ARVO.terminate()
            try: self.prosessi_ARVO.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.prosessi_ARVO.kill()
                self.prosessi_ARVO.wait()
        self.prosessi_ARVO.communicate()
        self.임시.cleanup()


def 보호커널(Directory_ARVO):
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
    항목들 = ['hello=' + str(paikka / 'build/apps/hello.elf')]
    for Nimi, Sisältö_ARVO in 사례들.items():
        lähdetiedosto = Directory_ARVO / (Nimi + '.s')
        lähdetiedosto.write_text('.code32\n.text\n.globl _start\n_start:\n' + Sisältö_ARVO +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Directory_ARVO / (Nimi + '.o')), str(lähdetiedosto)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(paikka.parent / 'compiler/käyttäjä_Linkki_Asettelu.ld'),
                        '-o', str(Directory_ARVO / (Nimi + '.elf')), str(Directory_ARVO / (Nimi + '.o'))], check=True)
        항목들.append(Nimi + '=' + str(Directory_ARVO / (Nimi + '.elf')))
    tietojärjestelmät_normaali = bytearray((paikka / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    pätemätön_KR = bytearray(tietojärjestelmät_normaali); pätemätön_KR[0] = 0; 변형들['badelf'] = pätemätön_KR
    pätemätön_KR = bytearray(tietojärjestelmät_normaali); struct.pack_into('<I', pätemätön_KR, 24, 0x00100000); 변형들['badentry'] = pätemätön_KR
    pätemätön_KR = bytearray(tietojärjestelmät_normaali); struct.pack_into('<I', pätemätön_KR, 28, 0x7fffffff); 변형들['badtable'] = pätemätön_KR
    pätemätön_KR = bytearray(tietojärjestelmät_normaali); HAKU_taulukko = struct.unpack_from('<I', pätemätön_KR, 28)[0]
    struct.pack_into('<I', pätemätön_KR, HAKU_taulukko + 20, 0x7fffffff); 변형들['badsize'] = pätemätön_KR
    for Nimi, data in 변형들.items():
        tiedoston_nimi = Directory_ARVO / (Nimi + '.elf'); tiedoston_nimi.write_bytes(data)
        항목들.append(Nimi + '=' + str(tiedoston_nimi))
    subprocess.run([sys.executable, str(paikka / 'työkalut/BIND_päätepiste.py'), '-o', str(Directory_ARVO / 'apps.bin')] + 항목들, check=True)
    lähdetiedosto = Directory_ARVO / 'apps.s'
    lähdetiedosto.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Directory_ARVO / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Directory_ARVO / 'apps.o'), str(lähdetiedosto)], check=True)
    ydin_ARVO = Directory_ARVO / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(paikka / 'koneen_käynnistys/linkitysasettelu.ld'), '-o', str(ydin_ARVO),
                    str(paikka / 'build/boot.o'), str(paikka / 'build/java.o'), str(paikka / 'build/user.o'), str(Directory_ARVO / 'apps.o')], check=True)
    return ydin_ARVO


def Suorita_komento():
    TULOS = {}
    palvelin_ARVO = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    palvelin_ARVO.bind(('127.0.0.1', 0))
    palvelin_ARVO.settimeout(0.1)
    portti_ARVO = palvelin_ARVO.getsockname()[1]
    SAATU_HINTA_kohde = []
    Lopeta_ohjelma = threading.Event()
    def päivitys_palaute():
        while not Lopeta_ohjelma.is_set():
            try: data, vertaissolmu_ARVO = palvelin_ARVO.recvfrom(4096)
            except socket.timeout: continue
            SAATU_HINTA_kohde.append(data)
            if data != b'drop-me': palvelin_ARVO.sendto(data, vertaissolmu_ARVO)
    työntekijä_ARVO = threading.Thread(target=päivitys_palaute, daemon=True)
    työntekijä_ARVO.start()
    try:
        for 종류 in ('elf', 'iso'):
            kone = VM(paikka / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                kone.komento('apps', ['hello', 'udp', 'netcheck', 'stress'])
                kone.komento('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                kone.komento('run missing', ['Exit: -2'])
                kone.komento('net', ['NET RTL8139'])
                kone.komento('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Sisältö_ARVO in ('hello-network', 'odd', 'even', 'repeat-123'):
                    kone.komento('run udp 10.0.2.2 {} {}'.format(portti_ARVO, Sisältö_ARVO), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Sisältö_ARVO.encode() in SAATU_HINTA_kohde, 'isäntä 서버에서 자료를 받지 못함'
                kone.komento('run stress {}'.format(portti_ARVO), ['UDP STRESS PASS', 'Exit: 0'])
                kone.komento('run udp 10.0.2.2 {} drop-me'.format(portti_ARVO), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                kone.komento('run hello recovered', ['arg: recovered', 'Exit: 0'])
                TULOS[종류] = kone.LOG_TIETUE.decode('utf-8', 'replace')
                print('PASS: {} käyttäjätila ELF/ring 3/argumentit/UDP isäntä 왕복/AIKA_ARVO 초과/liittymä 복귀'.format(종류), flush=True)
            finally:
                try: kone.komento('net', [])
                except Exception: pass
                (paikka / 'build/사용자통신-last.log').write_bytes(kone.LOG_TIETUE)
                kone.Sulje()
        kone = VM(paikka / 'build/kernel.elf', verkko_ARVO=False)
        try:
            kone.komento('net', ['NET unavailable'])
            kone.komento('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            kone.komento('run hello', ['USER MODE ring 3', 'Exit: 0'])
            TULOS['no_nic'] = kone.LOG_TIETUE.decode()
        finally: kone.Sulje()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            kone = VM(보호커널(Path(임시)), verkko_ARVO=False)
            try:
                for Nimi, Tila_ARVO in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    kone.komento('run ' + Nimi, ['Exit: ' + str(Tila_ARVO)])
                    kone.komento('run hello', ['USER MODE ring 3', 'Exit: 0'])
                TULOS['protection'] = kone.LOG_TIETUE.decode()
                print('PASS: käyttäjätila Muisti_data/laitteisto_portti 격리, 잘못된 osoitin/ELF, CPU poikkeus, 무한 sprintti_ARVO 제한', flush=True)
            finally:
                (paikka / 'build/Suojaus_testi-last.log').write_bytes(kone.LOG_TIETUE)
                kone.Sulje()
    finally:
        Lopeta_ohjelma.set()
        työntekijä_ARVO.join(timeout=2)
        palvelin_ARVO.close()
    TULOS['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in SAATU_HINTA_kohde]
    (paikka / 'build/testi_käyttäjä_verkko.json').write_text(json.dumps(TULOS, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Suorita_komento()
