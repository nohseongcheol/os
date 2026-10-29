#!/usr/bin/env python3
"""ପ୍ରକୃତ_ଡାଟା ring 3 ELF/ଆୟୋଜକ UDP 왕복/ପ୍ରତିରୋଧ_ମୂଲ୍ୟ ତ୍ରୁଟି/ସମୟ_ମୂଲ୍ୟ 제한/잘못된 ELF를 검증한다."""
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

ଅବସ୍ଥାନ = Path(__file__).resolve().parents[1]


class ବାସ୍ତବ_ମେସିନ୍:
    def __init__(self, ପଥ, 종류='elf', ନେଟ୍_ୱାର୍କ୍_ମୂଲ୍ୟ=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ = Path(self.임시.name)
        self.ଲଗ୍_ଧାଡ଼ି = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.ମନିଟର୍_ମୂଲ୍ୟ = socket.socket(socket.AF_UNIX)
        직렬경로, ମନିଟର୍_ପଥ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'serial.sock', ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'monitor.sock'
        ନିର୍ଦ୍ଦେଶ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ମନିଟର୍_ପଥ) + ',server,nowait']
        ନିର୍ଦ୍ଦେଶ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ନେଟ୍_ୱାର୍କ୍_ମୂଲ୍ୟ else ['-net', 'none']
        ନିର୍ଦ୍ଦେଶ += ['-kernel', str(ପଥ)] if 종류 == 'elf' else ['-cdrom', str(ପଥ), '-boot', 'd']
        if 저장매체 is not None:
            ନିର୍ଦ୍ଦେଶ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = subprocess.Popen(ନିର୍ଦ୍ଦେଶ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and ମନିଟର୍_ପଥ.exists()):
                if self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None:
                    raise AssertionError(self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ଚଳାନ୍ତୁ ସମୟ_ମୂଲ୍ୟ 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.ମନିଟର୍_ମୂଲ୍ୟ.connect(str(ମନିଟର୍_ପଥ))
            self.직렬.setblocking(False)
            self.ମନିଟର୍_ମୂଲ୍ୟ.sendall(b'cont\n')
            self.ଅପେକ୍ଷା_ସ୍ଥିତି('jkoros> ')
        except BaseException:
            self.ବନ୍ଦ_କରନ୍ତୁ()
            raise

    def ଅପେକ୍ଷା_ସ୍ଥିତି(self, 문구, ଚଳାନ୍ତୁ=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:]:
                return self.ଲଗ୍_ଧାଡ଼ି[ଚଳାନ୍ତୁ:].decode('utf-8', 'replace')
            ପଢନ୍ତୁ, _, _ = select.select([self.직렬], [], [], 0.1)
            if ପଢନ୍ତୁ:
                ଡାଟା = self.직렬.recv(65536)
                if not ଡାଟା: break
                self.ଲଗ୍_ଧାଡ଼ି.extend(ଡାଟା)
            if self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None: break
        raise AssertionError('ଅପେକ୍ଷା_ମୂଲ୍ୟ ବିଫଳତା_ମୂଲ୍ୟ: ' + 문구 + '\n' + self.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace'))

    def ନିର୍ଦ୍ଦେଶ(self, ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ, 기대):
        ଚଳାନ୍ତୁ = len(self.ଲଗ୍_ଧାଡ଼ି)
        self.직렬.sendall((ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ + '\n').encode())
        ମାପ = self.ଅପେକ୍ଷା_ସ୍ଥିତି('jkoros> ', ଚଳାନ୍ତୁ)
        for 문구 in 기대:
            assert 문구 in ମାପ, (ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ, 문구, ମାପ)
        assert 'PANIC' not in ମାପ, ମାପ
        return ମାପ

    def ବନ୍ଦ_କରନ୍ତୁ(self):
        self.직렬.close()
        self.ମନିଟର୍_ମୂଲ୍ୟ.close()
        if self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is None:
            self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.terminate()
            try: self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.kill()
                self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait()
        self.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.communicate()
        self.임시.cleanup()


def 보호커널(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ):
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
    항목들 = ['hello=' + str(ଅବସ୍ଥାନ / 'build/apps/hello.elf')]
    for ନାମ, ବିଷୟ_ମୂଲ୍ୟ in 사례들.items():
        ଉତ୍ସ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / (ନାମ + '.s')
        ଉତ୍ସ.write_text('.code32\n.text\n.globl _start\n_start:\n' + ବିଷୟ_ମୂଲ୍ୟ +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / (ନାମ + '.o')), str(ଉତ୍ସ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ଅବସ୍ଥାନ.parent / 'compiler/ଉପଭୋକ୍ତା_ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld'),
                        '-o', str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / (ନାମ + '.elf')), str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / (ନାମ + '.o'))], check=True)
        항목들.append(ନାମ + '=' + str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / (ନାମ + '.elf')))
    정상 = bytearray((ଅବସ୍ଥାନ / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ଅବୈଧ_ମାପ = bytearray(정상); ଅବୈଧ_ମାପ[0] = 0; 변형들['badelf'] = ଅବୈଧ_ମାପ
    ଅବୈଧ_ମାପ = bytearray(정상); struct.pack_into('<I', ଅବୈଧ_ମାପ, 24, 0x00100000); 변형들['badentry'] = ଅବୈଧ_ମାପ
    ଅବୈଧ_ମାପ = bytearray(정상); struct.pack_into('<I', ଅବୈଧ_ମାପ, 28, 0x7fffffff); 변형들['badtable'] = ଅବୈଧ_ମାପ
    ଅବୈଧ_ମାପ = bytearray(정상); ଦୃଷ୍ଟିପାତ_ସାରଣୀ = struct.unpack_from('<I', ଅବୈଧ_ମାପ, 28)[0]
    struct.pack_into('<I', ଅବୈଧ_ମାପ, ଦୃଷ୍ଟିପାତ_ସାରଣୀ + 20, 0x7fffffff); 변형들['badsize'] = ଅବୈଧ_ମାପ
    for ନାମ, ଡାଟା in 변형들.items():
        ଫାଇଲ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / (ନାମ + '.elf'); ଫାଇଲ.write_bytes(ଡାଟା)
        항목들.append(ନାମ + '=' + str(ଫାଇଲ))
    subprocess.run([sys.executable, str(ଅବସ୍ଥାନ / 'ଉପକରଣସମୂହ/묶기.py'), '-o', str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'apps.bin')] + 항목들, check=True)
    ଉତ୍ସ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'apps.s'
    ଉତ୍ସ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'apps.o'), str(ଉତ୍ସ)], check=True)
    କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ = ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ଅବସ୍ଥାନ / '부팅/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld'), '-o', str(କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ),
                    str(ଅବସ୍ଥାନ / 'build/boot.o'), str(ଅବସ୍ଥାନ / 'build/java.o'), str(ଅବସ୍ଥାନ / 'build/user.o'), str(ଡିରେକ୍ଟୋରୀ_ମୂଲ୍ୟ / 'apps.o')], check=True)
    return କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ


def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ():
    ମାପ = {}
    ସର୍ଭର୍_ମୂଲ୍ୟ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ସର୍ଭର୍_ମୂଲ୍ୟ.bind(('127.0.0.1', 0))
    ସର୍ଭର୍_ମୂଲ୍ୟ.settimeout(0.1)
    ପୋର୍ଟ_ମୂଲ୍ୟ = ସର୍ଭର୍_ମୂଲ୍ୟ.getsockname()[1]
    받은것 = []
    ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ = threading.Event()
    def 되보내기():
        while not ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ.is_set():
            try: ଡାଟା, ସମକକ୍ଷ_ମୂଲ୍ୟ = ସର୍ଭର୍_ମୂଲ୍ୟ.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ଡାଟା)
            if ଡାଟା != b'drop-me': ସର୍ଭର୍_ମୂଲ୍ୟ.sendto(ଡାଟା, ସମକକ୍ଷ_ମୂଲ୍ୟ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run missing', ['Exit: -2'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('net', ['NET RTL8139'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ବିଷୟ_ମୂଲ୍ୟ in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run udp 10.0.2.2 {} {}'.format(ପୋର୍ଟ_ମୂଲ୍ୟ, ବିଷୟ_ମୂଲ୍ୟ), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ବିଷୟ_ମୂଲ୍ୟ.encode() in 받은것, 'ଆୟୋଜକ 서버에서 자료를 받지 못함'
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run stress {}'.format(ପୋର୍ଟ_ମୂଲ୍ୟ), ['UDP STRESS PASS', 'Exit: 0'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run udp 10.0.2.2 {} drop-me'.format(ପୋର୍ଟ_ମୂଲ୍ୟ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ମାପ[종류] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode('utf-8', 'replace')
                print('PASS: {} ଉପଭୋକ୍ତା ELF/ring 3/인수/UDP ଆୟୋଜକ 왕복/ସମୟ_ମୂଲ୍ୟ 초과/ଖୋଳ 복귀'.format(종류), flush=True)
            finally:
                try: ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('net', [])
                except Exception: pass
                (ଅବସ୍ଥାନ / 'build/사용자통신-last.log').write_bytes(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
                ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
        ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(ଅବସ୍ଥାନ / 'build/kernel.elf', ନେଟ୍_ୱାର୍କ୍_ମୂଲ୍ୟ=False)
        try:
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('net', ['NET unavailable'])
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ମାପ['no_nic'] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode()
        finally: ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ମେସିନ୍ = ବାସ୍ତବ_ମେସିନ୍(보호커널(Path(임시)), ନେଟ୍_ୱାର୍କ୍_ମୂଲ୍ୟ=False)
            try:
                for ନାମ, ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run ' + ନାମ, ['Exit: ' + str(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1)])
                    ମେସିନ୍.ନିର୍ଦ୍ଦେଶ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ମାପ['protection'] = ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି.decode()
                print('PASS: ଉପଭୋକ୍ତା ମୋମରୀ_ଡାଟା/ହାର୍ଡୱେର୍_ପୋର୍ଟ 격리, 잘못된 ପଏଣ୍ଟର୍/ELF, CPU ବ୍ୟତିକ୍ରମ, 무한 ବାରମ୍ବାର_ମୂଲ୍ୟ 제한', flush=True)
            finally:
                (ଅବସ୍ଥାନ / 'build/보호시험-last.log').write_bytes(ମେସିନ୍.ଲଗ୍_ଧାଡ଼ି)
                ମେସିନ୍.ବନ୍ଦ_କରନ୍ତୁ()
    finally:
        ପ୍ରସ୍ଥାନ_ଅନୁପ୍ରୟୋଗ.set()
        일꾼.join(timeout=2)
        ସର୍ଭର୍_ମୂଲ୍ୟ.close()
    ମାପ['host_udp_received'] = [{'length': len(ଡାଟା), 'sha256': hashlib.sha256(ଡାଟା).hexdigest()} for ଡାଟା in 받은것]
    (ଅବସ୍ଥାନ / 'build/사용자통신시험.json').write_text(json.dumps(ମାପ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
