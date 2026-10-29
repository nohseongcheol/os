#!/usr/bin/env python3
"""ನಿಜವಾದ_ಡೇಟಾ ring 3 ELF/ಹೋಸ್ಟ್ UDP 왕복/ರಕ್ಷಿಸಿ_ಮೌಲ್ಯ ದೋಷ/ಸಮಯ_ಮೌಲ್ಯ 제한/잘못된 ELF를 검증한다."""
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

ಸ್ಥಾನ = Path(__file__).resolve().parents[1]


class ಅಗೋಚರ_ಯಂತ್ರ:
    def __init__(self, ಮಾರ್ಗ, 종류='elf', ನೆಟ್_ವರ್ಕ್_ಮೌಲ್ಯ=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ = Path(self.임시.name)
        self.ಲಾಗ್_ದಾಖಲೆ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.ಮಾನಿಟರ್_ಮೌಲ್ಯ = socket.socket(socket.AF_UNIX)
        직렬경로, ಮಾನಿಟರ್_ಹಾದಿ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'serial.sock', ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'monitor.sock'
        ಆಜ್ಞೆ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ಮಾನಿಟರ್_ಹಾದಿ) + ',server,nowait']
        ಆಜ್ಞೆ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ನೆಟ್_ವರ್ಕ್_ಮೌಲ್ಯ else ['-net', 'none']
        ಆಜ್ಞೆ += ['-kernel', str(ಮಾರ್ಗ)] if 종류 == 'elf' else ['-cdrom', str(ಮಾರ್ಗ), '-boot', 'd']
        if 저장매체 is not None:
            ಆಜ್ಞೆ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = subprocess.Popen(ಆಜ್ಞೆ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and ಮಾನಿಟರ್_ಹಾದಿ.exists()):
                if self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None:
                    raise AssertionError(self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ಚಲಾಯಿಸು_2 ಸಮಯ_ಮೌಲ್ಯ 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.ಮಾನಿಟರ್_ಮೌಲ್ಯ.connect(str(ಮಾನಿಟರ್_ಹಾದಿ))
            self.직렬.setblocking(False)
            self.ಮಾನಿಟರ್_ಮೌಲ್ಯ.sendall(b'cont\n')
            self.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('jkoros> ')
        except BaseException:
            self.ಮುಚ್ಚು()
            raise

    def ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ(self, 문구, ಚಲಾಯಿಸು_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:]:
                return self.ಲಾಗ್_ದಾಖಲೆ[ಚಲಾಯಿಸು_2:].decode('utf-8', 'replace')
            ಓದು, _, _ = select.select([self.직렬], [], [], 0.1)
            if ಓದು:
                ಡೇಟಾ = self.직렬.recv(65536)
                if not ಡೇಟಾ: break
                self.ಲಾಗ್_ದಾಖಲೆ.extend(ಡೇಟಾ)
            if self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None: break
        raise AssertionError('ನಿರೀಕ್ಷಣೆ_ಮೌಲ್ಯ ವೈಫಲ್ಯ_ಮೌಲ್ಯ: ' + 문구 + '\n' + self.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace'))

    def ಆಜ್ಞೆ(self, ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ, 기대):
        ಚಲಾಯಿಸು_2 = len(self.ಲಾಗ್_ದಾಖಲೆ)
        self.직렬.sendall((ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ + '\n').encode())
        ಮಾಪನ = self.ನಿರೀಕ್ಷಣೆ_ಸ್ಥಿತಿ('jkoros> ', ಚಲಾಯಿಸು_2)
        for 문구 in 기대:
            assert 문구 in ಮಾಪನ, (ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ, 문구, ಮಾಪನ)
        assert 'PANIC' not in ಮಾಪನ, ಮಾಪನ
        return ಮಾಪನ

    def ಮುಚ್ಚು(self):
        self.직렬.close()
        self.ಮಾನಿಟರ್_ಮೌಲ್ಯ.close()
        if self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is None:
            self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.terminate()
            try: self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.kill()
                self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait()
        self.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.communicate()
        self.임시.cleanup()


def 보호커널(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ):
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
    항목들 = ['hello=' + str(ಸ್ಥಾನ / 'build/apps/hello.elf')]
    for ಹೆಸರು, ವಿಷಯ_ಮೌಲ್ಯ in 사례들.items():
        ಮೂಲ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / (ಹೆಸರು + '.s')
        ಮೂಲ.write_text('.code32\n.text\n.globl _start\n_start:\n' + ವಿಷಯ_ಮೌಲ್ಯ +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / (ಹೆಸರು + '.o')), str(ಮೂಲ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ಸ್ಥಾನ.parent / 'compiler/ಬಳಕೆದಾರ_ಜೋಡಣೆ_ಲೇಔಟ್.ld'),
                        '-o', str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / (ಹೆಸರು + '.elf')), str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / (ಹೆಸರು + '.o'))], check=True)
        항목들.append(ಹೆಸರು + '=' + str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / (ಹೆಸರು + '.elf')))
    정상 = bytearray((ಸ್ಥಾನ / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ಅಮಾನ್ಯ_ಮಾಪನ = bytearray(정상); ಅಮಾನ್ಯ_ಮಾಪನ[0] = 0; 변형들['badelf'] = ಅಮಾನ್ಯ_ಮಾಪನ
    ಅಮಾನ್ಯ_ಮಾಪನ = bytearray(정상); struct.pack_into('<I', ಅಮಾನ್ಯ_ಮಾಪನ, 24, 0x00100000); 변형들['badentry'] = ಅಮಾನ್ಯ_ಮಾಪನ
    ಅಮಾನ್ಯ_ಮಾಪನ = bytearray(정상); struct.pack_into('<I', ಅಮಾನ್ಯ_ಮಾಪನ, 28, 0x7fffffff); 변형들['badtable'] = ಅಮಾನ್ಯ_ಮಾಪನ
    ಅಮಾನ್ಯ_ಮಾಪನ = bytearray(정상); ನೋಡುವ_ಕೋಷ್ಟಕ = struct.unpack_from('<I', ಅಮಾನ್ಯ_ಮಾಪನ, 28)[0]
    struct.pack_into('<I', ಅಮಾನ್ಯ_ಮಾಪನ, ನೋಡುವ_ಕೋಷ್ಟಕ + 20, 0x7fffffff); 변형들['badsize'] = ಅಮಾನ್ಯ_ಮಾಪನ
    for ಹೆಸರು, ಡೇಟಾ in 변형들.items():
        ಕಡತ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / (ಹೆಸರು + '.elf'); ಕಡತ.write_bytes(ಡೇಟಾ)
        항목들.append(ಹೆಸರು + '=' + str(ಕಡತ))
    subprocess.run([sys.executable, str(ಸ್ಥಾನ / 'ಪರಿಕರಗಳು/묶기.py'), '-o', str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'apps.bin')] + 항목들, check=True)
    ಮೂಲ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'apps.s'
    ಮೂಲ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'apps.o'), str(ಮೂಲ)], check=True)
    ಕರ್ನಲ್_ಮೌಲ್ಯ = ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ಸ್ಥಾನ / '부팅/ಜೋಡಣೆ_ಲೇಔಟ್.ld'), '-o', str(ಕರ್ನಲ್_ಮೌಲ್ಯ),
                    str(ಸ್ಥಾನ / 'build/boot.o'), str(ಸ್ಥಾನ / 'build/java.o'), str(ಸ್ಥಾನ / 'build/user.o'), str(ಡೈರೆಕ್ಟರಿ_ಮೌಲ್ಯ / 'apps.o')], check=True)
    return ಕರ್ನಲ್_ಮೌಲ್ಯ


def ಪೂರೈಸು_ಆದೇಶ():
    ಮಾಪನ = {}
    ಸರ್ವರ್_ಮೌಲ್ಯ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ಸರ್ವರ್_ಮೌಲ್ಯ.bind(('127.0.0.1', 0))
    ಸರ್ವರ್_ಮೌಲ್ಯ.settimeout(0.1)
    ಪೋರ್ಟ್_ಮೌಲ್ಯ = ಸರ್ವರ್_ಮೌಲ್ಯ.getsockname()[1]
    받은것 = []
    ನಿರ್ಗಮನ_ಅಪ್ಲಿ = threading.Event()
    def 되보내기():
        while not ನಿರ್ಗಮನ_ಅಪ್ಲಿ.is_set():
            try: ಡೇಟಾ, ಪೀರ್_ಮೌಲ್ಯ = ಸರ್ವರ್_ಮೌಲ್ಯ.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ಡೇಟಾ)
            if ಡೇಟಾ != b'drop-me': ಸರ್ವರ್_ಮೌಲ್ಯ.sendto(ಡೇಟಾ, ಪೀರ್_ಮೌಲ್ಯ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ಯಂತ್ರ.ಆಜ್ಞೆ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('run missing', ['Exit: -2'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('net', ['NET RTL8139'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ವಿಷಯ_ಮೌಲ್ಯ in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ಯಂತ್ರ.ಆಜ್ಞೆ('run udp 10.0.2.2 {} {}'.format(ಪೋರ್ಟ್_ಮೌಲ್ಯ, ವಿಷಯ_ಮೌಲ್ಯ), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ವಿಷಯ_ಮೌಲ್ಯ.encode() in 받은것, 'ಹೋಸ್ಟ್ 서버에서 자료를 받지 못함'
                ಯಂತ್ರ.ಆಜ್ಞೆ('run stress {}'.format(ಪೋರ್ಟ್_ಮೌಲ್ಯ), ['UDP STRESS PASS', 'Exit: 0'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('run udp 10.0.2.2 {} drop-me'.format(ಪೋರ್ಟ್_ಮೌಲ್ಯ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ಯಂತ್ರ.ಆಜ್ಞೆ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ಮಾಪನ[종류] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode('utf-8', 'replace')
                print('PASS: {} ಬಳಕೆದಾರ ELF/ring 3/인수/UDP ಹೋಸ್ಟ್ 왕복/ಸಮಯ_ಮೌಲ್ಯ 초과/ಶೆಲ್ 복귀'.format(종류), flush=True)
            finally:
                try: ಯಂತ್ರ.ಆಜ್ಞೆ('net', [])
                except Exception: pass
                (ಸ್ಥಾನ / 'build/사용자통신-last.log').write_bytes(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
                ಯಂತ್ರ.ಮುಚ್ಚು()
        ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(ಸ್ಥಾನ / 'build/kernel.elf', ನೆಟ್_ವರ್ಕ್_ಮೌಲ್ಯ=False)
        try:
            ಯಂತ್ರ.ಆಜ್ಞೆ('net', ['NET unavailable'])
            ಯಂತ್ರ.ಆಜ್ಞೆ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ಯಂತ್ರ.ಆಜ್ಞೆ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ಮಾಪನ['no_nic'] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode()
        finally: ಯಂತ್ರ.ಮುಚ್ಚು()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ಯಂತ್ರ = ಅಗೋಚರ_ಯಂತ್ರ(보호커널(Path(임시)), ನೆಟ್_ವರ್ಕ್_ಮೌಲ್ಯ=False)
            try:
                for ಹೆಸರು, ಸ್ಥಿತಿ_ಮೌಲ್ಯ in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ಯಂತ್ರ.ಆಜ್ಞೆ('run ' + ಹೆಸರು, ['Exit: ' + str(ಸ್ಥಿತಿ_ಮೌಲ್ಯ)])
                    ಯಂತ್ರ.ಆಜ್ಞೆ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ಮಾಪನ['protection'] = ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ.decode()
                print('PASS: ಬಳಕೆದಾರ ಮೆಮೊರಿ_ಡೇಟಾ/포트 격리, 잘못된 ಸೂಚಕ/ELF, CPU ವಿನಾಯಿತಿ, 무한 ಸ್ಪ್ರಿಂಟ್_ಮೌಲ್ಯ 제한', flush=True)
            finally:
                (ಸ್ಥಾನ / 'build/보호시험-last.log').write_bytes(ಯಂತ್ರ.ಲಾಗ್_ದಾಖಲೆ)
                ಯಂತ್ರ.ಮುಚ್ಚು()
    finally:
        ನಿರ್ಗಮನ_ಅಪ್ಲಿ.set()
        일꾼.join(timeout=2)
        ಸರ್ವರ್_ಮೌಲ್ಯ.close()
    ಮಾಪನ['host_udp_received'] = [{'length': len(ಡೇಟಾ), 'sha256': hashlib.sha256(ಡೇಟಾ).hexdigest()} for ಡೇಟಾ in 받은것]
    (ಸ್ಥಾನ / 'build/사용자통신시험.json').write_text(json.dumps(ಮಾಪನ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ಪೂರೈಸು_ಆದೇಶ()
