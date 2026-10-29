#!/usr/bin/env python3
"""वास्तविक_डेटा ring 3 ELF/आयोजक UDP 왕복/रक्षित_करें_मान त्रुटि/समय_उपयोगिता 제한/잘못된 ELF를 검증한다."""
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

स्थान = Path(__file__).resolve().parents[1]


class वर्चुअल_मशीन:
    def __init__(self, पथ, 종류='elf', नेटवर्क_मान=True, संग्रहण_मध्यम=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        डायरेक्टरी_मान = Path(self.임시.name)
        self.लॉग_रिकॉर्ड = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.मॉनीटर_मान = socket.socket(socket.AF_UNIX)
        직렬경로, मॉनीटर_पथ = डायरेक्टरी_मान / 'serial.sock', डायरेक्टरी_मान / 'monitor.sock'
        आदेश = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(मॉनीटर_पथ) + ',server,nowait']
        आदेश += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if नेटवर्क_मान else ['-net', 'none']
        आदेश += ['-kernel', str(पथ)] if 종류 == 'elf' else ['-cdrom', str(पथ), '-boot', 'd']
        if संग्रहण_मध्यम is not None:
            आदेश += ['-drive', 'file=' + str(संग्रहण_मध्यम) + ',format=raw,if=ide,index=0']
        self.प्रक्रिया_मान = subprocess.Popen(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and मॉनीटर_पथ.exists()):
                if self.प्रक्रिया_मान.poll() is not None:
                    raise AssertionError(self.प्रक्रिया_मान.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU चलाएँ समय_उपयोगिता 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.मॉनीटर_मान.connect(str(मॉनीटर_पथ))
            self.직렬.setblocking(False)
            self.मॉनीटर_मान.sendall(b'cont\n')
            self.प्रतीक्षा_स्थिति('jkoros> ')
        except BaseException:
            self.बंदकरें()
            raise

    def प्रतीक्षा_स्थिति(self, 문구, चलाएँ=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.लॉग_रिकॉर्ड[चलाएँ:]:
                return self.लॉग_रिकॉर्ड[चलाएँ:].decode('utf-8', 'replace')
            पढ़ें, _, _ = select.select([self.직렬], [], [], 0.1)
            if पढ़ें:
                आँकड़े = self.직렬.recv(65536)
                if not आँकड़े: break
                self.लॉग_रिकॉर्ड.extend(आँकड़े)
            if self.प्रक्रिया_मान.poll() is not None: break
        raise AssertionError('प्रतीक्षा_करें_मान विफलता_मान: ' + 문구 + '\n' + self.लॉग_रिकॉर्ड.decode('utf-8', 'replace'))

    def आदेश(self, स्ट्रिंग_मान, 기대):
        चलाएँ = len(self.लॉग_रिकॉर्ड)
        self.직렬.sendall((स्ट्रिंग_मान + '\n').encode())
        परिणाम = self.प्रतीक्षा_स्थिति('jkoros> ', चलाएँ)
        for 문구 in 기대:
            assert 문구 in परिणाम, (स्ट्रिंग_मान, 문구, परिणाम)
        assert 'PANIC' not in परिणाम, परिणाम
        return परिणाम

    def बंदकरें(self):
        self.직렬.close()
        self.मॉनीटर_मान.close()
        if self.प्रक्रिया_मान.poll() is None:
            self.प्रक्रिया_मान.terminate()
            try: self.प्रक्रिया_मान.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.प्रक्रिया_मान.kill()
                self.प्रक्रिया_मान.wait()
        self.प्रक्रिया_मान.communicate()
        self.임시.cleanup()


def 보호커널(डायरेक्टरी_मान):
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
    항목들 = ['hello=' + str(स्थान / 'build/apps/hello.elf')]
    for नाम, सामग्री_मान in 사례들.items():
        स्रोत = डायरेक्टरी_मान / (नाम + '.s')
        स्रोत.write_text('.code32\n.text\n.globl _start\n_start:\n' + सामग्री_मान +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(डायरेक्टरी_मान / (नाम + '.o')), str(स्रोत)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थान.parent / 'compiler/उपयोगकर्ता_लिंक_लेआउट.ld'),
                        '-o', str(डायरेक्टरी_मान / (नाम + '.elf')), str(डायरेक्टरी_मान / (नाम + '.o'))], check=True)
        항목들.append(नाम + '=' + str(डायरेक्टरी_मान / (नाम + '.elf')))
    정상 = bytearray((स्थान / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    अमान्य_परिणाम = bytearray(정상); अमान्य_परिणाम[0] = 0; 변형들['badelf'] = अमान्य_परिणाम
    अमान्य_परिणाम = bytearray(정상); struct.pack_into('<I', अमान्य_परिणाम, 24, 0x00100000); 변형들['badentry'] = अमान्य_परिणाम
    अमान्य_परिणाम = bytearray(정상); struct.pack_into('<I', अमान्य_परिणाम, 28, 0x7fffffff); 변형들['badtable'] = अमान्य_परिणाम
    अमान्य_परिणाम = bytearray(정상); लुकअप_तालिका = struct.unpack_from('<I', अमान्य_परिणाम, 28)[0]
    struct.pack_into('<I', अमान्य_परिणाम, लुकअप_तालिका + 20, 0x7fffffff); 변형들['badsize'] = अमान्य_परिणाम
    for नाम, आँकड़े in 변형들.items():
        संचिका = डायरेक्टरी_मान / (नाम + '.elf'); संचिका.write_bytes(आँकड़े)
        항목들.append(नाम + '=' + str(संचिका))
    subprocess.run([sys.executable, str(स्थान / 'उपकरण/बाइंड_करें_एंडपॉइंट.py'), '-o', str(डायरेक्टरी_मान / 'apps.bin')] + 항목들, check=True)
    स्रोत = डायरेक्टरी_मान / 'apps.s'
    स्रोत.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(डायरेक्टरी_मान / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(डायरेक्टरी_मान / 'apps.o'), str(स्रोत)], check=True)
    कर्नेल_मान = डायरेक्टरी_मान / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थान / '부팅/लिंक_लेआउट.ld'), '-o', str(कर्नेल_मान),
                    str(स्थान / 'build/boot.o'), str(स्थान / 'build/java.o'), str(स्थान / 'build/user.o'), str(डायरेक्टरी_मान / 'apps.o')], check=True)
    return कर्नेल_मान


def निष्पादित_करें_आदेश():
    परिणाम = {}
    서버 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    서버.bind(('127.0.0.1', 0))
    서버.settimeout(0.1)
    पोर्ट_मान = 서버.getsockname()[1]
    받은것 = []
    निर्गमन_ऐप = threading.Event()
    def प्रतिध्वनि_उत्तर():
        while not निर्गमन_ऐप.is_set():
            try: आँकड़े, पीअर_मान = 서버.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(आँकड़े)
            if आँकड़े != b'drop-me': 서버.sendto(आँकड़े, पीअर_मान)
    일꾼 = threading.Thread(target=प्रतिध्वनि_उत्तर, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            यंत्र = वर्चुअल_मशीन(स्थान / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                यंत्र.आदेश('apps', ['hello', 'udp', 'netcheck', 'stress'])
                यंत्र.आदेश('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                यंत्र.आदेश('run missing', ['Exit: -2'])
                यंत्र.आदेश('net', ['NET RTL8139'])
                यंत्र.आदेश('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for सामग्री_मान in ('hello-network', 'odd', 'even', 'repeat-123'):
                    यंत्र.आदेश('run udp 10.0.2.2 {} {}'.format(पोर्ट_मान, सामग्री_मान), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert सामग्री_मान.encode() in 받은것, 'आयोजक 서버에서 자료를 받지 못함'
                यंत्र.आदेश('run stress {}'.format(पोर्ट_मान), ['UDP STRESS PASS', 'Exit: 0'])
                यंत्र.आदेश('run udp 10.0.2.2 {} drop-me'.format(पोर्ट_मान), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                यंत्र.आदेश('run hello recovered', ['arg: recovered', 'Exit: 0'])
                परिणाम[종류] = यंत्र.लॉग_रिकॉर्ड.decode('utf-8', 'replace')
                print('PASS: {} उपयोगकर्ता ELF/ring 3/तर्क/UDP आयोजक 왕복/समय_उपयोगिता 초과/शेल 복귀'.format(종류), flush=True)
            finally:
                try: यंत्र.आदेश('net', [])
                except Exception: pass
                (स्थान / 'build/사용자통신-last.log').write_bytes(यंत्र.लॉग_रिकॉर्ड)
                यंत्र.बंदकरें()
        यंत्र = वर्चुअल_मशीन(स्थान / 'build/kernel.elf', नेटवर्क_मान=False)
        try:
            यंत्र.आदेश('net', ['NET unavailable'])
            यंत्र.आदेश('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            यंत्र.आदेश('run hello', ['USER MODE ring 3', 'Exit: 0'])
            परिणाम['no_nic'] = यंत्र.लॉग_रिकॉर्ड.decode()
        finally: यंत्र.बंदकरें()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            यंत्र = वर्चुअल_मशीन(보호커널(Path(임시)), नेटवर्क_मान=False)
            try:
                for नाम, अवस्था_मान in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    यंत्र.आदेश('run ' + नाम, ['Exit: ' + str(अवस्था_मान)])
                    यंत्र.आदेश('run hello', ['USER MODE ring 3', 'Exit: 0'])
                परिणाम['protection'] = यंत्र.लॉग_रिकॉर्ड.decode()
                print('PASS: उपयोगकर्ता मेमोरी_डेटा/포트 격리, 잘못된 सूचक/ELF, CPU अपवाद, 무한 पुनरावृति_मान 제한', flush=True)
            finally:
                (स्थान / 'build/보호시험-last.log').write_bytes(यंत्र.लॉग_रिकॉर्ड)
                यंत्र.बंदकरें()
    finally:
        निर्गमन_ऐप.set()
        일꾼.join(timeout=2)
        서버.close()
    परिणाम['host_udp_received'] = [{'length': len(आँकड़े), 'sha256': hashlib.sha256(आँकड़े).hexdigest()} for आँकड़े in 받은것]
    (स्थान / 'build/사용자통신시험.json').write_text(json.dumps(परिणाम, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    निष्पादित_करें_आदेश()
