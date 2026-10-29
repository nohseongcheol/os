#!/usr/bin/env python3
"""प्रत्यक्ष_डेटा ring 3 ELF/येजमान UDP 왕복/राखचें_मोल चूक/TIME_मोल 제한/잘못된 ELF를 검증한다."""
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

स्थिती = Path(__file__).resolve().parents[1]


class भ्रामक_यंत्र:
    def __init__(self, पाथ, 종류='elf', नॅटवर्क_मोल=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        नामावळ_मोल = Path(self.임시.name)
        self.LOG_नोंद = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.मॉनिटर_मोल = socket.socket(socket.AF_UNIX)
        직렬경로, मॉनिटर_पाथ = नामावळ_मोल / 'serial.sock', नामावळ_मोल / 'monitor.sock'
        आदेश = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(मॉनिटर_पाथ) + ',server,nowait']
        आदेश += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if नॅटवर्क_मोल else ['-net', 'none']
        आदेश += ['-kernel', str(पाथ)] if 종류 == 'elf' else ['-cdrom', str(पाथ), '-boot', 'd']
        if 저장매체 is not None:
            आदेश += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.प्रक्रिया_मोल = subprocess.Popen(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and मॉनिटर_पाथ.exists()):
                if self.प्रक्रिया_मोल.poll() is not None:
                    raise AssertionError(self.प्रक्रिया_मोल.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU चलोवप TIME_मोल 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.मॉनिटर_मोल.connect(str(मॉनिटर_पाथ))
            self.직렬.setblocking(False)
            self.मॉनिटर_मोल.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.शेवट()
            raise

    def 기다림(self, 문구, चलोवप=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_नोंद[चलोवप:]:
                return self.LOG_नोंद[चलोवप:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                डेटा = self.직렬.recv(65536)
                if not डेटा: break
                self.LOG_नोंद.extend(डेटा)
            if self.प्रक्रिया_मोल.poll() is not None: break
        raise AssertionError('대기 अपेस_मोल: ' + 문구 + '\n' + self.LOG_नोंद.decode('utf-8', 'replace'))

    def आदेश(self, स्ट्रिंग_मोल, 기대):
        चलोवप = len(self.LOG_नोंद)
        self.직렬.sendall((स्ट्रिंग_मोल + '\n').encode())
        मेजप = self.기다림('jkoros> ', चलोवप)
        for 문구 in 기대:
            assert 문구 in मेजप, (स्ट्रिंग_मोल, 문구, मेजप)
        assert 'PANIC' not in मेजप, मेजप
        return मेजप

    def शेवट(self):
        self.직렬.close()
        self.मॉनिटर_मोल.close()
        if self.प्रक्रिया_मोल.poll() is None:
            self.प्रक्रिया_मोल.terminate()
            try: self.प्रक्रिया_मोल.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.प्रक्रिया_मोल.kill()
                self.प्रक्रिया_मोल.wait()
        self.प्रक्रिया_मोल.communicate()
        self.임시.cleanup()


def 보호커널(नामावळ_मोल):
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
    항목들 = ['hello=' + str(स्थिती / 'build/apps/hello.elf')]
    for नांव, अनुक्रमणिका_मोल in 사례들.items():
        स्त्रोत = नामावळ_मोल / (नांव + '.s')
        स्त्रोत.write_text('.code32\n.text\n.globl _start\n_start:\n' + अनुक्रमणिका_मोल +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(नामावळ_मोल / (नांव + '.o')), str(स्त्रोत)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थिती.parent / 'compiler/उपेगकर्तो_लिंक_रचणाय.ld'),
                        '-o', str(नामावळ_मोल / (नांव + '.elf')), str(नामावळ_मोल / (नांव + '.o'))], check=True)
        항목들.append(नांव + '=' + str(नामावळ_मोल / (नांव + '.elf')))
    정상 = bytearray((स्थिती / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    अवैध_मेजप = bytearray(정상); अवैध_मेजप[0] = 0; 변형들['badelf'] = अवैध_मेजप
    अवैध_मेजप = bytearray(정상); struct.pack_into('<I', अवैध_मेजप, 24, 0x00100000); 변형들['badentry'] = अवैध_मेजप
    अवैध_मेजप = bytearray(정상); struct.pack_into('<I', अवैध_मेजप, 28, 0x7fffffff); 변형들['badtable'] = अवैध_मेजप
    अवैध_मेजप = bytearray(정상); लूकअप_तकटो = struct.unpack_from('<I', अवैध_मेजप, 28)[0]
    struct.pack_into('<I', अवैध_मेजप, लूकअप_तकटो + 20, 0x7fffffff); 변형들['badsize'] = अवैध_मेजप
    for नांव, डेटा in 변형들.items():
        फायल = नामावळ_मोल / (नांव + '.elf'); फायल.write_bytes(डेटा)
        항목들.append(नांव + '=' + str(फायल))
    subprocess.run([sys.executable, str(स्थिती / 'साधनां/묶기.py'), '-o', str(नामावळ_मोल / 'apps.bin')] + 항목들, check=True)
    स्त्रोत = नामावळ_मोल / 'apps.s'
    स्त्रोत.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(नामावळ_मोल / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(नामावळ_मोल / 'apps.o'), str(स्त्रोत)], check=True)
    कर्नेल_मोल = नामावळ_मोल / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(स्थिती / '부팅/लिंक_रचणाय.ld'), '-o', str(कर्नेल_मोल),
                    str(स्थिती / 'build/boot.o'), str(स्थिती / 'build/java.o'), str(स्थिती / 'build/user.o'), str(नामावळ_मोल / 'apps.o')], check=True)
    return कर्नेल_मोल


def पाळो_दिवचो_आदेश():
    मेजप = {}
    सर्वर_मोल = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    सर्वर_मोल.bind(('127.0.0.1', 0))
    सर्वर_मोल.settimeout(0.1)
    पोर्ट_मोल = सर्वर_मोल.getsockname()[1]
    RECEIVED_आयटम = []
    प्रस्थान_करचें_एप्लिकेशन = threading.Event()
    def 되보내기():
        while not प्रस्थान_करचें_एप्लिकेशन.is_set():
            try: डेटा, पीयर_मोल = सर्वर_मोल.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_आयटम.append(डेटा)
            if डेटा != b'drop-me': सर्वर_मोल.sendto(डेटा, पीयर_मोल)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            यंत्र = भ्रामक_यंत्र(स्थिती / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                यंत्र.आदेश('apps', ['hello', 'udp', 'netcheck', 'stress'])
                यंत्र.आदेश('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                यंत्र.आदेश('run missing', ['Exit: -2'])
                यंत्र.आदेश('net', ['NET RTL8139'])
                यंत्र.आदेश('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for अनुक्रमणिका_मोल in ('hello-network', 'odd', 'even', 'repeat-123'):
                    यंत्र.आदेश('run udp 10.0.2.2 {} {}'.format(पोर्ट_मोल, अनुक्रमणिका_मोल), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert अनुक्रमणिका_मोल.encode() in RECEIVED_आयटम, 'येजमान 서버에서 자료를 받지 못함'
                यंत्र.आदेश('run stress {}'.format(पोर्ट_मोल), ['UDP STRESS PASS', 'Exit: 0'])
                यंत्र.आदेश('run udp 10.0.2.2 {} drop-me'.format(पोर्ट_मोल), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                यंत्र.आदेश('run hello recovered', ['arg: recovered', 'Exit: 0'])
                मेजप[종류] = यंत्र.LOG_नोंद.decode('utf-8', 'replace')
                print('PASS: {} उपेगकर्तो ELF/ring 3/인수/UDP येजमान 왕복/TIME_मोल 초과/शॅल 복귀'.format(종류), flush=True)
            finally:
                try: यंत्र.आदेश('net', [])
                except Exception: pass
                (स्थिती / 'build/사용자통신-last.log').write_bytes(यंत्र.LOG_नोंद)
                यंत्र.शेवट()
        यंत्र = भ्रामक_यंत्र(स्थिती / 'build/kernel.elf', नॅटवर्क_मोल=False)
        try:
            यंत्र.आदेश('net', ['NET unavailable'])
            यंत्र.आदेश('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            यंत्र.आदेश('run hello', ['USER MODE ring 3', 'Exit: 0'])
            मेजप['no_nic'] = यंत्र.LOG_नोंद.decode()
        finally: यंत्र.शेवट()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            यंत्र = भ्रामक_यंत्र(보호커널(Path(임시)), नॅटवर्क_मोल=False)
            try:
                for नांव, स्थिती_मोल_e10195a1 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    यंत्र.आदेश('run ' + नांव, ['Exit: ' + str(स्थिती_मोल_e10195a1)])
                    यंत्र.आदेश('run hello', ['USER MODE ring 3', 'Exit: 0'])
                मेजप['protection'] = यंत्र.LOG_नोंद.decode()
                print('PASS: उपेगकर्तो मेमरी_डेटा/हार्डवॅर_पोर्ट 격리, 잘못된 पॉयंटर/ELF, CPU 예외, 무한 परतवण_मोल 제한', flush=True)
            finally:
                (स्थिती / 'build/보호시험-last.log').write_bytes(यंत्र.LOG_नोंद)
                यंत्र.शेवट()
    finally:
        प्रस्थान_करचें_एप्लिकेशन.set()
        일꾼.join(timeout=2)
        सर्वर_मोल.close()
    मेजप['host_udp_received'] = [{'length': len(डेटा), 'sha256': hashlib.sha256(डेटा).hexdigest()} for डेटा in RECEIVED_आयटम]
    (स्थिती / 'build/사용자통신시험.json').write_text(json.dumps(मेजप, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    पाळो_दिवचो_आदेश()
