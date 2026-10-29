#!/usr/bin/env python3
"""dejanski_podatki ring 3 ELF/gostiti UDP 왕복/zaščititi_VALUE NAPAKA/čas_VALUE 제한/잘못된 ELF를 검증한다."""
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


class navidezni_računalnik:
    def __init__(self, POT, 종류='elf', mreža_VALUE=True, Senzor_prostora_medij=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Imenik_VALUE = Path(self.임시.name)
        self.LOG_zapis = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_pot = Imenik_VALUE / 'serial.sock', Imenik_VALUE / 'monitor.sock'
        Ukaz = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_pot) + ',server,nowait']
        Ukaz += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if mreža_VALUE else ['-net', 'none']
        Ukaz += ['-kernel', str(POT)] if 종류 == 'elf' else ['-cdrom', str(POT), '-boot', 'd']
        if Senzor_prostora_medij is not None:
            Ukaz += ['-drive', 'file=' + str(Senzor_prostora_medij) + ',format=raw,if=ide,index=0']
        self.Proces_VALUE = subprocess.Popen(Ukaz, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_pot.exists()):
                if self.Proces_VALUE.poll() is not None:
                    raise AssertionError(self.Proces_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Zaženi čas_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_pot))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.čakalno_stanje('jkoros> ')
        except BaseException:
            self.Zapri()
            raise

    def čakalno_stanje(self, 문구, Zaženi=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_zapis[Zaženi:]:
                return self.LOG_zapis[Zaženi:].decode('utf-8', 'replace')
            Branje, _, _ = select.select([self.직렬], [], [], 0.1)
            if Branje:
                podatki = self.직렬.recv(65536)
                if not podatki: break
                self.LOG_zapis.extend(podatki)
            if self.Proces_VALUE.poll() is not None: break
        raise AssertionError('počakaj_VALUE napaka_VALUE: ' + 문구 + '\n' + self.LOG_zapis.decode('utf-8', 'replace'))

    def Ukaz(self, niz_VALUE, 기대):
        Zaženi = len(self.LOG_zapis)
        self.직렬.sendall((niz_VALUE + '\n').encode())
        REZULTAT = self.čakalno_stanje('jkoros> ', Zaženi)
        for 문구 in 기대:
            assert 문구 in REZULTAT, (niz_VALUE, 문구, REZULTAT)
        assert 'PANIC' not in REZULTAT, REZULTAT
        return REZULTAT

    def Zapri(self):
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
    항목들 = ['hello=' + str(Položaj / 'build/apps/hello.elf')]
    for Ime, vsebina_VALUE in 사례들.items():
        VIR = Imenik_VALUE / (Ime + '.s')
        VIR.write_text('.code32\n.text\n.globl _start\n_start:\n' + vsebina_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Imenik_VALUE / (Ime + '.o')), str(VIR)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Položaj.parent / 'compiler/uporabnik_Povezava_Krmarjenje.ld'),
                        '-o', str(Imenik_VALUE / (Ime + '.elf')), str(Imenik_VALUE / (Ime + '.o'))], check=True)
        항목들.append(Ime + '=' + str(Imenik_VALUE / (Ime + '.elf')))
    정상 = bytearray((Položaj / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    neveljaven_KR = bytearray(정상); neveljaven_KR[0] = 0; 변형들['badelf'] = neveljaven_KR
    neveljaven_KR = bytearray(정상); struct.pack_into('<I', neveljaven_KR, 24, 0x00100000); 변형들['badentry'] = neveljaven_KR
    neveljaven_KR = bytearray(정상); struct.pack_into('<I', neveljaven_KR, 28, 0x7fffffff); 변형들['badtable'] = neveljaven_KR
    neveljaven_KR = bytearray(정상); iskalna_tabela = struct.unpack_from('<I', neveljaven_KR, 28)[0]
    struct.pack_into('<I', neveljaven_KR, iskalna_tabela + 20, 0x7fffffff); 변형들['badsize'] = neveljaven_KR
    for Ime, podatki in 변형들.items():
        Datoteka = Imenik_VALUE / (Ime + '.elf'); Datoteka.write_bytes(podatki)
        항목들.append(Ime + '=' + str(Datoteka))
    subprocess.run([sys.executable, str(Položaj / 'Orodja/BIND_končna_točka.py'), '-o', str(Imenik_VALUE / 'apps.bin')] + 항목들, check=True)
    VIR = Imenik_VALUE / 'apps.s'
    VIR.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Imenik_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Imenik_VALUE / 'apps.o'), str(VIR)], check=True)
    jedro_VALUE = Imenik_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Položaj / '부팅/Povezava_Krmarjenje.ld'), '-o', str(jedro_VALUE),
                    str(Položaj / 'build/boot.o'), str(Položaj / 'build/java.o'), str(Položaj / 'build/user.o'), str(Imenik_VALUE / 'apps.o')], check=True)
    return jedro_VALUE


def Izvedi_ukaz():
    REZULTAT = {}
    strežnik_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    strežnik_VALUE.bind(('127.0.0.1', 0))
    strežnik_VALUE.settimeout(0.1)
    vrata_VALUE = strežnik_VALUE.getsockname()[1]
    RECEIVED_element = []
    Izhod_aplikacija = threading.Event()
    def odmev_odgovor():
        while not Izhod_aplikacija.is_set():
            try: podatki, enakovreden_VALUE = strežnik_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_element.append(podatki)
            if podatki != b'drop-me': strežnik_VALUE.sendto(podatki, enakovreden_VALUE)
    일꾼 = threading.Thread(target=odmev_odgovor, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            računalnik = navidezni_računalnik(Položaj / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                računalnik.Ukaz('apps', ['hello', 'udp', 'netcheck', 'stress'])
                računalnik.Ukaz('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                računalnik.Ukaz('run missing', ['Exit: -2'])
                računalnik.Ukaz('net', ['NET RTL8139'])
                računalnik.Ukaz('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for vsebina_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    računalnik.Ukaz('run udp 10.0.2.2 {} {}'.format(vrata_VALUE, vsebina_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert vsebina_VALUE.encode() in RECEIVED_element, 'gostiti 서버에서 자료를 받지 못함'
                računalnik.Ukaz('run stress {}'.format(vrata_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                računalnik.Ukaz('run udp 10.0.2.2 {} drop-me'.format(vrata_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                računalnik.Ukaz('run hello recovered', ['arg: recovered', 'Exit: 0'])
                REZULTAT[종류] = računalnik.LOG_zapis.decode('utf-8', 'replace')
                print('PASS: {} uporabnik ELF/ring 3/Argumenti/UDP gostiti 왕복/čas_VALUE 초과/lupina 복귀'.format(종류), flush=True)
            finally:
                try: računalnik.Ukaz('net', [])
                except Exception: pass
                (Položaj / 'build/사용자통신-last.log').write_bytes(računalnik.LOG_zapis)
                računalnik.Zapri()
        računalnik = navidezni_računalnik(Položaj / 'build/kernel.elf', mreža_VALUE=False)
        try:
            računalnik.Ukaz('net', ['NET unavailable'])
            računalnik.Ukaz('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            računalnik.Ukaz('run hello', ['USER MODE ring 3', 'Exit: 0'])
            REZULTAT['no_nic'] = računalnik.LOG_zapis.decode()
        finally: računalnik.Zapri()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            računalnik = navidezni_računalnik(보호커널(Path(임시)), mreža_VALUE=False)
            try:
                for Ime, stanje_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    računalnik.Ukaz('run ' + Ime, ['Exit: ' + str(stanje_VALUE)])
                    računalnik.Ukaz('run hello', ['USER MODE ring 3', 'Exit: 0'])
                REZULTAT['protection'] = računalnik.LOG_zapis.decode()
                print('PASS: uporabnik pomnilnik_podatki/strojna_oprema_vrata 격리, 잘못된 kazalec/ELF, CPU izjema, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (Položaj / 'build/Zaščita_preskusiti-last.log').write_bytes(računalnik.LOG_zapis)
                računalnik.Zapri()
    finally:
        Izhod_aplikacija.set()
        일꾼.join(timeout=2)
        strežnik_VALUE.close()
    REZULTAT['host_udp_received'] = [{'length': len(podatki), 'sha256': hashlib.sha256(podatki).hexdigest()} for podatki in RECEIVED_element]
    (Položaj / 'build/preskusiti_uporabnik_mreža.json').write_text(json.dumps(REZULTAT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Izvedi_ukaz()
