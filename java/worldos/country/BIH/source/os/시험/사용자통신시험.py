#!/usr/bin/env python3
"""стваран_подаци ring 3 ELF/хост_рачунар UDP 왕복/заштитити_вриједност грешка/시간 제한/잘못된 ELF를 검증한다."""
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
    def __init__(self, пут, 종류='elf', Мрежа_вриједност=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        директориј_вриједност = Path(self.임시.name)
        self.дневник_рада_ред = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монитор_вриједност = socket.socket(socket.AF_UNIX)
        직렬경로, монитор_пут = директориј_вриједност / 'serial.sock', директориј_вриједност / 'monitor.sock'
        команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_пут) + ',server,nowait']
        команда += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Мрежа_вриједност else ['-net', 'none']
        команда += ['-kernel', str(пут)] if 종류 == 'elf' else ['-cdrom', str(пут), '-boot', 'd']
        if 저장매체 is not None:
            команда += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.процес_вриједност = subprocess.Popen(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монитор_пут.exists()):
                if self.процес_вриједност.poll() is not None:
                    raise AssertionError(self.процес_вриједност.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU 시작 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монитор_вриједност.connect(str(монитор_пут))
            self.직렬.setblocking(False)
            self.монитор_вриједност.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.затворити()
            raise

    def 기다림(self, 문구, 시작=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.дневник_рада_ред[시작:]:
                return self.дневник_рада_ред[시작:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                подаци = self.직렬.recv(65536)
                if not подаци: break
                self.дневник_рада_ред.extend(подаци)
            if self.процес_вриједност.poll() is not None: break
        raise AssertionError('대기 неуспјех_вриједност: ' + 문구 + '\n' + self.дневник_рада_ред.decode('utf-8', 'replace'))

    def команда(self, стринг_вриједност, 기대):
        시작 = len(self.дневник_рада_ред)
        self.직렬.sendall((стринг_вриједност + '\n').encode())
        결과 = self.기다림('jkoros> ', 시작)
        for 문구 in 기대:
            assert 문구 in 결과, (стринг_вриједност, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def затворити(self):
        self.직렬.close()
        self.монитор_вриједност.close()
        if self.процес_вриједност.poll() is None:
            self.процес_вриједност.terminate()
            try: self.процес_вриједност.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.процес_вриједност.kill()
                self.процес_вриједност.wait()
        self.процес_вриједност.communicate()
        self.임시.cleanup()


def 보호커널(директориј_вриједност):
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
    for назив, Садржај_вриједност in 사례들.items():
        извор = директориј_вриједност / (назив + '.s')
        извор.write_text('.code32\n.text\n.globl _start\n_start:\n' + Садржај_вриједност +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(директориј_вриједност / (назив + '.o')), str(извор)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/корисник_веза_изглед.ld'),
                        '-o', str(директориј_вриједност / (назив + '.elf')), str(директориј_вриједност / (назив + '.o'))], check=True)
        항목들.append(назив + '=' + str(директориј_вриједност / (назив + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for назив, подаци in 변형들.items():
        фајл = директориј_вриједност / (назив + '.elf'); фајл.write_bytes(подаци)
        항목들.append(назив + '=' + str(фајл))
    subprocess.run([sys.executable, str(위치 / '도구/повезати_крајња_тачка_bbe6b410.py'), '-o', str(директориј_вриједност / 'apps.bin')] + 항목들, check=True)
    извор = директориј_вриједност / 'apps.s'
    извор.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(директориј_вриједност / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(директориј_вриједност / 'apps.o'), str(извор)], check=True)
    језгро_вриједност = директориј_вриједност / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/веза_изглед.ld'), '-o', str(језгро_вриједност),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(директориј_вриједност / 'apps.o')], check=True)
    return језгро_вриједност


def 실행():
    결과 = {}
    сервер_вриједност = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_вриједност.bind(('127.0.0.1', 0))
    сервер_вриједност.settimeout(0.1)
    порт_вриједност = сервер_вриједност.getsockname()[1]
    받은것 = []
    изаћи_програм = threading.Event()
    def 되보내기():
        while not изаћи_програм.is_set():
            try: подаци, peer_вриједност = сервер_вриједност.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(подаци)
            if подаци != b'drop-me': сервер_вриједност.sendto(подаци, peer_вриједност)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                기계.команда('apps', ['hello', 'udp', 'netcheck', 'stress'])
                기계.команда('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                기계.команда('run missing', ['Exit: -2'])
                기계.команда('net', ['NET RTL8139'])
                기계.команда('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Садржај_вриједност in ('hello-network', 'odd', 'even', 'repeat-123'):
                    기계.команда('run udp 10.0.2.2 {} {}'.format(порт_вриједност, Садржај_вриједност), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Садржај_вриједност.encode() in 받은것, 'хост_рачунар 서버에서 자료를 받지 못함'
                기계.команда('run stress {}'.format(порт_вриједност), ['UDP STRESS PASS', 'Exit: 0'])
                기계.команда('run udp 10.0.2.2 {} drop-me'.format(порт_вриједност), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                기계.команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.дневник_рада_ред.decode('utf-8', 'replace')
                print('PASS: {} корисник ELF/ring 3/인수/UDP хост_рачунар 왕복/시간 초과/љуска 복귀'.format(종류), flush=True)
            finally:
                try: 기계.команда('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(기계.дневник_рада_ред)
                기계.затворити()
        기계 = 가상기계(위치 / 'build/kernel.elf', Мрежа_вриједност=False)
        try:
            기계.команда('net', ['NET unavailable'])
            기계.команда('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            기계.команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = 기계.дневник_рада_ред.decode()
        finally: 기계.затворити()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            기계 = 가상기계(보호커널(Path(임시)), Мрежа_вриједност=False)
            try:
                for назив, стање_вриједност in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    기계.команда('run ' + назив, ['Exit: ' + str(стање_вриједност)])
                    기계.команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = 기계.дневник_рада_ред.decode()
                print('PASS: корисник меморија_подаци/포트 격리, 잘못된 포인터/ELF, CPU 예외, 무한 понављање_вриједност 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(기계.дневник_рада_ред)
                기계.затворити()
    finally:
        изаћи_програм.set()
        일꾼.join(timeout=2)
        сервер_вриједност.close()
    결과['host_udp_received'] = [{'length': len(подаци), 'sha256': hashlib.sha256(подаци).hexdigest()} for подаци in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    실행()
