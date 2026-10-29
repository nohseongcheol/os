#!/usr/bin/env python3
"""ਅਸਲ_ਸਮੱਗਰੀ ring 3 ELF/ਹੋਸਟ UDP 왕복/ਰੱਖਿਆ_ਕਰਨੀ_ਕੀਮਤ ਗਲਤੀ/시간 제한/잘못된 ELF를 검증한다."""
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

ਸਥਿਤੀ = Path(__file__).resolve().parents[1]


class ਵਰਚੁਅਲ_ਮਸ਼ੀਨ:
    def __init__(self, ਮਾਰਗ, 종류='elf', ਨੈਟਵਰਕ_ਕੀਮਤ=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ = Path(self.임시.name)
        self.ਲੌਗ_ਕਤਾਰ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.ਮੌਨੀਟਰ_ਕੀਮਤ = socket.socket(socket.AF_UNIX)
        직렬경로, ਮੌਨੀਟਰ_ਰਸਤਾ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'serial.sock', ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'monitor.sock'
        ਕਮਾਂਡ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ਮੌਨੀਟਰ_ਰਸਤਾ) + ',server,nowait']
        ਕਮਾਂਡ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ਨੈਟਵਰਕ_ਕੀਮਤ else ['-net', 'none']
        ਕਮਾਂਡ += ['-kernel', str(ਮਾਰਗ)] if 종류 == 'elf' else ['-cdrom', str(ਮਾਰਗ), '-boot', 'd']
        if 저장매체 is not None:
            ਕਮਾਂਡ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ਕਾਰਵਾਈ_ਕੀਮਤ = subprocess.Popen(ਕਮਾਂਡ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and ਮੌਨੀਟਰ_ਰਸਤਾ.exists()):
                if self.ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None:
                    raise AssertionError(self.ਕਾਰਵਾਈ_ਕੀਮਤ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ਚਲਾਓ_2 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.ਮੌਨੀਟਰ_ਕੀਮਤ.connect(str(ਮੌਨੀਟਰ_ਰਸਤਾ))
            self.직렬.setblocking(False)
            self.ਮੌਨੀਟਰ_ਕੀਮਤ.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.ਬੰਦ_ਕਰੋ()
            raise

    def 기다림(self, 문구, ਚਲਾਓ_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:]:
                return self.ਲੌਗ_ਕਤਾਰ[ਚਲਾਓ_2:].decode('utf-8', 'replace')
            ਪੜ੍ਹਨ, _, _ = select.select([self.직렬], [], [], 0.1)
            if ਪੜ੍ਹਨ:
                ਸਮੱਗਰੀ = self.직렬.recv(65536)
                if not ਸਮੱਗਰੀ: break
                self.ਲੌਗ_ਕਤਾਰ.extend(ਸਮੱਗਰੀ)
            if self.ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None: break
        raise AssertionError('대기 ਅਸਫਲ_ਕੀਮਤ: ' + 문구 + '\n' + self.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace'))

    def ਕਮਾਂਡ(self, ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ, 기대):
        ਚਲਾਓ_2 = len(self.ਲੌਗ_ਕਤਾਰ)
        self.직렬.sendall((ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ + '\n').encode())
        ਮਾਪ = self.기다림('jkoros> ', ਚਲਾਓ_2)
        for 문구 in 기대:
            assert 문구 in ਮਾਪ, (ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ, 문구, ਮਾਪ)
        assert 'PANIC' not in ਮਾਪ, ਮਾਪ
        return ਮਾਪ

    def ਬੰਦ_ਕਰੋ(self):
        self.직렬.close()
        self.ਮੌਨੀਟਰ_ਕੀਮਤ.close()
        if self.ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is None:
            self.ਕਾਰਵਾਈ_ਕੀਮਤ.terminate()
            try: self.ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ਕਾਰਵਾਈ_ਕੀਮਤ.kill()
                self.ਕਾਰਵਾਈ_ਕੀਮਤ.wait()
        self.ਕਾਰਵਾਈ_ਕੀਮਤ.communicate()
        self.임시.cleanup()


def 보호커널(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ):
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
    항목들 = ['hello=' + str(ਸਥਿਤੀ / 'build/apps/hello.elf')]
    for ਨਾਂ, ਤਤਕਰਾ_ਕੀਮਤ in 사례들.items():
        ਸਰੋਤ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / (ਨਾਂ + '.s')
        ਸਰੋਤ.write_text('.code32\n.text\n.globl _start\n_start:\n' + ਤਤਕਰਾ_ਕੀਮਤ +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / (ਨਾਂ + '.o')), str(ਸਰੋਤ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ਸਥਿਤੀ.parent / 'compiler/ਉਪਭੋਗਤਾ_ਲਿੰਕ_ਖਾਕਾ.ld'),
                        '-o', str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / (ਨਾਂ + '.elf')), str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / (ਨਾਂ + '.o'))], check=True)
        항목들.append(ਨਾਂ + '=' + str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / (ਨਾਂ + '.elf')))
    정상 = bytearray((ਸਥਿਤੀ / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ਅਯੋਗ_ਮਾਪ = bytearray(정상); ਅਯੋਗ_ਮਾਪ[0] = 0; 변형들['badelf'] = ਅਯੋਗ_ਮਾਪ
    ਅਯੋਗ_ਮਾਪ = bytearray(정상); struct.pack_into('<I', ਅਯੋਗ_ਮਾਪ, 24, 0x00100000); 변형들['badentry'] = ਅਯੋਗ_ਮਾਪ
    ਅਯੋਗ_ਮਾਪ = bytearray(정상); struct.pack_into('<I', ਅਯੋਗ_ਮਾਪ, 28, 0x7fffffff); 변형들['badtable'] = ਅਯੋਗ_ਮਾਪ
    ਅਯੋਗ_ਮਾਪ = bytearray(정상); ਲੱਭਣਾ_ਤਾਲਿਕਾ = struct.unpack_from('<I', ਅਯੋਗ_ਮਾਪ, 28)[0]
    struct.pack_into('<I', ਅਯੋਗ_ਮਾਪ, ਲੱਭਣਾ_ਤਾਲਿਕਾ + 20, 0x7fffffff); 변형들['badsize'] = ਅਯੋਗ_ਮਾਪ
    for ਨਾਂ, ਸਮੱਗਰੀ in 변형들.items():
        ਫਾਇਲ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / (ਨਾਂ + '.elf'); ਫਾਇਲ.write_bytes(ਸਮੱਗਰੀ)
        항목들.append(ਨਾਂ + '=' + str(ਫਾਇਲ))
    subprocess.run([sys.executable, str(ਸਥਿਤੀ / 'ਸਾਧਨ/묶기.py'), '-o', str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'apps.bin')] + 항목들, check=True)
    ਸਰੋਤ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'apps.s'
    ਸਰੋਤ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'apps.o'), str(ਸਰੋਤ)], check=True)
    ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ = ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ਸਥਿਤੀ / '부팅/ਲਿੰਕ_ਖਾਕਾ.ld'), '-o', str(ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ),
                    str(ਸਥਿਤੀ / 'build/boot.o'), str(ਸਥਿਤੀ / 'build/java.o'), str(ਸਥਿਤੀ / 'build/user.o'), str(ਨਿਰਦੇਸ਼ਕ_ਕੀਮਤ / 'apps.o')], check=True)
    return ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ


def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼():
    ਮਾਪ = {}
    ਸਰਵਰ_ਕੀਮਤ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ਸਰਵਰ_ਕੀਮਤ.bind(('127.0.0.1', 0))
    ਸਰਵਰ_ਕੀਮਤ.settimeout(0.1)
    ਪੋਰਟ_ਕੀਮਤ = ਸਰਵਰ_ਕੀਮਤ.getsockname()[1]
    받은것 = []
    ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼ = threading.Event()
    def 되보내기():
        while not ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼.is_set():
            try: ਸਮੱਗਰੀ, ਪਿਅਰ_ਕੀਮਤ = ਸਰਵਰ_ਕੀਮਤ.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ਸਮੱਗਰੀ)
            if ਸਮੱਗਰੀ != b'drop-me': ਸਰਵਰ_ਕੀਮਤ.sendto(ਸਮੱਗਰੀ, ਪਿਅਰ_ਕੀਮਤ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('run missing', ['Exit: -2'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('net', ['NET RTL8139'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ਤਤਕਰਾ_ਕੀਮਤ in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ਮਸ਼ੀਨ.ਕਮਾਂਡ('run udp 10.0.2.2 {} {}'.format(ਪੋਰਟ_ਕੀਮਤ, ਤਤਕਰਾ_ਕੀਮਤ), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ਤਤਕਰਾ_ਕੀਮਤ.encode() in 받은것, 'ਹੋਸਟ 서버에서 자료를 받지 못함'
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('run stress {}'.format(ਪੋਰਟ_ਕੀਮਤ), ['UDP STRESS PASS', 'Exit: 0'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('run udp 10.0.2.2 {} drop-me'.format(ਪੋਰਟ_ਕੀਮਤ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ਮਸ਼ੀਨ.ਕਮਾਂਡ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ਮਾਪ[종류] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode('utf-8', 'replace')
                print('PASS: {} ਉਪਭੋਗਤਾ ELF/ring 3/ਆਰਗੂਮੈਂਟ/UDP ਹੋਸਟ 왕복/시간 초과/ਸ਼ੈਲ 복귀'.format(종류), flush=True)
            finally:
                try: ਮਸ਼ੀਨ.ਕਮਾਂਡ('net', [])
                except Exception: pass
                (ਸਥਿਤੀ / 'build/사용자통신-last.log').write_bytes(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
                ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
        ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(ਸਥਿਤੀ / 'build/kernel.elf', ਨੈਟਵਰਕ_ਕੀਮਤ=False)
        try:
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('net', ['NET unavailable'])
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ਮਸ਼ੀਨ.ਕਮਾਂਡ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ਮਾਪ['no_nic'] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode()
        finally: ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ਮਸ਼ੀਨ = ਵਰਚੁਅਲ_ਮਸ਼ੀਨ(보호커널(Path(임시)), ਨੈਟਵਰਕ_ਕੀਮਤ=False)
            try:
                for ਨਾਂ, ਸਥਿਤੀ_ਕੀਮਤ in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ਮਸ਼ੀਨ.ਕਮਾਂਡ('run ' + ਨਾਂ, ['Exit: ' + str(ਸਥਿਤੀ_ਕੀਮਤ)])
                    ਮਸ਼ੀਨ.ਕਮਾਂਡ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ਮਾਪ['protection'] = ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ.decode()
                print('PASS: ਉਪਭੋਗਤਾ ਮੈਮਰੀ_ਸਮੱਗਰੀ/포트 격리, 잘못된 ਪੌਇੰਟਰ/ELF, CPU 예외, 무한 ਦੋਹਰਾਵ_ਕੀਮਤ 제한', flush=True)
            finally:
                (ਸਥਿਤੀ / 'build/보호시험-last.log').write_bytes(ਮਸ਼ੀਨ.ਲੌਗ_ਕਤਾਰ)
                ਮਸ਼ੀਨ.ਬੰਦ_ਕਰੋ()
    finally:
        ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼.set()
        일꾼.join(timeout=2)
        ਸਰਵਰ_ਕੀਮਤ.close()
    ਮਾਪ['host_udp_received'] = [{'length': len(ਸਮੱਗਰੀ), 'sha256': hashlib.sha256(ਸਮੱਗਰੀ).hexdigest()} for ਸਮੱਗਰੀ in 받은것]
    (ਸਥਿਤੀ / 'build/사용자통신시험.json').write_text(json.dumps(ਮਾਪ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼()
