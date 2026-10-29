#!/usr/bin/env python3
"""الفعلي_بيانات ring 3 ELF/مضيف UDP 왕복/يحمي_قيمة خطأ/قيمة_الوقت 제한/잘못된 ELF를 검증한다."""
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

موضع = Path(__file__).resolve().parents[1]


class جهاز_ظاهري:
    def __init__(self, مسار, 종류='elf', شبكة_قيمة=True, تخزين_متوسط=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        دليل_قيمة = Path(self.임시.name)
        self.سجل_سجل = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.يراقب_قيمة = socket.socket(socket.AF_UNIX)
        직렬경로, يراقب_مسار = دليل_قيمة / 'serial.sock', دليل_قيمة / 'monitor.sock'
        أمر = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(يراقب_مسار) + ',server,nowait']
        أمر += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if شبكة_قيمة else ['-net', 'none']
        أمر += ['-kernel', str(مسار)] if 종류 == 'elf' else ['-cdrom', str(مسار), '-boot', 'd']
        if تخزين_متوسط is not None:
            أمر += ['-drive', 'file=' + str(تخزين_متوسط) + ',format=raw,if=ide,index=0']
        self.عملية_قيمة = subprocess.Popen(أمر, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and يراقب_مسار.exists()):
                if self.عملية_قيمة.poll() is not None:
                    raise AssertionError(self.عملية_قيمة.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU تشغيل قيمة_الوقت 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.يراقب_قيمة.connect(str(يراقب_مسار))
            self.직렬.setblocking(False)
            self.يراقب_قيمة.sendall(b'cont\n')
            self.حالة_انتظار('jkoros> ')
        except BaseException:
            self.إغلاق()
            raise

    def حالة_انتظار(self, 문구, تشغيل=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.سجل_سجل[تشغيل:]:
                return self.سجل_سجل[تشغيل:].decode('utf-8', 'replace')
            قراءة, _, _ = select.select([self.직렬], [], [], 0.1)
            if قراءة:
                بيانات = self.직렬.recv(65536)
                if not بيانات: break
                self.سجل_سجل.extend(بيانات)
            if self.عملية_قيمة.poll() is not None: break
        raise AssertionError('انتظر_قيمة فشل_قيمة: ' + 문구 + '\n' + self.سجل_سجل.decode('utf-8', 'replace'))

    def أمر(self, سلسلة_قيمة, 기대):
        تشغيل = len(self.سجل_سجل)
        self.직렬.sendall((سلسلة_قيمة + '\n').encode())
        نتيجة = self.حالة_انتظار('jkoros> ', تشغيل)
        for 문구 in 기대:
            assert 문구 in نتيجة, (سلسلة_قيمة, 문구, نتيجة)
        assert 'PANIC' not in نتيجة, نتيجة
        return نتيجة

    def إغلاق(self):
        self.직렬.close()
        self.يراقب_قيمة.close()
        if self.عملية_قيمة.poll() is None:
            self.عملية_قيمة.terminate()
            try: self.عملية_قيمة.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.عملية_قيمة.kill()
                self.عملية_قيمة.wait()
        self.عملية_قيمة.communicate()
        self.임시.cleanup()


def 보호커널(دليل_قيمة):
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
    항목들 = ['hello=' + str(موضع / 'build/apps/hello.elf')]
    for اسم, محتوى_قيمة in 사례들.items():
        مصدر = دليل_قيمة / (اسم + '.s')
        مصدر.write_text('.code32\n.text\n.globl _start\n_start:\n' + محتوى_قيمة +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(دليل_قيمة / (اسم + '.o')), str(مصدر)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(موضع.parent / 'compiler/مستخدم_ربط_تخطيط.ld'),
                        '-o', str(دليل_قيمة / (اسم + '.elf')), str(دليل_قيمة / (اسم + '.o'))], check=True)
        항목들.append(اسم + '=' + str(دليل_قيمة / (اسم + '.elf')))
    أنظمة_المعلومات_عادي = bytearray((موضع / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    غير_صالح_مقياس = bytearray(أنظمة_المعلومات_عادي); غير_صالح_مقياس[0] = 0; 변형들['badelf'] = غير_صالح_مقياس
    غير_صالح_مقياس = bytearray(أنظمة_المعلومات_عادي); struct.pack_into('<I', غير_صالح_مقياس, 24, 0x00100000); 변형들['badentry'] = غير_صالح_مقياس
    غير_صالح_مقياس = bytearray(أنظمة_المعلومات_عادي); struct.pack_into('<I', غير_صالح_مقياس, 28, 0x7fffffff); 변형들['badtable'] = غير_صالح_مقياس
    غير_صالح_مقياس = bytearray(أنظمة_المعلومات_عادي); جدول_البحث = struct.unpack_from('<I', غير_صالح_مقياس, 28)[0]
    struct.pack_into('<I', غير_صالح_مقياس, جدول_البحث + 20, 0x7fffffff); 변형들['badsize'] = غير_صالح_مقياس
    for اسم, بيانات in 변형들.items():
        ملف = دليل_قيمة / (اسم + '.elf'); ملف.write_bytes(بيانات)
        항목들.append(اسم + '=' + str(ملف))
    subprocess.run([sys.executable, str(موضع / 'أدوات/يربط_المشارك.py'), '-o', str(دليل_قيمة / 'apps.bin')] + 항목들, check=True)
    مصدر = دليل_قيمة / 'apps.s'
    مصدر.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(دليل_قيمة / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(دليل_قيمة / 'apps.o'), str(مصدر)], check=True)
    نواة_قيمة = دليل_قيمة / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(موضع / 'إقلاع_الآلة/تخطيط_الربط.ld'), '-o', str(نواة_قيمة),
                    str(موضع / 'build/boot.o'), str(موضع / 'build/java.o'), str(موضع / 'build/user.o'), str(دليل_قيمة / 'apps.o')], check=True)
    return نواة_قيمة


def ينفذ_أمر():
    نتيجة = {}
    خادم_قيمة = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    خادم_قيمة.bind(('127.0.0.1', 0))
    خادم_قيمة.settimeout(0.1)
    منفذ_قيمة = خادم_قيمة.getsockname()[1]
    받은것 = []
    خروج_تطبيق = threading.Event()
    def ارتداد_رد():
        while not خروج_تطبيق.is_set():
            try: بيانات, نظير_قيمة = خادم_قيمة.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(بيانات)
            if بيانات != b'drop-me': خادم_قيمة.sendto(بيانات, نظير_قيمة)
    عامل_قيمة = threading.Thread(target=ارتداد_رد, daemon=True)
    عامل_قيمة.start()
    try:
        for 종류 in ('elf', 'iso'):
            جهاز = جهاز_ظاهري(موضع / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                جهاز.أمر('apps', ['hello', 'udp', 'netcheck', 'stress'])
                جهاز.أمر('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                جهاز.أمر('run missing', ['Exit: -2'])
                جهاز.أمر('net', ['NET RTL8139'])
                جهاز.أمر('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for محتوى_قيمة in ('hello-network', 'odd', 'even', 'repeat-123'):
                    جهاز.أمر('run udp 10.0.2.2 {} {}'.format(منفذ_قيمة, محتوى_قيمة), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert محتوى_قيمة.encode() in 받은것, 'مضيف 서버에서 자료를 받지 못함'
                جهاز.أمر('run stress {}'.format(منفذ_قيمة), ['UDP STRESS PASS', 'Exit: 0'])
                جهاز.أمر('run udp 10.0.2.2 {} drop-me'.format(منفذ_قيمة), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                جهاز.أمر('run hello recovered', ['arg: recovered', 'Exit: 0'])
                نتيجة[종류] = جهاز.سجل_سجل.decode('utf-8', 'replace')
                print('PASS: {} فضاء_المستخدم ELF/ring 3/وسائط/UDP مضيف 왕복/قيمة_الوقت 초과/셸 복귀'.format(종류), flush=True)
            finally:
                try: جهاز.أمر('net', [])
                except Exception: pass
                (موضع / 'build/사용자통신-last.log').write_bytes(جهاز.سجل_سجل)
                جهاز.إغلاق()
        جهاز = جهاز_ظاهري(موضع / 'build/kernel.elf', شبكة_قيمة=False)
        try:
            جهاز.أمر('net', ['NET unavailable'])
            جهاز.أمر('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            جهاز.أمر('run hello', ['USER MODE ring 3', 'Exit: 0'])
            نتيجة['no_nic'] = جهاز.سجل_سجل.decode()
        finally: جهاز.إغلاق()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            جهاز = جهاز_ظاهري(보호커널(Path(임시)), شبكة_قيمة=False)
            try:
                for اسم, حالة_قيمة in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    جهاز.أمر('run ' + اسم, ['Exit: ' + str(حالة_قيمة)])
                    جهاز.أمر('run hello', ['USER MODE ring 3', 'Exit: 0'])
                نتيجة['protection'] = جهاز.سجل_سجل.decode()
                print('PASS: فضاء_المستخدم ذاكرة_بيانات/أجهزة_منفذ 격리, 잘못된 مؤشر/ELF, CPU استثناء, 무한 تكرار_قيمة 제한', flush=True)
            finally:
                (موضع / 'build/حماية_يختبر-last.log').write_bytes(جهاز.سجل_سجل)
                جهاز.إغلاق()
    finally:
        خروج_تطبيق.set()
        عامل_قيمة.join(timeout=2)
        خادم_قيمة.close()
    نتيجة['host_udp_received'] = [{'length': len(بيانات), 'sha256': hashlib.sha256(بيانات).hexdigest()} for بيانات in 받은것]
    (موضع / 'build/يختبر_مستخدم_شبكة.json').write_text(json.dumps(نتيجة, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ينفذ_أمر()
