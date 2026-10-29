#!/usr/bin/env python3
"""რეალური_მონაცემები ring 3 ELF/მასპინძელი UDP 왕복/დაცვა_მნიშვნელობა შეცდომა/დრო_მნიშვნელობა 제한/잘못된 ELF를 검증한다."""
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

პოზიცია = Path(__file__).resolve().parents[1]


class ვირტუალური_კომპიუტერი:
    def __init__(self, გეზი, 종류='elf', ქსელი_მნიშვნელობა=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        საქაღალდე_მნიშვნელობა = Path(self.임시.name)
        self.ჟურნალი_ჩაწერა = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.მონიტორი_მნიშვნელობა = socket.socket(socket.AF_UNIX)
        직렬경로, მონიტორი_მდებარეობა = საქაღალდე_მნიშვნელობა / 'serial.sock', საქაღალდე_მნიშვნელობა / 'monitor.sock'
        ბრძანება = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(მონიტორი_მდებარეობა) + ',server,nowait']
        ბრძანება += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ქსელი_მნიშვნელობა else ['-net', 'none']
        ბრძანება += ['-kernel', str(გეზი)] if 종류 == 'elf' else ['-cdrom', str(გეზი), '-boot', 'd']
        if 저장매체 is not None:
            ბრძანება += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.პროცესი_მნიშვნელობა = subprocess.Popen(ბრძანება, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and მონიტორი_მდებარეობა.exists()):
                if self.პროცესი_მნიშვნელობა.poll() is not None:
                    raise AssertionError(self.პროცესი_მნიშვნელობა.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU გაშვება დრო_მნიშვნელობა 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.მონიტორი_მნიშვნელობა.connect(str(მონიტორი_მდებარეობა))
            self.직렬.setblocking(False)
            self.მონიტორი_მნიშვნელობა.sendall(b'cont\n')
            self.მოლოდინი_სტატუსი('jkoros> ')
        except BaseException:
            self.დახურვა()
            raise

    def მოლოდინი_სტატუსი(self, 문구, გაშვება=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ჟურნალი_ჩაწერა[გაშვება:]:
                return self.ჟურნალი_ჩაწერა[გაშვება:].decode('utf-8', 'replace')
            კითხვა, _, _ = select.select([self.직렬], [], [], 0.1)
            if კითხვა:
                მონაცემები = self.직렬.recv(65536)
                if not მონაცემები: break
                self.ჟურნალი_ჩაწერა.extend(მონაცემები)
            if self.პროცესი_მნიშვნელობა.poll() is not None: break
        raise AssertionError('მოლოდინი_მნიშვნელობა მარცხი_მნიშვნელობა: ' + 문구 + '\n' + self.ჟურნალი_ჩაწერა.decode('utf-8', 'replace'))

    def ბრძანება(self, სტრიქონი_მნიშვნელობა, 기대):
        გაშვება = len(self.ჟურნალი_ჩაწერა)
        self.직렬.sendall((სტრიქონი_მნიშვნელობა + '\n').encode())
        გაზომვა = self.მოლოდინი_სტატუსი('jkoros> ', გაშვება)
        for 문구 in 기대:
            assert 문구 in გაზომვა, (სტრიქონი_მნიშვნელობა, 문구, გაზომვა)
        assert 'PANIC' not in გაზომვა, გაზომვა
        return გაზომვა

    def დახურვა(self):
        self.직렬.close()
        self.მონიტორი_მნიშვნელობა.close()
        if self.პროცესი_მნიშვნელობა.poll() is None:
            self.პროცესი_მნიშვნელობა.terminate()
            try: self.პროცესი_მნიშვნელობა.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.პროცესი_მნიშვნელობა.kill()
                self.პროცესი_მნიშვნელობა.wait()
        self.პროცესი_მნიშვნელობა.communicate()
        self.임시.cleanup()


def 보호커널(საქაღალდე_მნიშვნელობა):
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
    항목들 = ['hello=' + str(პოზიცია / 'build/apps/hello.elf')]
    for სახელი, შიგთავსი_მნიშვნელობა in 사례들.items():
        წყარო = საქაღალდე_მნიშვნელობა / (სახელი + '.s')
        წყარო.write_text('.code32\n.text\n.globl _start\n_start:\n' + შიგთავსი_მნიშვნელობა +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(საქაღალდე_მნიშვნელობა / (სახელი + '.o')), str(წყარო)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(პოზიცია.parent / 'compiler/მომხმარებელი_ბმული_განლაგება.ld'),
                        '-o', str(საქაღალდე_მნიშვნელობა / (სახელი + '.elf')), str(საქაღალდე_მნიშვნელობა / (სახელი + '.o'))], check=True)
        항목들.append(სახელი + '=' + str(საქაღალდე_მნიშვნელობა / (სახელი + '.elf')))
    정상 = bytearray((პოზიცია / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    არასწორი_გაზომვა = bytearray(정상); არასწორი_გაზომვა[0] = 0; 변형들['badelf'] = არასწორი_გაზომვა
    არასწორი_გაზომვა = bytearray(정상); struct.pack_into('<I', არასწორი_გაზომვა, 24, 0x00100000); 변형들['badentry'] = არასწორი_გაზომვა
    არასწორი_გაზომვა = bytearray(정상); struct.pack_into('<I', არასწორი_გაზომვა, 28, 0x7fffffff); 변형들['badtable'] = არასწორი_გაზომვა
    არასწორი_გაზომვა = bytearray(정상); ძებნა_ცხრილი = struct.unpack_from('<I', არასწორი_გაზომვა, 28)[0]
    struct.pack_into('<I', არასწორი_გაზომვა, ძებნა_ცხრილი + 20, 0x7fffffff); 변형들['badsize'] = არასწორი_გაზომვა
    for სახელი, მონაცემები in 변형들.items():
        ფაილი = საქაღალდე_მნიშვნელობა / (სახელი + '.elf'); ფაილი.write_bytes(მონაცემები)
        항목들.append(სახელი + '=' + str(ფაილი))
    subprocess.run([sys.executable, str(პოზიცია / 'ხელსაწყოები/묶기.py'), '-o', str(საქაღალდე_მნიშვნელობა / 'apps.bin')] + 항목들, check=True)
    წყარო = საქაღალდე_მნიშვნელობა / 'apps.s'
    წყარო.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(საქაღალდე_მნიშვნელობა / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(საქაღალდე_მნიშვნელობა / 'apps.o'), str(წყარო)], check=True)
    ბირთვი_მნიშვნელობა = საქაღალდე_მნიშვნელობა / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(პოზიცია / '부팅/ბმული_განლაგება.ld'), '-o', str(ბირთვი_მნიშვნელობა),
                    str(პოზიცია / 'build/boot.o'), str(პოზიცია / 'build/java.o'), str(პოზიცია / 'build/user.o'), str(საქაღალდე_მნიშვნელობა / 'apps.o')], check=True)
    return ბირთვი_მნიშვნელობა


def შესრულება_ბრძანება():
    გაზომვა = {}
    სერვერი_მნიშვნელობა = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    სერვერი_მნიშვნელობა.bind(('127.0.0.1', 0))
    სერვერი_მნიშვნელობა.settimeout(0.1)
    პორტი_მნიშვნელობა = სერვერი_მნიშვნელობა.getsockname()[1]
    받은것 = []
    გასვლა_აპი = threading.Event()
    def 되보내기():
        while not გასვლა_აპი.is_set():
            try: მონაცემები, კვანძი_მნიშვნელობა_6a3b6fa7 = სერვერი_მნიშვნელობა.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(მონაცემები)
            if მონაცემები != b'drop-me': სერვერი_მნიშვნელობა.sendto(მონაცემები, კვანძი_მნიშვნელობა_6a3b6fa7)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                კომპიუტერი.ბრძანება('apps', ['hello', 'udp', 'netcheck', 'stress'])
                კომპიუტერი.ბრძანება('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                კომპიუტერი.ბრძანება('run missing', ['Exit: -2'])
                კომპიუტერი.ბრძანება('net', ['NET RTL8139'])
                კომპიუტერი.ბრძანება('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for შიგთავსი_მნიშვნელობა in ('hello-network', 'odd', 'even', 'repeat-123'):
                    კომპიუტერი.ბრძანება('run udp 10.0.2.2 {} {}'.format(პორტი_მნიშვნელობა, შიგთავსი_მნიშვნელობა), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert შიგთავსი_მნიშვნელობა.encode() in 받은것, 'მასპინძელი 서버에서 자료를 받지 못함'
                კომპიუტერი.ბრძანება('run stress {}'.format(პორტი_მნიშვნელობა), ['UDP STRESS PASS', 'Exit: 0'])
                კომპიუტერი.ბრძანება('run udp 10.0.2.2 {} drop-me'.format(პორტი_მნიშვნელობა), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                კომპიუტერი.ბრძანება('run hello recovered', ['arg: recovered', 'Exit: 0'])
                გაზომვა[종류] = კომპიუტერი.ჟურნალი_ჩაწერა.decode('utf-8', 'replace')
                print('PASS: {} მომხმარებელი ELF/ring 3/인수/UDP მასპინძელი 왕복/დრო_მნიშვნელობა 초과/გარემო 복귀'.format(종류), flush=True)
            finally:
                try: კომპიუტერი.ბრძანება('net', [])
                except Exception: pass
                (პოზიცია / 'build/사용자통신-last.log').write_bytes(კომპიუტერი.ჟურნალი_ჩაწერა)
                კომპიუტერი.დახურვა()
        კომპიუტერი = ვირტუალური_კომპიუტერი(პოზიცია / 'build/kernel.elf', ქსელი_მნიშვნელობა=False)
        try:
            კომპიუტერი.ბრძანება('net', ['NET unavailable'])
            კომპიუტერი.ბრძანება('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            კომპიუტერი.ბრძანება('run hello', ['USER MODE ring 3', 'Exit: 0'])
            გაზომვა['no_nic'] = კომპიუტერი.ჟურნალი_ჩაწერა.decode()
        finally: კომპიუტერი.დახურვა()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            კომპიუტერი = ვირტუალური_კომპიუტერი(보호커널(Path(임시)), ქსელი_მნიშვნელობა=False)
            try:
                for სახელი, სტატუსი_მნიშვნელობა in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    კომპიუტერი.ბრძანება('run ' + სახელი, ['Exit: ' + str(სტატუსი_მნიშვნელობა)])
                    კომპიუტერი.ბრძანება('run hello', ['USER MODE ring 3', 'Exit: 0'])
                გაზომვა['protection'] = კომპიუტერი.ჟურნალი_ჩაწერა.decode()
                print('PASS: მომხმარებელი მეხსიერება_მონაცემები/포트 격리, 잘못된 კურსორი/ELF, CPU 예외, 무한 იტერაცია_მნიშვნელობა 제한', flush=True)
            finally:
                (პოზიცია / 'build/보호시험-last.log').write_bytes(კომპიუტერი.ჟურნალი_ჩაწერა)
                კომპიუტერი.დახურვა()
    finally:
        გასვლა_აპი.set()
        일꾼.join(timeout=2)
        სერვერი_მნიშვნელობა.close()
    გაზომვა['host_udp_received'] = [{'length': len(მონაცემები), 'sha256': hashlib.sha256(მონაცემები).hexdigest()} for მონაცემები in 받은것]
    (პოზიცია / 'build/사용자통신시험.json').write_text(json.dumps(გაზომვა, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    შესრულება_ბრძანება()
