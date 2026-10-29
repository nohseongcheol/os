#!/usr/bin/env python3
"""aktual_të_dhëna ring 3 ELF/pritës UDP 왕복/mbroj_VALUE GABIM/Ora_VALUE_4692cef5 제한/잘못된 ELF를 검증한다."""
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

Pozicioni = Path(__file__).resolve().parents[1]


class virtual_makinë:
    def __init__(self, POZICIONI, 종류='elf', rrjet_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        direktori_VALUE = Path(self.임시.name)
        self.LOG_RECORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_shteg = direktori_VALUE / 'serial.sock', direktori_VALUE / 'monitor.sock'
        Komanda = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_shteg) + ',server,nowait']
        Komanda += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if rrjet_VALUE else ['-net', 'none']
        Komanda += ['-kernel', str(POZICIONI)] if 종류 == 'elf' else ['-cdrom', str(POZICIONI), '-boot', 'd']
        if 저장매체 is not None:
            Komanda += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Proces_VALUE = subprocess.Popen(Komanda, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_shteg.exists()):
                if self.Proces_VALUE.poll() is not None:
                    raise AssertionError(self.Proces_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Ekzekuto Ora_VALUE_4692cef5 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_shteg))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.Prit_status('jkoros> ')
        except BaseException:
            self.Mbyll()
            raise

    def Prit_status(self, 문구, Ekzekuto=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_RECORD[Ekzekuto:]:
                return self.LOG_RECORD[Ekzekuto:].decode('utf-8', 'replace')
            Leximi, _, _ = select.select([self.직렬], [], [], 0.1)
            if Leximi:
                të_dhëna = self.직렬.recv(65536)
                if not të_dhëna: break
                self.LOG_RECORD.extend(të_dhëna)
            if self.Proces_VALUE.poll() is not None: break
        raise AssertionError('Prit_VALUE dështim_VALUE: ' + 문구 + '\n' + self.LOG_RECORD.decode('utf-8', 'replace'))

    def Komanda(self, varg_VALUE, 기대):
        Ekzekuto = len(self.LOG_RECORD)
        self.직렬.sendall((varg_VALUE + '\n').encode())
        llogaritje = self.Prit_status('jkoros> ', Ekzekuto)
        for 문구 in 기대:
            assert 문구 in llogaritje, (varg_VALUE, 문구, llogaritje)
        assert 'PANIC' not in llogaritje, llogaritje
        return llogaritje

    def Mbyll(self):
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


def 보호커널(direktori_VALUE):
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
    항목들 = ['hello=' + str(Pozicioni / 'build/apps/hello.elf')]
    for Emër, Përmbajtje_VALUE in 사례들.items():
        BURIMI = direktori_VALUE / (Emër + '.s')
        BURIMI.write_text('.code32\n.text\n.globl _start\n_start:\n' + Përmbajtje_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(direktori_VALUE / (Emër + '.o')), str(BURIMI)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozicioni.parent / 'compiler/përdorues_lidh_Navigimi.ld'),
                        '-o', str(direktori_VALUE / (Emër + '.elf')), str(direktori_VALUE / (Emër + '.o'))], check=True)
        항목들.append(Emër + '=' + str(direktori_VALUE / (Emër + '.elf')))
    정상 = bytearray((Pozicioni / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    i_pavlefshëm_llogaritje = bytearray(정상); i_pavlefshëm_llogaritje[0] = 0; 변형들['badelf'] = i_pavlefshëm_llogaritje
    i_pavlefshëm_llogaritje = bytearray(정상); struct.pack_into('<I', i_pavlefshëm_llogaritje, 24, 0x00100000); 변형들['badentry'] = i_pavlefshëm_llogaritje
    i_pavlefshëm_llogaritje = bytearray(정상); struct.pack_into('<I', i_pavlefshëm_llogaritje, 28, 0x7fffffff); 변형들['badtable'] = i_pavlefshëm_llogaritje
    i_pavlefshëm_llogaritje = bytearray(정상); LOOKUP_tabelë = struct.unpack_from('<I', i_pavlefshëm_llogaritje, 28)[0]
    struct.pack_into('<I', i_pavlefshëm_llogaritje, LOOKUP_tabelë + 20, 0x7fffffff); 변형들['badsize'] = i_pavlefshëm_llogaritje
    for Emër, të_dhëna in 변형들.items():
        Kartelë = direktori_VALUE / (Emër + '.elf'); Kartelë.write_bytes(të_dhëna)
        항목들.append(Emër + '=' + str(Kartelë))
    subprocess.run([sys.executable, str(Pozicioni / 'Mjete/묶기.py'), '-o', str(direktori_VALUE / 'apps.bin')] + 항목들, check=True)
    BURIMI = direktori_VALUE / 'apps.s'
    BURIMI.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(direktori_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(direktori_VALUE / 'apps.o'), str(BURIMI)], check=True)
    bërthamë_VALUE = direktori_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozicioni / '부팅/lidh_Navigimi.ld'), '-o', str(bërthamë_VALUE),
                    str(Pozicioni / 'build/boot.o'), str(Pozicioni / 'build/java.o'), str(Pozicioni / 'build/user.o'), str(direktori_VALUE / 'apps.o')], check=True)
    return bërthamë_VALUE


def zbatoj_komandë():
    llogaritje = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    portë_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_njësi = []
    dal_program = threading.Event()
    def 되보내기():
        while not dal_program.is_set():
            try: të_dhëna, homolog_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_njësi.append(të_dhëna)
            if të_dhëna != b'drop-me': server_VALUE.sendto(të_dhëna, homolog_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            makinë = virtual_makinë(Pozicioni / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                makinë.Komanda('apps', ['hello', 'udp', 'netcheck', 'stress'])
                makinë.Komanda('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                makinë.Komanda('run missing', ['Exit: -2'])
                makinë.Komanda('net', ['NET RTL8139'])
                makinë.Komanda('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Përmbajtje_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    makinë.Komanda('run udp 10.0.2.2 {} {}'.format(portë_VALUE, Përmbajtje_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Përmbajtje_VALUE.encode() in RECEIVED_njësi, 'pritës 서버에서 자료를 받지 못함'
                makinë.Komanda('run stress {}'.format(portë_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                makinë.Komanda('run udp 10.0.2.2 {} drop-me'.format(portë_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                makinë.Komanda('run hello recovered', ['arg: recovered', 'Exit: 0'])
                llogaritje[종류] = makinë.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS: {} përdorues ELF/ring 3/Argumente/UDP pritës 왕복/Ora_VALUE_4692cef5 초과/pasues 복귀'.format(종류), flush=True)
            finally:
                try: makinë.Komanda('net', [])
                except Exception: pass
                (Pozicioni / 'build/사용자통신-last.log').write_bytes(makinë.LOG_RECORD)
                makinë.Mbyll()
        makinë = virtual_makinë(Pozicioni / 'build/kernel.elf', rrjet_VALUE=False)
        try:
            makinë.Komanda('net', ['NET unavailable'])
            makinë.Komanda('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            makinë.Komanda('run hello', ['USER MODE ring 3', 'Exit: 0'])
            llogaritje['no_nic'] = makinë.LOG_RECORD.decode()
        finally: makinë.Mbyll()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            makinë = virtual_makinë(보호커널(Path(임시)), rrjet_VALUE=False)
            try:
                for Emër, status_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    makinë.Komanda('run ' + Emër, ['Exit: ' + str(status_VALUE)])
                    makinë.Komanda('run hello', ['USER MODE ring 3', 'Exit: 0'])
                llogaritje['protection'] = makinë.LOG_RECORD.decode()
                print('PASS: përdorues Memorie_të_dhëna/포트 격리, 잘못된 tregues/ELF, CPU përjashtim, 무한 përsëritje_VALUE 제한', flush=True)
            finally:
                (Pozicioni / 'build/보호시험-last.log').write_bytes(makinë.LOG_RECORD)
                makinë.Mbyll()
    finally:
        dal_program.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    llogaritje['host_udp_received'] = [{'length': len(të_dhëna), 'sha256': hashlib.sha256(të_dhëna).hexdigest()} for të_dhëna in RECEIVED_njësi]
    (Pozicioni / 'build/사용자통신시험.json').write_text(json.dumps(llogaritje, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    zbatoj_komandë()
