#!/usr/bin/env python3
"""প্রকৃত_ডাটা ring 3 ELF/হোস্ট UDP 왕복/রক্ষা_করুন_মান ত্রুটি/সময়_মান 제한/잘못된 ELF를 검증한다."""
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

অবস্থান = Path(__file__).resolve().parents[1]


class কল্পিত_মেশিন:
    def __init__(self, পথ_2, 종류='elf', নেটওয়ার্ক_মান=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ডিরেক্টরি_মান = Path(self.임시.name)
        self.লগ_সারি = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.মনিটর_মান = socket.socket(socket.AF_UNIX)
        직렬경로, মনিটর_পথ = ডিরেক্টরি_মান / 'serial.sock', ডিরেক্টরি_মান / 'monitor.sock'
        আদেশ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(মনিটর_পথ) + ',server,nowait']
        আদেশ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if নেটওয়ার্ক_মান else ['-net', 'none']
        আদেশ += ['-kernel', str(পথ_2)] if 종류 == 'elf' else ['-cdrom', str(পথ_2), '-boot', 'd']
        if 저장매체 is not None:
            আদেশ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.প্রসেসর_মান = subprocess.Popen(আদেশ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and মনিটর_পথ.exists()):
                if self.প্রসেসর_মান.poll() is not None:
                    raise AssertionError(self.প্রসেসর_মান.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU চালনা সময়_মান 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.মনিটর_মান.connect(str(মনিটর_পথ))
            self.직렬.setblocking(False)
            self.মনিটর_মান.sendall(b'cont\n')
            self.অপেক্ষা_অবস্হা('jkoros> ')
        except BaseException:
            self.বন্ধ_করুন()
            raise

    def অপেক্ষা_অবস্হা(self, 문구, চালনা=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.লগ_সারি[চালনা:]:
                return self.লগ_সারি[চালনা:].decode('utf-8', 'replace')
            পড়া, _, _ = select.select([self.직렬], [], [], 0.1)
            if পড়া:
                ডাটা = self.직렬.recv(65536)
                if not ডাটা: break
                self.লগ_সারি.extend(ডাটা)
            if self.প্রসেসর_মান.poll() is not None: break
        raise AssertionError('অপেক্ষা_মান বিফলতা_মান: ' + 문구 + '\n' + self.লগ_সারি.decode('utf-8', 'replace'))

    def আদেশ(self, স্ট্রিং_মান, 기대):
        চালনা = len(self.লগ_সারি)
        self.직렬.sendall((স্ট্রিং_মান + '\n').encode())
        পরিমাপ = self.অপেক্ষা_অবস্হা('jkoros> ', চালনা)
        for 문구 in 기대:
            assert 문구 in পরিমাপ, (স্ট্রিং_মান, 문구, পরিমাপ)
        assert 'PANIC' not in পরিমাপ, পরিমাপ
        return পরিমাপ

    def বন্ধ_করুন(self):
        self.직렬.close()
        self.মনিটর_মান.close()
        if self.প্রসেসর_মান.poll() is None:
            self.প্রসেসর_মান.terminate()
            try: self.প্রসেসর_মান.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.প্রসেসর_মান.kill()
                self.প্রসেসর_মান.wait()
        self.প্রসেসর_মান.communicate()
        self.임시.cleanup()


def 보호커널(ডিরেক্টরি_মান):
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
    항목들 = ['hello=' + str(অবস্থান / 'build/apps/hello.elf')]
    for নাম, সামগ্রি_মান in 사례들.items():
        উৎস_নথি = ডিরেক্টরি_মান / (নাম + '.s')
        উৎস_নথি.write_text('.code32\n.text\n.globl _start\n_start:\n' + সামগ্রি_মান +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ডিরেক্টরি_মান / (নাম + '.o')), str(উৎস_নথি)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(অবস্থান.parent / 'compiler/ব্যবহারকারী_লিংক_লেআউট.ld'),
                        '-o', str(ডিরেক্টরি_মান / (নাম + '.elf')), str(ডিরেক্টরি_মান / (নাম + '.o'))], check=True)
        항목들.append(নাম + '=' + str(ডিরেক্টরি_মান / (নাম + '.elf')))
    정상 = bytearray((অবস্থান / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    অবৈধ_পরিমাপ = bytearray(정상); অবৈধ_পরিমাপ[0] = 0; 변형들['badelf'] = অবৈধ_পরিমাপ
    অবৈধ_পরিমাপ = bytearray(정상); struct.pack_into('<I', অবৈধ_পরিমাপ, 24, 0x00100000); 변형들['badentry'] = অবৈধ_পরিমাপ
    অবৈধ_পরিমাপ = bytearray(정상); struct.pack_into('<I', অবৈধ_পরিমাপ, 28, 0x7fffffff); 변형들['badtable'] = অবৈধ_পরিমাপ
    অবৈধ_পরিমাপ = bytearray(정상); লুকআপ_সারণি = struct.unpack_from('<I', অবৈধ_পরিমাপ, 28)[0]
    struct.pack_into('<I', অবৈধ_পরিমাপ, লুকআপ_সারণি + 20, 0x7fffffff); 변형들['badsize'] = অবৈধ_পরিমাপ
    for নাম, ডাটা in 변형들.items():
        নথির_নাম = ডিরেক্টরি_মান / (নাম + '.elf'); নথির_নাম.write_bytes(ডাটা)
        항목들.append(নাম + '=' + str(নথির_নাম))
    subprocess.run([sys.executable, str(অবস্থান / 'সরঞ্জামগুলি/묶기.py'), '-o', str(ডিরেক্টরি_মান / 'apps.bin')] + 항목들, check=True)
    উৎস_নথি = ডিরেক্টরি_মান / 'apps.s'
    উৎস_নথি.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ডিরেক্টরি_মান / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ডিরেক্টরি_মান / 'apps.o'), str(উৎস_নথি)], check=True)
    কারনেল_মান = ডিরেক্টরি_মান / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(অবস্থান / '부팅/লিংক_লেআউট.ld'), '-o', str(কারনেল_মান),
                    str(অবস্থান / 'build/boot.o'), str(অবস্থান / 'build/java.o'), str(অবস্থান / 'build/user.o'), str(ডিরেক্টরি_মান / 'apps.o')], check=True)
    return কারনেল_মান


def কার্যকর_করুন_আদেশ():
    পরিমাপ = {}
    সার্ভার_মান = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    সার্ভার_মান.bind(('127.0.0.1', 0))
    সার্ভার_মান.settimeout(0.1)
    পোর্ট_মান = সার্ভার_মান.getsockname()[1]
    받은것 = []
    প্রস্থান_অ্যাপ = threading.Event()
    def 되보내기():
        while not প্রস্থান_অ্যাপ.is_set():
            try: ডাটা, পিয়ার_মান = সার্ভার_মান.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ডাটা)
            if ডাটা != b'drop-me': সার্ভার_মান.sendto(ডাটা, পিয়ার_মান)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            মেশিন = কল্পিত_মেশিন(অবস্থান / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                মেশিন.আদেশ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                মেশিন.আদেশ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                মেশিন.আদেশ('run missing', ['Exit: -2'])
                মেশিন.আদেশ('net', ['NET RTL8139'])
                মেশিন.আদেশ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for সামগ্রি_মান in ('hello-network', 'odd', 'even', 'repeat-123'):
                    মেশিন.আদেশ('run udp 10.0.2.2 {} {}'.format(পোর্ট_মান, সামগ্রি_মান), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert সামগ্রি_মান.encode() in 받은것, 'হোস্ট 서버에서 자료를 받지 못함'
                মেশিন.আদেশ('run stress {}'.format(পোর্ট_মান), ['UDP STRESS PASS', 'Exit: 0'])
                মেশিন.আদেশ('run udp 10.0.2.2 {} drop-me'.format(পোর্ট_মান), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                মেশিন.আদেশ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                পরিমাপ[종류] = মেশিন.লগ_সারি.decode('utf-8', 'replace')
                print('PASS: {} ব্যবহারকারী ELF/ring 3/আর্গুমেন্ট_তালিকা/UDP হোস্ট 왕복/সময়_মান 초과/শেল 복귀'.format(종류), flush=True)
            finally:
                try: মেশিন.আদেশ('net', [])
                except Exception: pass
                (অবস্থান / 'build/사용자통신-last.log').write_bytes(মেশিন.লগ_সারি)
                মেশিন.বন্ধ_করুন()
        মেশিন = কল্পিত_মেশিন(অবস্থান / 'build/kernel.elf', নেটওয়ার্ক_মান=False)
        try:
            মেশিন.আদেশ('net', ['NET unavailable'])
            মেশিন.আদেশ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            মেশিন.আদেশ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            পরিমাপ['no_nic'] = মেশিন.লগ_সারি.decode()
        finally: মেশিন.বন্ধ_করুন()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            মেশিন = কল্পিত_মেশিন(보호커널(Path(임시)), নেটওয়ার্ক_মান=False)
            try:
                for নাম, অবস্হা_মান in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    মেশিন.আদেশ('run ' + নাম, ['Exit: ' + str(অবস্হা_মান)])
                    মেশিন.আদেশ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                পরিমাপ['protection'] = মেশিন.লগ_সারি.decode()
                print('PASS: ব্যবহারকারী মেমরি_ডাটা/হার্ডওয়্যার_পোর্ট 격리, 잘못된 নির্দেশক/ELF, CPU ব্যতিক্রম, 무한 পুনরুক্তি_মান 제한', flush=True)
            finally:
                (অবস্থান / 'build/보호시험-last.log').write_bytes(মেশিন.লগ_সারি)
                মেশিন.বন্ধ_করুন()
    finally:
        প্রস্থান_অ্যাপ.set()
        일꾼.join(timeout=2)
        সার্ভার_মান.close()
    পরিমাপ['host_udp_received'] = [{'length': len(ডাটা), 'sha256': hashlib.sha256(ডাটা).hexdigest()} for ডাটা in 받은것]
    (অবস্থান / 'build/사용자통신시험.json').write_text(json.dumps(পরিমাপ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    কার্যকর_করুন_আদেশ()
