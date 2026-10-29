#!/usr/bin/env python3
"""ትኽክለኛ_ሓበሬታ ring 3 ELF/አዐንግድ UDP 왕복/ሓልው_ዋጋ ጌጋ/시간 제한/잘못된 ELF를 검증한다."""
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


class መሳሊ_ማሽን:
    def __init__(self, መገዲ, 종류='elf', ማሕበራዊ_ኔትወርክ_ዋጋ=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ሓባሪ_ማህደር_ዋጋ = Path(self.임시.name)
        self.ምዝጉብ_ሪጋ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.መርኣዪ_ዋጋ = socket.socket(socket.AF_UNIX)
        직렬경로, መርኣዪ_መገዲ = ሓባሪ_ማህደር_ዋጋ / 'serial.sock', ሓባሪ_ማህደር_ዋጋ / 'monitor.sock'
        ትእዛዝ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(መርኣዪ_መገዲ) + ',server,nowait']
        ትእዛዝ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ማሕበራዊ_ኔትወርክ_ዋጋ else ['-net', 'none']
        ትእዛዝ += ['-kernel', str(መገዲ)] if 종류 == 'elf' else ['-cdrom', str(መገዲ), '-boot', 'd']
        if 저장매체 is not None:
            ትእዛዝ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.መስርሕ_ዋጋ = subprocess.Popen(ትእዛዝ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and መርኣዪ_መገዲ.exists()):
                if self.መስርሕ_ዋጋ.poll() is not None:
                    raise AssertionError(self.መስርሕ_ዋጋ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ኣኺድ 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.መርኣዪ_ዋጋ.connect(str(መርኣዪ_መገዲ))
            self.직렬.setblocking(False)
            self.መርኣዪ_ዋጋ.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.ዕጸው()
            raise

    def 기다림(self, 문구, ኣኺድ=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ምዝጉብ_ሪጋ[ኣኺድ:]:
                return self.ምዝጉብ_ሪጋ[ኣኺድ:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                ሓበሬታ = self.직렬.recv(65536)
                if not ሓበሬታ: break
                self.ምዝጉብ_ሪጋ.extend(ሓበሬታ)
            if self.መስርሕ_ዋጋ.poll() is not None: break
        raise AssertionError('대기 ፍሽለት_ዋጋ: ' + 문구 + '\n' + self.ምዝጉብ_ሪጋ.decode('utf-8', 'replace'))

    def ትእዛዝ(self, ሕብረ_ቁምፊ_ዋጋ, 기대):
        ኣኺድ = len(self.ምዝጉብ_ሪጋ)
        self.직렬.sendall((ሕብረ_ቁምፊ_ዋጋ + '\n').encode())
        결과 = self.기다림('jkoros> ', ኣኺድ)
        for 문구 in 기대:
            assert 문구 in 결과, (ሕብረ_ቁምፊ_ዋጋ, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def ዕጸው(self):
        self.직렬.close()
        self.መርኣዪ_ዋጋ.close()
        if self.መስርሕ_ዋጋ.poll() is None:
            self.መስርሕ_ዋጋ.terminate()
            try: self.መስርሕ_ዋጋ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.መስርሕ_ዋጋ.kill()
                self.መስርሕ_ዋጋ.wait()
        self.መስርሕ_ዋጋ.communicate()
        self.임시.cleanup()


def 보호커널(ሓባሪ_ማህደር_ዋጋ):
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
    for ሽም, ትሕዝቶ_ዋጋ in 사례들.items():
        ምንጪ = ሓባሪ_ማህደር_ዋጋ / (ሽም + '.s')
        ምንጪ.write_text('.code32\n.text\n.globl _start\n_start:\n' + ትሕዝቶ_ዋጋ +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ሓባሪ_ማህደር_ዋጋ / (ሽም + '.o')), str(ምንጪ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/ተጠቃሚ_መጋጠሚ_ኣቀማምጣ.ld'),
                        '-o', str(ሓባሪ_ማህደር_ዋጋ / (ሽም + '.elf')), str(ሓባሪ_ማህደር_ዋጋ / (ሽም + '.o'))], check=True)
        항목들.append(ሽም + '=' + str(ሓባሪ_ማህደር_ዋጋ / (ሽም + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for ሽም, ሓበሬታ in 변형들.items():
        ፋይል = ሓባሪ_ማህደር_ዋጋ / (ሽም + '.elf'); ፋይል.write_bytes(ሓበሬታ)
        항목들.append(ሽም + '=' + str(ፋይል))
    subprocess.run([sys.executable, str(위치 / 'መሳርሒታት/묶기.py'), '-o', str(ሓባሪ_ማህደር_ዋጋ / 'apps.bin')] + 항목들, check=True)
    ምንጪ = ሓባሪ_ማህደር_ዋጋ / 'apps.s'
    ምንጪ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ሓባሪ_ማህደር_ዋጋ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ሓባሪ_ማህደር_ዋጋ / 'apps.o'), str(ምንጪ)], check=True)
    ፍረ_ዋጋ = ሓባሪ_ማህደር_ዋጋ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/መጋጠሚ_ኣቀማምጣ.ld'), '-o', str(ፍረ_ዋጋ),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(ሓባሪ_ማህደር_ዋጋ / 'apps.o')], check=True)
    return ፍረ_ዋጋ


def ተግብር_ትእዛዝ():
    결과 = {}
    ኣገልጋሊ_ዋጋ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ኣገልጋሊ_ዋጋ.bind(('127.0.0.1', 0))
    ኣገልጋሊ_ዋጋ.settimeout(0.1)
    ወደብ_ዋጋ = ኣገልጋሊ_ዋጋ.getsockname()[1]
    받은것 = []
    ውጻእ_መተግበሪ = threading.Event()
    def 되보내기():
        while not ውጻእ_መተግበሪ.is_set():
            try: ሓበሬታ, መዘና_ዋጋ = ኣገልጋሊ_ዋጋ.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ሓበሬታ)
            if ሓበሬታ != b'drop-me': ኣገልጋሊ_ዋጋ.sendto(ሓበሬታ, መዘና_ዋጋ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ማሽን = መሳሊ_ማሽን(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ማሽን.ትእዛዝ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ማሽን.ትእዛዝ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ማሽን.ትእዛዝ('run missing', ['Exit: -2'])
                ማሽን.ትእዛዝ('net', ['NET RTL8139'])
                ማሽን.ትእዛዝ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ትሕዝቶ_ዋጋ in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ማሽን.ትእዛዝ('run udp 10.0.2.2 {} {}'.format(ወደብ_ዋጋ, ትሕዝቶ_ዋጋ), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ትሕዝቶ_ዋጋ.encode() in 받은것, 'አዐንግድ 서버에서 자료를 받지 못함'
                ማሽን.ትእዛዝ('run stress {}'.format(ወደብ_ዋጋ), ['UDP STRESS PASS', 'Exit: 0'])
                ማሽን.ትእዛዝ('run udp 10.0.2.2 {} drop-me'.format(ወደብ_ዋጋ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ማሽን.ትእዛዝ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = ማሽን.ምዝጉብ_ሪጋ.decode('utf-8', 'replace')
                print('PASS: {} ተጠቃሚ ELF/ring 3/인수/UDP አዐንግድ 왕복/시간 초과/ሽፋን 복귀'.format(종류), flush=True)
            finally:
                try: ማሽን.ትእዛዝ('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(ማሽን.ምዝጉብ_ሪጋ)
                ማሽን.ዕጸው()
        ማሽን = መሳሊ_ማሽን(위치 / 'build/kernel.elf', ማሕበራዊ_ኔትወርክ_ዋጋ=False)
        try:
            ማሽን.ትእዛዝ('net', ['NET unavailable'])
            ማሽን.ትእዛዝ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ማሽን.ትእዛዝ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = ማሽን.ምዝጉብ_ሪጋ.decode()
        finally: ማሽን.ዕጸው()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ማሽን = መሳሊ_ማሽን(보호커널(Path(임시)), ማሕበራዊ_ኔትወርክ_ዋጋ=False)
            try:
                for ሽም, ደረጃ_ዋጋ in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ማሽን.ትእዛዝ('run ' + ሽም, ['Exit: ' + str(ደረጃ_ዋጋ)])
                    ማሽን.ትእዛዝ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = ማሽን.ምዝጉብ_ሪጋ.decode()
                print('PASS: ተጠቃሚ ማህደር_ዝኽረት_ሓበሬታ/ሃርድዌር_ወደብ 격리, 잘못된 ኣመልካቲ/ELF, CPU 예외, 무한 ዝርዝር_ዋጋ 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(ማሽን.ምዝጉብ_ሪጋ)
                ማሽን.ዕጸው()
    finally:
        ውጻእ_መተግበሪ.set()
        일꾼.join(timeout=2)
        ኣገልጋሊ_ዋጋ.close()
    결과['host_udp_received'] = [{'length': len(ሓበሬታ), 'sha256': hashlib.sha256(ሓበሬታ).hexdigest()} for ሓበሬታ in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ተግብር_ትእዛዝ()
