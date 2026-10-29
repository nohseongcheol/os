#!/usr/bin/env python3
"""ھەقىقىي_مەلۇمات ring 3 ELF/باقار UDP 왕복/قوغدىماق_قىممىتى خاتالىق/시간 제한/잘못된 ELF를 검증한다."""
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

ئورۇن = Path(__file__).resolve().parents[1]


class مەۋھۇم_ماشىنا:
    def __init__(self, يول, 종류='elf', تور_قىممىتى=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        مۇندەرىجە_قىممىتى = Path(self.임시.name)
        self.خاتىرە_قۇر = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.كۆرسەتكۈچ_قىممىتى = socket.socket(socket.AF_UNIX)
        직렬경로, كۆرسەتكۈچ_يول = مۇندەرىجە_قىممىتى / 'serial.sock', مۇندەرىجە_قىممىتى / 'monitor.sock'
        بۇيرۇق = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(كۆرسەتكۈچ_يول) + ',server,nowait']
        بۇيرۇق += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if تور_قىممىتى else ['-net', 'none']
        بۇيرۇق += ['-kernel', str(يول)] if 종류 == 'elf' else ['-cdrom', str(يول), '-boot', 'd']
        if 저장매체 is not None:
            بۇيرۇق += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.جەريان_قىممىتى = subprocess.Popen(بۇيرۇق, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and كۆرسەتكۈچ_يول.exists()):
                if self.جەريان_قىممىتى.poll() is not None:
                    raise AssertionError(self.جەريان_قىممىتى.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ئىجرا_قىل_2 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.كۆرسەتكۈچ_قىممىتى.connect(str(كۆرسەتكۈچ_يول))
            self.직렬.setblocking(False)
            self.كۆرسەتكۈچ_قىممىتى.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.ياپ()
            raise

    def 기다림(self, 문구, ئىجرا_قىل_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.خاتىرە_قۇر[ئىجرا_قىل_2:]:
                return self.خاتىرە_قۇر[ئىجرا_قىل_2:].decode('utf-8', 'replace')
            ئوقۇ, _, _ = select.select([self.직렬], [], [], 0.1)
            if ئوقۇ:
                مەلۇمات = self.직렬.recv(65536)
                if not مەلۇمات: break
                self.خاتىرە_قۇر.extend(مەلۇمات)
            if self.جەريان_قىممىتى.poll() is not None: break
        raise AssertionError('대기 مەغلۇپ_بولۇش_قىممىتى: ' + 문구 + '\n' + self.خاتىرە_قۇر.decode('utf-8', 'replace'))

    def بۇيرۇق(self, ھەرپ_تىزمىسى_قىممىتى, 기대):
        ئىجرا_قىل_2 = len(self.خاتىرە_قۇر)
        self.직렬.sendall((ھەرپ_تىزمىسى_قىممىتى + '\n').encode())
        ئۆلچەم = self.기다림('jkoros> ', ئىجرا_قىل_2)
        for 문구 in 기대:
            assert 문구 in ئۆلچەم, (ھەرپ_تىزمىسى_قىممىتى, 문구, ئۆلچەم)
        assert 'PANIC' not in ئۆلچەم, ئۆلچەم
        return ئۆلچەم

    def ياپ(self):
        self.직렬.close()
        self.كۆرسەتكۈچ_قىممىتى.close()
        if self.جەريان_قىممىتى.poll() is None:
            self.جەريان_قىممىتى.terminate()
            try: self.جەريان_قىممىتى.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.جەريان_قىممىتى.kill()
                self.جەريان_قىممىتى.wait()
        self.جەريان_قىممىتى.communicate()
        self.임시.cleanup()


def 보호커널(مۇندەرىجە_قىممىتى):
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
    항목들 = ['hello=' + str(ئورۇن / 'build/apps/hello.elf')]
    for ئاتى, مەزمۇن_قىممىتى in 사례들.items():
        مەنبە = مۇندەرىجە_قىممىتى / (ئاتى + '.s')
        مەنبە.write_text('.code32\n.text\n.globl _start\n_start:\n' + مەزمۇن_قىممىتى +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(مۇندەرىجە_قىممىتى / (ئاتى + '.o')), str(مەنبە)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ئورۇن.parent / 'compiler/ئىشلەتكۈچى_ئۇلانما_لايىھە.ld'),
                        '-o', str(مۇندەرىجە_قىممىتى / (ئاتى + '.elf')), str(مۇندەرىجە_قىممىتى / (ئاتى + '.o'))], check=True)
        항목들.append(ئاتى + '=' + str(مۇندەرىجە_قىممىتى / (ئاتى + '.elf')))
    정상 = bytearray((ئورۇن / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ئۈنۈمسىز_ئۆلچەم = bytearray(정상); ئۈنۈمسىز_ئۆلچەم[0] = 0; 변형들['badelf'] = ئۈنۈمسىز_ئۆلچەم
    ئۈنۈمسىز_ئۆلچەم = bytearray(정상); struct.pack_into('<I', ئۈنۈمسىز_ئۆلچەم, 24, 0x00100000); 변형들['badentry'] = ئۈنۈمسىز_ئۆلچەم
    ئۈنۈمسىز_ئۆلچەم = bytearray(정상); struct.pack_into('<I', ئۈنۈمسىز_ئۆلچەم, 28, 0x7fffffff); 변형들['badtable'] = ئۈنۈمسىز_ئۆلچەم
    ئۈنۈمسىز_ئۆلچەم = bytearray(정상); ئىزدەش_جەدۋەل = struct.unpack_from('<I', ئۈنۈمسىز_ئۆلچەم, 28)[0]
    struct.pack_into('<I', ئۈنۈمسىز_ئۆلچەم, ئىزدەش_جەدۋەل + 20, 0x7fffffff); 변형들['badsize'] = ئۈنۈمسىز_ئۆلچەم
    for ئاتى, مەلۇمات in 변형들.items():
        ھۆججەت = مۇندەرىجە_قىممىتى / (ئاتى + '.elf'); ھۆججەت.write_bytes(مەلۇمات)
        항목들.append(ئاتى + '=' + str(ھۆججەت))
    subprocess.run([sys.executable, str(ئورۇن / 'قوراللار/묶기.py'), '-o', str(مۇندەرىجە_قىممىتى / 'apps.bin')] + 항목들, check=True)
    مەنبە = مۇندەرىجە_قىممىتى / 'apps.s'
    مەنبە.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(مۇندەرىجە_قىممىتى / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(مۇندەرىجە_قىممىتى / 'apps.o'), str(مەنبە)], check=True)
    يادرو_قىممىتى = مۇندەرىجە_قىممىتى / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ئورۇن / '부팅/ئۇلانما_لايىھە.ld'), '-o', str(يادرو_قىممىتى),
                    str(ئورۇن / 'build/boot.o'), str(ئورۇن / 'build/java.o'), str(ئورۇن / 'build/user.o'), str(مۇندەرىجە_قىممىتى / 'apps.o')], check=True)
    return يادرو_قىممىتى


def ئىجرا_قىلىش_بۇيرۇق():
    ئۆلچەم = {}
    مۇلازىمىتېر_قىممىتى = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    مۇلازىمىتېر_قىممىتى.bind(('127.0.0.1', 0))
    مۇلازىمىتېر_قىممىتى.settimeout(0.1)
    ئېغىز_قىممىتى = مۇلازىمىتېر_قىممىتى.getsockname()[1]
    받은것 = []
    چىقىش_ئەپ = threading.Event()
    def 되보내기():
        while not چىقىش_ئەپ.is_set():
            try: مەلۇمات, باراۋەرلىك_قىممىتى = مۇلازىمىتېر_قىممىتى.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(مەلۇمات)
            if مەلۇمات != b'drop-me': مۇلازىمىتېر_قىممىتى.sendto(مەلۇمات, باراۋەرلىك_قىممىتى)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ماشىنا.بۇيرۇق('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ماشىنا.بۇيرۇق('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ماشىنا.بۇيرۇق('run missing', ['Exit: -2'])
                ماشىنا.بۇيرۇق('net', ['NET RTL8139'])
                ماشىنا.بۇيرۇق('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for مەزمۇن_قىممىتى in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ماشىنا.بۇيرۇق('run udp 10.0.2.2 {} {}'.format(ئېغىز_قىممىتى, مەزمۇن_قىممىتى), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert مەزمۇن_قىممىتى.encode() in 받은것, 'باقار 서버에서 자료를 받지 못함'
                ماشىنا.بۇيرۇق('run stress {}'.format(ئېغىز_قىممىتى), ['UDP STRESS PASS', 'Exit: 0'])
                ماشىنا.بۇيرۇق('run udp 10.0.2.2 {} drop-me'.format(ئېغىز_قىممىتى), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ماشىنا.بۇيرۇق('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ئۆلچەم[종류] = ماشىنا.خاتىرە_قۇر.decode('utf-8', 'replace')
                print('PASS: {} ئىشلەتكۈچى ELF/ring 3/ئۆزگەرگۈچىلەر/UDP باقار 왕복/시간 초과/قاپ 복귀'.format(종류), flush=True)
            finally:
                try: ماشىنا.بۇيرۇق('net', [])
                except Exception: pass
                (ئورۇن / 'build/사용자통신-last.log').write_bytes(ماشىنا.خاتىرە_قۇر)
                ماشىنا.ياپ()
        ماشىنا = مەۋھۇم_ماشىنا(ئورۇن / 'build/kernel.elf', تور_قىممىتى=False)
        try:
            ماشىنا.بۇيرۇق('net', ['NET unavailable'])
            ماشىنا.بۇيرۇق('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ماشىنا.بۇيرۇق('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ئۆلچەم['no_nic'] = ماشىنا.خاتىرە_قۇر.decode()
        finally: ماشىنا.ياپ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ماشىنا = مەۋھۇم_ماشىنا(보호커널(Path(임시)), تور_قىممىتى=False)
            try:
                for ئاتى, ھالەت_قىممىتى in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ماشىنا.بۇيرۇق('run ' + ئاتى, ['Exit: ' + str(ھالەت_قىممىتى)])
                    ماشىنا.بۇيرۇق('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ئۆلچەم['protection'] = ماشىنا.خاتىرە_قۇر.decode()
                print('PASS: ئىشلەتكۈچى ساقلىغۇچ_مەلۇمات/قاتتىق_دېتال_ئېغىز 격리, 잘못된 ئىسترېلكا/ELF, CPU 예외, 무한 ئېنتىراتسىيە_قىممىتى 제한', flush=True)
            finally:
                (ئورۇن / 'build/보호시험-last.log').write_bytes(ماشىنا.خاتىرە_قۇر)
                ماشىنا.ياپ()
    finally:
        چىقىش_ئەپ.set()
        일꾼.join(timeout=2)
        مۇلازىمىتېر_قىممىتى.close()
    ئۆلچەم['host_udp_received'] = [{'length': len(مەلۇمات), 'sha256': hashlib.sha256(مەلۇمات).hexdigest()} for مەلۇمات in 받은것]
    (ئورۇن / 'build/사용자통신시험.json').write_text(json.dumps(ئۆلچەم, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ئىجرا_قىلىش_بۇيرۇق()
