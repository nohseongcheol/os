#!/usr/bin/env python3
"""실제 ring 3 ELF/کوربه UDP 왕복/خونديېل_ارزښت تېروتنه/시간 제한/잘못된 ELF를 검증한다."""
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

ځای = Path(__file__).resolve().parents[1]


class 가상기계:
    def __init__(self, يونلور, 종류='elf', جال_ارزښت=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        نوملړ_ارزښت = Path(self.임시.name)
        self.خبرال_کیل = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.ليدانى_ارزښت = socket.socket(socket.AF_UNIX)
        직렬경로, ليدانى_يونلور = نوملړ_ارزښت / 'serial.sock', نوملړ_ارزښت / 'monitor.sock'
        بولۍ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ليدانى_يونلور) + ',server,nowait']
        بولۍ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if جال_ارزښت else ['-net', 'none']
        بولۍ += ['-kernel', str(يونلور)] if 종류 == 'elf' else ['-cdrom', str(يونلور), '-boot', 'd']
        if 저장매체 is not None:
            بولۍ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.과정 = subprocess.Popen(بولۍ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and ليدانى_يونلور.exists()):
                if self.과정.poll() is not None:
                    raise AssertionError(self.과정.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ځغلول 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.ليدانى_ارزښت.connect(str(ليدانى_يونلور))
            self.직렬.setblocking(False)
            self.ليدانى_ارزښت.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.بندول()
            raise

    def 기다림(self, 문구, ځغلول=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.خبرال_کیل[ځغلول:]:
                return self.خبرال_کیل[ځغلول:].decode('utf-8', 'replace')
            لوستل, _, _ = select.select([self.직렬], [], [], 0.1)
            if لوستل:
                اومتوک = self.직렬.recv(65536)
                if not اومتوک: break
                self.خبرال_کیل.extend(اومتوک)
            if self.과정.poll() is not None: break
        raise AssertionError('대기 پاتېينه_ارزښت: ' + 문구 + '\n' + self.خبرال_کیل.decode('utf-8', 'replace'))

    def بولۍ(self, مزى_ارزښت_6ca8363c, 기대):
        ځغلول = len(self.خبرال_کیل)
        self.직렬.sendall((مزى_ارزښت_6ca8363c + '\n').encode())
        결과 = self.기다림('jkoros> ', ځغلول)
        for 문구 in 기대:
            assert 문구 in 결과, (مزى_ارزښت_6ca8363c, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def بندول(self):
        self.직렬.close()
        self.ليدانى_ارزښت.close()
        if self.과정.poll() is None:
            self.과정.terminate()
            try: self.과정.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.과정.kill()
                self.과정.wait()
        self.과정.communicate()
        self.임시.cleanup()


def 보호커널(نوملړ_ارزښت):
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
    항목들 = ['hello=' + str(ځای / 'build/apps/hello.elf')]
    for نوم, منځپانګه_ارزښت in 사례들.items():
        سرچينه = نوملړ_ارزښت / (نوم + '.s')
        سرچينه.write_text('.code32\n.text\n.globl _start\n_start:\n' + منځپانګه_ارزښت +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(نوملړ_ارزښت / (نوم + '.o')), str(سرچينه)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ځای.parent / 'compiler/کارن_پيوند_هډوانه.ld'),
                        '-o', str(نوملړ_ارزښت / (نوم + '.elf')), str(نوملړ_ارزښت / (نوم + '.o'))], check=True)
        항목들.append(نوم + '=' + str(نوملړ_ارزښت / (نوم + '.elf')))
    정상 = bytearray((ځای / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for نوم, اومتوک in 변형들.items():
        دوتنه = نوملړ_ارزښت / (نوم + '.elf'); دوتنه.write_bytes(اومتوک)
        항목들.append(نوم + '=' + str(دوتنه))
    subprocess.run([sys.executable, str(ځای / '도구/묶기.py'), '-o', str(نوملړ_ارزښت / 'apps.bin')] + 항목들, check=True)
    سرچينه = نوملړ_ارزښت / 'apps.s'
    سرچينه.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(نوملړ_ارزښت / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(نوملړ_ارزښت / 'apps.o'), str(سرچينه)], check=True)
    نوغی_ارزښت = نوملړ_ارزښت / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ځای / '부팅/پيوند_هډوانه.ld'), '-o', str(نوغی_ارزښت),
                    str(ځای / 'build/boot.o'), str(ځای / 'build/java.o'), str(ځای / 'build/user.o'), str(نوملړ_ارزښت / 'apps.o')], check=True)
    return نوغی_ارزښت


def 실행():
    결과 = {}
    서버 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    서버.bind(('127.0.0.1', 0))
    서버.settimeout(0.1)
    درشل_ارزښت = 서버.getsockname()[1]
    받은것 = []
    وتون_کاريال = threading.Event()
    def 되보내기():
        while not وتون_کاريال.is_set():
            try: اومتوک, جوړه_ارزښت = 서버.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(اومتوک)
            if اومتوک != b'drop-me': 서버.sendto(اومتوک, جوړه_ارزښت)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(ځای / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                기계.بولۍ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                기계.بولۍ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                기계.بولۍ('run missing', ['Exit: -2'])
                기계.بولۍ('net', ['NET RTL8139'])
                기계.بولۍ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for منځپانګه_ارزښت in ('hello-network', 'odd', 'even', 'repeat-123'):
                    기계.بولۍ('run udp 10.0.2.2 {} {}'.format(درشل_ارزښت, منځپانګه_ارزښت), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert منځپانګه_ارزښت.encode() in 받은것, 'کوربه 서버에서 자료를 받지 못함'
                기계.بولۍ('run stress {}'.format(درشل_ارزښت), ['UDP STRESS PASS', 'Exit: 0'])
                기계.بولۍ('run udp 10.0.2.2 {} drop-me'.format(درشل_ارزښت), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                기계.بولۍ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.خبرال_کیل.decode('utf-8', 'replace')
                print('PASS: {} کارن ELF/ring 3/인수/UDP کوربه 왕복/시간 초과/سیپۍ 복귀'.format(종류), flush=True)
            finally:
                try: 기계.بولۍ('net', [])
                except Exception: pass
                (ځای / 'build/사용자통신-last.log').write_bytes(기계.خبرال_کیل)
                기계.بندول()
        기계 = 가상기계(ځای / 'build/kernel.elf', جال_ارزښت=False)
        try:
            기계.بولۍ('net', ['NET unavailable'])
            기계.بولۍ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            기계.بولۍ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = 기계.خبرال_کیل.decode()
        finally: 기계.بندول()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            기계 = 가상기계(보호커널(Path(임시)), جال_ارزښت=False)
            try:
                for نوم, انکړ_ارزښت in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    기계.بولۍ('run ' + نوم, ['Exit: ' + str(انکړ_ارزښت)])
                    기계.بولۍ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = 기계.خبرال_کیل.decode()
                print('PASS: کارن 메모리/포트 격리, 잘못된 포인터/ELF, CPU 예외, 무한 تکرار_ارزښت 제한', flush=True)
            finally:
                (ځای / 'build/보호시험-last.log').write_bytes(기계.خبرال_کیل)
                기계.بندول()
    finally:
        وتون_کاريال.set()
        일꾼.join(timeout=2)
        서버.close()
    결과['host_udp_received'] = [{'length': len(اومتوک), 'sha256': hashlib.sha256(اومتوک).hexdigest()} for اومتوک in 받은것]
    (ځای / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    실행()
