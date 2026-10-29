#!/usr/bin/env python3
"""real_date ring 3 ELF/gazdă UDP 왕복/proteja_VALUE eroare/oră_VALUE 제한/잘못된 ELF를 검증한다."""
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

Poziție = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, Cale, 종류='elf', rețea_VALUE=True, Stocare_Mediu=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Director_VALUE = Path(self.임시.name)
        self.LOG_RECORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_cale = Director_VALUE / 'serial.sock', Director_VALUE / 'monitor.sock'
        Comandă = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_cale) + ',server,nowait']
        Comandă += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if rețea_VALUE else ['-net', 'none']
        Comandă += ['-kernel', str(Cale)] if 종류 == 'elf' else ['-cdrom', str(Cale), '-boot', 'd']
        if Stocare_Mediu is not None:
            Comandă += ['-drive', 'file=' + str(Stocare_Mediu) + ',format=raw,if=ide,index=0']
        self.Proces_VALUE = subprocess.Popen(Comandă, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_cale.exists()):
                if self.Proces_VALUE.poll() is not None:
                    raise AssertionError(self.Proces_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Pornește oră_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_cale))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.stare_de_așteptare('jkoros> ')
        except BaseException:
            self.Închide()
            raise

    def stare_de_așteptare(self, 문구, Pornește=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_RECORD[Pornește:]:
                return self.LOG_RECORD[Pornește:].decode('utf-8', 'replace')
            Citire, _, _ = select.select([self.직렬], [], [], 0.1)
            if Citire:
                date = self.직렬.recv(65536)
                if not date: break
                self.LOG_RECORD.extend(date)
            if self.Proces_VALUE.poll() is not None: break
        raise AssertionError('대기 eroare_VALUE: ' + 문구 + '\n' + self.LOG_RECORD.decode('utf-8', 'replace'))

    def Comandă(self, șir_VALUE, 기대):
        Pornește = len(self.LOG_RECORD)
        self.직렬.sendall((șir_VALUE + '\n').encode())
        KR = self.stare_de_așteptare('jkoros> ', Pornește)
        for 문구 in 기대:
            assert 문구 in KR, (șir_VALUE, 문구, KR)
        assert 'PANIC' not in KR, KR
        return KR

    def Închide(self):
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


def 보호커널(Director_VALUE):
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
    항목들 = ['hello=' + str(Poziție / 'build/apps/hello.elf')]
    for Nume, Conținut_VALUE in 사례들.items():
        SURSĂ = Director_VALUE / (Nume + '.s')
        SURSĂ.write_text('.code32\n.text\n.globl _start\n_start:\n' + Conținut_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Director_VALUE / (Nume + '.o')), str(SURSĂ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Poziție.parent / 'compiler/utilizator_Link_Aspect.ld'),
                        '-o', str(Director_VALUE / (Nume + '.elf')), str(Director_VALUE / (Nume + '.o'))], check=True)
        항목들.append(Nume + '=' + str(Director_VALUE / (Nume + '.elf')))
    정상 = bytearray((Poziție / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    nul_KR = bytearray(정상); nul_KR[0] = 0; 변형들['badelf'] = nul_KR
    nul_KR = bytearray(정상); struct.pack_into('<I', nul_KR, 24, 0x00100000); 변형들['badentry'] = nul_KR
    nul_KR = bytearray(정상); struct.pack_into('<I', nul_KR, 28, 0x7fffffff); 변형들['badtable'] = nul_KR
    nul_KR = bytearray(정상); tabel_de_căutare = struct.unpack_from('<I', nul_KR, 28)[0]
    struct.pack_into('<I', nul_KR, tabel_de_căutare + 20, 0x7fffffff); 변형들['badsize'] = nul_KR
    for Nume, date in 변형들.items():
        Fișier = Director_VALUE / (Nume + '.elf'); Fișier.write_bytes(date)
        항목들.append(Nume + '=' + str(Fișier))
    subprocess.run([sys.executable, str(Poziție / 'Instrumente/BIND_participant.py'), '-o', str(Director_VALUE / 'apps.bin')] + 항목들, check=True)
    SURSĂ = Director_VALUE / 'apps.s'
    SURSĂ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Director_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Director_VALUE / 'apps.o'), str(SURSĂ)], check=True)
    nucleu_VALUE = Director_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Poziție / '부팅/Link_Aspect.ld'), '-o', str(nucleu_VALUE),
                    str(Poziție / 'build/boot.o'), str(Poziție / 'build/java.o'), str(Poziție / 'build/user.o'), str(Director_VALUE / 'apps.o')], check=True)
    return nucleu_VALUE


def executa_comandă():
    KR = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    muta_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_element = []
    ieși_program = threading.Event()
    def ecou_replică():
        while not ieși_program.is_set():
            try: date, pereche_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_element.append(date)
            if date != b'drop-me': server_VALUE.sendto(date, pereche_VALUE)
    일꾼 = threading.Thread(target=ecou_replică, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mașină = VM(Poziție / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                mașină.Comandă('apps', ['hello', 'udp', 'netcheck', 'stress'])
                mașină.Comandă('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                mașină.Comandă('run missing', ['Exit: -2'])
                mașină.Comandă('net', ['NET RTL8139'])
                mașină.Comandă('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Conținut_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    mașină.Comandă('run udp 10.0.2.2 {} {}'.format(muta_VALUE, Conținut_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Conținut_VALUE.encode() in RECEIVED_element, 'gazdă 서버에서 자료를 받지 못함'
                mașină.Comandă('run stress {}'.format(muta_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                mașină.Comandă('run udp 10.0.2.2 {} drop-me'.format(muta_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                mașină.Comandă('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = mașină.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS: {} utilizator ELF/ring 3/Argumente/UDP gazdă 왕복/oră_VALUE 초과/shell 복귀'.format(종류), flush=True)
            finally:
                try: mașină.Comandă('net', [])
                except Exception: pass
                (Poziție / 'build/사용자통신-last.log').write_bytes(mașină.LOG_RECORD)
                mașină.Închide()
        mașină = VM(Poziție / 'build/kernel.elf', rețea_VALUE=False)
        try:
            mașină.Comandă('net', ['NET unavailable'])
            mașină.Comandă('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            mașină.Comandă('run hello', ['USER MODE ring 3', 'Exit: 0'])
            KR['no_nic'] = mașină.LOG_RECORD.decode()
        finally: mașină.Închide()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            mașină = VM(보호커널(Path(임시)), rețea_VALUE=False)
            try:
                for Nume, Stare_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    mașină.Comandă('run ' + Nume, ['Exit: ' + str(Stare_VALUE)])
                    mașină.Comandă('run hello', ['USER MODE ring 3', 'Exit: 0'])
                KR['protection'] = mașină.LOG_RECORD.decode()
                print('PASS: utilizator Memorie_date/포트 격리, 잘못된 cursor/ELF, CPU excepție, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (Poziție / 'build/보호시험-last.log').write_bytes(mașină.LOG_RECORD)
                mașină.Închide()
    finally:
        ieși_program.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    KR['host_udp_received'] = [{'length': len(date), 'sha256': hashlib.sha256(date).hexdigest()} for date in RECEIVED_element]
    (Poziție / 'build/사용자통신시험.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    executa_comandă()
