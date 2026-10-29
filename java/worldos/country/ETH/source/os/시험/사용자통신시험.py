#!/usr/bin/env python3
"""ትክክለኛ_ውሂብ ring 3 ELF/አዘጋጅ_b78e430d UDP 왕복/ጠብቅ_እሴት ስህተት/ጊዜ_እሴት 제한/잘못된 ELF를 검증한다."""
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

አካባቢ = Path(__file__).resolve().parents[1]


class ምናባዊ_ማሽን:
    def __init__(self, መተላለፊያ, 종류='elf', መረብ_እሴት=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ማውጫ_እሴት = Path(self.임시.name)
        self.መዝግብ_ረድፍ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.ማሳያ_እሴት = socket.socket(socket.AF_UNIX)
        직렬경로, ማሳያ_ዱካ = ማውጫ_እሴት / 'serial.sock', ማውጫ_እሴት / 'monitor.sock'
        ትእዛዝ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ማሳያ_ዱካ) + ',server,nowait']
        ትእዛዝ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if መረብ_እሴት else ['-net', 'none']
        ትእዛዝ += ['-kernel', str(መተላለፊያ)] if 종류 == 'elf' else ['-cdrom', str(መተላለፊያ), '-boot', 'd']
        if 저장매체 is not None:
            ትእዛዝ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ሂደት_እሴት = subprocess.Popen(ትእዛዝ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and ማሳያ_ዱካ.exists()):
                if self.ሂደት_እሴት.poll() is not None:
                    raise AssertionError(self.ሂደት_እሴት.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ማስኬጃ ጊዜ_እሴት 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.ማሳያ_እሴት.connect(str(ማሳያ_ዱካ))
            self.직렬.setblocking(False)
            self.ማሳያ_እሴት.sendall(b'cont\n')
            self.መጠበቅ_ዞን('jkoros> ')
        except BaseException:
            self.መዝጊያ()
            raise

    def መጠበቅ_ዞን(self, 문구, ማስኬጃ=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.መዝግብ_ረድፍ[ማስኬጃ:]:
                return self.መዝግብ_ረድፍ[ማስኬጃ:].decode('utf-8', 'replace')
            ማንበቢያ, _, _ = select.select([self.직렬], [], [], 0.1)
            if ማንበቢያ:
                ውሂብ = self.직렬.recv(65536)
                if not ውሂብ: break
                self.መዝግብ_ረድፍ.extend(ውሂብ)
            if self.ሂደት_እሴት.poll() is not None: break
        raise AssertionError('መጠበቅ_እሴት ተስኖት_እሴት: ' + 문구 + '\n' + self.መዝግብ_ረድፍ.decode('utf-8', 'replace'))

    def ትእዛዝ(self, ኅብረቁምፊ_እሴት, 기대):
        ማስኬጃ = len(self.መዝግብ_ረድፍ)
        self.직렬.sendall((ኅብረቁምፊ_እሴት + '\n').encode())
        ልኬት = self.መጠበቅ_ዞን('jkoros> ', ማስኬጃ)
        for 문구 in 기대:
            assert 문구 in ልኬት, (ኅብረቁምፊ_እሴት, 문구, ልኬት)
        assert 'PANIC' not in ልኬት, ልኬት
        return ልኬት

    def መዝጊያ(self):
        self.직렬.close()
        self.ማሳያ_እሴት.close()
        if self.ሂደት_እሴት.poll() is None:
            self.ሂደት_እሴት.terminate()
            try: self.ሂደት_እሴት.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ሂደት_እሴት.kill()
                self.ሂደት_እሴት.wait()
        self.ሂደት_እሴት.communicate()
        self.임시.cleanup()


def 보호커널(ማውጫ_እሴት):
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
    항목들 = ['hello=' + str(አካባቢ / 'build/apps/hello.elf')]
    for ስም, ይዘት_እሴት in 사례들.items():
        ምንጭ = ማውጫ_እሴት / (ስም + '.s')
        ምንጭ.write_text('.code32\n.text\n.globl _start\n_start:\n' + ይዘት_እሴት +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ማውጫ_እሴት / (ስም + '.o')), str(ምንጭ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(አካባቢ.parent / 'compiler/ተጠቃሚ_አገናኝ_አሰሳ.ld'),
                        '-o', str(ማውጫ_እሴት / (ስም + '.elf')), str(ማውጫ_እሴት / (ስም + '.o'))], check=True)
        항목들.append(ስም + '=' + str(ማውጫ_እሴት / (ስም + '.elf')))
    정상 = bytearray((አካባቢ / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ልክ_ያልኾነ_ልኬት = bytearray(정상); ልክ_ያልኾነ_ልኬት[0] = 0; 변형들['badelf'] = ልክ_ያልኾነ_ልኬት
    ልክ_ያልኾነ_ልኬት = bytearray(정상); struct.pack_into('<I', ልክ_ያልኾነ_ልኬት, 24, 0x00100000); 변형들['badentry'] = ልክ_ያልኾነ_ልኬት
    ልክ_ያልኾነ_ልኬት = bytearray(정상); struct.pack_into('<I', ልክ_ያልኾነ_ልኬት, 28, 0x7fffffff); 변형들['badtable'] = ልክ_ያልኾነ_ልኬት
    ልክ_ያልኾነ_ልኬት = bytearray(정상); ፍለጋ_ሰንጠረዥ = struct.unpack_from('<I', ልክ_ያልኾነ_ልኬት, 28)[0]
    struct.pack_into('<I', ልክ_ያልኾነ_ልኬት, ፍለጋ_ሰንጠረዥ + 20, 0x7fffffff); 변형들['badsize'] = ልክ_ያልኾነ_ልኬት
    for ስም, ውሂብ in 변형들.items():
        ፋይል = ማውጫ_እሴት / (ስም + '.elf'); ፋይል.write_bytes(ውሂብ)
        항목들.append(ስም + '=' + str(ፋይል))
    subprocess.run([sys.executable, str(አካባቢ / 'መሳሪያዎች/묶기.py'), '-o', str(ማውጫ_እሴት / 'apps.bin')] + 항목들, check=True)
    ምንጭ = ማውጫ_እሴት / 'apps.s'
    ምንጭ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ማውጫ_እሴት / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ማውጫ_እሴት / 'apps.o'), str(ምንጭ)], check=True)
    ዓንኳር_እሴት = ማውጫ_እሴት / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(አካባቢ / '부팅/አገናኝ_አሰሳ.ld'), '-o', str(ዓንኳር_እሴት),
                    str(አካባቢ / 'build/boot.o'), str(አካባቢ / 'build/java.o'), str(አካባቢ / 'build/user.o'), str(ማውጫ_እሴት / 'apps.o')], check=True)
    return ዓንኳር_እሴት


def ፈጽም_ትእዛዝ():
    ልኬት = {}
    አገልጋይ_እሴት = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    አገልጋይ_እሴት.bind(('127.0.0.1', 0))
    አገልጋይ_እሴት.settimeout(0.1)
    ወደብ_እሴት = አገልጋይ_እሴት.getsockname()[1]
    받은것 = []
    ውጣ_ፕሮግራም = threading.Event()
    def 되보내기():
        while not ውጣ_ፕሮግራም.is_set():
            try: ውሂብ, አቻ_እሴት = አገልጋይ_እሴት.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ውሂብ)
            if ውሂብ != b'drop-me': አገልጋይ_እሴት.sendto(ውሂብ, አቻ_እሴት)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ማሽን = ምናባዊ_ማሽን(አካባቢ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ማሽን.ትእዛዝ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ማሽን.ትእዛዝ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ማሽን.ትእዛዝ('run missing', ['Exit: -2'])
                ማሽን.ትእዛዝ('net', ['NET RTL8139'])
                ማሽን.ትእዛዝ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ይዘት_እሴት in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ማሽን.ትእዛዝ('run udp 10.0.2.2 {} {}'.format(ወደብ_እሴት, ይዘት_እሴት), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ይዘት_እሴት.encode() in 받은것, 'አዘጋጅ_b78e430d 서버에서 자료를 받지 못함'
                ማሽን.ትእዛዝ('run stress {}'.format(ወደብ_እሴት), ['UDP STRESS PASS', 'Exit: 0'])
                ማሽን.ትእዛዝ('run udp 10.0.2.2 {} drop-me'.format(ወደብ_እሴት), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ማሽን.ትእዛዝ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ልኬት[종류] = ማሽን.መዝግብ_ረድፍ.decode('utf-8', 'replace')
                print('PASS: {} ተጠቃሚ ELF/ring 3/인수/UDP አዘጋጅ_b78e430d 왕복/ጊዜ_እሴት 초과/ሼል 복귀'.format(종류), flush=True)
            finally:
                try: ማሽን.ትእዛዝ('net', [])
                except Exception: pass
                (አካባቢ / 'build/사용자통신-last.log').write_bytes(ማሽን.መዝግብ_ረድፍ)
                ማሽን.መዝጊያ()
        ማሽን = ምናባዊ_ማሽን(አካባቢ / 'build/kernel.elf', መረብ_እሴት=False)
        try:
            ማሽን.ትእዛዝ('net', ['NET unavailable'])
            ማሽን.ትእዛዝ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ማሽን.ትእዛዝ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ልኬት['no_nic'] = ማሽን.መዝግብ_ረድፍ.decode()
        finally: ማሽን.መዝጊያ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ማሽን = ምናባዊ_ማሽን(보호커널(Path(임시)), መረብ_እሴት=False)
            try:
                for ስም, ዞን_እሴት in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ማሽን.ትእዛዝ('run ' + ስም, ['Exit: ' + str(ዞን_እሴት)])
                    ማሽን.ትእዛዝ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ልኬት['protection'] = ማሽን.መዝግብ_ረድፍ.decode()
                print('PASS: ተጠቃሚ ማስቀመጫ_ውሂብ/포트 격리, 잘못된 ጠቋሚ/ELF, CPU ልዩነት, 무한 ሽምጥ_እሴት 제한', flush=True)
            finally:
                (አካባቢ / 'build/보호시험-last.log').write_bytes(ማሽን.መዝግብ_ረድፍ)
                ማሽን.መዝጊያ()
    finally:
        ውጣ_ፕሮግራም.set()
        일꾼.join(timeout=2)
        አገልጋይ_እሴት.close()
    ልኬት['host_udp_received'] = [{'length': len(ውሂብ), 'sha256': hashlib.sha256(ውሂብ).hexdigest()} for ውሂብ in 받은것]
    (አካባቢ / 'build/사용자통신시험.json').write_text(json.dumps(ልኬት, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ፈጽም_ትእዛዝ()
