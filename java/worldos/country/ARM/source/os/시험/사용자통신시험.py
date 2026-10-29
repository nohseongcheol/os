#!/usr/bin/env python3
"""իրական_տվյալ ring 3 ELF/հոստ UDP 왕복/պաշտպանել_արժեք Սխալ/시간 제한/잘못된 ELF를 검증한다."""
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

Դիրք = Path(__file__).resolve().parents[1]


class վիրտուալ_մեքենա:
    def __init__(self, Ճանապարհ, 종류='elf', Ցանց_արժեք=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        գրացուցակ_արժեք = Path(self.임시.name)
        self.մատյան_տող = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.մոնիտոր_արժեք = socket.socket(socket.AF_UNIX)
        직렬경로, մոնիտոր_ուղի = գրացուցակ_արժեք / 'serial.sock', գրացուցակ_արժեք / 'monitor.sock'
        Հրահանգ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(մոնիտոր_ուղի) + ',server,nowait']
        Հրահանգ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Ցանց_արժեք else ['-net', 'none']
        Հրահանգ += ['-kernel', str(Ճանապարհ)] if 종류 == 'elf' else ['-cdrom', str(Ճանապարհ), '-boot', 'd']
        if 저장매체 is not None:
            Հրահանգ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Ընթացք_արժեք = subprocess.Popen(Հրահանգ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and մոնիտոր_ուղի.exists()):
                if self.Ընթացք_արժեք.poll() is not None:
                    raise AssertionError(self.Ընթացք_արժեք.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Գործարկել 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.մոնիտոր_արժեք.connect(str(մոնիտոր_ուղի))
            self.직렬.setblocking(False)
            self.մոնիտոր_արժեք.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Փակ()
            raise

    def 기다림(self, 문구, Գործարկել=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.մատյան_տող[Գործարկել:]:
                return self.մատյան_տող[Գործարկել:].decode('utf-8', 'replace')
            Ընթերցում, _, _ = select.select([self.직렬], [], [], 0.1)
            if Ընթերցում:
                տվյալ = self.직렬.recv(65536)
                if not տվյալ: break
                self.մատյան_տող.extend(տվյալ)
            if self.Ընթացք_արժեք.poll() is not None: break
        raise AssertionError('대기 ձախողում_արժեք: ' + 문구 + '\n' + self.մատյան_տող.decode('utf-8', 'replace'))

    def Հրահանգ(self, տող_արժեք_6ca8363c, 기대):
        Գործարկել = len(self.մատյան_տող)
        self.직렬.sendall((տող_արժեք_6ca8363c + '\n').encode())
        չափ = self.기다림('jkoros> ', Գործարկել)
        for 문구 in 기대:
            assert 문구 in չափ, (տող_արժեք_6ca8363c, 문구, չափ)
        assert 'PANIC' not in չափ, չափ
        return չափ

    def Փակ(self):
        self.직렬.close()
        self.մոնիտոր_արժեք.close()
        if self.Ընթացք_արժեք.poll() is None:
            self.Ընթացք_արժեք.terminate()
            try: self.Ընթացք_արժեք.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Ընթացք_արժեք.kill()
                self.Ընթացք_արժեք.wait()
        self.Ընթացք_արժեք.communicate()
        self.임시.cleanup()


def 보호커널(գրացուցակ_արժեք):
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
    항목들 = ['hello=' + str(Դիրք / 'build/apps/hello.elf')]
    for Անուն, Բովանդակություն_արժեք in 사례들.items():
        ԱՂԲՅՈՒՐ = գրացուցակ_արժեք / (Անուն + '.s')
        ԱՂԲՅՈՒՐ.write_text('.code32\n.text\n.globl _start\n_start:\n' + Բովանդակություն_արժեք +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(գրացուցակ_արժեք / (Անուն + '.o')), str(ԱՂԲՅՈՒՐ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Դիրք.parent / 'compiler/օգտվող_կապ_Դասավորություն.ld'),
                        '-o', str(գրացուցակ_արժեք / (Անուն + '.elf')), str(գրացուցակ_արժեք / (Անուն + '.o'))], check=True)
        항목들.append(Անուն + '=' + str(գրացուցակ_արժեք / (Անուն + '.elf')))
    정상 = bytearray((Դիրք / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    անվավեր_չափ = bytearray(정상); անվավեր_չափ[0] = 0; 변형들['badelf'] = անվավեր_չափ
    անվավեր_չափ = bytearray(정상); struct.pack_into('<I', անվավեր_չափ, 24, 0x00100000); 변형들['badentry'] = անվավեր_չափ
    անվավեր_չափ = bytearray(정상); struct.pack_into('<I', անվավեր_չափ, 28, 0x7fffffff); 변형들['badtable'] = անվավեր_չափ
    անվավեր_չափ = bytearray(정상); Փնտրում_աղյուսակ = struct.unpack_from('<I', անվավեր_չափ, 28)[0]
    struct.pack_into('<I', անվավեր_չափ, Փնտրում_աղյուսակ + 20, 0x7fffffff); 변형들['badsize'] = անվավեր_չափ
    for Անուն, տվյալ in 변형들.items():
        Ֆայլ = գրացուցակ_արժեք / (Անուն + '.elf'); Ֆայլ.write_bytes(տվյալ)
        항목들.append(Անուն + '=' + str(Ֆայլ))
    subprocess.run([sys.executable, str(Դիրք / 'Գործիքներ/묶기.py'), '-o', str(գրացուցակ_արժեք / 'apps.bin')] + 항목들, check=True)
    ԱՂԲՅՈՒՐ = գրացուցակ_արժեք / 'apps.s'
    ԱՂԲՅՈՒՐ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(գրացուցակ_արժեք / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(գրացուցակ_արժեք / 'apps.o'), str(ԱՂԲՅՈՒՐ)], check=True)
    միջուկ_արժեք = գրացուցակ_արժեք / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Դիրք / '부팅/կապ_Դասավորություն.ld'), '-o', str(միջուկ_արժեք),
                    str(Դիրք / 'build/boot.o'), str(Դիրք / 'build/java.o'), str(Դիրք / 'build/user.o'), str(գրացուցակ_արժեք / 'apps.o')], check=True)
    return միջուկ_արժեք


def կատարել_հրաման():
    չափ = {}
    սպասարկիչ_արժեք = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    սպասարկիչ_արժեք.bind(('127.0.0.1', 0))
    սպասարկիչ_արժեք.settimeout(0.1)
    միացք_արժեք = սպասարկիչ_արժեք.getsockname()[1]
    받은것 = []
    Ելք_ծրագիր = threading.Event()
    def 되보내기():
        while not Ելք_ծրագիր.is_set():
            try: տվյալ, հավասարազոր_սարք_արժեք = սպասարկիչ_արժեք.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(տվյալ)
            if տվյալ != b'drop-me': սպասարկիչ_արժեք.sendto(տվյալ, հավասարազոր_սարք_արժեք)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            մեքենա = վիրտուալ_մեքենա(Դիրք / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                մեքենա.Հրահանգ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                մեքենա.Հրահանգ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                մեքենա.Հրահանգ('run missing', ['Exit: -2'])
                մեքենա.Հրահանգ('net', ['NET RTL8139'])
                մեքենա.Հրահանգ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Բովանդակություն_արժեք in ('hello-network', 'odd', 'even', 'repeat-123'):
                    մեքենա.Հրահանգ('run udp 10.0.2.2 {} {}'.format(միացք_արժեք, Բովանդակություն_արժեք), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Բովանդակություն_արժեք.encode() in 받은것, 'հոստ 서버에서 자료를 받지 못함'
                մեքենա.Հրահանգ('run stress {}'.format(միացք_արժեք), ['UDP STRESS PASS', 'Exit: 0'])
                մեքենա.Հրահանգ('run udp 10.0.2.2 {} drop-me'.format(միացք_արժեք), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                մեքենա.Հրահանգ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                չափ[종류] = մեքենա.մատյան_տող.decode('utf-8', 'replace')
                print('PASS: {} օգտվող ELF/ring 3/인수/UDP հոստ 왕복/시간 초과/խեցի 복귀'.format(종류), flush=True)
            finally:
                try: մեքենա.Հրահանգ('net', [])
                except Exception: pass
                (Դիրք / 'build/사용자통신-last.log').write_bytes(մեքենա.մատյան_տող)
                մեքենա.Փակ()
        մեքենա = վիրտուալ_մեքենա(Դիրք / 'build/kernel.elf', Ցանց_արժեք=False)
        try:
            մեքենա.Հրահանգ('net', ['NET unavailable'])
            մեքենա.Հրահանգ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            մեքենա.Հրահանգ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            չափ['no_nic'] = մեքենա.մատյան_տող.decode()
        finally: մեքենա.Փակ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            մեքենա = վիրտուալ_մեքենա(보호커널(Path(임시)), Ցանց_արժեք=False)
            try:
                for Անուն, վիճակ_արժեք in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    մեքենա.Հրահանգ('run ' + Անուն, ['Exit: ' + str(վիճակ_արժեք)])
                    մեքենա.Հրահանգ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                չափ['protection'] = մեքենա.մատյան_տող.decode()
                print('PASS: օգտվող Հիշողություն_տվյալ/포트 격리, 잘못된 նշորդ/ELF, CPU 예외, 무한 բազմակրկնություն_արժեք 제한', flush=True)
            finally:
                (Դիրք / 'build/보호시험-last.log').write_bytes(մեքենա.մատյան_տող)
                մեքենա.Փակ()
    finally:
        Ելք_ծրագիր.set()
        일꾼.join(timeout=2)
        սպասարկիչ_արժեք.close()
    չափ['host_udp_received'] = [{'length': len(տվյալ), 'sha256': hashlib.sha256(տվյալ).hexdigest()} for տվյալ in 받은것]
    (Դիրք / 'build/사용자통신시험.json').write_text(json.dumps(չափ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    կատարել_հրաման()
