#!/usr/bin/env python3
"""skutočný_údaje ring 3 ELF/hostiteľ UDP 왕복/chrániť_VALUE chyba/čas_VALUE 제한/잘못된 ELF를 검증한다."""
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

Pozícia = Path(__file__).resolve().parents[1]


class virtuálny_počítač:
    def __init__(self, Cesta, 종류='elf', sieť_VALUE=True, Úložisko_médium=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Adresár_VALUE = Path(self.임시.name)
        self.LOG_RECORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_cesta = Adresár_VALUE / 'serial.sock', Adresár_VALUE / 'monitor.sock'
        Príkaz = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_cesta) + ',server,nowait']
        Príkaz += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if sieť_VALUE else ['-net', 'none']
        Príkaz += ['-kernel', str(Cesta)] if 종류 == 'elf' else ['-cdrom', str(Cesta), '-boot', 'd']
        if Úložisko_médium is not None:
            Príkaz += ['-drive', 'file=' + str(Úložisko_médium) + ',format=raw,if=ide,index=0']
        self.Proces_VALUE = subprocess.Popen(Príkaz, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_cesta.exists()):
                if self.Proces_VALUE.poll() is not None:
                    raise AssertionError(self.Proces_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Spustiť_2 čas_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_cesta))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.stav_čakania('jkoros> ')
        except BaseException:
            self.Zatvoriť()
            raise

    def stav_čakania(self, 문구, Spustiť_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_RECORD[Spustiť_2:]:
                return self.LOG_RECORD[Spustiť_2:].decode('utf-8', 'replace')
            Čítanie, _, _ = select.select([self.직렬], [], [], 0.1)
            if Čítanie:
                údaje = self.직렬.recv(65536)
                if not údaje: break
                self.LOG_RECORD.extend(údaje)
            if self.Proces_VALUE.poll() is not None: break
        raise AssertionError('počkaj_VALUE zlyhanie_VALUE: ' + 문구 + '\n' + self.LOG_RECORD.decode('utf-8', 'replace'))

    def Príkaz(self, reťazec_VALUE, 기대):
        Spustiť_2 = len(self.LOG_RECORD)
        self.직렬.sendall((reťazec_VALUE + '\n').encode())
        KR = self.stav_čakania('jkoros> ', Spustiť_2)
        for 문구 in 기대:
            assert 문구 in KR, (reťazec_VALUE, 문구, KR)
        assert 'PANIC' not in KR, KR
        return KR

    def Zatvoriť(self):
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


def 보호커널(Adresár_VALUE):
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
    항목들 = ['hello=' + str(Pozícia / 'build/apps/hello.elf')]
    for Názov, obsah_VALUE in 사례들.items():
        ZDROJ = Adresár_VALUE / (Názov + '.s')
        ZDROJ.write_text('.code32\n.text\n.globl _start\n_start:\n' + obsah_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Adresár_VALUE / (Názov + '.o')), str(ZDROJ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozícia.parent / 'compiler/používateľ_odkaz_Navigácia.ld'),
                        '-o', str(Adresár_VALUE / (Názov + '.elf')), str(Adresár_VALUE / (Názov + '.o'))], check=True)
        항목들.append(Názov + '=' + str(Adresár_VALUE / (Názov + '.elf')))
    정상 = bytearray((Pozícia / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    neplatné_KR = bytearray(정상); neplatné_KR[0] = 0; 변형들['badelf'] = neplatné_KR
    neplatné_KR = bytearray(정상); struct.pack_into('<I', neplatné_KR, 24, 0x00100000); 변형들['badentry'] = neplatné_KR
    neplatné_KR = bytearray(정상); struct.pack_into('<I', neplatné_KR, 28, 0x7fffffff); 변형들['badtable'] = neplatné_KR
    neplatné_KR = bytearray(정상); vyhľadávacia_tabuľka = struct.unpack_from('<I', neplatné_KR, 28)[0]
    struct.pack_into('<I', neplatné_KR, vyhľadávacia_tabuľka + 20, 0x7fffffff); 변형들['badsize'] = neplatné_KR
    for Názov, údaje in 변형들.items():
        Súbor = Adresár_VALUE / (Názov + '.elf'); Súbor.write_bytes(údaje)
        항목들.append(Názov + '=' + str(Súbor))
    subprocess.run([sys.executable, str(Pozícia / 'Nástroje/BIND_účastník.py'), '-o', str(Adresár_VALUE / 'apps.bin')] + 항목들, check=True)
    ZDROJ = Adresár_VALUE / 'apps.s'
    ZDROJ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Adresár_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Adresár_VALUE / 'apps.o'), str(ZDROJ)], check=True)
    jadro_VALUE = Adresár_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozícia / '부팅/odkaz_Navigácia.ld'), '-o', str(jadro_VALUE),
                    str(Pozícia / 'build/boot.o'), str(Pozícia / 'build/java.o'), str(Pozícia / 'build/user.o'), str(Adresár_VALUE / 'apps.o')], check=True)
    return jadro_VALUE


def Vykonať_príkaz():
    KR = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_položka = []
    Skončiť_program = threading.Event()
    def ozvena_odozva():
        while not Skončiť_program.is_set():
            try: údaje, partnerský_uzol_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_položka.append(údaje)
            if údaje != b'drop-me': server_VALUE.sendto(údaje, partnerský_uzol_VALUE)
    일꾼 = threading.Thread(target=ozvena_odozva, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            počítač_5eb260fa = virtuálny_počítač(Pozícia / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                počítač_5eb260fa.Príkaz('apps', ['hello', 'udp', 'netcheck', 'stress'])
                počítač_5eb260fa.Príkaz('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                počítač_5eb260fa.Príkaz('run missing', ['Exit: -2'])
                počítač_5eb260fa.Príkaz('net', ['NET RTL8139'])
                počítač_5eb260fa.Príkaz('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for obsah_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    počítač_5eb260fa.Príkaz('run udp 10.0.2.2 {} {}'.format(port_VALUE, obsah_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert obsah_VALUE.encode() in RECEIVED_položka, 'hostiteľ 서버에서 자료를 받지 못함'
                počítač_5eb260fa.Príkaz('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                počítač_5eb260fa.Príkaz('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                počítač_5eb260fa.Príkaz('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = počítač_5eb260fa.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS: {} používateľ ELF/ring 3/Argumenty/UDP hostiteľ 왕복/čas_VALUE 초과/셸 복귀'.format(종류), flush=True)
            finally:
                try: počítač_5eb260fa.Príkaz('net', [])
                except Exception: pass
                (Pozícia / 'build/사용자통신-last.log').write_bytes(počítač_5eb260fa.LOG_RECORD)
                počítač_5eb260fa.Zatvoriť()
        počítač_5eb260fa = virtuálny_počítač(Pozícia / 'build/kernel.elf', sieť_VALUE=False)
        try:
            počítač_5eb260fa.Príkaz('net', ['NET unavailable'])
            počítač_5eb260fa.Príkaz('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            počítač_5eb260fa.Príkaz('run hello', ['USER MODE ring 3', 'Exit: 0'])
            KR['no_nic'] = počítač_5eb260fa.LOG_RECORD.decode()
        finally: počítač_5eb260fa.Zatvoriť()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            počítač_5eb260fa = virtuálny_počítač(보호커널(Path(임시)), sieť_VALUE=False)
            try:
                for Názov, Stav_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    počítač_5eb260fa.Príkaz('run ' + Názov, ['Exit: ' + str(Stav_VALUE)])
                    počítač_5eb260fa.Príkaz('run hello', ['USER MODE ring 3', 'Exit: 0'])
                KR['protection'] = počítač_5eb260fa.LOG_RECORD.decode()
                print('PASS: používateľ Pamäť_údaje/hardvér_port 격리, 잘못된 ukazovateľ/ELF, CPU výnimka, 무한 šprint_VALUE 제한', flush=True)
            finally:
                (Pozícia / 'build/Ochrana_test-last.log').write_bytes(počítač_5eb260fa.LOG_RECORD)
                počítač_5eb260fa.Zatvoriť()
    finally:
        Skončiť_program.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    KR['host_udp_received'] = [{'length': len(údaje), 'sha256': hashlib.sha256(údaje).hexdigest()} for údaje in RECEIVED_položka]
    (Pozícia / 'build/test_používateľ_sieť.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Vykonať_príkaz()
