#!/usr/bin/env python3
"""اصلي_ڪوائف ring 3 ELF/مهمان UDP 왕복/حفاظت_ڪريو_قدر نقص/시간 제한/잘못된 ELF를 검증한다."""
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


class مجازي_مشين:
    def __init__(self, راههه, 종류='elf', نيٽ_ورڪ_قدر=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ڊائريڪٽري_قدر = Path(self.임시.name)
        self.لاگ_صف = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.مانيٽر_قدر = socket.socket(socket.AF_UNIX)
        직렬경로, مانيٽر_راههه = ڊائريڪٽري_قدر / 'serial.sock', ڊائريڪٽري_قدر / 'monitor.sock'
        حڪم = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(مانيٽر_راههه) + ',server,nowait']
        حڪم += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if نيٽ_ورڪ_قدر else ['-net', 'none']
        حڪم += ['-kernel', str(راههه)] if 종류 == 'elf' else ['-cdrom', str(راههه), '-boot', 'd']
        if 저장매체 is not None:
            حڪم += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.عمل_قدر = subprocess.Popen(حڪم, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and مانيٽر_راههه.exists()):
                if self.عمل_قدر.poll() is not None:
                    raise AssertionError(self.عمل_قدر.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU هلائڻ 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.مانيٽر_قدر.connect(str(مانيٽر_راههه))
            self.직렬.setblocking(False)
            self.مانيٽر_قدر.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.بند_ڪرڻ()
            raise

    def 기다림(self, 문구, هلائڻ=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.لاگ_صف[هلائڻ:]:
                return self.لاگ_صف[هلائڻ:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                ڪوائف = self.직렬.recv(65536)
                if not ڪوائف: break
                self.لاگ_صف.extend(ڪوائف)
            if self.عمل_قدر.poll() is not None: break
        raise AssertionError('대기 ناڪامي_قدر: ' + 문구 + '\n' + self.لاگ_صف.decode('utf-8', 'replace'))

    def حڪم(self, اسٽرنگ_قدر, 기대):
        هلائڻ = len(self.لاگ_صف)
        self.직렬.sendall((اسٽرنگ_قدر + '\n').encode())
        결과 = self.기다림('jkoros> ', هلائڻ)
        for 문구 in 기대:
            assert 문구 in 결과, (اسٽرنگ_قدر, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def بند_ڪرڻ(self):
        self.직렬.close()
        self.مانيٽر_قدر.close()
        if self.عمل_قدر.poll() is None:
            self.عمل_قدر.terminate()
            try: self.عمل_قدر.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.عمل_قدر.kill()
                self.عمل_قدر.wait()
        self.عمل_قدر.communicate()
        self.임시.cleanup()


def 보호커널(ڊائريڪٽري_قدر):
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
    for نالو, مواد_قدر in 사례들.items():
        ماخذ = ڊائريڪٽري_قدر / (نالو + '.s')
        ماخذ.write_text('.code32\n.text\n.globl _start\n_start:\n' + مواد_قدر +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ڊائريڪٽري_قدر / (نالو + '.o')), str(ماخذ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/صارف_ڪڙي_لي_آئوٽ.ld'),
                        '-o', str(ڊائريڪٽري_قدر / (نالو + '.elf')), str(ڊائريڪٽري_قدر / (نالو + '.o'))], check=True)
        항목들.append(نالو + '=' + str(ڊائريڪٽري_قدر / (نالو + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for نالو, ڪوائف in 변형들.items():
        فائل = ڊائريڪٽري_قدر / (نالو + '.elf'); فائل.write_bytes(ڪوائف)
        항목들.append(نالو + '=' + str(فائل))
    subprocess.run([sys.executable, str(위치 / 'اوزار/묶기.py'), '-o', str(ڊائريڪٽري_قدر / 'apps.bin')] + 항목들, check=True)
    ماخذ = ڊائريڪٽري_قدر / 'apps.s'
    ماخذ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ڊائريڪٽري_قدر / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ڊائريڪٽري_قدر / 'apps.o'), str(ماخذ)], check=True)
    ڪرنل_قدر = ڊائريڪٽري_قدر / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/ڪڙي_لي_آئوٽ.ld'), '-o', str(ڪرنل_قدر),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(ڊائريڪٽري_قدر / 'apps.o')], check=True)
    return ڪرنل_قدر


def تعميل_ڪرڻ_حڪم():
    결과 = {}
    سرور_قدر = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    سرور_قدر.bind(('127.0.0.1', 0))
    سرور_قدر.settimeout(0.1)
    پورٽ_قدر = سرور_قدر.getsockname()[1]
    받은것 = []
    خارج_ڪريو_ائپ = threading.Event()
    def 되보내기():
        while not خارج_ڪريو_ائپ.is_set():
            try: ڪوائف, همعصر_قدر = سرور_قدر.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ڪوائف)
            if ڪوائف != b'drop-me': سرور_قدر.sendto(ڪوائف, همعصر_قدر)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            مشين = مجازي_مشين(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                مشين.حڪم('apps', ['hello', 'udp', 'netcheck', 'stress'])
                مشين.حڪم('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                مشين.حڪم('run missing', ['Exit: -2'])
                مشين.حڪم('net', ['NET RTL8139'])
                مشين.حڪم('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for مواد_قدر in ('hello-network', 'odd', 'even', 'repeat-123'):
                    مشين.حڪم('run udp 10.0.2.2 {} {}'.format(پورٽ_قدر, مواد_قدر), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert مواد_قدر.encode() in 받은것, 'مهمان 서버에서 자료를 받지 못함'
                مشين.حڪم('run stress {}'.format(پورٽ_قدر), ['UDP STRESS PASS', 'Exit: 0'])
                مشين.حڪم('run udp 10.0.2.2 {} drop-me'.format(پورٽ_قدر), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                مشين.حڪم('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = مشين.لاگ_صف.decode('utf-8', 'replace')
                print('PASS: {} صارف ELF/ring 3/인수/UDP مهمان 왕복/시간 초과/شيل 복귀'.format(종류), flush=True)
            finally:
                try: مشين.حڪم('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(مشين.لاگ_صف)
                مشين.بند_ڪرڻ()
        مشين = مجازي_مشين(위치 / 'build/kernel.elf', نيٽ_ورڪ_قدر=False)
        try:
            مشين.حڪم('net', ['NET unavailable'])
            مشين.حڪم('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            مشين.حڪم('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = مشين.لاگ_صف.decode()
        finally: مشين.بند_ڪرڻ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            مشين = مجازي_مشين(보호커널(Path(임시)), نيٽ_ورڪ_قدر=False)
            try:
                for نالو, حالت_قدر in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    مشين.حڪم('run ' + نالو, ['Exit: ' + str(حالت_قدر)])
                    مشين.حڪم('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = مشين.لاگ_صف.decode()
                print('PASS: صارف ميموري_ڪوائف/포트 격리, 잘못된 پوائنٽر/ELF, CPU 예외, 무한 دهرائڻ_قدر 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(مشين.لاگ_صف)
                مشين.بند_ڪرڻ()
    finally:
        خارج_ڪريو_ائپ.set()
        일꾼.join(timeout=2)
        سرور_قدر.close()
    결과['host_udp_received'] = [{'length': len(ڪوائف), 'sha256': hashlib.sha256(ڪوائف).hexdigest()} for ڪوائف in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    تعميل_ڪرڻ_حڪم()
