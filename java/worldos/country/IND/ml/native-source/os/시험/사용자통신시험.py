#!/usr/bin/env python3
"""വാസ്തവമായ_ഡാറ്റാ ring 3 ELF/ഹോസ്റ്റ് UDP 왕복/പരിരക്ഷിക്കുക_മൂല്യം പിശക്/സമയ_മൂല്യം 제한/잘못된 ELF를 검증한다."""
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

സ്ഥാനം = Path(__file__).resolve().parents[1]


class അയഥാര്_ഥ_മെഷീൻ:
    def __init__(self, വഴി, 종류='elf', നെറ്റ്_വർക്ക്_മൂല്യം=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ഡയറക്ടറി_മൂല്യം = Path(self.임시.name)
        self.ലോഗ്_രേഖ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.മോണിട്ടര്_മൂല്യം = socket.socket(socket.AF_UNIX)
        직렬경로, മോണിട്ടര്_പാത = ഡയറക്ടറി_മൂല്യം / 'serial.sock', ഡയറക്ടറി_മൂല്യം / 'monitor.sock'
        ആജ്ഞ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(മോണിട്ടര്_പാത) + ',server,nowait']
        ആജ്ഞ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if നെറ്റ്_വർക്ക്_മൂല്യം else ['-net', 'none']
        ആജ്ഞ += ['-kernel', str(വഴി)] if 종류 == 'elf' else ['-cdrom', str(വഴി), '-boot', 'd']
        if 저장매체 is not None:
            ആജ്ഞ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.പ്രോസസ്_മൂല്യം = subprocess.Popen(ആജ്ഞ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and മോണിട്ടര്_പാത.exists()):
                if self.പ്രോസസ്_മൂല്യം.poll() is not None:
                    raise AssertionError(self.പ്രോസസ്_മൂല്യം.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU നടപ്പിലാക്കുക സമയ_മൂല്യം 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.മോണിട്ടര്_മൂല്യം.connect(str(മോണിട്ടര്_പാത))
            self.직렬.setblocking(False)
            self.മോണിട്ടര്_മൂല്യം.sendall(b'cont\n')
            self.കാക്കുക_അവസ്ഥ('jkoros> ')
        except BaseException:
            self.അടയ്ക്കു()
            raise

    def കാക്കുക_അവസ്ഥ(self, 문구, നടപ്പിലാക്കുക=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ലോഗ്_രേഖ[നടപ്പിലാക്കുക:]:
                return self.ലോഗ്_രേഖ[നടപ്പിലാക്കുക:].decode('utf-8', 'replace')
            വായന, _, _ = select.select([self.직렬], [], [], 0.1)
            if വായന:
                ഡാറ്റാ = self.직렬.recv(65536)
                if not ഡാറ്റാ: break
                self.ലോഗ്_രേഖ.extend(ഡാറ്റാ)
            if self.പ്രോസസ്_മൂല്യം.poll() is not None: break
        raise AssertionError('കാക്കുക_മൂല്യം പരാജയം_മൂല്യം: ' + 문구 + '\n' + self.ലോഗ്_രേഖ.decode('utf-8', 'replace'))

    def ആജ്ഞ(self, സ്ട്രിംഗ്_മൂല്യം, 기대):
        നടപ്പിലാക്കുക = len(self.ലോഗ്_രേഖ)
        self.직렬.sendall((സ്ട്രിംഗ്_മൂല്യം + '\n').encode())
        അളവ് = self.കാക്കുക_അവസ്ഥ('jkoros> ', നടപ്പിലാക്കുക)
        for 문구 in 기대:
            assert 문구 in അളവ്, (സ്ട്രിംഗ്_മൂല്യം, 문구, അളവ്)
        assert 'PANIC' not in അളവ്, അളവ്
        return അളവ്

    def അടയ്ക്കു(self):
        self.직렬.close()
        self.മോണിട്ടര്_മൂല്യം.close()
        if self.പ്രോസസ്_മൂല്യം.poll() is None:
            self.പ്രോസസ്_മൂല്യം.terminate()
            try: self.പ്രോസസ്_മൂല്യം.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.പ്രോസസ്_മൂല്യം.kill()
                self.പ്രോസസ്_മൂല്യം.wait()
        self.പ്രോസസ്_മൂല്യം.communicate()
        self.임시.cleanup()


def 보호커널(ഡയറക്ടറി_മൂല്യം):
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
    항목들 = ['hello=' + str(സ്ഥാനം / 'build/apps/hello.elf')]
    for പേരു്, ഉള്ളടക്കം_മൂല്യം in 사례들.items():
        ഉറവിടം = ഡയറക്ടറി_മൂല്യം / (പേരു് + '.s')
        ഉറവിടം.write_text('.code32\n.text\n.globl _start\n_start:\n' + ഉള്ളടക്കം_മൂല്യം +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ഡയറക്ടറി_മൂല്യം / (പേരു് + '.o')), str(ഉറവിടം)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(സ്ഥാനം.parent / 'compiler/ഉപയോക്താവ്_ലിങ്ക്_ലേഔട്ട്.ld'),
                        '-o', str(ഡയറക്ടറി_മൂല്യം / (പേരു് + '.elf')), str(ഡയറക്ടറി_മൂല്യം / (പേരു് + '.o'))], check=True)
        항목들.append(പേരു് + '=' + str(ഡയറക്ടറി_മൂല്യം / (പേരു് + '.elf')))
    정상 = bytearray((സ്ഥാനം / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    അസാധുവായ_അളവ് = bytearray(정상); അസാധുവായ_അളവ്[0] = 0; 변형들['badelf'] = അസാധുവായ_അളവ്
    അസാധുവായ_അളവ് = bytearray(정상); struct.pack_into('<I', അസാധുവായ_അളവ്, 24, 0x00100000); 변형들['badentry'] = അസാധുവായ_അളവ്
    അസാധുവായ_അളവ് = bytearray(정상); struct.pack_into('<I', അസാധുവായ_അളവ്, 28, 0x7fffffff); 변형들['badtable'] = അസാധുവായ_അളവ്
    അസാധുവായ_അളവ് = bytearray(정상); തിരഞ്ഞു_നോക്കൽ_పట్టిక = struct.unpack_from('<I', അസാധുവായ_അളവ്, 28)[0]
    struct.pack_into('<I', അസാധുവായ_അളവ്, തിരഞ്ഞു_നോക്കൽ_పట్టిక + 20, 0x7fffffff); 변형들['badsize'] = അസാധുവായ_അളവ്
    for പേരു്, ഡാറ്റാ in 변형들.items():
        ഫയല് = ഡയറക്ടറി_മൂല്യം / (പേരു് + '.elf'); ഫയല്.write_bytes(ഡാറ്റാ)
        항목들.append(പേരു് + '=' + str(ഫയല്))
    subprocess.run([sys.executable, str(സ്ഥാനം / 'ഉപകരണങ്ങൾ/బైండ్_చేయి_അവസാനബിന്ദു.py'), '-o', str(ഡയറക്ടറി_മൂല്യം / 'apps.bin')] + 항목들, check=True)
    ഉറവിടം = ഡയറക്ടറി_മൂല്യം / 'apps.s'
    ഉറവിടം.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ഡയറക്ടറി_മൂല്യം / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ഡയറക്ടറി_മൂല്യം / 'apps.o'), str(ഉറവിടം)], check=True)
    കെര്_ണല്_മൂല്യം = ഡയറക്ടറി_മൂല്യം / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(സ്ഥാനം / '부팅/ലിങ്ക്_ലേഔട്ട്.ld'), '-o', str(കെര്_ണല്_മൂല്യം),
                    str(സ്ഥാനം / 'build/boot.o'), str(സ്ഥാനം / 'build/java.o'), str(സ്ഥാനം / 'build/user.o'), str(ഡയറക്ടറി_മൂല്യം / 'apps.o')], check=True)
    return കെര്_ണല്_മൂല്യം


def നടപ്പാക്കുക_കമാന്_ഡ്():
    അളവ് = {}
    സെര്_വര്_മൂല്യം = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    സെര്_വര്_മൂല്യം.bind(('127.0.0.1', 0))
    സെര്_വര്_മൂല്യം.settimeout(0.1)
    പോര്_ട്ട്_മൂല്യം = സെര്_വര്_മൂല്യം.getsockname()[1]
    받은것 = []
    പുറത്തുകടക്കൽ_പ്രോഗ്രാം = threading.Event()
    def 되보내기():
        while not പുറത്തുകടക്കൽ_പ്രോഗ്രാം.is_set():
            try: ഡാറ്റാ, പീര്_മൂല്യം = സെര്_വര്_മൂല്യം.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ഡാറ്റാ)
            if ഡാറ്റാ != b'drop-me': സെര്_വര്_മൂല്യം.sendto(ഡാറ്റാ, പീര്_മൂല്യം)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                മെഷീൻ.ആജ്ഞ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                മെഷീൻ.ആജ്ഞ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                മെഷീൻ.ആജ്ഞ('run missing', ['Exit: -2'])
                മെഷീൻ.ആജ്ഞ('net', ['NET RTL8139'])
                മെഷീൻ.ആജ്ഞ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ഉള്ളടക്കം_മൂല്യം in ('hello-network', 'odd', 'even', 'repeat-123'):
                    മെഷീൻ.ആജ്ഞ('run udp 10.0.2.2 {} {}'.format(പോര്_ട്ട്_മൂല്യം, ഉള്ളടക്കം_മൂല്യം), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ഉള്ളടക്കം_മൂല്യം.encode() in 받은것, 'ഹോസ്റ്റ് 서버에서 자료를 받지 못함'
                മെഷീൻ.ആജ്ഞ('run stress {}'.format(പോര്_ട്ട്_മൂല്യം), ['UDP STRESS PASS', 'Exit: 0'])
                മെഷീൻ.ആജ്ഞ('run udp 10.0.2.2 {} drop-me'.format(പോര്_ട്ട്_മൂല്യം), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                മെഷീൻ.ആജ്ഞ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                അളവ്[종류] = മെഷീൻ.ലോഗ്_രേഖ.decode('utf-8', 'replace')
                print('PASS: {} ഉപയോക്താവ് ELF/ring 3/인수/UDP ഹോസ്റ്റ് 왕복/സമയ_മൂല്യം 초과/ഷെല് 복귀'.format(종류), flush=True)
            finally:
                try: മെഷീൻ.ആജ്ഞ('net', [])
                except Exception: pass
                (സ്ഥാനം / 'build/사용자통신-last.log').write_bytes(മെഷീൻ.ലോഗ്_രേഖ)
                മെഷീൻ.അടയ്ക്കു()
        മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(സ്ഥാനം / 'build/kernel.elf', നെറ്റ്_വർക്ക്_മൂല്യം=False)
        try:
            മെഷീൻ.ആജ്ഞ('net', ['NET unavailable'])
            മെഷീൻ.ആജ്ഞ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            മെഷീൻ.ആജ്ഞ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            അളവ്['no_nic'] = മെഷീൻ.ലോഗ്_രേഖ.decode()
        finally: മെഷീൻ.അടയ്ക്കു()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            മെഷീൻ = അയഥാര്_ഥ_മെഷീൻ(보호커널(Path(임시)), നെറ്റ്_വർക്ക്_മൂല്യം=False)
            try:
                for പേരു്, അവസ്ഥ_മൂല്യം in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    മെഷീൻ.ആജ്ഞ('run ' + പേരു്, ['Exit: ' + str(അവസ്ഥ_മൂല്യം)])
                    മെഷീൻ.ആജ്ഞ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                അളവ്['protection'] = മെഷീൻ.ലോഗ്_രേഖ.decode()
                print('PASS: ഉപയോക്താവ് മെമ്മറി_ഡാറ്റാ/포트 격리, 잘못된 പോയിന്_റര്/ELF, CPU ഒഴിവാക്കൽ, 무한 ആവര്_ത്തനം_മൂല്യം 제한', flush=True)
            finally:
                (സ്ഥാനം / 'build/보호시험-last.log').write_bytes(മെഷീൻ.ലോഗ്_രേഖ)
                മെഷീൻ.അടയ്ക്കു()
    finally:
        പുറത്തുകടക്കൽ_പ്രോഗ്രാം.set()
        일꾼.join(timeout=2)
        സെര്_വര്_മൂല്യം.close()
    അളവ്['host_udp_received'] = [{'length': len(ഡാറ്റാ), 'sha256': hashlib.sha256(ഡാറ്റാ).hexdigest()} for ഡാറ്റാ in 받은것]
    (സ്ഥാനം / 'build/사용자통신시험.json').write_text(json.dumps(അളവ്, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    നടപ്പാക്കുക_കമാന്_ഡ്()
