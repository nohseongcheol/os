#!/usr/bin/env python3
"""واقعی_داده_ها ring 3 ELF/میزبان UDP 왕복/حفاظت_کردن_مقدار خطا/زمان_مقدار 제한/잘못된 ELF를 검증한다."""
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

مرتب_کردن = Path(__file__).resolve().parents[1]


class مجازی_دستگاه:
    def __init__(self, مسیر, 종류='elf', شبکه_مقدار=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        فهرست_مقدار_e5561a2b = Path(self.임시.name)
        self.واقعه_نگار_ردیف = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.مانیتور_مقدار = socket.socket(socket.AF_UNIX)
        직렬경로, مانیتور_مسیر = فهرست_مقدار_e5561a2b / 'serial.sock', فهرست_مقدار_e5561a2b / 'monitor.sock'
        فرمان = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(مانیتور_مسیر) + ',server,nowait']
        فرمان += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if شبکه_مقدار else ['-net', 'none']
        فرمان += ['-kernel', str(مسیر)] if 종류 == 'elf' else ['-cdrom', str(مسیر), '-boot', 'd']
        if 저장매체 is not None:
            فرمان += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.فرآیند_مقدار = subprocess.Popen(فرمان, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and مانیتور_مسیر.exists()):
                if self.فرآیند_مقدار.poll() is not None:
                    raise AssertionError(self.فرآیند_مقدار.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU اجرا_2 زمان_مقدار 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.مانیتور_مقدار.connect(str(مانیتور_مسیر))
            self.직렬.setblocking(False)
            self.مانیتور_مقدار.sendall(b'cont\n')
            self.منتظر_ماندن_وضعیت('jkoros> ')
        except BaseException:
            self.بستن()
            raise

    def منتظر_ماندن_وضعیت(self, 문구, اجرا_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.واقعه_نگار_ردیف[اجرا_2:]:
                return self.واقعه_نگار_ردیف[اجرا_2:].decode('utf-8', 'replace')
            خواندن, _, _ = select.select([self.직렬], [], [], 0.1)
            if خواندن:
                داده_ها = self.직렬.recv(65536)
                if not داده_ها: break
                self.واقعه_نگار_ردیف.extend(داده_ها)
            if self.فرآیند_مقدار.poll() is not None: break
        raise AssertionError('منتظر_ماندن_مقدار عدم_موفقیت_مقدار: ' + 문구 + '\n' + self.واقعه_نگار_ردیف.decode('utf-8', 'replace'))

    def فرمان(self, رشته_مقدار_6ca8363c, 기대):
        اجرا_2 = len(self.واقعه_نگار_ردیف)
        self.직렬.sendall((رشته_مقدار_6ca8363c + '\n').encode())
        سنجش = self.منتظر_ماندن_وضعیت('jkoros> ', اجرا_2)
        for 문구 in 기대:
            assert 문구 in سنجش, (رشته_مقدار_6ca8363c, 문구, سنجش)
        assert 'PANIC' not in سنجش, سنجش
        return سنجش

    def بستن(self):
        self.직렬.close()
        self.مانیتور_مقدار.close()
        if self.فرآیند_مقدار.poll() is None:
            self.فرآیند_مقدار.terminate()
            try: self.فرآیند_مقدار.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.فرآیند_مقدار.kill()
                self.فرآیند_مقدار.wait()
        self.فرآیند_مقدار.communicate()
        self.임시.cleanup()


def 보호커널(فهرست_مقدار_e5561a2b):
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
    항목들 = ['hello=' + str(مرتب_کردن / 'build/apps/hello.elf')]
    for نام, محتوا_مقدار in 사례들.items():
        مبداء = فهرست_مقدار_e5561a2b / (نام + '.s')
        مبداء.write_text('.code32\n.text\n.globl _start\n_start:\n' + محتوا_مقدار +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(فهرست_مقدار_e5561a2b / (نام + '.o')), str(مبداء)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(مرتب_کردن.parent / 'compiler/کاربر_پیوند_پیمایش.ld'),
                        '-o', str(فهرست_مقدار_e5561a2b / (نام + '.elf')), str(فهرست_مقدار_e5561a2b / (نام + '.o'))], check=True)
        항목들.append(نام + '=' + str(فهرست_مقدار_e5561a2b / (نام + '.elf')))
    정상 = bytearray((مرتب_کردن / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    بی_اعتبار_سنجش = bytearray(정상); بی_اعتبار_سنجش[0] = 0; 변형들['badelf'] = بی_اعتبار_سنجش
    بی_اعتبار_سنجش = bytearray(정상); struct.pack_into('<I', بی_اعتبار_سنجش, 24, 0x00100000); 변형들['badentry'] = بی_اعتبار_سنجش
    بی_اعتبار_سنجش = bytearray(정상); struct.pack_into('<I', بی_اعتبار_سنجش, 28, 0x7fffffff); 변형들['badtable'] = بی_اعتبار_سنجش
    بی_اعتبار_سنجش = bytearray(정상); جستجو_جدول = struct.unpack_from('<I', بی_اعتبار_سنجش, 28)[0]
    struct.pack_into('<I', بی_اعتبار_سنجش, جستجو_جدول + 20, 0x7fffffff); 변형들['badsize'] = بی_اعتبار_سنجش
    for نام, داده_ها in 변형들.items():
        پرونده = فهرست_مقدار_e5561a2b / (نام + '.elf'); پرونده.write_bytes(داده_ها)
        항목들.append(نام + '=' + str(پرونده))
    subprocess.run([sys.executable, str(مرتب_کردن / 'ابزارها/묶기.py'), '-o', str(فهرست_مقدار_e5561a2b / 'apps.bin')] + 항목들, check=True)
    مبداء = فهرست_مقدار_e5561a2b / 'apps.s'
    مبداء.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(فهرست_مقدار_e5561a2b / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(فهرست_مقدار_e5561a2b / 'apps.o'), str(مبداء)], check=True)
    هسته_مقدار = فهرست_مقدار_e5561a2b / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(مرتب_کردن / '부팅/پیوند_پیمایش.ld'), '-o', str(هسته_مقدار),
                    str(مرتب_کردن / 'build/boot.o'), str(مرتب_کردن / 'build/java.o'), str(مرتب_کردن / 'build/user.o'), str(فهرست_مقدار_e5561a2b / 'apps.o')], check=True)
    return هسته_مقدار


def اجرا_فرمان():
    سنجش = {}
    سرور_مقدار = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    سرور_مقدار.bind(('127.0.0.1', 0))
    سرور_مقدار.settimeout(0.1)
    تبدیل_مقدار = سرور_مقدار.getsockname()[1]
    받은것 = []
    خروج_برنامه = threading.Event()
    def 되보내기():
        while not خروج_برنامه.is_set():
            try: داده_ها, مشابه_مقدار = سرور_مقدار.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(داده_ها)
            if داده_ها != b'drop-me': سرور_مقدار.sendto(داده_ها, مشابه_مقدار)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            دستگاه = مجازی_دستگاه(مرتب_کردن / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                دستگاه.فرمان('apps', ['hello', 'udp', 'netcheck', 'stress'])
                دستگاه.فرمان('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                دستگاه.فرمان('run missing', ['Exit: -2'])
                دستگاه.فرمان('net', ['NET RTL8139'])
                دستگاه.فرمان('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for محتوا_مقدار in ('hello-network', 'odd', 'even', 'repeat-123'):
                    دستگاه.فرمان('run udp 10.0.2.2 {} {}'.format(تبدیل_مقدار, محتوا_مقدار), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert محتوا_مقدار.encode() in 받은것, 'میزبان 서버에서 자료를 받지 못함'
                دستگاه.فرمان('run stress {}'.format(تبدیل_مقدار), ['UDP STRESS PASS', 'Exit: 0'])
                دستگاه.فرمان('run udp 10.0.2.2 {} drop-me'.format(تبدیل_مقدار), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                دستگاه.فرمان('run hello recovered', ['arg: recovered', 'Exit: 0'])
                سنجش[종류] = دستگاه.واقعه_نگار_ردیف.decode('utf-8', 'replace')
                print('PASS: {} کاربر ELF/ring 3/نشانوندها/UDP میزبان 왕복/زمان_مقدار 초과/واسط 복귀'.format(종류), flush=True)
            finally:
                try: دستگاه.فرمان('net', [])
                except Exception: pass
                (مرتب_کردن / 'build/사용자통신-last.log').write_bytes(دستگاه.واقعه_نگار_ردیف)
                دستگاه.بستن()
        دستگاه = مجازی_دستگاه(مرتب_کردن / 'build/kernel.elf', شبکه_مقدار=False)
        try:
            دستگاه.فرمان('net', ['NET unavailable'])
            دستگاه.فرمان('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            دستگاه.فرمان('run hello', ['USER MODE ring 3', 'Exit: 0'])
            سنجش['no_nic'] = دستگاه.واقعه_نگار_ردیف.decode()
        finally: دستگاه.بستن()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            دستگاه = مجازی_دستگاه(보호커널(Path(임시)), شبکه_مقدار=False)
            try:
                for نام, وضعیت_مقدار in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    دستگاه.فرمان('run ' + نام, ['Exit: ' + str(وضعیت_مقدار)])
                    دستگاه.فرمان('run hello', ['USER MODE ring 3', 'Exit: 0'])
                سنجش['protection'] = دستگاه.واقعه_نگار_ردیف.decode()
                print('PASS: کاربر حافظه_داده_ها/포트 격리, 잘못된 اشاره_گر/ELF, CPU استثنا, 무한 تکرار_مقدار 제한', flush=True)
            finally:
                (مرتب_کردن / 'build/보호시험-last.log').write_bytes(دستگاه.واقعه_نگار_ردیف)
                دستگاه.بستن()
    finally:
        خروج_برنامه.set()
        일꾼.join(timeout=2)
        سرور_مقدار.close()
    سنجش['host_udp_received'] = [{'length': len(داده_ها), 'sha256': hashlib.sha256(داده_ها).hexdigest()} for داده_ها in 받은것]
    (مرتب_کردن / 'build/사용자통신시험.json').write_text(json.dumps(سنجش, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    اجرا_فرمان()
