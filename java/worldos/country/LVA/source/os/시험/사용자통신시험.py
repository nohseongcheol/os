#!/usr/bin/env python3
"""faktisks_dati ring 3 ELF/viesot UDP 왕복/aizsargāt_VALUE Kļūda/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

Novietojums = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, CEĻŠ, 종류='elf', tīkls_VALUE=True, Krātuve_vide=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Direktorijs_VALUE = Path(self.임시.name)
        self.LOG_RECORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitors_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitors_ceļš = Direktorijs_VALUE / 'serial.sock', Direktorijs_VALUE / 'monitor.sock'
        Komanda = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitors_ceļš) + ',server,nowait']
        Komanda += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if tīkls_VALUE else ['-net', 'none']
        Komanda += ['-kernel', str(CEĻŠ)] if 종류 == 'elf' else ['-cdrom', str(CEĻŠ), '-boot', 'd']
        if Krātuve_vide is not None:
            Komanda += ['-drive', 'file=' + str(Krātuve_vide) + ',format=raw,if=ide,index=0']
        self.Process_VALUE = subprocess.Popen(Komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitors_ceļš.exists()):
                if self.Process_VALUE.poll() is not None:
                    raise AssertionError(self.Process_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Palaist TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitors_VALUE.connect(str(monitors_ceļš))
            self.직렬.setblocking(False)
            self.monitors_VALUE.sendall(b'cont\n')
            self.nogaides_stāvoklis('jkoros> ')
        except BaseException:
            self.Aizvērt()
            raise

    def nogaides_stāvoklis(self, 문구, Palaist=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_RECORD[Palaist:]:
                return self.LOG_RECORD[Palaist:].decode('utf-8', 'replace')
            Lasīt, _, _ = select.select([self.직렬], [], [], 0.1)
            if Lasīt:
                dati = self.직렬.recv(65536)
                if not dati: break
                self.LOG_RECORD.extend(dati)
            if self.Process_VALUE.poll() is not None: break
        raise AssertionError('pagaidi_VALUE kļūme_VALUE: ' + 문구 + '\n' + self.LOG_RECORD.decode('utf-8', 'replace'))

    def Komanda(self, virkne_VALUE, 기대):
        Palaist = len(self.LOG_RECORD)
        self.직렬.sendall((virkne_VALUE + '\n').encode())
        mērs = self.nogaides_stāvoklis('jkoros> ', Palaist)
        for 문구 in 기대:
            assert 문구 in mērs, (virkne_VALUE, 문구, mērs)
        assert 'PANIC' not in mērs, mērs
        return mērs

    def Aizvērt(self):
        self.직렬.close()
        self.monitors_VALUE.close()
        if self.Process_VALUE.poll() is None:
            self.Process_VALUE.terminate()
            try: self.Process_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Process_VALUE.kill()
                self.Process_VALUE.wait()
        self.Process_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(Direktorijs_VALUE):
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
    항목들 = ['hello=' + str(Novietojums / 'build/apps/hello.elf')]
    for Nosaukums, Saturs_VALUE in 사례들.items():
        AVOTS = Direktorijs_VALUE / (Nosaukums + '.s')
        AVOTS.write_text('.code32\n.text\n.globl _start\n_start:\n' + Saturs_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Direktorijs_VALUE / (Nosaukums + '.o')), str(AVOTS)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Novietojums.parent / 'compiler/lietotājs_Saite_shēma.ld'),
                        '-o', str(Direktorijs_VALUE / (Nosaukums + '.elf')), str(Direktorijs_VALUE / (Nosaukums + '.o'))], check=True)
        항목들.append(Nosaukums + '=' + str(Direktorijs_VALUE / (Nosaukums + '.elf')))
    정상 = bytearray((Novietojums / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    nederīgs_mērs = bytearray(정상); nederīgs_mērs[0] = 0; 변형들['badelf'] = nederīgs_mērs
    nederīgs_mērs = bytearray(정상); struct.pack_into('<I', nederīgs_mērs, 24, 0x00100000); 변형들['badentry'] = nederīgs_mērs
    nederīgs_mērs = bytearray(정상); struct.pack_into('<I', nederīgs_mērs, 28, 0x7fffffff); 변형들['badtable'] = nederīgs_mērs
    nederīgs_mērs = bytearray(정상); LOOKUP_tabula = struct.unpack_from('<I', nederīgs_mērs, 28)[0]
    struct.pack_into('<I', nederīgs_mērs, LOOKUP_tabula + 20, 0x7fffffff); 변형들['badsize'] = nederīgs_mērs
    for Nosaukums, dati in 변형들.items():
        Fails = Direktorijs_VALUE / (Nosaukums + '.elf'); Fails.write_bytes(dati)
        항목들.append(Nosaukums + '=' + str(Fails))
    subprocess.run([sys.executable, str(Novietojums / 'Rīki/BIND_dalībnieks.py'), '-o', str(Direktorijs_VALUE / 'apps.bin')] + 항목들, check=True)
    AVOTS = Direktorijs_VALUE / 'apps.s'
    AVOTS.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Direktorijs_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Direktorijs_VALUE / 'apps.o'), str(AVOTS)], check=True)
    kodols_VALUE = Direktorijs_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Novietojums / '부팅/Saite_shēma.ld'), '-o', str(kodols_VALUE),
                    str(Novietojums / 'build/boot.o'), str(Novietojums / 'build/java.o'), str(Novietojums / 'build/user.o'), str(Direktorijs_VALUE / 'apps.o')], check=True)
    return kodols_VALUE


def Izpildīt_komanda():
    mērs = {}
    serveris_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serveris_VALUE.bind(('127.0.0.1', 0))
    serveris_VALUE.settimeout(0.1)
    ports_VALUE = serveris_VALUE.getsockname()[1]
    RECEIVED_krājums = []
    Iziet_programma = threading.Event()
    def atbalss_atbilde():
        while not Iziet_programma.is_set():
            try: dati, vienranga_VALUE = serveris_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_krājums.append(dati)
            if dati != b'drop-me': serveris_VALUE.sendto(dati, vienranga_VALUE)
    nodarbinātais_VALUE = threading.Thread(target=atbalss_atbilde, daemon=True)
    nodarbinātais_VALUE.start()
    try:
        for 종류 in ('elf', 'iso'):
            mašīna = VM(Novietojums / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                mašīna.Komanda('apps', ['hello', 'udp', 'netcheck', 'stress'])
                mašīna.Komanda('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                mašīna.Komanda('run missing', ['Exit: -2'])
                mašīna.Komanda('net', ['NET RTL8139'])
                mašīna.Komanda('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Saturs_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    mašīna.Komanda('run udp 10.0.2.2 {} {}'.format(ports_VALUE, Saturs_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Saturs_VALUE.encode() in RECEIVED_krājums, 'viesot 서버에서 자료를 받지 못함'
                mašīna.Komanda('run stress {}'.format(ports_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                mašīna.Komanda('run udp 10.0.2.2 {} drop-me'.format(ports_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                mašīna.Komanda('run hello recovered', ['arg: recovered', 'Exit: 0'])
                mērs[종류] = mašīna.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS: {} lietotājs ELF/ring 3/Parametri/UDP viesot 왕복/TIME_VALUE 초과/čaula 복귀'.format(종류), flush=True)
            finally:
                try: mašīna.Komanda('net', [])
                except Exception: pass
                (Novietojums / 'build/사용자통신-last.log').write_bytes(mašīna.LOG_RECORD)
                mašīna.Aizvērt()
        mašīna = VM(Novietojums / 'build/kernel.elf', tīkls_VALUE=False)
        try:
            mašīna.Komanda('net', ['NET unavailable'])
            mašīna.Komanda('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            mašīna.Komanda('run hello', ['USER MODE ring 3', 'Exit: 0'])
            mērs['no_nic'] = mašīna.LOG_RECORD.decode()
        finally: mašīna.Aizvērt()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            mašīna = VM(보호커널(Path(임시)), tīkls_VALUE=False)
            try:
                for Nosaukums, Statuss_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    mašīna.Komanda('run ' + Nosaukums, ['Exit: ' + str(Statuss_VALUE)])
                    mašīna.Komanda('run hello', ['USER MODE ring 3', 'Exit: 0'])
                mērs['protection'] = mašīna.LOG_RECORD.decode()
                print('PASS: lietotājs atmiņa_dati/포트 격리, 잘못된 rādītājs/ELF, CPU izņēmums, 무한 sprints_VALUE 제한', flush=True)
            finally:
                (Novietojums / 'build/보호시험-last.log').write_bytes(mašīna.LOG_RECORD)
                mašīna.Aizvērt()
    finally:
        Iziet_programma.set()
        nodarbinātais_VALUE.join(timeout=2)
        serveris_VALUE.close()
    mērs['host_udp_received'] = [{'length': len(dati), 'sha256': hashlib.sha256(dati).hexdigest()} for dati in RECEIVED_krājums]
    (Novietojums / 'build/사용자통신시험.json').write_text(json.dumps(mērs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Izpildīt_komanda()
