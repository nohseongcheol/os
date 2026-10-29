#!/usr/bin/env python3
"""اصل_کوائف ring 3 ELF/میزبان UDP 왕복/بچانا_قدر غلطی/وقت_قدر 제한/잘못된 ELF를 검증한다."""
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

مقام = Path(__file__).resolve().parents[1]


class مجازی_مشین:
    def __init__(self, راستہ_2, 종류='elf', نیٹ_ورک_قدر=True, 저장매체=None):
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
        حکم += ['-kernel', str(راستہ_2)] if 종류 == 'elf' else ['-cdrom', str(راستہ_2), '-boot', 'd']
        if 저장매체 is not None:
            حکم += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.عمل_قدر = subprocess.Popen(حکم, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and مانیٹر_راہ.exists()):
                if self.عمل_قدر.poll() is not None:
                    raise AssertionError(self.عمل_قدر.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU چلائیں وقت_قدر 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.مانیٹر_قدر.connect(str(مانیٹر_راہ))
            self.직렬.setblocking(False)
            self.مانیٹر_قدر.sendall(b'cont\n')
            self.انتظار_حالت('jkoros> ')
        except BaseException:
            self.بند_کریں()
            raise

    def انتظار_حالت(self, 문구, چلائیں=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.لاگ_صف[چلائیں:]:
                return self.لاگ_صف[چلائیں:].decode('utf-8', 'replace')
            پڑھیں, _, _ = select.select([self.직렬], [], [], 0.1)
            if پڑھیں:
                کوائف = self.직렬.recv(65536)
                if not کوائف: break
                self.لاگ_صف.extend(کوائف)
            if self.عمل_قدر.poll() is not None: break
        raise AssertionError('انتظار_قدر ناکامی_قدر: ' + 문구 + '\n' + self.لاگ_صف.decode('utf-8', 'replace'))

    def حکم(self, سلک_قدر, 기대):
        چلائیں = len(self.لاگ_صف)
        self.직렬.sendall((سلک_قدر + '\n').encode())
        پیمائش = self.انتظار_حالت('jkoros> ', چلائیں)
        for 문구 in 기대:
            assert 문구 in پیمائش, (سلک_قدر, 문구, پیمائش)
        assert 'PANIC' not in پیمائش, پیمائش
        return پیمائش

    def بند_کریں(self):
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
    항목들 = ['hello=' + str(مقام / 'build/apps/hello.elf')]
    for نام, مشمول_قدر in 사례들.items():
        ماخذ_فائل = ڈائریکٹری_قدر / (نام + '.s')
        ماخذ_فائل.write_text('.code32\n.text\n.globl _start\n_start:\n' + مشمول_قدر +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ڈائریکٹری_قدر / (نام + '.o')), str(ماخذ_فائل)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(مقام.parent / 'compiler/صارف_ربط_ترتیب.ld'),
                        '-o', str(ڈائریکٹری_قدر / (نام + '.elf')), str(ڈائریکٹری_قدر / (نام + '.o'))], check=True)
        항목들.append(نام + '=' + str(ڈائریکٹری_قدر / (نام + '.elf')))
    정상 = bytearray((مقام / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    بے_جواز_پیمائش = bytearray(정상); بے_جواز_پیمائش[0] = 0; 변형들['badelf'] = بے_جواز_پیمائش
    بے_جواز_پیمائش = bytearray(정상); struct.pack_into('<I', بے_جواز_پیمائش, 24, 0x00100000); 변형들['badentry'] = بے_جواز_پیمائش
    بے_جواز_پیمائش = bytearray(정상); struct.pack_into('<I', بے_جواز_پیمائش, 28, 0x7fffffff); 변형들['badtable'] = بے_جواز_پیمائش
    بے_جواز_پیمائش = bytearray(정상); لُک_اپ_جدول = struct.unpack_from('<I', بے_جواز_پیمائش, 28)[0]
    struct.pack_into('<I', بے_جواز_پیمائش, لُک_اپ_جدول + 20, 0x7fffffff); 변형들['badsize'] = بے_جواز_پیمائش
    for نام, کوائف in 변형들.items():
        فائل_کا_نام = ڈائریکٹری_قدر / (نام + '.elf'); فائل_کا_نام.write_bytes(کوائف)
        항목들.append(نام + '=' + str(فائل_کا_نام))
    subprocess.run([sys.executable, str(مقام / 'ٹولز/묶기.py'), '-o', str(ڈائریکٹری_قدر / 'apps.bin')] + 항목들, check=True)
    ماخذ_فائل = ڈائریکٹری_قدر / 'apps.s'
    ماخذ_فائل.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ڈائریکٹری_قدر / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ڈائریکٹری_قدر / 'apps.o'), str(ماخذ_فائل)], check=True)
    کرنیل_قدر = ڈائریکٹری_قدر / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(مقام / '부팅/ربط_ترتیب.ld'), '-o', str(کرنیل_قدر),
                    str(مقام / 'build/boot.o'), str(مقام / 'build/java.o'), str(مقام / 'build/user.o'), str(ڈائریکٹری_قدر / 'apps.o')], check=True)
    return کرنیل_قدر


def نفاذ_کریں_حکم():
    پیمائش = {}
    سرور_قدر = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    سرور_قدر.bind(('127.0.0.1', 0))
    سرور_قدر.settimeout(0.1)
    پورٹ_قدر = سرور_قدر.getsockname()[1]
    받은것 = []
    خروج_ایپ = threading.Event()
    def 되보내기():
        while not خروج_ایپ.is_set():
            try: کوائف, ساتھی_قدر = سرور_قدر.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(کوائف)
            if کوائف != b'drop-me': سرور_قدر.sendto(کوائف, ساتھی_قدر)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            مشین = مجازی_مشین(مقام / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                مشین.حکم('apps', ['hello', 'udp', 'netcheck', 'stress'])
                مشین.حکم('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                مشین.حکم('run missing', ['Exit: -2'])
                مشین.حکم('net', ['NET RTL8139'])
                مشین.حکم('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for مشمول_قدر in ('hello-network', 'odd', 'even', 'repeat-123'):
                    مشین.حکم('run udp 10.0.2.2 {} {}'.format(پورٹ_قدر, مشمول_قدر), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert مشمول_قدر.encode() in 받은것, 'میزبان 서버에서 자료를 받지 못함'
                مشین.حکم('run stress {}'.format(پورٹ_قدر), ['UDP STRESS PASS', 'Exit: 0'])
                مشین.حکم('run udp 10.0.2.2 {} drop-me'.format(پورٹ_قدر), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                مشین.حکم('run hello recovered', ['arg: recovered', 'Exit: 0'])
                پیمائش[종류] = مشین.لاگ_صف.decode('utf-8', 'replace')
                print('PASS: {} صارف ELF/ring 3/دلائل/UDP میزبان 왕복/وقت_قدر 초과/شیل 복귀'.format(종류), flush=True)
            finally:
                try: مشین.حکم('net', [])
                except Exception: pass
                (مقام / 'build/사용자통신-last.log').write_bytes(مشین.لاگ_صف)
                مشین.بند_کریں()
        مشین = مجازی_مشین(مقام / 'build/kernel.elf', نیٹ_ورک_قدر=False)
        try:
            مشین.حکم('net', ['NET unavailable'])
            مشین.حکم('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            مشین.حکم('run hello', ['USER MODE ring 3', 'Exit: 0'])
            پیمائش['no_nic'] = مشین.لاگ_صف.decode()
        finally: مشین.بند_کریں()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            مشین = مجازی_مشین(보호커널(Path(임시)), نیٹ_ورک_قدر=False)
            try:
                for نام, حالت_قدر in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    مشین.حکم('run ' + نام, ['Exit: ' + str(حالت_قدر)])
                    مشین.حکم('run hello', ['USER MODE ring 3', 'Exit: 0'])
                پیمائش['protection'] = مشین.لاگ_صف.decode()
                print('PASS: صارف میموری_کوائف/포트 격리, 잘못된 پوائنٹر/ELF, CPU استثنا, 무한 تکرار_قدر 제한', flush=True)
            finally:
                (مقام / 'build/보호시험-last.log').write_bytes(مشین.لاگ_صف)
                مشین.بند_کریں()
    finally:
        خروج_ایپ.set()
        일꾼.join(timeout=2)
        سرور_قدر.close()
    پیمائش['host_udp_received'] = [{'length': len(کوائف), 'sha256': hashlib.sha256(کوائف).hexdigest()} for کوائف in 받은것]
    (مقام / 'build/사용자통신시험.json').write_text(json.dumps(پیمائش, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    نفاذ_کریں_حکم()
