#!/usr/bin/env python3
"""அசல்_தரவு ring 3 ELF/ஓம்பு UDP 왕복/பாதுகாப்பளி_மதிப்பு பிழை/நேர_மதிப்பு 제한/잘못된 ELF를 검증한다."""
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

இடம் = Path(__file__).resolve().parents[1]


class தோற்றநிலை_இயந்திரம்:
    def __init__(self, பாதை_2, 종류='elf', பிணையம்_மதிப்பு=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        கோப்பகம்_மதிப்பு = Path(self.임시.name)
        self.பதிவு_பதிவு = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.திரையகம்_மதிப்பு = socket.socket(socket.AF_UNIX)
        직렬경로, திரையகம்_பாதை = கோப்பகம்_மதிப்பு / 'serial.sock', கோப்பகம்_மதிப்பு / 'monitor.sock'
        கட்டளை = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(திரையகம்_பாதை) + ',server,nowait']
        கட்டளை += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if பிணையம்_மதிப்பு else ['-net', 'none']
        கட்டளை += ['-kernel', str(பாதை_2)] if 종류 == 'elf' else ['-cdrom', str(பாதை_2), '-boot', 'd']
        if 저장매체 is not None:
            கட்டளை += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.செயலகம்_மதிப்பு = subprocess.Popen(கட்டளை, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and திரையகம்_பாதை.exists()):
                if self.செயலகம்_மதிப்பு.poll() is not None:
                    raise AssertionError(self.செயலகம்_மதிப்பு.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU செயல்படுத்துக நேர_மதிப்பு 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.திரையகம்_மதிப்பு.connect(str(திரையகம்_பாதை))
            self.직렬.setblocking(False)
            self.திரையகம்_மதிப்பு.sendall(b'cont\n')
            self.காத்திரு_நிலை('jkoros> ')
        except BaseException:
            self.மூடு()
            raise

    def காத்திரு_நிலை(self, 문구, செயல்படுத்துக=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.பதிவு_பதிவு[செயல்படுத்துக:]:
                return self.பதிவு_பதிவு[செயல்படுத்துக:].decode('utf-8', 'replace')
            படி, _, _ = select.select([self.직렬], [], [], 0.1)
            if படி:
                தரவு = self.직렬.recv(65536)
                if not தரவு: break
                self.பதிவு_பதிவு.extend(தரவு)
            if self.செயலகம்_மதிப்பு.poll() is not None: break
        raise AssertionError('காத்திரு_மதிப்பு செயலிழப்பு_மதிப்பு: ' + 문구 + '\n' + self.பதிவு_பதிவு.decode('utf-8', 'replace'))

    def கட்டளை(self, சரம்_மதிப்பு, 기대):
        செயல்படுத்துக = len(self.பதிவு_பதிவு)
        self.직렬.sendall((சரம்_மதிப்பு + '\n').encode())
        அளவிடக்கூடியது = self.காத்திரு_நிலை('jkoros> ', செயல்படுத்துக)
        for 문구 in 기대:
            assert 문구 in அளவிடக்கூடியது, (சரம்_மதிப்பு, 문구, அளவிடக்கூடியது)
        assert 'PANIC' not in அளவிடக்கூடியது, அளவிடக்கூடியது
        return அளவிடக்கூடியது

    def மூடு(self):
        self.직렬.close()
        self.திரையகம்_மதிப்பு.close()
        if self.செயலகம்_மதிப்பு.poll() is None:
            self.செயலகம்_மதிப்பு.terminate()
            try: self.செயலகம்_மதிப்பு.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.செயலகம்_மதிப்பு.kill()
                self.செயலகம்_மதிப்பு.wait()
        self.செயலகம்_மதிப்பு.communicate()
        self.임시.cleanup()


def 보호커널(கோப்பகம்_மதிப்பு):
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
    항목들 = ['hello=' + str(இடம் / 'build/apps/hello.elf')]
    for பெயர், உள்ளடக்கம்_மதிப்பு in 사례들.items():
        மூலக்_கோப்பு = கோப்பகம்_மதிப்பு / (பெயர் + '.s')
        மூலக்_கோப்பு.write_text('.code32\n.text\n.globl _start\n_start:\n' + உள்ளடக்கம்_மதிப்பு +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(கோப்பகம்_மதிப்பு / (பெயர் + '.o')), str(மூலக்_கோப்பு)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(இடம்.parent / 'compiler/பயனர்_இணை_லேஅவுட்.ld'),
                        '-o', str(கோப்பகம்_மதிப்பு / (பெயர் + '.elf')), str(கோப்பகம்_மதிப்பு / (பெயர் + '.o'))], check=True)
        항목들.append(பெயர் + '=' + str(கோப்பகம்_மதிப்பு / (பெயர் + '.elf')))
    정상 = bytearray((இடம் / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    செல்லுபடியாகாத_அளவிடக்கூடியது = bytearray(정상); செல்லுபடியாகாத_அளவிடக்கூடியது[0] = 0; 변형들['badelf'] = செல்லுபடியாகாத_அளவிடக்கூடியது
    செல்லுபடியாகாத_அளவிடக்கூடியது = bytearray(정상); struct.pack_into('<I', செல்லுபடியாகாத_அளவிடக்கூடியது, 24, 0x00100000); 변형들['badentry'] = செல்லுபடியாகாத_அளவிடக்கூடியது
    செல்லுபடியாகாத_அளவிடக்கூடியது = bytearray(정상); struct.pack_into('<I', செல்லுபடியாகாத_அளவிடக்கூடியது, 28, 0x7fffffff); 변형들['badtable'] = செல்லுபடியாகாத_அளவிடக்கூடியது
    செல்லுபடியாகாத_அளவிடக்கூடியது = bytearray(정상); தேடுதல்_அட்டவணை = struct.unpack_from('<I', செல்லுபடியாகாத_அளவிடக்கூடியது, 28)[0]
    struct.pack_into('<I', செல்லுபடியாகாத_அளவிடக்கூடியது, தேடுதல்_அட்டவணை + 20, 0x7fffffff); 변형들['badsize'] = செல்லுபடியாகாத_அளவிடக்கூடியது
    for பெயர், தரவு in 변형들.items():
        கோப்பின்_பெயர் = கோப்பகம்_மதிப்பு / (பெயர் + '.elf'); கோப்பின்_பெயர்.write_bytes(தரவு)
        항목들.append(பெயர் + '=' + str(கோப்பின்_பெயர்))
    subprocess.run([sys.executable, str(இடம் / 'கருவிகள்/கட்டு_முடிவுப்_புள்ளி.py'), '-o', str(கோப்பகம்_மதிப்பு / 'apps.bin')] + 항목들, check=True)
    மூலக்_கோப்பு = கோப்பகம்_மதிப்பு / 'apps.s'
    மூலக்_கோப்பு.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(கோப்பகம்_மதிப்பு / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(கோப்பகம்_மதிப்பு / 'apps.o'), str(மூலக்_கோப்பு)], check=True)
    கரு_மதிப்பு = கோப்பகம்_மதிப்பு / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(இடம் / '부팅/இணை_லேஅவுட்.ld'), '-o', str(கரு_மதிப்பு),
                    str(இடம் / 'build/boot.o'), str(இடம் / 'build/java.o'), str(இடம் / 'build/user.o'), str(கோப்பகம்_மதிப்பு / 'apps.o')], check=True)
    return கரு_மதிப்பு


def இயக்கு_கட்டளை():
    அளவிடக்கூடியது = {}
    சேவையகம்_மதிப்பு = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    சேவையகம்_மதிப்பு.bind(('127.0.0.1', 0))
    சேவையகம்_மதிப்பு.settimeout(0.1)
    முணையம்_மதிப்பு = சேவையகம்_மதிப்பு.getsockname()[1]
    받은것 = []
    முடிவு_நிரல் = threading.Event()
    def 되보내기():
        while not முடிவு_நிரல்.is_set():
            try: தரவு, பியர்_மதிப்பு = சேவையகம்_மதிப்பு.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(தரவு)
            if தரவு != b'drop-me': சேவையகம்_மதிப்பு.sendto(தரவு, பியர்_மதிப்பு)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                இயந்திரம்.கட்டளை('apps', ['hello', 'udp', 'netcheck', 'stress'])
                இயந்திரம்.கட்டளை('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                இயந்திரம்.கட்டளை('run missing', ['Exit: -2'])
                இயந்திரம்.கட்டளை('net', ['NET RTL8139'])
                இயந்திரம்.கட்டளை('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for உள்ளடக்கம்_மதிப்பு in ('hello-network', 'odd', 'even', 'repeat-123'):
                    இயந்திரம்.கட்டளை('run udp 10.0.2.2 {} {}'.format(முணையம்_மதிப்பு, உள்ளடக்கம்_மதிப்பு), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert உள்ளடக்கம்_மதிப்பு.encode() in 받은것, 'ஓம்பு 서버에서 자료를 받지 못함'
                இயந்திரம்.கட்டளை('run stress {}'.format(முணையம்_மதிப்பு), ['UDP STRESS PASS', 'Exit: 0'])
                இயந்திரம்.கட்டளை('run udp 10.0.2.2 {} drop-me'.format(முணையம்_மதிப்பு), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                இயந்திரம்.கட்டளை('run hello recovered', ['arg: recovered', 'Exit: 0'])
                அளவிடக்கூடியது[종류] = இயந்திரம்.பதிவு_பதிவு.decode('utf-8', 'replace')
                print('PASS: {} பயனர் ELF/ring 3/செயலுருபுகள்/UDP ஓம்பு 왕복/நேர_மதிப்பு 초과/கூடு 복귀'.format(종류), flush=True)
            finally:
                try: இயந்திரம்.கட்டளை('net', [])
                except Exception: pass
                (இடம் / 'build/사용자통신-last.log').write_bytes(இயந்திரம்.பதிவு_பதிவு)
                இயந்திரம்.மூடு()
        இயந்திரம் = தோற்றநிலை_இயந்திரம்(இடம் / 'build/kernel.elf', பிணையம்_மதிப்பு=False)
        try:
            இயந்திரம்.கட்டளை('net', ['NET unavailable'])
            இயந்திரம்.கட்டளை('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            இயந்திரம்.கட்டளை('run hello', ['USER MODE ring 3', 'Exit: 0'])
            அளவிடக்கூடியது['no_nic'] = இயந்திரம்.பதிவு_பதிவு.decode()
        finally: இயந்திரம்.மூடு()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            இயந்திரம் = தோற்றநிலை_இயந்திரம்(보호커널(Path(임시)), பிணையம்_மதிப்பு=False)
            try:
                for பெயர், நிலை_மதிப்பு_e10195a1 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    இயந்திரம்.கட்டளை('run ' + பெயர், ['Exit: ' + str(நிலை_மதிப்பு_e10195a1)])
                    இயந்திரம்.கட்டளை('run hello', ['USER MODE ring 3', 'Exit: 0'])
                அளவிடக்கூடியது['protection'] = இயந்திரம்.பதிவு_பதிவு.decode()
                print('PASS: பயனர் நினைவகம்_தரவு/포트 격리, 잘못된 குறிப்பான்/ELF, CPU விதிவிலக்கு, 무한 மீள்செயல்_மதிப்பு 제한', flush=True)
            finally:
                (இடம் / 'build/보호시험-last.log').write_bytes(இயந்திரம்.பதிவு_பதிவு)
                இயந்திரம்.மூடு()
    finally:
        முடிவு_நிரல்.set()
        일꾼.join(timeout=2)
        சேவையகம்_மதிப்பு.close()
    அளவிடக்கூடியது['host_udp_received'] = [{'length': len(தரவு), 'sha256': hashlib.sha256(தரவு).hexdigest()} for தரவு in 받은것]
    (இடம் / 'build/사용자통신시험.json').write_text(json.dumps(அளவிடக்கூடியது, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    இயக்கு_கட்டளை()
