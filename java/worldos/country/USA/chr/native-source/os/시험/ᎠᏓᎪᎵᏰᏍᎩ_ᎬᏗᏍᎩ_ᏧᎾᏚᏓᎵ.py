#!/usr/bin/env python3
"""ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ ring 3 ELF/ᎠᏁᏢᏍᎩ UDP 왕복/ᎠᏓᎦᏎᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ ᎦᎵᏓᏍᏔᏅ/시간 제한/잘못된 ELF를 검증한다."""
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


class 가상기계:
    def __init__(self, ᎠᏍᏓᏩᏛᏍᏗ, 종류='elf', ᏧᎾᏚᏓᎵ_ᏧᎬᏩᎶᏗᏯ=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ = Path(self.임시.name)
        self.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.ᎠᏓᏴᎵᏛᏍᎩ_ᏧᎬᏩᎶᏗᏯ = socket.socket(socket.AF_UNIX)
        직렬경로, ᎠᏓᏴᎵᏛᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'serial.sock', ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'monitor.sock'
        ᎤᏁᏤᎸᎩ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ᎠᏓᏴᎵᏛᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ) + ',server,nowait']
        ᎤᏁᏤᎸᎩ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ᏧᎾᏚᏓᎵ_ᏧᎬᏩᎶᏗᏯ else ['-net', 'none']
        ᎤᏁᏤᎸᎩ += ['-kernel', str(ᎠᏍᏓᏩᏛᏍᏗ)] if 종류 == 'elf' else ['-cdrom', str(ᎠᏍᏓᏩᏛᏍᏗ), '-boot', 'd']
        if 저장매체 is not None:
            ᎤᏁᏤᎸᎩ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = subprocess.Popen(ᎤᏁᏤᎸᎩ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and ᎠᏓᏴᎵᏛᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ.exists()):
                if self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is not None:
                    raise AssertionError(self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ᎠᎢᏎᏍᏗ 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.ᎠᏓᏴᎵᏛᏍᎩ_ᏧᎬᏩᎶᏗᏯ.connect(str(ᎠᏓᏴᎵᏛᏍᎩ_ᎠᏍᏓᏩᏛᏍᏗ))
            self.직렬.setblocking(False)
            self.ᎠᏓᏴᎵᏛᏍᎩ_ᏧᎬᏩᎶᏗᏯ.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.ᎯᏍᏚᎲᎦ()
            raise

    def 기다림(self, 문구, ᎠᎢᏎᏍᏗ=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:]:
                return self.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[ᎠᎢᏎᏍᏗ:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                ᎦᏟᏌᏅᎯ = self.직렬.recv(65536)
                if not ᎦᏟᏌᏅᎯ: break
                self.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(ᎦᏟᏌᏅᎯ)
            if self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is not None: break
        raise AssertionError('대기 ᎤᏄᎸᎲᎦ_ᏧᎬᏩᎶᏗᏯ: ' + 문구 + '\n' + self.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace'))

    def ᎤᏁᏤᎸᎩ(self, ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ, 기대):
        ᎠᎢᏎᏍᏗ = len(self.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        self.직렬.sendall((ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ + '\n').encode())
        결과 = self.기다림('jkoros> ', ᎠᎢᏎᏍᏗ)
        for 문구 in 기대:
            assert 문구 in 결과, (ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def ᎯᏍᏚᎲᎦ(self):
        self.직렬.close()
        self.ᎠᏓᏴᎵᏛᏍᎩ_ᏧᎬᏩᎶᏗᏯ.close()
        if self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is None:
            self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.terminate()
            try: self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.kill()
                self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait()
        self.ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.communicate()
        self.임시.cleanup()


def 보호커널(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ):
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
    for ᏚᏙᎥᎢ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ in 사례들.items():
        ᎦᏟᏌᏅᎯ_0201f362 = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / (ᏚᏙᎥᎢ + '.s')
        ᎦᏟᏌᏅᎯ_0201f362.write_text('.code32\n.text\n.globl _start\n_start:\n' + ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / (ᏚᏙᎥᎢ + '.o')), str(ᎦᏟᏌᏅᎯ_0201f362)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/ᎬᏗᏍᎩ_ᎫᏓᎸᎢ_ᏱᎬᏂ.ld'),
                        '-o', str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / (ᏚᏙᎥᎢ + '.elf')), str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / (ᏚᏙᎥᎢ + '.o'))], check=True)
        항목들.append(ᏚᏙᎥᎢ + '=' + str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / (ᏚᏙᎥᎢ + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ in 변형들.items():
        ᎠᏍᏆᏂᎪᏙᏗ = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / (ᏚᏙᎥᎢ + '.elf'); ᎠᏍᏆᏂᎪᏙᏗ.write_bytes(ᎦᏟᏌᏅᎯ)
        항목들.append(ᏚᏙᎥᎢ + '=' + str(ᎠᏍᏆᏂᎪᏙᏗ))
    subprocess.run([sys.executable, str(위치 / '도구/묶기.py'), '-o', str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'apps.bin')] + 항목들, check=True)
    ᎦᏟᏌᏅᎯ_0201f362 = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'apps.s'
    ᎦᏟᏌᏅᎯ_0201f362.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'apps.o'), str(ᎦᏟᏌᏅᎯ_0201f362)], check=True)
    kernel_ᏧᎬᏩᎶᏗᏯ = ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/ᎫᏓᎸᎢ_ᏱᎬᏂ.ld'), '-o', str(kernel_ᏧᎬᏩᎶᏗᏯ),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'apps.o')], check=True)
    return kernel_ᏧᎬᏩᎶᏗᏯ


def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ():
    결과 = {}
    ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.bind(('127.0.0.1', 0))
    ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.settimeout(0.1)
    ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.getsockname()[1]
    받은것 = []
    ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ = threading.Event()
    def 되보내기():
        while not ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ.is_set():
            try: ᎦᏟᏌᏅᎯ, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ᎦᏟᏌᏅᎯ)
            if ᎦᏟᏌᏅᎯ != b'drop-me': ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.sendto(ᎦᏟᏌᏅᎯ, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                기계.ᎤᏁᏤᎸᎩ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                기계.ᎤᏁᏤᎸᎩ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                기계.ᎤᏁᏤᎸᎩ('run missing', ['Exit: -2'])
                기계.ᎤᏁᏤᎸᎩ('net', ['NET RTL8139'])
                기계.ᎤᏁᏤᎸᎩ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ in ('hello-network', 'odd', 'even', 'repeat-123'):
                    기계.ᎤᏁᏤᎸᎩ('run udp 10.0.2.2 {} {}'.format(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.encode() in 받은것, 'ᎠᏁᏢᏍᎩ 서버에서 자료를 받지 못함'
                기계.ᎤᏁᏤᎸᎩ('run stress {}'.format(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ), ['UDP STRESS PASS', 'Exit: 0'])
                기계.ᎤᏁᏤᎸᎩ('run udp 10.0.2.2 {} drop-me'.format(ᎫᏓᎸᏗ_ᏧᎬᏩᎶᏗᏯ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                기계.ᎤᏁᏤᎸᎩ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode('utf-8', 'replace')
                print('PASS: {} ᎬᏗᏍᎩ ELF/ring 3/인수/UDP ᎠᏁᏢᏍᎩ 왕복/시간 초과/ᎤᏯᏍᎦ 복귀'.format(종류), flush=True)
            finally:
                try: 기계.ᎤᏁᏤᎸᎩ('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                기계.ᎯᏍᏚᎲᎦ()
        기계 = 가상기계(위치 / 'build/kernel.elf', ᏧᎾᏚᏓᎵ_ᏧᎬᏩᎶᏗᏯ=False)
        try:
            기계.ᎤᏁᏤᎸᎩ('net', ['NET unavailable'])
            기계.ᎤᏁᏤᎸᎩ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            기계.ᎤᏁᏤᎸᎩ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode()
        finally: 기계.ᎯᏍᏚᎲᎦ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            기계 = 가상기계(보호커널(Path(임시)), ᏧᎾᏚᏓᎵ_ᏧᎬᏩᎶᏗᏯ=False)
            try:
                for ᏚᏙᎥᎢ, ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    기계.ᎤᏁᏤᎸᎩ('run ' + ᏚᏙᎥᎢ, ['Exit: ' + str(ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ)])
                    기계.ᎤᏁᏤᎸᎩ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = 기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.decode()
                print('PASS: ᎬᏗᏍᎩ ᎠᏅᏓᏗᏍᏙ_ᎦᏟᏌᏅᎯ/포트 격리, 잘못된 ᎠᏎᎯᎯ/ELF, CPU 예외, 무한 반복 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(기계.ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                기계.ᎯᏍᏚᎲᎦ()
    finally:
        ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ.set()
        일꾼.join(timeout=2)
        ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.close()
    결과['host_udp_received'] = [{'length': len(ᎦᏟᏌᏅᎯ), 'sha256': hashlib.sha256(ᎦᏟᏌᏅᎯ).hexdigest()} for ᎦᏟᏌᏅᎯ in 받은것]
    (위치 / 'build/ᎠᏓᎪᎵᏰᏍᎩ_ᎬᏗᏍᎩ_ᏧᎾᏚᏓᎵ.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
