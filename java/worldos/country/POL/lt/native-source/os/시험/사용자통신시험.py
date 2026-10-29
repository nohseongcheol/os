#!/usr/bin/env python3
"""faktinis_duomenys ring 3 ELF/organizuoti UDP 왕복/apsaugoti_VALUE KLAIDA/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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


class VM:
    def __init__(self, KELIAS, 종류='elf', tinklas_VALUE=True, Saugykla_terpė=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Katalogas_VALUE = Path(self.임시.name)
        self.LOG_RECORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.stebėti_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, stebėti_kelias = Katalogas_VALUE / 'serial.sock', Katalogas_VALUE / 'monitor.sock'
        Komanda = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(stebėti_kelias) + ',server,nowait']
        Komanda += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if tinklas_VALUE else ['-net', 'none']
        Komanda += ['-kernel', str(KELIAS)] if 종류 == 'elf' else ['-cdrom', str(KELIAS), '-boot', 'd']
        if Saugykla_terpė is not None:
            Komanda += ['-drive', 'file=' + str(Saugykla_terpė) + ',format=raw,if=ide,index=0']
        self.Procesas_VALUE = subprocess.Popen(Komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and stebėti_kelias.exists()):
                if self.Procesas_VALUE.poll() is not None:
                    raise AssertionError(self.Procesas_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Paleisti TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.stebėti_VALUE.connect(str(stebėti_kelias))
            self.직렬.setblocking(False)
            self.stebėti_VALUE.sendall(b'cont\n')
            self.laukimo_būsena('jkoros> ')
        except BaseException:
            self.Užverti()
            raise

    def laukimo_būsena(self, 문구, Paleisti=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_RECORD[Paleisti:]:
                return self.LOG_RECORD[Paleisti:].decode('utf-8', 'replace')
            Skaitymas, _, _ = select.select([self.직렬], [], [], 0.1)
            if Skaitymas:
                duomenys = self.직렬.recv(65536)
                if not duomenys: break
                self.LOG_RECORD.extend(duomenys)
            if self.Procesas_VALUE.poll() is not None: break
        raise AssertionError('Palauk_VALUE triktis_VALUE: ' + 문구 + '\n' + self.LOG_RECORD.decode('utf-8', 'replace'))

    def Komanda(self, eilutė_VALUE, 기대):
        Paleisti = len(self.LOG_RECORD)
        self.직렬.sendall((eilutė_VALUE + '\n').encode())
        REZULTATAS = self.laukimo_būsena('jkoros> ', Paleisti)
        for 문구 in 기대:
            assert 문구 in REZULTATAS, (eilutė_VALUE, 문구, REZULTATAS)
        assert 'PANIC' not in REZULTATAS, REZULTATAS
        return REZULTATAS

    def Užverti(self):
        self.직렬.close()
        self.stebėti_VALUE.close()
        if self.Procesas_VALUE.poll() is None:
            self.Procesas_VALUE.terminate()
            try: self.Procesas_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Procesas_VALUE.kill()
                self.Procesas_VALUE.wait()
        self.Procesas_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(Katalogas_VALUE):
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
    for Pavadinimas_2, Turinys_VALUE in 사례들.items():
        ŠALTINIS = Katalogas_VALUE / (Pavadinimas_2 + '.s')
        ŠALTINIS.write_text('.code32\n.text\n.globl _start\n_start:\n' + Turinys_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Katalogas_VALUE / (Pavadinimas_2 + '.o')), str(ŠALTINIS)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozicija.parent / 'compiler/naudotojas_sieti_schema.ld'),
                        '-o', str(Katalogas_VALUE / (Pavadinimas_2 + '.elf')), str(Katalogas_VALUE / (Pavadinimas_2 + '.o'))], check=True)
        항목들.append(Pavadinimas_2 + '=' + str(Katalogas_VALUE / (Pavadinimas_2 + '.elf')))
    정상 = bytearray((Pozicija / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    neleistinas_KR = bytearray(정상); neleistinas_KR[0] = 0; 변형들['badelf'] = neleistinas_KR
    neleistinas_KR = bytearray(정상); struct.pack_into('<I', neleistinas_KR, 24, 0x00100000); 변형들['badentry'] = neleistinas_KR
    neleistinas_KR = bytearray(정상); struct.pack_into('<I', neleistinas_KR, 28, 0x7fffffff); 변형들['badtable'] = neleistinas_KR
    neleistinas_KR = bytearray(정상); LOOKUP_lentelė = struct.unpack_from('<I', neleistinas_KR, 28)[0]
    struct.pack_into('<I', neleistinas_KR, LOOKUP_lentelė + 20, 0x7fffffff); 변형들['badsize'] = neleistinas_KR
    for Pavadinimas_2, duomenys in 변형들.items():
        Failas = Katalogas_VALUE / (Pavadinimas_2 + '.elf'); Failas.write_bytes(duomenys)
        항목들.append(Pavadinimas_2 + '=' + str(Failas))
    subprocess.run([sys.executable, str(Pozicija / 'Įrankiai/BIND_dalyvis.py'), '-o', str(Katalogas_VALUE / 'apps.bin')] + 항목들, check=True)
    ŠALTINIS = Katalogas_VALUE / 'apps.s'
    ŠALTINIS.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Katalogas_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Katalogas_VALUE / 'apps.o'), str(ŠALTINIS)], check=True)
    branduolys_VALUE = Katalogas_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozicija / '부팅/sieti_schema.ld'), '-o', str(branduolys_VALUE),
                    str(Pozicija / 'build/boot.o'), str(Pozicija / 'build/java.o'), str(Pozicija / 'build/user.o'), str(Katalogas_VALUE / 'apps.o')], check=True)
    return branduolys_VALUE


def Vykdyti_komanda():
    REZULTATAS = {}
    serveris_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serveris_VALUE.bind(('127.0.0.1', 0))
    serveris_VALUE.settimeout(0.1)
    jungtis_VALUE = serveris_VALUE.getsockname()[1]
    RECEIVED_prekė = []
    Baigti_programa_086bb533 = threading.Event()
    def aidas_atsakyti():
        while not Baigti_programa_086bb533.is_set():
            try: duomenys, lygiavertis_mazgas_VALUE = serveris_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_prekė.append(duomenys)
            if duomenys != b'drop-me': serveris_VALUE.sendto(duomenys, lygiavertis_mazgas_VALUE)
    darbininkas_VALUE = threading.Thread(target=aidas_atsakyti, daemon=True)
    darbininkas_VALUE.start()
    try:
        for 종류 in ('elf', 'iso'):
            mašina = VM(Pozicija / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                mašina.Komanda('apps', ['hello', 'udp', 'netcheck', 'stress'])
                mašina.Komanda('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                mašina.Komanda('run missing', ['Exit: -2'])
                mašina.Komanda('net', ['NET RTL8139'])
                mašina.Komanda('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Turinys_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    mašina.Komanda('run udp 10.0.2.2 {} {}'.format(jungtis_VALUE, Turinys_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Turinys_VALUE.encode() in RECEIVED_prekė, 'organizuoti 서버에서 자료를 받지 못함'
                mašina.Komanda('run stress {}'.format(jungtis_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                mašina.Komanda('run udp 10.0.2.2 {} drop-me'.format(jungtis_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                mašina.Komanda('run hello recovered', ['arg: recovered', 'Exit: 0'])
                REZULTATAS[종류] = mašina.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS: {} naudotojas ELF/ring 3/Argumentai/UDP organizuoti 왕복/TIME_VALUE 초과/apvalkalas 복귀'.format(종류), flush=True)
            finally:
                try: mašina.Komanda('net', [])
                except Exception: pass
                (Pozicija / 'build/사용자통신-last.log').write_bytes(mašina.LOG_RECORD)
                mašina.Užverti()
        mašina = VM(Pozicija / 'build/kernel.elf', tinklas_VALUE=False)
        try:
            mašina.Komanda('net', ['NET unavailable'])
            mašina.Komanda('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            mašina.Komanda('run hello', ['USER MODE ring 3', 'Exit: 0'])
            REZULTATAS['no_nic'] = mašina.LOG_RECORD.decode()
        finally: mašina.Užverti()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            mašina = VM(보호커널(Path(임시)), tinklas_VALUE=False)
            try:
                for Pavadinimas_2, Būsena_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    mašina.Komanda('run ' + Pavadinimas_2, ['Exit: ' + str(Būsena_VALUE)])
                    mašina.Komanda('run hello', ['USER MODE ring 3', 'Exit: 0'])
                REZULTATAS['protection'] = mašina.LOG_RECORD.decode()
                print('PASS: naudotojas atmintis_duomenys/aparatūra_jungtis 격리, 잘못된 rodyklė/ELF, CPU išimtis, 무한 sprintas_VALUE 제한', flush=True)
            finally:
                (Pozicija / 'build/보호시험-last.log').write_bytes(mašina.LOG_RECORD)
                mašina.Užverti()
    finally:
        Baigti_programa_086bb533.set()
        darbininkas_VALUE.join(timeout=2)
        serveris_VALUE.close()
    REZULTATAS['host_udp_received'] = [{'length': len(duomenys), 'sha256': hashlib.sha256(duomenys).hexdigest()} for duomenys in RECEIVED_prekė]
    (Pozicija / 'build/사용자통신시험.json').write_text(json.dumps(REZULTATAS, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Vykdyti_komanda()
