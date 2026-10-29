#!/usr/bin/env python3
"""raun_gögn ring 3 ELF/hýsa UDP 왕복/verja_VALUE Villa/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

Staðsetning = Path(__file__).resolve().parents[1]


class sýndar_vél:
    def __init__(self, SLÓÐ, 종류='elf', Net_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        skráasafn_VALUE = Path(self.임시.name)
        self.LOG_lína = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.skjár_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, skjár_slóð = skráasafn_VALUE / 'serial.sock', skráasafn_VALUE / 'monitor.sock'
        Skipun = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(skjár_slóð) + ',server,nowait']
        Skipun += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Net_VALUE else ['-net', 'none']
        Skipun += ['-kernel', str(SLÓÐ)] if 종류 == 'elf' else ['-cdrom', str(SLÓÐ), '-boot', 'd']
        if 저장매체 is not None:
            Skipun += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Ferli_VALUE = subprocess.Popen(Skipun, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and skjár_slóð.exists()):
                if self.Ferli_VALUE.poll() is not None:
                    raise AssertionError(self.Ferli_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Keyra_2 TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.skjár_VALUE.connect(str(skjár_slóð))
            self.직렬.setblocking(False)
            self.skjár_VALUE.sendall(b'cont\n')
            self.Bíddu_staða('jkoros> ')
        except BaseException:
            self.Loka()
            raise

    def Bíddu_staða(self, 문구, Keyra_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_lína[Keyra_2:]:
                return self.LOG_lína[Keyra_2:].decode('utf-8', 'replace')
            Lestur, _, _ = select.select([self.직렬], [], [], 0.1)
            if Lestur:
                gögn = self.직렬.recv(65536)
                if not gögn: break
                self.LOG_lína.extend(gögn)
            if self.Ferli_VALUE.poll() is not None: break
        raise AssertionError('Bíddu_VALUE bilun_VALUE: ' + 문구 + '\n' + self.LOG_lína.decode('utf-8', 'replace'))

    def Skipun(self, strengur_VALUE, 기대):
        Keyra_2 = len(self.LOG_lína)
        self.직렬.sendall((strengur_VALUE + '\n').encode())
        NIÐURSTAÐA = self.Bíddu_staða('jkoros> ', Keyra_2)
        for 문구 in 기대:
            assert 문구 in NIÐURSTAÐA, (strengur_VALUE, 문구, NIÐURSTAÐA)
        assert 'PANIC' not in NIÐURSTAÐA, NIÐURSTAÐA
        return NIÐURSTAÐA

    def Loka(self):
        self.직렬.close()
        self.skjár_VALUE.close()
        if self.Ferli_VALUE.poll() is None:
            self.Ferli_VALUE.terminate()
            try: self.Ferli_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Ferli_VALUE.kill()
                self.Ferli_VALUE.wait()
        self.Ferli_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(skráasafn_VALUE):
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
    항목들 = ['hello=' + str(Staðsetning / 'build/apps/hello.elf')]
    for Heiti, Efni_VALUE in 사례들.items():
        Uppruni = skráasafn_VALUE / (Heiti + '.s')
        Uppruni.write_text('.code32\n.text\n.globl _start\n_start:\n' + Efni_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(skráasafn_VALUE / (Heiti + '.o')), str(Uppruni)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Staðsetning.parent / 'compiler/notandi_tengja_útlit.ld'),
                        '-o', str(skráasafn_VALUE / (Heiti + '.elf')), str(skráasafn_VALUE / (Heiti + '.o'))], check=True)
        항목들.append(Heiti + '=' + str(skráasafn_VALUE / (Heiti + '.elf')))
    정상 = bytearray((Staðsetning / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ógilt_mæld_stærð = bytearray(정상); ógilt_mæld_stærð[0] = 0; 변형들['badelf'] = ógilt_mæld_stærð
    ógilt_mæld_stærð = bytearray(정상); struct.pack_into('<I', ógilt_mæld_stærð, 24, 0x00100000); 변형들['badentry'] = ógilt_mæld_stærð
    ógilt_mæld_stærð = bytearray(정상); struct.pack_into('<I', ógilt_mæld_stærð, 28, 0x7fffffff); 변형들['badtable'] = ógilt_mæld_stærð
    ógilt_mæld_stærð = bytearray(정상); LOOKUP_tafla = struct.unpack_from('<I', ógilt_mæld_stærð, 28)[0]
    struct.pack_into('<I', ógilt_mæld_stærð, LOOKUP_tafla + 20, 0x7fffffff); 변형들['badsize'] = ógilt_mæld_stærð
    for Heiti, gögn in 변형들.items():
        Skrá = skráasafn_VALUE / (Heiti + '.elf'); Skrá.write_bytes(gögn)
        항목들.append(Heiti + '=' + str(Skrá))
    subprocess.run([sys.executable, str(Staðsetning / 'Verkfæri/BIND_endastöð.py'), '-o', str(skráasafn_VALUE / 'apps.bin')] + 항목들, check=True)
    Uppruni = skráasafn_VALUE / 'apps.s'
    Uppruni.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(skráasafn_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(skráasafn_VALUE / 'apps.o'), str(Uppruni)], check=True)
    kjarni_VALUE = skráasafn_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Staðsetning / '부팅/tengja_útlit.ld'), '-o', str(kjarni_VALUE),
                    str(Staðsetning / 'build/boot.o'), str(Staðsetning / 'build/java.o'), str(Staðsetning / 'build/user.o'), str(skráasafn_VALUE / 'apps.o')], check=True)
    return kjarni_VALUE


def keyra_skipun():
    NIÐURSTAÐA = {}
    þjónn_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    þjónn_VALUE.bind(('127.0.0.1', 0))
    þjónn_VALUE.settimeout(0.1)
    gátt_VALUE = þjónn_VALUE.getsockname()[1]
    RECEIVED_vara = []
    loka_forrit = threading.Event()
    def 되보내기():
        while not loka_forrit.is_set():
            try: gögn, jafningi_VALUE = þjónn_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_vara.append(gögn)
            if gögn != b'drop-me': þjónn_VALUE.sendto(gögn, jafningi_VALUE)
    starfskraftur_VALUE = threading.Thread(target=되보내기, daemon=True)
    starfskraftur_VALUE.start()
    try:
        for 종류 in ('elf', 'iso'):
            vél = sýndar_vél(Staðsetning / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                vél.Skipun('apps', ['hello', 'udp', 'netcheck', 'stress'])
                vél.Skipun('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                vél.Skipun('run missing', ['Exit: -2'])
                vél.Skipun('net', ['NET RTL8139'])
                vél.Skipun('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Efni_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    vél.Skipun('run udp 10.0.2.2 {} {}'.format(gátt_VALUE, Efni_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Efni_VALUE.encode() in RECEIVED_vara, 'hýsa 서버에서 자료를 받지 못함'
                vél.Skipun('run stress {}'.format(gátt_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                vél.Skipun('run udp 10.0.2.2 {} drop-me'.format(gátt_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                vél.Skipun('run hello recovered', ['arg: recovered', 'Exit: 0'])
                NIÐURSTAÐA[종류] = vél.LOG_lína.decode('utf-8', 'replace')
                print('PASS: {} notandi ELF/ring 3/Viðföng/UDP hýsa 왕복/TIME_VALUE 초과/skel 복귀'.format(종류), flush=True)
            finally:
                try: vél.Skipun('net', [])
                except Exception: pass
                (Staðsetning / 'build/사용자통신-last.log').write_bytes(vél.LOG_lína)
                vél.Loka()
        vél = sýndar_vél(Staðsetning / 'build/kernel.elf', Net_VALUE=False)
        try:
            vél.Skipun('net', ['NET unavailable'])
            vél.Skipun('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            vél.Skipun('run hello', ['USER MODE ring 3', 'Exit: 0'])
            NIÐURSTAÐA['no_nic'] = vél.LOG_lína.decode()
        finally: vél.Loka()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            vél = sýndar_vél(보호커널(Path(임시)), Net_VALUE=False)
            try:
                for Heiti, staða_VALUE_e10195a1 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    vél.Skipun('run ' + Heiti, ['Exit: ' + str(staða_VALUE_e10195a1)])
                    vél.Skipun('run hello', ['USER MODE ring 3', 'Exit: 0'])
                NIÐURSTAÐA['protection'] = vél.LOG_lína.decode()
                print('PASS: notandi Minni_gögn/포트 격리, 잘못된 bendill/ELF, CPU undantekning, 무한 ítrekun_VALUE 제한', flush=True)
            finally:
                (Staðsetning / 'build/보호시험-last.log').write_bytes(vél.LOG_lína)
                vél.Loka()
    finally:
        loka_forrit.set()
        starfskraftur_VALUE.join(timeout=2)
        þjónn_VALUE.close()
    NIÐURSTAÐA['host_udp_received'] = [{'length': len(gögn), 'sha256': hashlib.sha256(gögn).hexdigest()} for gögn in RECEIVED_vara]
    (Staðsetning / 'build/사용자통신시험.json').write_text(json.dumps(NIÐURSTAÐA, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    keyra_skipun()
