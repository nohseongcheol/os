#!/usr/bin/env python3
"""প্ৰকৃত_ডাটা ring 3 ELF/হ_ষ্ট UDP 왕복/প্রতিৰোধ_কৰক_মান ত্ৰুটি/시간 제한/잘못된 ELF를 검증한다."""
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

অৱস্থান = Path(__file__).resolve().parents[1]


class ভাৰ্ছুৱেল_মেচিন:
    def __init__(self, পথ, 종류='elf', নেটৱৰ্ক_মান=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ডাইৰেক্টৰী_মান = Path(self.임시.name)
        self.লগ_শাৰী = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.মনিটৰ_মান = socket.socket(socket.AF_UNIX)
        직렬경로, মনিটৰ_পথ = ডাইৰেক্টৰী_মান / 'serial.sock', ডাইৰেক্টৰী_মান / 'monitor.sock'
        কমান্ড = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(মনিটৰ_পথ) + ',server,nowait']
        কমান্ড += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if নেটৱৰ্ক_মান else ['-net', 'none']
        কমান্ড += ['-kernel', str(পথ)] if 종류 == 'elf' else ['-cdrom', str(পথ), '-boot', 'd']
        if 저장매체 is not None:
            কমান্ড += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.প্ৰক্ৰিয়া_মান = subprocess.Popen(কমান্ড, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and মনিটৰ_পথ.exists()):
                if self.প্ৰক্ৰিয়া_মান.poll() is not None:
                    raise AssertionError(self.প্ৰক্ৰিয়া_মান.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU সঞ্চালন 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.মনিটৰ_মান.connect(str(মনিটৰ_পথ))
            self.직렬.setblocking(False)
            self.মনিটৰ_মান.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.বন্ধ_কৰক()
            raise

    def 기다림(self, 문구, সঞ্চালন=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.লগ_শাৰী[সঞ্চালন:]:
                return self.লগ_শাৰী[সঞ্চালন:].decode('utf-8', 'replace')
            পড়া, _, _ = select.select([self.직렬], [], [], 0.1)
            if পড়া:
                ডাটা = self.직렬.recv(65536)
                if not ডাটা: break
                self.লগ_শাৰী.extend(ডাটা)
            if self.প্ৰক্ৰিয়া_মান.poll() is not None: break
        raise AssertionError('대기 বিফলতা_মান: ' + 문구 + '\n' + self.লগ_শাৰী.decode('utf-8', 'replace'))

    def কমান্ড(self, ষ্ট্ৰিং_মান, 기대):
        সঞ্চালন = len(self.লগ_শাৰী)
        self.직렬.sendall((ষ্ট্ৰিং_মান + '\n').encode())
        পৰিমাপ = self.기다림('jkoros> ', সঞ্চালন)
        for 문구 in 기대:
            assert 문구 in পৰিমাপ, (ষ্ট্ৰিং_মান, 문구, পৰিমাপ)
        assert 'PANIC' not in পৰিমাপ, পৰিমাপ
        return পৰিমাপ

    def বন্ধ_কৰক(self):
        self.직렬.close()
        self.মনিটৰ_মান.close()
        if self.প্ৰক্ৰিয়া_মান.poll() is None:
            self.প্ৰক্ৰিয়া_মান.terminate()
            try: self.প্ৰক্ৰিয়া_মান.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.প্ৰক্ৰিয়া_মান.kill()
                self.প্ৰক্ৰিয়া_মান.wait()
        self.প্ৰক্ৰিয়া_মান.communicate()
        self.임시.cleanup()


def 보호커널(ডাইৰেক্টৰী_মান):
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
    항목들 = ['hello=' + str(অৱস্থান / 'build/apps/hello.elf')]
    for নাম, সামগ্ৰী_মান in 사례들.items():
        উৎস = ডাইৰেক্টৰী_মান / (নাম + '.s')
        উৎস.write_text('.code32\n.text\n.globl _start\n_start:\n' + সামগ্ৰী_মান +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ডাইৰেক্টৰী_মান / (নাম + '.o')), str(উৎস)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(অৱস্থান.parent / 'compiler/ব্যৱহাৰকৰ্তা_লিংক_লেআউট.ld'),
                        '-o', str(ডাইৰেক্টৰী_মান / (নাম + '.elf')), str(ডাইৰেক্টৰী_মান / (নাম + '.o'))], check=True)
        항목들.append(নাম + '=' + str(ডাইৰেক্টৰী_মান / (নাম + '.elf')))
    정상 = bytearray((অৱস্থান / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    অবৈধ_পৰিমাপ = bytearray(정상); অবৈধ_পৰিমাপ[0] = 0; 변형들['badelf'] = অবৈধ_পৰিমাপ
    অবৈধ_পৰিমাপ = bytearray(정상); struct.pack_into('<I', অবৈধ_পৰিমাপ, 24, 0x00100000); 변형들['badentry'] = অবৈধ_পৰিমাপ
    অবৈধ_পৰিমাপ = bytearray(정상); struct.pack_into('<I', অবৈধ_পৰিমাপ, 28, 0x7fffffff); 변형들['badtable'] = অবৈধ_পৰিমাপ
    অবৈধ_পৰিমাপ = bytearray(정상); লুকআপ_তালিকা = struct.unpack_from('<I', অবৈধ_পৰিমাপ, 28)[0]
    struct.pack_into('<I', অবৈধ_পৰিমাপ, লুকআপ_তালিকা + 20, 0x7fffffff); 변형들['badsize'] = অবৈধ_পৰিমাপ
    for নাম, ডাটা in 변형들.items():
        নথিপত্ৰ = ডাইৰেক্টৰী_মান / (নাম + '.elf'); নথিপত্ৰ.write_bytes(ডাটা)
        항목들.append(নাম + '=' + str(নথিপত্ৰ))
    subprocess.run([sys.executable, str(অৱস্থান / 'সঁজুলিসমূহ/묶기.py'), '-o', str(ডাইৰেক্টৰী_মান / 'apps.bin')] + 항목들, check=True)
    উৎস = ডাইৰেক্টৰী_মান / 'apps.s'
    উৎস.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ডাইৰেক্টৰী_মান / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ডাইৰেক্টৰী_মান / 'apps.o'), str(উৎস)], check=True)
    কাৰ্ণেল_মান = ডাইৰেক্টৰী_মান / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(অৱস্থান / '부팅/লিংক_লেআউট.ld'), '-o', str(কাৰ্ণেল_মান),
                    str(অৱস্থান / 'build/boot.o'), str(অৱস্থান / 'build/java.o'), str(অৱস্থান / 'build/user.o'), str(ডাইৰেক্টৰী_মান / 'apps.o')], check=True)
    return কাৰ্ণেল_মান


def নিষ্পাদন_আদেশ():
    পৰিমাপ = {}
    ছাৰ্ভাৰ_মান = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ছাৰ্ভাৰ_মান.bind(('127.0.0.1', 0))
    ছাৰ্ভাৰ_মান.settimeout(0.1)
    পৰ্ট_মান = ছাৰ্ভাৰ_মান.getsockname()[1]
    받은것 = []
    প্ৰস্থান_এপ্প্ = threading.Event()
    def 되보내기():
        while not প্ৰস্থান_এপ্প্.is_set():
            try: ডাটা, পীয়েৰ_মান = ছাৰ্ভাৰ_মান.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ডাটা)
            if ডাটা != b'drop-me': ছাৰ্ভাৰ_মান.sendto(ডাটা, পীয়েৰ_মান)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                মেচিন.কমান্ড('apps', ['hello', 'udp', 'netcheck', 'stress'])
                মেচিন.কমান্ড('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                মেচিন.কমান্ড('run missing', ['Exit: -2'])
                মেচিন.কমান্ড('net', ['NET RTL8139'])
                মেচিন.কমান্ড('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for সামগ্ৰী_মান in ('hello-network', 'odd', 'even', 'repeat-123'):
                    মেচিন.কমান্ড('run udp 10.0.2.2 {} {}'.format(পৰ্ট_মান, সামগ্ৰী_মান), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert সামগ্ৰী_মান.encode() in 받은것, 'হ_ষ্ট 서버에서 자료를 받지 못함'
                মেচিন.কমান্ড('run stress {}'.format(পৰ্ট_মান), ['UDP STRESS PASS', 'Exit: 0'])
                মেচিন.কমান্ড('run udp 10.0.2.2 {} drop-me'.format(পৰ্ট_মান), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                মেচিন.কমান্ড('run hello recovered', ['arg: recovered', 'Exit: 0'])
                পৰিমাপ[종류] = মেচিন.লগ_শাৰী.decode('utf-8', 'replace')
                print('PASS: {} ব্যৱহাৰকৰ্তা ELF/ring 3/인수/UDP হ_ষ্ট 왕복/시간 초과/শ্বেল 복귀'.format(종류), flush=True)
            finally:
                try: মেচিন.কমান্ড('net', [])
                except Exception: pass
                (অৱস্থান / 'build/사용자통신-last.log').write_bytes(মেচিন.লগ_শাৰী)
                মেচিন.বন্ধ_কৰক()
        মেচিন = ভাৰ্ছুৱেল_মেচিন(অৱস্থান / 'build/kernel.elf', নেটৱৰ্ক_মান=False)
        try:
            মেচিন.কমান্ড('net', ['NET unavailable'])
            মেচিন.কমান্ড('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            মেচিন.কমান্ড('run hello', ['USER MODE ring 3', 'Exit: 0'])
            পৰিমাপ['no_nic'] = মেচিন.লগ_শাৰী.decode()
        finally: মেচিন.বন্ধ_কৰক()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            মেচিন = ভাৰ্ছুৱেল_মেচিন(보호커널(Path(임시)), নেটৱৰ্ক_মান=False)
            try:
                for নাম, অৱস্থা_মান in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    মেচিন.কমান্ড('run ' + নাম, ['Exit: ' + str(অৱস্থা_মান)])
                    মেচিন.কমান্ড('run hello', ['USER MODE ring 3', 'Exit: 0'])
                পৰিমাপ['protection'] = মেচিন.লগ_শাৰী.decode()
                print('PASS: ব্যৱহাৰকৰ্তা মেম_ৰি_ডাটা/포트 격리, 잘못된 পইণ্টাৰ/ELF, CPU 예외, 무한 পুণৰাবৃত্তি_মান 제한', flush=True)
            finally:
                (অৱস্থান / 'build/보호시험-last.log').write_bytes(মেচিন.লগ_শাৰী)
                মেচিন.বন্ধ_কৰক()
    finally:
        প্ৰস্থান_এপ্প্.set()
        일꾼.join(timeout=2)
        ছাৰ্ভাৰ_মান.close()
    পৰিমাপ['host_udp_received'] = [{'length': len(ডাটা), 'sha256': hashlib.sha256(ডাটা).hexdigest()} for ডাটা in 받은것]
    (অৱস্থান / 'build/사용자통신시험.json').write_text(json.dumps(পৰিমাপ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    নিষ্পাদন_আদেশ()
