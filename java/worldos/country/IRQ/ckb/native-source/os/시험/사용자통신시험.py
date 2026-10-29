#!/usr/bin/env python3
"""ڕاستەکی_دەیتا ring 3 ELF/جێدەر UDP 왕복/پاراستن_نرخ هەڵە/کات_نرخ 제한/잘못된 ELF를 검증한다."""
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


class مەجازی_مەکینه:
    def __init__(self, گوزەر, 종류='elf', تۆڕ_نرخ=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ڕێبەرنامە_نرخ = Path(self.임시.name)
        self.تۆمار_ڕزن = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.مۆنیتۆر_نرخ = socket.socket(socket.AF_UNIX)
        직렬경로, مۆنیتۆر_گوزەر = ڕێبەرنامە_نرخ / 'serial.sock', ڕێبەرنامە_نرخ / 'monitor.sock'
        فەرمان = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(مۆنیتۆر_گوزەر) + ',server,nowait']
        فەرمان += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if تۆڕ_نرخ else ['-net', 'none']
        فەرمان += ['-kernel', str(گوزەر)] if 종류 == 'elf' else ['-cdrom', str(گوزەر), '-boot', 'd']
        if 저장매체 is not None:
            فەرمان += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.پرۆسە_نرخ = subprocess.Popen(فەرمان, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and مۆنیتۆر_گوزەر.exists()):
                if self.پرۆسە_نرخ.poll() is not None:
                    raise AssertionError(self.پرۆسە_نرخ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ڕادان کات_نرخ 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.مۆنیتۆر_نرخ.connect(str(مۆنیتۆر_گوزەر))
            self.직렬.setblocking(False)
            self.مۆنیتۆر_نرخ.sendall(b'cont\n')
            self.چاوەڕوان_کردن_دۆخ('jkoros> ')
        except BaseException:
            self.داخستن()
            raise

    def چاوەڕوان_کردن_دۆخ(self, 문구, ڕادان=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.تۆمار_ڕزن[ڕادان:]:
                return self.تۆمار_ڕزن[ڕادان:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                دەیتا = self.직렬.recv(65536)
                if not دەیتا: break
                self.تۆمار_ڕزن.extend(دەیتا)
            if self.پرۆسە_نرخ.poll() is not None: break
        raise AssertionError('چاوەڕوان_کردن_نرخ شکستهێنان_نرخ: ' + 문구 + '\n' + self.تۆمار_ڕزن.decode('utf-8', 'replace'))

    def فەرمان(self, رست_نرخ, 기대):
        ڕادان = len(self.تۆمار_ڕزن)
        self.직렬.sendall((رست_نرخ + '\n').encode())
        결과 = self.چاوەڕوان_کردن_دۆخ('jkoros> ', ڕادان)
        for 문구 in 기대:
            assert 문구 in 결과, (رست_نرخ, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def داخستن(self):
        self.직렬.close()
        self.مۆنیتۆر_نرخ.close()
        if self.پرۆسە_نرخ.poll() is None:
            self.پرۆسە_نرخ.terminate()
            try: self.پرۆسە_نرخ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.پرۆسە_نرخ.kill()
                self.پرۆسە_نرخ.wait()
        self.پرۆسە_نرخ.communicate()
        self.임시.cleanup()


def 보호커널(ڕێبەرنامە_نرخ):
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
    for ناو, ناوەرۆک_نرخ in 사례들.items():
        ژێدەر = ڕێبەرنامە_نرخ / (ناو + '.s')
        ژێدەر.write_text('.code32\n.text\n.globl _start\n_start:\n' + ناوەرۆک_نرخ +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ڕێبەرنامە_نرخ / (ناو + '.o')), str(ژێدەر)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/بەکارهێنەر_لینك_ڕیزبەست.ld'),
                        '-o', str(ڕێبەرنامە_نرخ / (ناو + '.elf')), str(ڕێبەرنامە_نرخ / (ناو + '.o'))], check=True)
        항목들.append(ناو + '=' + str(ڕێبەرنامە_نرخ / (ناو + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for ناو, دەیتا in 변형들.items():
        فایل = ڕێبەرنامە_نرخ / (ناو + '.elf'); فایل.write_bytes(دەیتا)
        항목들.append(ناو + '=' + str(فایل))
    subprocess.run([sys.executable, str(위치 / 'ئامرازەکان/묶기.py'), '-o', str(ڕێبەرنامە_نرخ / 'apps.bin')] + 항목들, check=True)
    ژێدەر = ڕێبەرنامە_نرخ / 'apps.s'
    ژێدەر.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ڕێبەرنامە_نرخ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ڕێبەرنامە_نرخ / 'apps.o'), str(ژێدەر)], check=True)
    کوورەک_نرخ = ڕێبەرنامە_نرخ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/لینك_ڕیزبەست.ld'), '-o', str(کوورەک_نرخ),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(ڕێبەرنامە_نرخ / 'apps.o')], check=True)
    return کوورەک_نرخ


def جێبەجێکردن_فەرمان():
    결과 = {}
    ڕاژەکار_نرخ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ڕاژەکار_نرخ.bind(('127.0.0.1', 0))
    ڕاژەکار_نرخ.settimeout(0.1)
    دەرگا_نرخ = ڕاژەکار_نرخ.getsockname()[1]
    받은것 = []
    بزربوون_بەرنامە = threading.Event()
    def 되보내기():
        while not بزربوون_بەرنامە.is_set():
            try: دەیتا, هاوتا_نرخ = ڕاژەکار_نرخ.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(دەیتا)
            if دەیتا != b'drop-me': ڕاژەکار_نرخ.sendto(دەیتا, هاوتا_نرخ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            مەکینه = مەجازی_مەکینه(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                مەکینه.فەرمان('apps', ['hello', 'udp', 'netcheck', 'stress'])
                مەکینه.فەرمان('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                مەکینه.فەرمان('run missing', ['Exit: -2'])
                مەکینه.فەرمان('net', ['NET RTL8139'])
                مەکینه.فەرمان('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ناوەرۆک_نرخ in ('hello-network', 'odd', 'even', 'repeat-123'):
                    مەکینه.فەرمان('run udp 10.0.2.2 {} {}'.format(دەرگا_نرخ, ناوەرۆک_نرخ), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ناوەرۆک_نرخ.encode() in 받은것, 'جێدەر 서버에서 자료를 받지 못함'
                مەکینه.فەرمان('run stress {}'.format(دەرگا_نرخ), ['UDP STRESS PASS', 'Exit: 0'])
                مەکینه.فەرمان('run udp 10.0.2.2 {} drop-me'.format(دەرگا_نرخ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                مەکینه.فەرمان('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = مەکینه.تۆمار_ڕزن.decode('utf-8', 'replace')
                print('PASS: {} بەکارهێنەر ELF/ring 3/인수/UDP جێدەر 왕복/کات_نرخ 초과/توێکڵ 복귀'.format(종류), flush=True)
            finally:
                try: مەکینه.فەرمان('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(مەکینه.تۆمار_ڕزن)
                مەکینه.داخستن()
        مەکینه = مەجازی_مەکینه(위치 / 'build/kernel.elf', تۆڕ_نرخ=False)
        try:
            مەکینه.فەرمان('net', ['NET unavailable'])
            مەکینه.فەرمان('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            مەکینه.فەرمان('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = مەکینه.تۆمار_ڕزن.decode()
        finally: مەکینه.داخستن()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            مەکینه = مەجازی_مەکینه(보호커널(Path(임시)), تۆڕ_نرخ=False)
            try:
                for ناو, دۆخ_نرخ in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    مەکینه.فەرمان('run ' + ناو, ['Exit: ' + str(دۆخ_نرخ)])
                    مەکینه.فەرمان('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = مەکینه.تۆمار_ڕزن.decode()
                print('PASS: بەکارهێنەر بیرگە_دەیتا/포트 격리, 잘못된 نیشاندەر/ELF, CPU 예외, 무한 دووبارەکردنەوە_نرخ 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(مەکینه.تۆمار_ڕزن)
                مەکینه.داخستن()
    finally:
        بزربوون_بەرنامە.set()
        일꾼.join(timeout=2)
        ڕاژەکار_نرخ.close()
    결과['host_udp_received'] = [{'length': len(دەیتا), 'sha256': hashlib.sha256(دەیتا).hexdigest()} for دەیتا in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    جێبەجێکردن_فەرمان()
