#!/usr/bin/env python3
"""laatii_keɓe ring 3 ELF/njaatigi UDP 왕복/suurde_njaru juumre/시간 제한/잘못된 ELF를 검증한다."""
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

위치 = Path(__file__).resolve().parents[1]


class 가상기계:
    def __init__(self, laawol, 종류='elf', laylaytol_njaru=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        mooftordu_njaru = Path(self.임시.name)
        self.suurnal_winndande = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.moniteer_njaru = socket.socket(socket.AF_UNIX)
        직렬경로, moniteer_laawol = mooftordu_njaru / 'serial.sock', mooftordu_njaru / 'monitor.sock'
        ginol = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(moniteer_laawol) + ',server,nowait']
        ginol += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if laylaytol_njaru else ['-net', 'none']
        ginol += ['-kernel', str(laawol)] if 종류 == 'elf' else ['-cdrom', str(laawol), '-boot', 'd']
        if 저장매체 is not None:
            ginol += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Yuɓɓo_golle_njaru = subprocess.Popen(ginol, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and moniteer_laawol.exists()):
                if self.Yuɓɓo_golle_njaru.poll() is not None:
                    raise AssertionError(self.Yuɓɓo_golle_njaru.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU huutoraade 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.moniteer_njaru.connect(str(moniteer_laawol))
            self.직렬.setblocking(False)
            self.moniteer_njaru.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.uddude()
            raise

    def 기다림(self, 문구, huutoraade=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.suurnal_winndande[huutoraade:]:
                return self.suurnal_winndande[huutoraade:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                keɓe = self.직렬.recv(65536)
                if not keɓe: break
                self.suurnal_winndande.extend(keɓe)
            if self.Yuɓɓo_golle_njaru.poll() is not None: break
        raise AssertionError('대기 ella_njaru: ' + 문구 + '\n' + self.suurnal_winndande.decode('utf-8', 'replace'))

    def ginol(self, ɓoggol_njaru, 기대):
        huutoraade = len(self.suurnal_winndande)
        self.직렬.sendall((ɓoggol_njaru + '\n').encode())
        결과 = self.기다림('jkoros> ', huutoraade)
        for 문구 in 기대:
            assert 문구 in 결과, (ɓoggol_njaru, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def uddude(self):
        self.직렬.close()
        self.moniteer_njaru.close()
        if self.Yuɓɓo_golle_njaru.poll() is None:
            self.Yuɓɓo_golle_njaru.terminate()
            try: self.Yuɓɓo_golle_njaru.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Yuɓɓo_golle_njaru.kill()
                self.Yuɓɓo_golle_njaru.wait()
        self.Yuɓɓo_golle_njaru.communicate()
        self.임시.cleanup()


def 보호커널(mooftordu_njaru):
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
    항목들 = ['hello=' + str(위치 / 'build/apps/hello.elf')]
    for innde, loowdi_njaru in 사례들.items():
        sewnde = mooftordu_njaru / (innde + '.s')
        sewnde.write_text('.code32\n.text\n.globl _start\n_start:\n' + loowdi_njaru +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(mooftordu_njaru / (innde + '.o')), str(sewnde)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/kuutoro_jokkere_lelngo.ld'),
                        '-o', str(mooftordu_njaru / (innde + '.elf')), str(mooftordu_njaru / (innde + '.o'))], check=True)
        항목들.append(innde + '=' + str(mooftordu_njaru / (innde + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for innde, keɓe in 변형들.items():
        fiilde = mooftordu_njaru / (innde + '.elf'); fiilde.write_bytes(keɓe)
        항목들.append(innde + '=' + str(fiilde))
    subprocess.run([sys.executable, str(위치 / '도구/묶기.py'), '-o', str(mooftordu_njaru / 'apps.bin')] + 항목들, check=True)
    sewnde = mooftordu_njaru / 'apps.s'
    sewnde.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(mooftordu_njaru / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(mooftordu_njaru / 'apps.o'), str(sewnde)], check=True)
    aaluude_njaru = mooftordu_njaru / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/jokkere_lelngo.ld'), '-o', str(aaluude_njaru),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(mooftordu_njaru / 'apps.o')], check=True)
    return aaluude_njaru


def 실행():
    결과 = {}
    sarworde_njaru = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sarworde_njaru.bind(('127.0.0.1', 0))
    sarworde_njaru.settimeout(0.1)
    poor_njaru = sarworde_njaru.getsockname()[1]
    받은것 = []
    yaltude_tafirde = threading.Event()
    def 되보내기():
        while not yaltude_tafirde.is_set():
            try: keɓe, giƴiraaɗo_njaru = sarworde_njaru.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(keɓe)
            if keɓe != b'drop-me': sarworde_njaru.sendto(keɓe, giƴiraaɗo_njaru)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                기계.ginol('apps', ['hello', 'udp', 'netcheck', 'stress'])
                기계.ginol('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                기계.ginol('run missing', ['Exit: -2'])
                기계.ginol('net', ['NET RTL8139'])
                기계.ginol('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for loowdi_njaru in ('hello-network', 'odd', 'even', 'repeat-123'):
                    기계.ginol('run udp 10.0.2.2 {} {}'.format(poor_njaru, loowdi_njaru), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert loowdi_njaru.encode() in 받은것, 'njaatigi 서버에서 자료를 받지 못함'
                기계.ginol('run stress {}'.format(poor_njaru), ['UDP STRESS PASS', 'Exit: 0'])
                기계.ginol('run udp 10.0.2.2 {} drop-me'.format(poor_njaru), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                기계.ginol('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.suurnal_winndande.decode('utf-8', 'replace')
                print('PASS: {} kuutoro ELF/ring 3/인수/UDP njaatigi 왕복/시간 초과/laalagal 복귀'.format(종류), flush=True)
            finally:
                try: 기계.ginol('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(기계.suurnal_winndande)
                기계.uddude()
        기계 = 가상기계(위치 / 'build/kernel.elf', laylaytol_njaru=False)
        try:
            기계.ginol('net', ['NET unavailable'])
            기계.ginol('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            기계.ginol('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = 기계.suurnal_winndande.decode()
        finally: 기계.uddude()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            기계 = 가상기계(보호커널(Path(임시)), laylaytol_njaru=False)
            try:
                for innde, ngonka_njaru in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    기계.ginol('run ' + innde, ['Exit: ' + str(ngonka_njaru)])
                    기계.ginol('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = 기계.suurnal_winndande.decode()
                print('PASS: kuutoro teskordu_keɓe/포트 격리, 잘못된 포인터/ELF, CPU 예외, 무한 반복 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(기계.suurnal_winndande)
                기계.uddude()
    finally:
        yaltude_tafirde.set()
        일꾼.join(timeout=2)
        sarworde_njaru.close()
    결과['host_udp_received'] = [{'length': len(keɓe), 'sha256': hashlib.sha256(keɓe).hexdigest()} for keɓe in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    실행()
