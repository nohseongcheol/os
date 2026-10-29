#!/usr/bin/env python3
"""실제 ring 3 ELF/호스트 UDP 왕복/보호 Kiremya/시간 제한/잘못된 ELF를 검증한다."""
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
    def __init__(self, 경로, 종류='elf', 망=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        폴더 = Path(self.임시.name)
        self.기록 = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.감시 = socket.socket(socket.AF_UNIX)
        직렬경로, 감시경로 = 폴더 / 'serial.sock', 폴더 / 'monitor.sock'
        Mulimu = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(감시경로) + ',server,nowait']
        Mulimu += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if 망 else ['-net', 'none']
        Mulimu += ['-kernel', str(경로)] if 종류 == 'elf' else ['-cdrom', str(경로), '-boot', 'd']
        if 저장매체 is not None:
            Mulimu += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.과정 = subprocess.Popen(Mulimu, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and 감시경로.exists()):
                if self.과정.poll() is not None:
                    raise AssertionError(self.과정.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Tandika 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.감시.connect(str(감시경로))
            self.직렬.setblocking(False)
            self.감시.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Bikka()
            raise

    def 기다림(self, 문구, Tandika=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.기록[Tandika:]:
                return self.기록[Tandika:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                자료 = self.직렬.recv(65536)
                if not 자료: break
                self.기록.extend(자료)
            if self.과정.poll() is not None: break
        raise AssertionError('대기 실패: ' + 문구 + '\n' + self.기록.decode('utf-8', 'replace'))

    def Mulimu(self, 문자열, 기대):
        Tandika = len(self.기록)
        self.직렬.sendall((문자열 + '\n').encode())
        KIGENDERWA = self.기다림('jkoros> ', Tandika)
        for 문구 in 기대:
            assert 문구 in KIGENDERWA, (문자열, 문구, KIGENDERWA)
        assert 'PANIC' not in KIGENDERWA, KIGENDERWA
        return KIGENDERWA

    def Bikka(self):
        self.직렬.close()
        self.감시.close()
        if self.과정.poll() is None:
            self.과정.terminate()
            try: self.과정.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.과정.kill()
                self.과정.wait()
        self.과정.communicate()
        self.임시.cleanup()


def 보호커널(폴더):
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
    for Linnya, 내용 in 사례들.items():
        NNONO = 폴더 / (Linnya + '.s')
        NNONO.write_text('.code32\n.text\n.globl _start\n_start:\n' + 내용 +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(폴더 / (Linnya + '.o')), str(NNONO)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/사용자배치.ld'),
                        '-o', str(폴더 / (Linnya + '.elf')), str(폴더 / (Linnya + '.o'))], check=True)
        항목들.append(Linnya + '=' + str(폴더 / (Linnya + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Linnya, 자료 in 변형들.items():
        Fayiro = 폴더 / (Linnya + '.elf'); Fayiro.write_bytes(자료)
        항목들.append(Linnya + '=' + str(Fayiro))
    subprocess.run([sys.executable, str(위치 / '도구/묶기.py'), '-o', str(폴더 / 'apps.bin')] + 항목들, check=True)
    NNONO = 폴더 / 'apps.s'
    NNONO.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(폴더 / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(폴더 / 'apps.o'), str(NNONO)], check=True)
    커널 = 폴더 / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/배치.ld'), '-o', str(커널),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(폴더 / 'apps.o')], check=True)
    return 커널


def 실행():
    KIGENDERWA = {}
    서버 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    서버.bind(('127.0.0.1', 0))
    서버.settimeout(0.1)
    창구 = 서버.getsockname()[1]
    받은것 = []
    종료 = threading.Event()
    def 되보내기():
        while not 종료.is_set():
            try: 자료, 상대 = 서버.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(자료)
            if 자료 != b'drop-me': 서버.sendto(자료, 상대)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                기계.Mulimu('apps', ['hello', 'udp', 'netcheck', 'stress'])
                기계.Mulimu('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                기계.Mulimu('run missing', ['Exit: -2'])
                기계.Mulimu('net', ['NET RTL8139'])
                기계.Mulimu('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for 내용 in ('hello-network', 'odd', 'even', 'repeat-123'):
                    기계.Mulimu('run udp 10.0.2.2 {} {}'.format(창구, 내용), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert 내용.encode() in 받은것, '호스트 서버에서 자료를 받지 못함'
                기계.Mulimu('run stress {}'.format(창구), ['UDP STRESS PASS', 'Exit: 0'])
                기계.Mulimu('run udp 10.0.2.2 {} drop-me'.format(창구), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                기계.Mulimu('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KIGENDERWA[종류] = 기계.기록.decode('utf-8', 'replace')
                print('PASS: {} 사용자 ELF/ring 3/인수/UDP 호스트 왕복/시간 초과/셸 복귀'.format(종류), flush=True)
            finally:
                try: 기계.Mulimu('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(기계.기록)
                기계.Bikka()
        기계 = 가상기계(위치 / 'build/kernel.elf', 망=False)
        try:
            기계.Mulimu('net', ['NET unavailable'])
            기계.Mulimu('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            기계.Mulimu('run hello', ['USER MODE ring 3', 'Exit: 0'])
            KIGENDERWA['no_nic'] = 기계.기록.decode()
        finally: 기계.Bikka()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            기계 = 가상기계(보호커널(Path(임시)), 망=False)
            try:
                for Linnya, 상태 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    기계.Mulimu('run ' + Linnya, ['Exit: ' + str(상태)])
                    기계.Mulimu('run hello', ['USER MODE ring 3', 'Exit: 0'])
                KIGENDERWA['protection'] = 기계.기록.decode()
                print('PASS: 사용자 메모리/포트 격리, 잘못된 포인터/ELF, CPU 예외, 무한 반복 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(기계.기록)
                기계.Bikka()
    finally:
        종료.set()
        일꾼.join(timeout=2)
        서버.close()
    KIGENDERWA['host_udp_received'] = [{'length': len(자료), 'sha256': hashlib.sha256(자료).hexdigest()} for 자료 in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(KIGENDERWA, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    실행()
