#!/usr/bin/env python3
"""اصلی_کوائف ring 3 ELF/مہمان_b78e430d UDP 왕복/حفاظت_کرو_قدر نقص/시간 제한/잘못된 ELF를 검증한다."""
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


class مجازی_مشین:
    def __init__(self, راہ, 종류='elf', نیٹ_ورک_قدر=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ڈائریکٹری_قدر = Path(self.임시.name)
        self.لاگ_صف = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.مانیٹر_قدر = socket.socket(socket.AF_UNIX)
        직렬경로, مانیٹر_راہ = ڈائریکٹری_قدر / 'serial.sock', ڈائریکٹری_قدر / 'monitor.sock'
        حکم = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(مانیٹر_راہ) + ',server,nowait']
        حکم += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if نیٹ_ورک_قدر else ['-net', 'none']
        حکم += ['-kernel', str(راہ)] if 종류 == 'elf' else ['-cdrom', str(راہ), '-boot', 'd']
        if 저장매체 is not None:
            حکم += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.عمل_قدر = subprocess.Popen(حکم, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and مانیٹر_راہ.exists()):
                if self.عمل_قدر.poll() is not None:
                    raise AssertionError(self.عمل_قدر.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU چلاؤ 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.مانیٹر_قدر.connect(str(مانیٹر_راہ))
            self.직렬.setblocking(False)
            self.مانیٹر_قدر.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.بند_کرو()
            raise

    def 기다림(self, 문구, چلاؤ=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.لاگ_صف[چلاؤ:]:
                return self.لاگ_صف[چلاؤ:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                کوائف = self.직렬.recv(65536)
                if not کوائف: break
                self.لاگ_صف.extend(کوائف)
            if self.عمل_قدر.poll() is not None: break
        raise AssertionError('대기 ناکامی_قدر: ' + 문구 + '\n' + self.لاگ_صف.decode('utf-8', 'replace'))

    def حکم(self, سٹرنگ_قدر, 기대):
        چلاؤ = len(self.لاگ_صف)
        self.직렬.sendall((سٹرنگ_قدر + '\n').encode())
        결과 = self.기다림('jkoros> ', چلاؤ)
        for 문구 in 기대:
            assert 문구 in 결과, (سٹرنگ_قدر, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def بند_کرو(self):
        self.직렬.close()
        self.مانیٹر_قدر.close()
        if self.عمل_قدر.poll() is None:
            self.عمل_قدر.terminate()
            try: self.عمل_قدر.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.عمل_قدر.kill()
                self.عمل_قدر.wait()
        self.عمل_قدر.communicate()
        self.임시.cleanup()


def 보호커널(ڈائریکٹری_قدر):
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
    for ناں, اجزاء_قدر in 사례들.items():
        ماخذ = ڈائریکٹری_قدر / (ناں + '.s')
        ماخذ.write_text('.code32\n.text\n.globl _start\n_start:\n' + اجزاء_قدر +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ڈائریکٹری_قدر / (ناں + '.o')), str(ماخذ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/صارف_ربط_لے_آؤٹ.ld'),
                        '-o', str(ڈائریکٹری_قدر / (ناں + '.elf')), str(ڈائریکٹری_قدر / (ناں + '.o'))], check=True)
        항목들.append(ناں + '=' + str(ڈائریکٹری_قدر / (ناں + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for ناں, کوائف in 변형들.items():
        فائل = ڈائریکٹری_قدر / (ناں + '.elf'); فائل.write_bytes(کوائف)
        항목들.append(ناں + '=' + str(فائل))
    subprocess.run([sys.executable, str(위치 / 'اوزار/묶기.py'), '-o', str(ڈائریکٹری_قدر / 'apps.bin')] + 항목들, check=True)
    ماخذ = ڈائریکٹری_قدر / 'apps.s'
    ماخذ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ڈائریکٹری_قدر / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ڈائریکٹری_قدر / 'apps.o'), str(ماخذ)], check=True)
    کرنل_قدر = ڈائریکٹری_قدر / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/ربط_لے_آؤٹ.ld'), '-o', str(کرنل_قدر),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(ڈائریکٹری_قدر / 'apps.o')], check=True)
    return کرنل_قدر


def نفاذ_کرو_حکم():
    결과 = {}
    سرور_قدر = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    سرور_قدر.bind(('127.0.0.1', 0))
    سرور_قدر.settimeout(0.1)
    دہانہ_قدر = سرور_قدر.getsockname()[1]
    받은것 = []
    خارج_کرو_ایپ = threading.Event()
    def 되보내기():
        while not خارج_کرو_ایپ.is_set():
            try: کوائف, ہم_سر_قدر = سرور_قدر.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(کوائف)
            if کوائف != b'drop-me': سرور_قدر.sendto(کوائف, ہم_سر_قدر)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            مشین = مجازی_مشین(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                مشین.حکم('apps', ['hello', 'udp', 'netcheck', 'stress'])
                مشین.حکم('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                مشین.حکم('run missing', ['Exit: -2'])
                مشین.حکم('net', ['NET RTL8139'])
                مشین.حکم('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for اجزاء_قدر in ('hello-network', 'odd', 'even', 'repeat-123'):
                    مشین.حکم('run udp 10.0.2.2 {} {}'.format(دہانہ_قدر, اجزاء_قدر), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert اجزاء_قدر.encode() in 받은것, 'مہمان_b78e430d 서버에서 자료를 받지 못함'
                مشین.حکم('run stress {}'.format(دہانہ_قدر), ['UDP STRESS PASS', 'Exit: 0'])
                مشین.حکم('run udp 10.0.2.2 {} drop-me'.format(دہانہ_قدر), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                مشین.حکم('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = مشین.لاگ_صف.decode('utf-8', 'replace')
                print('PASS: {} صارف ELF/ring 3/인수/UDP مہمان_b78e430d 왕복/시간 초과/شیل 복귀'.format(종류), flush=True)
            finally:
                try: مشین.حکم('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(مشین.لاگ_صف)
                مشین.بند_کرو()
        مشین = مجازی_مشین(위치 / 'build/kernel.elf', نیٹ_ورک_قدر=False)
        try:
            مشین.حکم('net', ['NET unavailable'])
            مشین.حکم('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            مشین.حکم('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = مشین.لاگ_صف.decode()
        finally: مشین.بند_کرو()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            مشین = مجازی_مشین(보호커널(Path(임시)), نیٹ_ورک_قدر=False)
            try:
                for ناں, حالت_قدر in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    مشین.حکم('run ' + ناں, ['Exit: ' + str(حالت_قدر)])
                    مشین.حکم('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = مشین.لاگ_صف.decode()
                print('PASS: صارف میموری_کوائف/포트 격리, 잘못된 پوائنٹر/ELF, CPU 예외, 무한 تکرار_قدر 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(مشین.لاگ_صف)
                مشین.بند_کرو()
    finally:
        خارج_کرو_ایپ.set()
        일꾼.join(timeout=2)
        سرور_قدر.close()
    결과['host_udp_received'] = [{'length': len(کوائف), 'sha256': hashlib.sha256(کوائف).hexdigest()} for کوائف in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    نفاذ_کرو_حکم()
