#!/usr/bin/env python3
"""વાસ્તવિક_ડેટા ring 3 ELF/હોસ્ટ UDP 왕복/રક્ષણ_કરો_મૂલ્ય ભૂલ/સમય_મૂલ્ય 제한/잘못된 ELF를 검증한다."""
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

સ્થાન = Path(__file__).resolve().parents[1]


class વર્ચુઅલ_મશીન:
    def __init__(self, પથ, 종류='elf', નેટવર્ક_મૂલ્ય=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        નિર્દેશિકા_મૂલ્ય = Path(self.임시.name)
        self.લૉગ_પંક્તિ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.મૉનિટર_મૂલ્ય = socket.socket(socket.AF_UNIX)
        직렬경로, મૉનિટર_પાથ = નિર્દેશિકા_મૂલ્ય / 'serial.sock', નિર્દેશિકા_મૂલ્ય / 'monitor.sock'
        આદેશ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(મૉનિટર_પાથ) + ',server,nowait']
        આદેશ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if નેટવર્ક_મૂલ્ય else ['-net', 'none']
        આદેશ += ['-kernel', str(પથ)] if 종류 == 'elf' else ['-cdrom', str(પથ), '-boot', 'd']
        if 저장매체 is not None:
            આદેશ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.પ્રક્રિયા_મૂલ્ય = subprocess.Popen(આદેશ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and મૉનિટર_પાથ.exists()):
                if self.પ્રક્રિયા_મૂલ્ય.poll() is not None:
                    raise AssertionError(self.પ્રક્રિયા_મૂલ્ય.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ચલાવો_2 સમય_મૂલ્ય 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.મૉનિટર_મૂલ્ય.connect(str(મૉનિટર_પાથ))
            self.직렬.setblocking(False)
            self.મૉનિટર_મૂલ્ય.sendall(b'cont\n')
            self.પ્રતીક્ષા_સ્થિતિ('jkoros> ')
        except BaseException:
            self.બંધ_કરો()
            raise

    def પ્રતીક્ષા_સ્થિતિ(self, 문구, ચલાવો_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.લૉગ_પંક્તિ[ચલાવો_2:]:
                return self.લૉગ_પંક્તિ[ચલાવો_2:].decode('utf-8', 'replace')
            વાંચો, _, _ = select.select([self.직렬], [], [], 0.1)
            if વાંચો:
                ડેટા = self.직렬.recv(65536)
                if not ડેટા: break
                self.લૉગ_પંક્તિ.extend(ડેટા)
            if self.પ્રક્રિયા_મૂલ્ય.poll() is not None: break
        raise AssertionError('પ્રતીક્ષા_મૂલ્ય નિષ્ફળતા_મૂલ્ય: ' + 문구 + '\n' + self.લૉગ_પંક્તિ.decode('utf-8', 'replace'))

    def આદેશ(self, સ્ટ્રિંગ_મૂલ્ય, 기대):
        ચલાવો_2 = len(self.લૉગ_પંક્તિ)
        self.직렬.sendall((સ્ટ્રિંગ_મૂલ્ય + '\n').encode())
        પરિમાણ = self.પ્રતીક્ષા_સ્થિતિ('jkoros> ', ચલાવો_2)
        for 문구 in 기대:
            assert 문구 in પરિમાણ, (સ્ટ્રિંગ_મૂલ્ય, 문구, પરિમાણ)
        assert 'PANIC' not in પરિમાણ, પરિમાણ
        return પરિમાણ

    def બંધ_કરો(self):
        self.직렬.close()
        self.મૉનિટર_મૂલ્ય.close()
        if self.પ્રક્રિયા_મૂલ્ય.poll() is None:
            self.પ્રક્રિયા_મૂલ્ય.terminate()
            try: self.પ્રક્રિયા_મૂલ્ય.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.પ્રક્રિયા_મૂલ્ય.kill()
                self.પ્રક્રિયા_મૂલ્ય.wait()
        self.પ્રક્રિયા_મૂલ્ય.communicate()
        self.임시.cleanup()


def 보호커널(નિર્દેશિકા_મૂલ્ય):
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
    항목들 = ['hello=' + str(સ્થાન / 'build/apps/hello.elf')]
    for નામ, સામગ્રી_મૂલ્ય in 사례들.items():
        સ્રોત = નિર્દેશિકા_મૂલ્ય / (નામ + '.s')
        સ્રોત.write_text('.code32\n.text\n.globl _start\n_start:\n' + સામગ્રી_મૂલ્ય +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(નિર્દેશિકા_મૂલ્ય / (નામ + '.o')), str(સ્રોત)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(સ્થાન.parent / 'compiler/ઉપયોગકર્તા_લિંક_લેઆઉટ.ld'),
                        '-o', str(નિર્દેશિકા_મૂલ્ય / (નામ + '.elf')), str(નિર્દેશિકા_મૂલ્ય / (નામ + '.o'))], check=True)
        항목들.append(નામ + '=' + str(નિર્દેશિકા_મૂલ્ય / (નામ + '.elf')))
    정상 = bytearray((સ્થાન / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    અમાન્ય_પરિમાણ = bytearray(정상); અમાન્ય_પરિમાણ[0] = 0; 변형들['badelf'] = અમાન્ય_પરિમાણ
    અમાન્ય_પરિમાણ = bytearray(정상); struct.pack_into('<I', અમાન્ય_પરિમાણ, 24, 0x00100000); 변형들['badentry'] = અમાન્ય_પરિમાણ
    અમાન્ય_પરિમાણ = bytearray(정상); struct.pack_into('<I', અમાન્ય_પરિમાણ, 28, 0x7fffffff); 변형들['badtable'] = અમાન્ય_પરિમાણ
    અમાન્ય_પરિમાણ = bytearray(정상); લુકઅપ_કોષ્ટક = struct.unpack_from('<I', અમાન્ય_પરિમાણ, 28)[0]
    struct.pack_into('<I', અમાન્ય_પરિમાણ, લુકઅપ_કોષ્ટક + 20, 0x7fffffff); 변형들['badsize'] = અમાન્ય_પરિમાણ
    for નામ, ડેટા in 변형들.items():
        ફાઈલ = નિર્દેશિકા_મૂલ્ય / (નામ + '.elf'); ફાઈલ.write_bytes(ડેટા)
        항목들.append(નામ + '=' + str(ફાઈલ))
    subprocess.run([sys.executable, str(સ્થાન / 'ઉપકરણો/묶기.py'), '-o', str(નિર્દેશિકા_મૂલ્ય / 'apps.bin')] + 항목들, check=True)
    સ્રોત = નિર્દેશિકા_મૂલ્ય / 'apps.s'
    સ્રોત.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(નિર્દેશિકા_મૂલ્ય / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(નિર્દેશિકા_મૂલ્ય / 'apps.o'), str(સ્રોત)], check=True)
    કર્નેલ_મૂલ્ય = નિર્દેશિકા_મૂલ્ય / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(સ્થાન / '부팅/લિંક_લેઆઉટ.ld'), '-o', str(કર્નેલ_મૂલ્ય),
                    str(સ્થાન / 'build/boot.o'), str(સ્થાન / 'build/java.o'), str(સ્થાન / 'build/user.o'), str(નિર્દેશિકા_મૂલ્ય / 'apps.o')], check=True)
    return કર્નેલ_મૂલ્ય


def અમલ_કરો_આદેશ():
    પરિમાણ = {}
    સર્વર_મૂલ્ય = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    સર્વર_મૂલ્ય.bind(('127.0.0.1', 0))
    સર્વર_મૂલ્ય.settimeout(0.1)
    પૉર્ટ_મૂલ્ય = સર્વર_મૂલ્ય.getsockname()[1]
    받은것 = []
    પ્રસ્થાન_એપ્લિકેશન = threading.Event()
    def 되보내기():
        while not પ્રસ્થાન_એપ્લિકેશન.is_set():
            try: ડેટા, પીઅર_મૂલ્ય = સર્વર_મૂલ્ય.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ડેટા)
            if ડેટા != b'drop-me': સર્વર_મૂલ્ય.sendto(ડેટા, પીઅર_મૂલ્ય)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            મશીન = વર્ચુઅલ_મશીન(સ્થાન / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                મશીન.આદેશ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                મશીન.આદેશ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                મશીન.આદેશ('run missing', ['Exit: -2'])
                મશીન.આદેશ('net', ['NET RTL8139'])
                મશીન.આદેશ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for સામગ્રી_મૂલ્ય in ('hello-network', 'odd', 'even', 'repeat-123'):
                    મશીન.આદેશ('run udp 10.0.2.2 {} {}'.format(પૉર્ટ_મૂલ્ય, સામગ્રી_મૂલ્ય), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert સામગ્રી_મૂલ્ય.encode() in 받은것, 'હોસ્ટ 서버에서 자료를 받지 못함'
                મશીન.આદેશ('run stress {}'.format(પૉર્ટ_મૂલ્ય), ['UDP STRESS PASS', 'Exit: 0'])
                મશીન.આદેશ('run udp 10.0.2.2 {} drop-me'.format(પૉર્ટ_મૂલ્ય), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                મશીન.આદેશ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                પરિમાણ[종류] = મશીન.લૉગ_પંક્તિ.decode('utf-8', 'replace')
                print('PASS: {} ઉપયોગકર્તા ELF/ring 3/દલીલો/UDP હોસ્ટ 왕복/સમય_મૂલ્ય 초과/શેલ 복귀'.format(종류), flush=True)
            finally:
                try: મશીન.આદેશ('net', [])
                except Exception: pass
                (સ્થાન / 'build/사용자통신-last.log').write_bytes(મશીન.લૉગ_પંક્તિ)
                મશીન.બંધ_કરો()
        મશીન = વર્ચુઅલ_મશીન(સ્થાન / 'build/kernel.elf', નેટવર્ક_મૂલ્ય=False)
        try:
            મશીન.આદેશ('net', ['NET unavailable'])
            મશીન.આદેશ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            મશીન.આદેશ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            પરિમાણ['no_nic'] = મશીન.લૉગ_પંક્તિ.decode()
        finally: મશીન.બંધ_કરો()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            મશીન = વર્ચુઅલ_મશીન(보호커널(Path(임시)), નેટવર્ક_મૂલ્ય=False)
            try:
                for નામ, સ્થિતિ_મૂલ્ય_e10195a1 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    મશીન.આદેશ('run ' + નામ, ['Exit: ' + str(સ્થિતિ_મૂલ્ય_e10195a1)])
                    મશીન.આદેશ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                પરિમાણ['protection'] = મશીન.લૉગ_પંક્તિ.decode()
                print('PASS: ઉપયોગકર્તા મેમરી_ડેટા/હાર્ડવેર_પૉર્ટ 격리, 잘못된 સૂચક/ELF, CPU 예외, 무한 પુનરાવર્તન_મૂલ્ય 제한', flush=True)
            finally:
                (સ્થાન / 'build/보호시험-last.log').write_bytes(મશીન.લૉગ_પંક્તિ)
                મશીન.બંધ_કરો()
    finally:
        પ્રસ્થાન_એપ્લિકેશન.set()
        일꾼.join(timeout=2)
        સર્વર_મૂલ્ય.close()
    પરિમાણ['host_udp_received'] = [{'length': len(ડેટા), 'sha256': hashlib.sha256(ડેટા).hexdigest()} for ડેટા in 받은것]
    (સ્થાન / 'build/사용자통신시험.json').write_text(json.dumps(પરિમાણ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    અમલ_કરો_આદેશ()
