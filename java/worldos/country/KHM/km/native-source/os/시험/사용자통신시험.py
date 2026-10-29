#!/usr/bin/env python3
"""ដែលពិត_ទិន្នន័យ ring 3 ELF/ហូស UDP 왕복/ការពារ_តំលៃ កំហុស/ពេល_វេលា_តំលៃ 제한/잘못된 ELF를 검증한다."""
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

កំណត់ទីតាំង = Path(__file__).resolve().parents[1]


class និម្មិត_ម៉ាស៊ីន:
    def __init__(self, ផ្លូវ, 종류='elf', ណិតវឺក_តំលៃ=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        បញ្ជី_តំលៃ = Path(self.임시.name)
        self.កំណត់_ហេតុ_ថត = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.ម៉ូនីទ័រ_តំលៃ = socket.socket(socket.AF_UNIX)
        직렬경로, ម៉ូនីទ័រ_ផ្លូវ = បញ្ជី_តំលៃ / 'serial.sock', បញ្ជី_តំលៃ / 'monitor.sock'
        ពាក្យ_បញ្ជា = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ម៉ូនីទ័រ_ផ្លូវ) + ',server,nowait']
        ពាក្យ_បញ្ជា += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ណិតវឺក_តំលៃ else ['-net', 'none']
        ពាក្យ_បញ្ជា += ['-kernel', str(ផ្លូវ)] if 종류 == 'elf' else ['-cdrom', str(ផ្លូវ), '-boot', 'd']
        if 저장매체 is not None:
            ពាក្យ_បញ្ជា += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ដំណើរការ_តំលៃ = subprocess.Popen(ពាក្យ_បញ្ជា, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and ម៉ូនីទ័រ_ផ្លូវ.exists()):
                if self.ដំណើរការ_តំលៃ.poll() is not None:
                    raise AssertionError(self.ដំណើរការ_តំលៃ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU រត់ ពេល_វេលា_តំលៃ 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.ម៉ូនីទ័រ_តំលៃ.connect(str(ម៉ូនីទ័រ_ផ្លូវ))
            self.직렬.setblocking(False)
            self.ម៉ូនីទ័រ_តំលៃ.sendall(b'cont\n')
            self.រង់ចាំ_ភាព('jkoros> ')
        except BaseException:
            self.បិទ()
            raise

    def រង់ចាំ_ភាព(self, 문구, រត់=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.កំណត់_ហេតុ_ថត[រត់:]:
                return self.កំណត់_ហេតុ_ថត[រត់:].decode('utf-8', 'replace')
            អាន, _, _ = select.select([self.직렬], [], [], 0.1)
            if អាន:
                ទិន្នន័យ = self.직렬.recv(65536)
                if not ទិន្នន័យ: break
                self.កំណត់_ហេតុ_ថត.extend(ទិន្នន័យ)
            if self.ដំណើរការ_តំលៃ.poll() is not None: break
        raise AssertionError('រង់ចាំ_តំលៃ បរាជ័យ_តំលៃ: ' + 문구 + '\n' + self.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace'))

    def ពាក្យ_បញ្ជា(self, សំនុំអក្សរ_តំលៃ, 기대):
        រត់ = len(self.កំណត់_ហេតុ_ថត)
        self.직렬.sendall((សំនុំអក្សរ_តំលៃ + '\n').encode())
        ការវាស់វែង = self.រង់ចាំ_ភាព('jkoros> ', រត់)
        for 문구 in 기대:
            assert 문구 in ការវាស់វែង, (សំនុំអក្សរ_តំលៃ, 문구, ការវាស់វែង)
        assert 'PANIC' not in ការវាស់វែង, ការវាស់វែង
        return ការវាស់វែង

    def បិទ(self):
        self.직렬.close()
        self.ម៉ូនីទ័រ_តំលៃ.close()
        if self.ដំណើរការ_តំលៃ.poll() is None:
            self.ដំណើរការ_តំលៃ.terminate()
            try: self.ដំណើរការ_តំលៃ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ដំណើរការ_តំលៃ.kill()
                self.ដំណើរការ_តំលៃ.wait()
        self.ដំណើរការ_តំលៃ.communicate()
        self.임시.cleanup()


def 보호커널(បញ្ជី_តំលៃ):
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
    항목들 = ['hello=' + str(កំណត់ទីតាំង / 'build/apps/hello.elf')]
    for ឈ្មោះ, មាតិកា_តំលៃ in 사례들.items():
        ប្រភព = បញ្ជី_តំលៃ / (ឈ្មោះ + '.s')
        ប្រភព.write_text('.code32\n.text\n.globl _start\n_start:\n' + មាតិកា_តំលៃ +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(បញ្ជី_តំលៃ / (ឈ្មោះ + '.o')), str(ប្រភព)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(កំណត់ទីតាំង.parent / 'compiler/អ្នកប្រើ_តំណ_ប្លង់.ld'),
                        '-o', str(បញ្ជី_តំលៃ / (ឈ្មោះ + '.elf')), str(បញ្ជី_តំលៃ / (ឈ្មោះ + '.o'))], check=True)
        항목들.append(ឈ្មោះ + '=' + str(បញ្ជី_តំលៃ / (ឈ្មោះ + '.elf')))
    정상 = bytearray((កំណត់ទីតាំង / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    មិនត្រឹមត្រូវ_ការវាស់វែង = bytearray(정상); មិនត្រឹមត្រូវ_ការវាស់វែង[0] = 0; 변형들['badelf'] = មិនត្រឹមត្រូវ_ការវាស់វែង
    មិនត្រឹមត្រូវ_ការវាស់វែង = bytearray(정상); struct.pack_into('<I', មិនត្រឹមត្រូវ_ការវាស់វែង, 24, 0x00100000); 변형들['badentry'] = មិនត្រឹមត្រូវ_ការវាស់វែង
    មិនត្រឹមត្រូវ_ការវាស់វែង = bytearray(정상); struct.pack_into('<I', មិនត្រឹមត្រូវ_ការវាស់វែង, 28, 0x7fffffff); 변형들['badtable'] = មិនត្រឹមត្រូវ_ការវាស់វែង
    មិនត្រឹមត្រូវ_ការវាស់វែង = bytearray(정상); រុករក_តារាង = struct.unpack_from('<I', មិនត្រឹមត្រូវ_ការវាស់វែង, 28)[0]
    struct.pack_into('<I', មិនត្រឹមត្រូវ_ការវាស់វែង, រុករក_តារាង + 20, 0x7fffffff); 변형들['badsize'] = មិនត្រឹមត្រូវ_ការវាស់វែង
    for ឈ្មោះ, ទិន្នន័យ in 변형들.items():
        ឯកសារ = បញ្ជី_តំលៃ / (ឈ្មោះ + '.elf'); ឯកសារ.write_bytes(ទិន្នន័យ)
        항목들.append(ឈ្មោះ + '=' + str(ឯកសារ))
    subprocess.run([sys.executable, str(កំណត់ទីតាំង / 'ឧបករណ៍/묶기.py'), '-o', str(បញ្ជី_តំលៃ / 'apps.bin')] + 항목들, check=True)
    ប្រភព = បញ្ជី_តំលៃ / 'apps.s'
    ប្រភព.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(បញ្ជី_តំលៃ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(បញ្ជី_តំលៃ / 'apps.o'), str(ប្រភព)], check=True)
    ខឺណេល_តំលៃ = បញ្ជី_តំលៃ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(កំណត់ទីតាំង / '부팅/តំណ_ប្លង់.ld'), '-o', str(ខឺណេល_តំលៃ),
                    str(កំណត់ទីតាំង / 'build/boot.o'), str(កំណត់ទីតាំង / 'build/java.o'), str(កំណត់ទីតាំង / 'build/user.o'), str(បញ្ជី_តំលៃ / 'apps.o')], check=True)
    return ខឺណេល_តំលៃ


def អនុវត្ត_ពាក្យបញ្ជា():
    ការវាស់វែង = {}
    ម៉ាស៊ីនមេ_តំលៃ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ម៉ាស៊ីនមេ_តំលៃ.bind(('127.0.0.1', 0))
    ម៉ាស៊ីនមេ_តំលៃ.settimeout(0.1)
    ច្រក_តំលៃ = ម៉ាស៊ីនមេ_តំលៃ.getsockname()[1]
    받은것 = []
    ចេញ_កម្មវិធី = threading.Event()
    def 되보내기():
        while not ចេញ_កម្មវិធី.is_set():
            try: ទិន្នន័យ, សិទ្ធស្មើ_តំលៃ = ម៉ាស៊ីនមេ_តំលៃ.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ទិន្នន័យ)
            if ទិន្នន័យ != b'drop-me': ម៉ាស៊ីនមេ_តំលៃ.sendto(ទិន្នន័យ, សិទ្ធស្មើ_តំលៃ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run missing', ['Exit: -2'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('net', ['NET RTL8139'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for មាតិកា_តំលៃ in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run udp 10.0.2.2 {} {}'.format(ច្រក_តំលៃ, មាតិកា_តំលៃ), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert មាតិកា_តំលៃ.encode() in 받은것, 'ហូស 서버에서 자료를 받지 못함'
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run stress {}'.format(ច្រក_តំលៃ), ['UDP STRESS PASS', 'Exit: 0'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run udp 10.0.2.2 {} drop-me'.format(ច្រក_តំលៃ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ការវាស់វែង[종류] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode('utf-8', 'replace')
                print('PASS: {} អ្នកប្រើ ELF/ring 3/អាគុយម៉ង់/UDP ហូស 왕복/ពេល_វេលា_តំលៃ 초과/셸 복귀'.format(종류), flush=True)
            finally:
                try: ម៉ាស៊ីន.ពាក្យ_បញ្ជា('net', [])
                except Exception: pass
                (កំណត់ទីតាំង / 'build/사용자통신-last.log').write_bytes(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
                ម៉ាស៊ីន.បិទ()
        ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(កំណត់ទីតាំង / 'build/kernel.elf', ណិតវឺក_តំលៃ=False)
        try:
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('net', ['NET unavailable'])
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ការវាស់វែង['no_nic'] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode()
        finally: ម៉ាស៊ីន.បិទ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ម៉ាស៊ីន = និម្មិត_ម៉ាស៊ីន(보호커널(Path(임시)), ណិតវឺក_តំលៃ=False)
            try:
                for ឈ្មោះ, ភាព_តំលៃ in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run ' + ឈ្មោះ, ['Exit: ' + str(ភាព_តំលៃ)])
                    ម៉ាស៊ីន.ពាក្យ_បញ្ជា('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ការវាស់វែង['protection'] = ម៉ាស៊ីន.កំណត់_ហេតុ_ថត.decode()
                print('PASS: អ្នកប្រើ សតិ_ទិន្នន័យ/포트 격리, 잘못된 អង្គ_ចង្អុល_កណ្ដុរ/ELF, CPU ការលើកលែង, 무한 ការធ្វើឡើងវិញ_តំលៃ 제한', flush=True)
            finally:
                (កំណត់ទីតាំង / 'build/보호시험-last.log').write_bytes(ម៉ាស៊ីន.កំណត់_ហេតុ_ថត)
                ម៉ាស៊ីន.បិទ()
    finally:
        ចេញ_កម្មវិធី.set()
        일꾼.join(timeout=2)
        ម៉ាស៊ីនមេ_តំលៃ.close()
    ការវាស់វែង['host_udp_received'] = [{'length': len(ទិន្នន័យ), 'sha256': hashlib.sha256(ទិន្នន័យ).hexdigest()} for ទិន្នន័យ in 받은것]
    (កំណត់ទីតាំង / 'build/사용자통신시험.json').write_text(json.dumps(ការវាស់វែង, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    អនុវត្ត_ពាក្យបញ្ជា()
