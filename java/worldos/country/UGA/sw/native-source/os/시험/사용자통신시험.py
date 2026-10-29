#!/usr/bin/env python3
"""halisi_data ring 3 ELF/mwenyeji UDP 왕복/linda_thamani kosa/saa_thamani_4692cef5 제한/잘못된 ELF를 검증한다."""
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


class pepe_mashine:
    def __init__(self, njia, 종류='elf', Mtandao_thamani=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Saraka_thamani = Path(self.임시.name)
        self.batli_REKODI = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monita_thamani = socket.socket(socket.AF_UNIX)
        직렬경로, monita_njia = Saraka_thamani / 'serial.sock', Saraka_thamani / 'monitor.sock'
        amri = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monita_njia) + ',server,nowait']
        amri += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Mtandao_thamani else ['-net', 'none']
        amri += ['-kernel', str(njia)] if 종류 == 'elf' else ['-cdrom', str(njia), '-boot', 'd']
        if 저장매체 is not None:
            amri += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Mchakato_thamani = subprocess.Popen(amri, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monita_njia.exists()):
                if self.Mchakato_thamani.poll() is not None:
                    raise AssertionError(self.Mchakato_thamani.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU endesha saa_thamani_4692cef5 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monita_thamani.connect(str(monita_njia))
            self.직렬.setblocking(False)
            self.monita_thamani.sendall(b'cont\n')
            self.subiri_hali('jkoros> ')
        except BaseException:
            self.funga()
            raise

    def subiri_hali(self, 문구, endesha=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.batli_REKODI[endesha:]:
                return self.batli_REKODI[endesha:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                data = self.직렬.recv(65536)
                if not data: break
                self.batli_REKODI.extend(data)
            if self.Mchakato_thamani.poll() is not None: break
        raise AssertionError('subiri_thamani kushindwa_thamani: ' + 문구 + '\n' + self.batli_REKODI.decode('utf-8', 'replace'))

    def amri(self, tungo_thamani, 기대):
        endesha = len(self.batli_REKODI)
        self.직렬.sendall((tungo_thamani + '\n').encode())
        결과 = self.subiri_hali('jkoros> ', endesha)
        for 문구 in 기대:
            assert 문구 in 결과, (tungo_thamani, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def funga(self):
        self.직렬.close()
        self.monita_thamani.close()
        if self.Mchakato_thamani.poll() is None:
            self.Mchakato_thamani.terminate()
            try: self.Mchakato_thamani.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Mchakato_thamani.kill()
                self.Mchakato_thamani.wait()
        self.Mchakato_thamani.communicate()
        self.임시.cleanup()


def 보호커널(Saraka_thamani):
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
    for Jina, maudhui_thamani in 사례들.items():
        chanzo = Saraka_thamani / (Jina + '.s')
        chanzo.write_text('.code32\n.text\n.globl _start\n_start:\n' + maudhui_thamani +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Saraka_thamani / (Jina + '.o')), str(chanzo)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/mtumiaji_Kiungo_Muundo.ld'),
                        '-o', str(Saraka_thamani / (Jina + '.elf')), str(Saraka_thamani / (Jina + '.o'))], check=True)
        항목들.append(Jina + '=' + str(Saraka_thamani / (Jina + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Jina, data in 변형들.items():
        faili = Saraka_thamani / (Jina + '.elf'); faili.write_bytes(data)
        항목들.append(Jina + '=' + str(faili))
    subprocess.run([sys.executable, str(위치 / 'Zana/묶기.py'), '-o', str(Saraka_thamani / 'apps.bin')] + 항목들, check=True)
    chanzo = Saraka_thamani / 'apps.s'
    chanzo.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Saraka_thamani / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Saraka_thamani / 'apps.o'), str(chanzo)], check=True)
    kiini_thamani_0611a8a8 = Saraka_thamani / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Kiungo_Muundo.ld'), '-o', str(kiini_thamani_0611a8a8),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(Saraka_thamani / 'apps.o')], check=True)
    return kiini_thamani_0611a8a8


def tekeleza_amri():
    결과 = {}
    seva_thamani = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seva_thamani.bind(('127.0.0.1', 0))
    seva_thamani.settimeout(0.1)
    kituo_thamani = seva_thamani.getsockname()[1]
    받은것 = []
    toka_programu = threading.Event()
    def 되보내기():
        while not toka_programu.is_set():
            try: data, kompyuta_rika_thamani = seva_thamani.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(data)
            if data != b'drop-me': seva_thamani.sendto(data, kompyuta_rika_thamani)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mashine = pepe_mashine(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                mashine.amri('apps', ['hello', 'udp', 'netcheck', 'stress'])
                mashine.amri('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                mashine.amri('run missing', ['Exit: -2'])
                mashine.amri('net', ['NET RTL8139'])
                mashine.amri('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for maudhui_thamani in ('hello-network', 'odd', 'even', 'repeat-123'):
                    mashine.amri('run udp 10.0.2.2 {} {}'.format(kituo_thamani, maudhui_thamani), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert maudhui_thamani.encode() in 받은것, 'mwenyeji 서버에서 자료를 받지 못함'
                mashine.amri('run stress {}'.format(kituo_thamani), ['UDP STRESS PASS', 'Exit: 0'])
                mashine.amri('run udp 10.0.2.2 {} drop-me'.format(kituo_thamani), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                mashine.amri('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = mashine.batli_REKODI.decode('utf-8', 'replace')
                print('PASS: {} mtumiaji ELF/ring 3/인수/UDP mwenyeji 왕복/saa_thamani_4692cef5 초과/sheli 복귀'.format(종류), flush=True)
            finally:
                try: mashine.amri('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(mashine.batli_REKODI)
                mashine.funga()
        mashine = pepe_mashine(위치 / 'build/kernel.elf', Mtandao_thamani=False)
        try:
            mashine.amri('net', ['NET unavailable'])
            mashine.amri('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            mashine.amri('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = mashine.batli_REKODI.decode()
        finally: mashine.funga()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            mashine = pepe_mashine(보호커널(Path(임시)), Mtandao_thamani=False)
            try:
                for Jina, hali_thamani in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    mashine.amri('run ' + Jina, ['Exit: ' + str(hali_thamani)])
                    mashine.amri('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = mashine.batli_REKODI.decode()
                print('PASS: mtumiaji kumbukumbu_data/포트 격리, 잘못된 kielekezi/ELF, CPU vighairi, 무한 sprint_thamani 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(mashine.batli_REKODI)
                mashine.funga()
    finally:
        toka_programu.set()
        일꾼.join(timeout=2)
        seva_thamani.close()
    결과['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    tekeleza_amri()
