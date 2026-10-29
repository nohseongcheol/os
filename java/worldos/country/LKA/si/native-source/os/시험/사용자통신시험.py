#!/usr/bin/env python3
"""තථ්_ය_දත්ත ring 3 ELF/ධාරකය UDP 왕복/ආරක්ෂා_කරන්න_අගය දෝෂය/시간 제한/잘못된 ELF를 검증한다."""
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

පිහිටීම = Path(__file__).resolve().parents[1]


class අතථ්_ය_යන්ත්_රය:
    def __init__(self, මාර්_ගය, 종류='elf', ජාලය_අගය=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        නාමාවලිය_අගය = Path(self.임시.name)
        self.ලොගය_පේළිය = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.මොනිටරය_අගය = socket.socket(socket.AF_UNIX)
        직렬경로, මොනිටරය_පෙත = නාමාවලිය_අගය / 'serial.sock', නාමාවලිය_අගය / 'monitor.sock'
        විධානය = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(මොනිටරය_පෙත) + ',server,nowait']
        විධානය += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ජාලය_අගය else ['-net', 'none']
        විධානය += ['-kernel', str(මාර්_ගය)] if 종류 == 'elf' else ['-cdrom', str(මාර්_ගය), '-boot', 'd']
        if 저장매체 is not None:
            විධානය += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ක්_රියාවලිය_අගය = subprocess.Popen(විධානය, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and මොනිටරය_පෙත.exists()):
                if self.ක්_රියාවලිය_අගය.poll() is not None:
                    raise AssertionError(self.ක්_රියාවලිය_අගය.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ක්_රියාත්මක_කරන්න_2 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.මොනිටරය_අගය.connect(str(මොනිටරය_පෙත))
            self.직렬.setblocking(False)
            self.මොනිටරය_අගය.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.වසන්න()
            raise

    def 기다림(self, 문구, ක්_රියාත්මක_කරන්න_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:]:
                return self.ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:].decode('utf-8', 'replace')
            කියවීම, _, _ = select.select([self.직렬], [], [], 0.1)
            if කියවීම:
                දත්ත = self.직렬.recv(65536)
                if not දත්ත: break
                self.ලොගය_පේළිය.extend(දත්ත)
            if self.ක්_රියාවලිය_අගය.poll() is not None: break
        raise AssertionError('대기 අසමත්වීම_අගය: ' + 문구 + '\n' + self.ලොගය_පේළිය.decode('utf-8', 'replace'))

    def විධානය(self, අනුලකුණු_වැල_අගය, 기대):
        ක්_රියාත්මක_කරන්න_2 = len(self.ලොගය_පේළිය)
        self.직렬.sendall((අනුලකුණු_වැල_අගය + '\n').encode())
        결과 = self.기다림('jkoros> ', ක්_රියාත්මක_කරන්න_2)
        for 문구 in 기대:
            assert 문구 in 결과, (අනුලකුණු_වැල_අගය, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def වසන්න(self):
        self.직렬.close()
        self.මොනිටරය_අගය.close()
        if self.ක්_රියාවලිය_අගය.poll() is None:
            self.ක්_රියාවලිය_අගය.terminate()
            try: self.ක්_රියාවලිය_අගය.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ක්_රියාවලිය_අගය.kill()
                self.ක්_රියාවලිය_අගය.wait()
        self.ක්_රියාවලිය_අගය.communicate()
        self.임시.cleanup()


def 보호커널(නාමාවලිය_අගය):
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
    항목들 = ['hello=' + str(පිහිටීම / 'build/apps/hello.elf')]
    for නම, අන්තර්ගතය_අගය in 사례들.items():
        මූලය = නාමාවලිය_අගය / (නම + '.s')
        මූලය.write_text('.code32\n.text\n.globl _start\n_start:\n' + අන්තර්ගතය_අගය +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(නාමාවලිය_අගය / (නම + '.o')), str(මූලය)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(පිහිටීම.parent / 'compiler/පරිශීලක_සබැඳිය_සැකැස්ම.ld'),
                        '-o', str(නාමාවලිය_අගය / (නම + '.elf')), str(නාමාවලිය_අගය / (නම + '.o'))], check=True)
        항목들.append(නම + '=' + str(නාමාවලිය_අගය / (නම + '.elf')))
    정상 = bytearray((පිහිටීම / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for නම, දත්ත in 변형들.items():
        ගොනු = නාමාවලිය_අගය / (නම + '.elf'); ගොනු.write_bytes(දත්ත)
        항목들.append(නම + '=' + str(ගොනු))
    subprocess.run([sys.executable, str(පිහිටීම / 'මෙවලම්/묶기.py'), '-o', str(නාමාවලිය_අගය / 'apps.bin')] + 항목들, check=True)
    මූලය = නාමාවලිය_අගය / 'apps.s'
    මූලය.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(නාමාවලිය_අගය / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(නාමාවලිය_අගය / 'apps.o'), str(මූලය)], check=True)
    කර්නලය_අගය = නාමාවලිය_අගය / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(පිහිටීම / '부팅/සබැඳිය_සැකැස්ම.ld'), '-o', str(කර්නලය_අගය),
                    str(පිහිටීම / 'build/boot.o'), str(පිහිටීම / 'build/java.o'), str(පිහිටීම / 'build/user.o'), str(නාමාවලිය_අගය / 'apps.o')], check=True)
    return කර්නලය_අගය


def ක්_රියාත්මක_කරන්න_විධානය():
    결과 = {}
    සේවාදායකය_අගය = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    සේවාදායකය_අගය.bind(('127.0.0.1', 0))
    සේවාදායකය_අගය.settimeout(0.1)
    තොට_අගය = සේවාදායකය_අගය.getsockname()[1]
    받은것 = []
    පිටවීම_යෙදු = threading.Event()
    def 되보내기():
        while not පිටවීම_යෙදු.is_set():
            try: දත්ත, සමානයා_අගය = සේවාදායකය_අගය.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(දත්ත)
            if දත්ත != b'drop-me': සේවාදායකය_අගය.sendto(දත්ත, සමානයා_අගය)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                යන්ත්_රය.විධානය('apps', ['hello', 'udp', 'netcheck', 'stress'])
                යන්ත්_රය.විධානය('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                යන්ත්_රය.විධානය('run missing', ['Exit: -2'])
                යන්ත්_රය.විධානය('net', ['NET RTL8139'])
                යන්ත්_රය.විධානය('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for අන්තර්ගතය_අගය in ('hello-network', 'odd', 'even', 'repeat-123'):
                    යන්ත්_රය.විධානය('run udp 10.0.2.2 {} {}'.format(තොට_අගය, අන්තර්ගතය_අගය), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert අන්තර්ගතය_අගය.encode() in 받은것, 'ධාරකය 서버에서 자료를 받지 못함'
                යන්ත්_රය.විධානය('run stress {}'.format(තොට_අගය), ['UDP STRESS PASS', 'Exit: 0'])
                යන්ත්_රය.විධානය('run udp 10.0.2.2 {} drop-me'.format(තොට_අගය), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                යන්ත්_රය.විධානය('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = යන්ත්_රය.ලොගය_පේළිය.decode('utf-8', 'replace')
                print('PASS: {} පරිශීලක ELF/ring 3/විස්තාරක/UDP ධාරකය 왕복/시간 초과/කවචය 복귀'.format(종류), flush=True)
            finally:
                try: යන්ත්_රය.විධානය('net', [])
                except Exception: pass
                (පිහිටීම / 'build/사용자통신-last.log').write_bytes(යන්ත්_රය.ලොගය_පේළිය)
                යන්ත්_රය.වසන්න()
        යන්ත්_රය = අතථ්_ය_යන්ත්_රය(පිහිටීම / 'build/kernel.elf', ජාලය_අගය=False)
        try:
            යන්ත්_රය.විධානය('net', ['NET unavailable'])
            යන්ත්_රය.විධානය('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            යන්ත්_රය.විධානය('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = යන්ත්_රය.ලොගය_පේළිය.decode()
        finally: යන්ත්_රය.වසන්න()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            යන්ත්_රය = අතථ්_ය_යන්ත්_රය(보호커널(Path(임시)), ජාලය_අගය=False)
            try:
                for නම, තත්වය_අගය in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    යන්ත්_රය.විධානය('run ' + නම, ['Exit: ' + str(තත්වය_අගය)])
                    යන්ත්_රය.විධානය('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = යන්ත්_රය.ලොගය_පේළිය.decode()
                print('PASS: පරිශීලක මතකය_දත්ත/포트 격리, 잘못된 පොයින්ටරය/ELF, CPU 예외, 무한 පුනර්කරණය_අගය 제한', flush=True)
            finally:
                (පිහිටීම / 'build/보호시험-last.log').write_bytes(යන්ත්_රය.ලොගය_පේළිය)
                යන්ත්_රය.වසන්න()
    finally:
        පිටවීම_යෙදු.set()
        일꾼.join(timeout=2)
        සේවාදායකය_අගය.close()
    결과['host_udp_received'] = [{'length': len(දත්ත), 'sha256': hashlib.sha256(දත්ත).hexdigest()} for දත්ත in 받은것]
    (පිහිටීම / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_විධානය()
