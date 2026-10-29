#!/usr/bin/env python3
"""वास्तविक_लगत ring 3 ELF/होस्ट UDP 왕복/सुरक्षित_गर्नुहोस्_मान त्रुटि/시간 제한/잘못된 ELF를 검증한다."""
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

स्थिति = Path(__file__).resolve().parents[1]


class अवास्तविक_मेशिन:
    def __init__(self, मार्ग, 종류='elf', सञ्जाल_मान=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        डाइरेक्टरी_मान = Path(self.임시.name)
        self.लग_रेकर्ड = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.मनिटर_मान = socket.socket(socket.AF_UNIX)
        직렬경로, मनिटर_बाटो = डाइरेक्टरी_मान / 'serial.sock', डाइरेक्टरी_मान / 'monitor.sock'
        आदेश = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(मनिटर_बाटो) + ',server,nowait']
        आदेश += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if सञ्जाल_मान else ['-net', 'none']
        आदेश += ['-kernel', str(मार्ग)] if 종류 == 'elf' else ['-cdrom', str(मार्ग), '-boot', 'd']
        if 저장매체 is not None:
            आदेश += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.प्रक्रिया_मान = subprocess.Popen(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and मनिटर_बाटो.exists()):
                if self.प्रक्रिया_मान.poll() is not None:
                    raise AssertionError(self.प्रक्रिया_मान.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU चलाउनुहोस् 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.मनिटर_मान.connect(str(मनिटर_बाटो))
            self.직렬.setblocking(False)
            self.मनिटर_मान.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.बन्दगर्नुहोस्()
            raise

    def 기다림(self, 문구, चलाउनुहोस्=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.लग_रेकर्ड[चलाउनुहोस्:]:
                return self.लग_रेकर्ड[चलाउनुहोस्:].decode('utf-8', 'replace')
            पढनुहोस्, _, _ = select.select([self.직렬], [], [], 0.1)
            if पढनुहोस्:
                लगत = self.직렬.recv(65536)
                if not लगत: break
                self.लग_रेकर्ड.extend(लगत)
            if self.प्रक्रिया_मान.poll() is not None: break
        raise AssertionError('대기 विफल_मान: ' + 문구 + '\n' + self.लग_रेकर्ड.decode('utf-8', 'replace'))

    def आदेश(self, स्ट्रिङ_मान, 기대):
        चलाउनुहोस् = len(self.लग_रेकर्ड)
        self.직렬.sendall((स्ट्रिङ_मान + '\n').encode())
        मापन = self.기다림('jkoros> ', चलाउनुहोस्)
        for 문구 in 기대:
            assert 문구 in मापन, (स्ट्रिङ_मान, 문구, मापन)
        assert 'PANIC' not in मापन, मापन
        return मापन

    def बन्दगर्नुहोस्(self):
        self.직렬.close()
        self.मनिटर_मान.close()
        if self.प्रक्रिया_मान.poll() is None:
            self.प्रक्रिया_मान.terminate()
            try: self.प्रक्रिया_मान.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.प्रक्रिया_मान.kill()
                self.प्रक्रिया_मान.wait()
        self.प्रक्रिया_मान.communicate()
        self.임시.cleanup()


def 보호커널(डाइरेक्टरी_मान):
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
    항목들 = ['hello=' + str(स्थिति / 'build/apps/hello.elf')]
    for नाम, सामग्री_मान in 사례들.items():
        स्रोत = डाइरेक्टरी_मान / (नाम + '.s')
        स्रोत.write_text('.code32\n.text\n.globl _start\n_start:\n' + सामग्री_मान +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(डाइरेक्टरी_मान / (नाम + '.o')), str(स्रोत)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थिति.parent / 'compiler/प्रयोगकर्ता_लिङ्क_लेआउट.ld'),
                        '-o', str(डाइरेक्टरी_मान / (नाम + '.elf')), str(डाइरेक्टरी_मान / (नाम + '.o'))], check=True)
        항목들.append(नाम + '=' + str(डाइरेक्टरी_मान / (नाम + '.elf')))
    정상 = bytearray((स्थिति / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    अवैधानिक_मापन = bytearray(정상); अवैधानिक_मापन[0] = 0; 변형들['badelf'] = अवैधानिक_मापन
    अवैधानिक_मापन = bytearray(정상); struct.pack_into('<I', अवैधानिक_मापन, 24, 0x00100000); 변형들['badentry'] = अवैधानिक_मापन
    अवैधानिक_मापन = bytearray(정상); struct.pack_into('<I', अवैधानिक_मापन, 28, 0x7fffffff); 변형들['badtable'] = अवैधानिक_मापन
    अवैधानिक_मापन = bytearray(정상); विवरण_हेर्ने_सुविधा_तालिका = struct.unpack_from('<I', अवैधानिक_मापन, 28)[0]
    struct.pack_into('<I', अवैधानिक_मापन, विवरण_हेर्ने_सुविधा_तालिका + 20, 0x7fffffff); 변형들['badsize'] = अवैधानिक_मापन
    for नाम, लगत in 변형들.items():
        फाइल = डाइरेक्टरी_मान / (नाम + '.elf'); फाइल.write_bytes(लगत)
        항목들.append(नाम + '=' + str(फाइल))
    subprocess.run([sys.executable, str(स्थिति / 'उपकरणहरू/묶기.py'), '-o', str(डाइरेक्टरी_मान / 'apps.bin')] + 항목들, check=True)
    स्रोत = डाइरेक्टरी_मान / 'apps.s'
    स्रोत.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(डाइरेक्टरी_मान / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(डाइरेक्टरी_मान / 'apps.o'), str(स्रोत)], check=True)
    कर्णेल_मान = डाइरेक्टरी_मान / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थिति / '부팅/लिङ्क_लेआउट.ld'), '-o', str(कर्णेल_मान),
                    str(स्थिति / 'build/boot.o'), str(स्थिति / 'build/java.o'), str(स्थिति / 'build/user.o'), str(डाइरेक्टरी_मान / 'apps.o')], check=True)
    return कर्णेल_मान


def कार्यान्वयन_गर्नुहोस्_आदेश():
    मापन = {}
    सर्भर_मान = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    सर्भर_मान.bind(('127.0.0.1', 0))
    सर्भर_मान.settimeout(0.1)
    पोर्ट_मान = सर्भर_मान.getsockname()[1]
    받은것 = []
    बाहिर_जानुहोस्_अनुप्रयोग = threading.Event()
    def 되보내기():
        while not बाहिर_जानुहोस्_अनुप्रयोग.is_set():
            try: लगत, समान_मान = सर्भर_मान.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(लगत)
            if लगत != b'drop-me': सर्भर_मान.sendto(लगत, समान_मान)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            मेशिन = अवास्तविक_मेशिन(स्थिति / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                मेशिन.आदेश('apps', ['hello', 'udp', 'netcheck', 'stress'])
                मेशिन.आदेश('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                मेशिन.आदेश('run missing', ['Exit: -2'])
                मेशिन.आदेश('net', ['NET RTL8139'])
                मेशिन.आदेश('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for सामग्री_मान in ('hello-network', 'odd', 'even', 'repeat-123'):
                    मेशिन.आदेश('run udp 10.0.2.2 {} {}'.format(पोर्ट_मान, सामग्री_मान), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert सामग्री_मान.encode() in 받은것, 'होस्ट 서버에서 자료를 받지 못함'
                मेशिन.आदेश('run stress {}'.format(पोर्ट_मान), ['UDP STRESS PASS', 'Exit: 0'])
                मेशिन.आदेश('run udp 10.0.2.2 {} drop-me'.format(पोर्ट_मान), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                मेशिन.आदेश('run hello recovered', ['arg: recovered', 'Exit: 0'])
                मापन[종류] = मेशिन.लग_रेकर्ड.decode('utf-8', 'replace')
                print('PASS: {} प्रयोगकर्ता ELF/ring 3/तर्क/UDP होस्ट 왕복/시간 초과/शेल 복귀'.format(종류), flush=True)
            finally:
                try: मेशिन.आदेश('net', [])
                except Exception: pass
                (स्थिति / 'build/사용자통신-last.log').write_bytes(मेशिन.लग_रेकर्ड)
                मेशिन.बन्दगर्नुहोस्()
        मेशिन = अवास्तविक_मेशिन(स्थिति / 'build/kernel.elf', सञ्जाल_मान=False)
        try:
            मेशिन.आदेश('net', ['NET unavailable'])
            मेशिन.आदेश('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            मेशिन.आदेश('run hello', ['USER MODE ring 3', 'Exit: 0'])
            मापन['no_nic'] = मेशिन.लग_रेकर्ड.decode()
        finally: मेशिन.बन्दगर्नुहोस्()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            मेशिन = अवास्तविक_मेशिन(보호커널(Path(임시)), सञ्जाल_मान=False)
            try:
                for नाम, स्थिति_मान in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    मेशिन.आदेश('run ' + नाम, ['Exit: ' + str(स्थिति_मान)])
                    मेशिन.आदेश('run hello', ['USER MODE ring 3', 'Exit: 0'])
                मापन['protection'] = मेशिन.लग_रेकर्ड.decode()
                print('PASS: प्रयोगकर्ता मेमोरी_लगत/हार्डवेयर_पोर्ट 격리, 잘못된 पोइन्टर/ELF, CPU 예외, 무한 दोहर्_याउनु_मान 제한', flush=True)
            finally:
                (स्थिति / 'build/보호시험-last.log').write_bytes(मेशिन.लग_रेकर्ड)
                मेशिन.बन्दगर्नुहोस्()
    finally:
        बाहिर_जानुहोस्_अनुप्रयोग.set()
        일꾼.join(timeout=2)
        सर्भर_मान.close()
    मापन['host_udp_received'] = [{'length': len(लगत), 'sha256': hashlib.sha256(लगत).hexdigest()} for लगत in 받은것]
    (स्थिति / 'build/사용자통신시험.json').write_text(json.dumps(मापन, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    कार्यान्वयन_गर्नुहोस्_आदेश()
