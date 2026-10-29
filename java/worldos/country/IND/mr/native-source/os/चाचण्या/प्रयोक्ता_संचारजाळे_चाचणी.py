#!/usr/bin/env python3
"""वास्तविक_डेटा ring 3 ELF/होस्ट UDP 왕복/संरक्षण_मूल्य त्रुटी/वेळ_मूल्य मर्यादा_मूल्य/잘못된 ELF를 검증한다."""
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

जागा = Path(__file__).resolve().parents[1]


class व्हर्च्युअल_मशीन:
    def __init__(self, मार्ग, प्रकार_मूल्य='elf', संचारजाळे_मूल्य=True, संग्रह_माध्यम=None):
        self.तात्पुरते_मूल्य = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        निर्देशिका_मूल्य = Path(self.तात्पुरते_मूल्य.name)
        self.लॉग_नोंद = bytearray()
        self.अनुक्रमिक_मूल्य = socket.socket(socket.AF_UNIX)
        self.मॉनिटर_मूल्य = socket.socket(socket.AF_UNIX)
        अनुक्रमिक_पथ, मॉनिटर_पथ = निर्देशिका_मूल्य / 'serial.sock', निर्देशिका_मूल्य / 'monitor.sock'
        आदेश = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(अनुक्रमिक_पथ) + ',server,nowait',
                '-monitor', 'unix:' + str(मॉनिटर_पथ) + ',server,nowait']
        आदेश += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if संचारजाळे_मूल्य else ['-net', 'none']
        आदेश += ['-kernel', str(मार्ग)] if प्रकार_मूल्य == 'elf' else ['-cdrom', str(मार्ग), '-boot', 'd']
        if संग्रह_माध्यम is not None:
            आदेश += ['-drive', 'file=' + str(संग्रह_माध्यम) + ',format=raw,if=ide,index=0']
        self.प्रक्रिया_मूल्य = subprocess.Popen(आदेश, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            शेवट = time.monotonic() + 10
            while not (अनुक्रमिक_पथ.exists() and मॉनिटर_पथ.exists()):
                if self.प्रक्रिया_मूल्य.poll() is not None:
                    raise AssertionError(self.प्रक्रिया_मूल्य.stderr.read().decode())
                if time.monotonic() > शेवट: raise AssertionError('QEMU सुरू_करा वेळ_मूल्य 초과')
                time.sleep(0.03)
            self.अनुक्रमिक_मूल्य.connect(str(अनुक्रमिक_पथ))
            self.मॉनिटर_मूल्य.connect(str(मॉनिटर_पथ))
            self.अनुक्रमिक_मूल्य.setblocking(False)
            self.मॉनिटर_मूल्य.sendall(b'cont\n')
            self.प्रतीक्षा_करा_राज्य('jkoros> ')
        except BaseException:
            self.बंद_करा()
            raise

    def प्रतीक्षा_करा_राज्य(self, शब्दसमूह_मूल्य, सुरू_करा=0, मर्यादा_मूल्य=15):
        शेवट = time.monotonic() + मर्यादा_मूल्य
        while time.monotonic() < शेवट:
            if शब्दसमूह_मूल्य.encode() in self.लॉग_नोंद[सुरू_करा:]:
                return self.लॉग_नोंद[सुरू_करा:].decode('utf-8', 'replace')
            वाचन, _, _ = select.select([self.अनुक्रमिक_मूल्य], [], [], 0.1)
            if वाचन:
                डेटा = self.अनुक्रमिक_मूल्य.recv(65536)
                if not डेटा: break
                self.लॉग_नोंद.extend(डेटा)
            if self.प्रक्रिया_मूल्य.poll() is not None: break
        raise AssertionError('प्रतीक्षा_करा_मूल्य बिघाड_मूल्य: ' + शब्दसमूह_मूल्य + '\n' + self.लॉग_नोंद.decode('utf-8', 'replace'))

    def आदेश(self, स्ट्रींग_मूल्य, अपेक्षा):
        सुरू_करा = len(self.लॉग_नोंद)
        self.अनुक्रमिक_मूल्य.sendall((स्ट्रींग_मूल्य + '\n').encode())
        मोजमाप = self.प्रतीक्षा_करा_राज्य('jkoros> ', सुरू_करा)
        for शब्दसमूह_मूल्य in अपेक्षा:
            assert शब्दसमूह_मूल्य in मोजमाप, (स्ट्रींग_मूल्य, शब्दसमूह_मूल्य, मोजमाप)
        assert 'PANIC' not in मोजमाप, मोजमाप
        return मोजमाप

    def बंद_करा(self):
        self.अनुक्रमिक_मूल्य.close()
        self.मॉनिटर_मूल्य.close()
        if self.प्रक्रिया_मूल्य.poll() is None:
            self.प्रक्रिया_मूल्य.terminate()
            try: self.प्रक्रिया_मूल्य.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.प्रक्रिया_मूल्य.kill()
                self.प्रक्रिया_मूल्य.wait()
        self.प्रक्रिया_मूल्य.communicate()
        self.तात्पुरते_मूल्य.cleanup()


def संरक्षित_गाभा(निर्देशिका_मूल्य):
    प्रकरणे_यादी = {
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
    नोंदी_यादी = ['hello=' + str(जागा / 'build/apps/hello.elf')]
    for नाव, सामुग्री_मूल्य in प्रकरणे_यादी.items():
        स्रोत = निर्देशिका_मूल्य / (नाव + '.s')
        स्रोत.write_text('.code32\n.text\n.globl _start\n_start:\n' + सामुग्री_मूल्य +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(निर्देशिका_मूल्य / (नाव + '.o')), str(स्रोत)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(जागा.parent / 'compiler/प्रयोक्ता_लिंक_लेआउट.ld'),
                        '-o', str(निर्देशिका_मूल्य / (नाव + '.elf')), str(निर्देशिका_मूल्य / (नाव + '.o'))], check=True)
        नोंदी_यादी.append(नाव + '=' + str(निर्देशिका_मूल्य / (नाव + '.elf')))
    आहे_सामान्य = bytearray((जागा / 'build/apps/hello.elf').read_bytes())
    प्रकारांतरे_यादी = {}
    अवैध_मोजमाप = bytearray(आहे_सामान्य); अवैध_मोजमाप[0] = 0; प्रकारांतरे_यादी['badelf'] = अवैध_मोजमाप
    अवैध_मोजमाप = bytearray(आहे_सामान्य); struct.pack_into('<I', अवैध_मोजमाप, 24, 0x00100000); प्रकारांतरे_यादी['badentry'] = अवैध_मोजमाप
    अवैध_मोजमाप = bytearray(आहे_सामान्य); struct.pack_into('<I', अवैध_मोजमाप, 28, 0x7fffffff); प्रकारांतरे_यादी['badtable'] = अवैध_मोजमाप
    अवैध_मोजमाप = bytearray(आहे_सामान्य); लुकअप_सारणी = struct.unpack_from('<I', अवैध_मोजमाप, 28)[0]
    struct.pack_into('<I', अवैध_मोजमाप, लुकअप_सारणी + 20, 0x7fffffff); प्रकारांतरे_यादी['badsize'] = अवैध_मोजमाप
    for नाव, डेटा in प्रकारांतरे_यादी.items():
        फाइल = निर्देशिका_मूल्य / (नाव + '.elf'); फाइल.write_bytes(डेटा)
        नोंदी_यादी.append(नाव + '=' + str(फाइल))
    subprocess.run([sys.executable, str(जागा / 'साधने/बाइंड_करा_संचारटोक.py'), '-o', str(निर्देशिका_मूल्य / 'apps.bin')] + नोंदी_यादी, check=True)
    स्रोत = निर्देशिका_मूल्य / 'apps.s'
    स्रोत.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(निर्देशिका_मूल्य / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(निर्देशिका_मूल्य / 'apps.o'), str(स्रोत)], check=True)
    गाभा_मूल्य = निर्देशिका_मूल्य / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(जागा / 'प्रणालीप्रारंभ/लिंक_लेआउट.ld'), '-o', str(गाभा_मूल्य),
                    str(जागा / 'build/boot.o'), str(जागा / 'build/java.o'), str(जागा / 'build/user.o'), str(निर्देशिका_मूल्य / 'apps.o')], check=True)
    return गाभा_मूल्य


def आज्ञा_कार्यवाही_करा():
    मोजमाप = {}
    सर्व्हर_मूल्य = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    सर्व्हर_मूल्य.bind(('127.0.0.1', 0))
    सर्व्हर_मूल्य.settimeout(0.1)
    पॉर्ट_मूल्य = सर्व्हर_मूल्य.getsockname()[1]
    स्वीकारलेले_आयटम = []
    निर्गमन_करा_अनुप्रयोग = threading.Event()
    def प्रतिध्वनी_प्रत्युत्तर_द्या():
        while not निर्गमन_करा_अनुप्रयोग.is_set():
            try: डेटा, समकक्ष_मूल्य = सर्व्हर_मूल्य.recvfrom(4096)
            except socket.timeout: continue
            स्वीकारलेले_आयटम.append(डेटा)
            if डेटा != b'drop-me': सर्व्हर_मूल्य.sendto(डेटा, समकक्ष_मूल्य)
    कार्यसूत्र_मूल्य = threading.Thread(target=प्रतिध्वनी_प्रत्युत्तर_द्या, daemon=True)
    कार्यसूत्र_मूल्य.start()
    try:
        for प्रकार_मूल्य in ('elf', 'iso'):
            मशीन = व्हर्च्युअल_मशीन(जागा / ('build/kernel.elf' if प्रकार_मूल्य == 'elf' else 'build/kernel.iso'), प्रकार_मूल्य)
            try:
                मशीन.आदेश('apps', ['hello', 'udp', 'netcheck', 'stress'])
                मशीन.आदेश('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                मशीन.आदेश('run missing', ['Exit: -2'])
                मशीन.आदेश('net', ['NET RTL8139'])
                मशीन.आदेश('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for सामुग्री_मूल्य in ('hello-network', 'odd', 'even', 'repeat-123'):
                    मशीन.आदेश('run udp 10.0.2.2 {} {}'.format(पॉर्ट_मूल्य, सामुग्री_मूल्य), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert सामुग्री_मूल्य.encode() in स्वीकारलेले_आयटम, 'होस्ट 서버에서 자료를 받지 못함'
                मशीन.आदेश('run stress {}'.format(पॉर्ट_मूल्य), ['UDP STRESS PASS', 'Exit: 0'])
                मशीन.आदेश('run udp 10.0.2.2 {} drop-me'.format(पॉर्ट_मूल्य), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                मशीन.आदेश('run hello recovered', ['arg: recovered', 'Exit: 0'])
                मोजमाप[प्रकार_मूल्य] = मशीन.लॉग_नोंद.decode('utf-8', 'replace')
                print('PASS: {} प्रयोक्ता ELF/ring 3/बाबी/UDP होस्ट 왕복/वेळ_मूल्य 초과/शेल 복귀'.format(प्रकार_मूल्य), flush=True)
            finally:
                try: मशीन.आदेश('net', [])
                except Exception: pass
                (जागा / 'build/사용자통신-last.log').write_bytes(मशीन.लॉग_नोंद)
                मशीन.बंद_करा()
        मशीन = व्हर्च्युअल_मशीन(जागा / 'build/kernel.elf', संचारजाळे_मूल्य=False)
        try:
            मशीन.आदेश('net', ['NET unavailable'])
            मशीन.आदेश('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            मशीन.आदेश('run hello', ['USER MODE ring 3', 'Exit: 0'])
            मोजमाप['no_nic'] = मशीन.लॉग_नोंद.decode()
        finally: मशीन.बंद_करा()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as तात्पुरते_मूल्य:
            मशीन = व्हर्च्युअल_मशीन(संरक्षित_गाभा(Path(तात्पुरते_मूल्य)), संचारजाळे_मूल्य=False)
            try:
                for नाव, राज्य_मूल्य in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    मशीन.आदेश('run ' + नाव, ['Exit: ' + str(राज्य_मूल्य)])
                    मशीन.आदेश('run hello', ['USER MODE ring 3', 'Exit: 0'])
                मोजमाप['protection'] = मशीन.लॉग_नोंद.decode()
                print('PASS: प्रयोक्ता स्मृती_डेटा/हार्डवेअर_पॉर्ट 격리, 잘못된 निर्देशक/ELF, CPU अपवाद, 무한 पुनरावृत्ती_मूल्य मर्यादा_मूल्य', flush=True)
            finally:
                (जागा / 'build/संरक्षण_चाचणी-last.log').write_bytes(मशीन.लॉग_नोंद)
                मशीन.बंद_करा()
    finally:
        निर्गमन_करा_अनुप्रयोग.set()
        कार्यसूत्र_मूल्य.join(timeout=2)
        सर्व्हर_मूल्य.close()
    मोजमाप['host_udp_received'] = [{'length': len(डेटा), 'sha256': hashlib.sha256(डेटा).hexdigest()} for डेटा in स्वीकारलेले_आयटम]
    (जागा / 'build/प्रयोक्ता_संचारजाळे_चाचणी.json').write_text(json.dumps(मोजमाप, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    आज्ञा_कार्यवाही_करा()
