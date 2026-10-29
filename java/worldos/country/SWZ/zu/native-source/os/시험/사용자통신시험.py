#!/usr/bin/env python3
"""ulwazi_ngokwenzekile_imininingwane ring 3 ELF/singatha UDP 왕복/vikela_inani Iphutha/시간 제한/잘못된 ELF를 검증한다."""
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


class utalagu_umshini:
    def __init__(self, Indlela_2, 종류='elf', iNethiwekhi_inani=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        umkhombandlela_inani = Path(self.임시.name)
        self.loga_umugqa = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.imonitha_inani = socket.socket(socket.AF_UNIX)
        직렬경로, imonitha_umzila = umkhombandlela_inani / 'serial.sock', umkhombandlela_inani / 'monitor.sock'
        Umlayelo = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(imonitha_umzila) + ',server,nowait']
        Umlayelo += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if iNethiwekhi_inani else ['-net', 'none']
        Umlayelo += ['-kernel', str(Indlela_2)] if 종류 == 'elf' else ['-cdrom', str(Indlela_2), '-boot', 'd']
        if 저장매체 is not None:
            Umlayelo += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Inqubo_inani = subprocess.Popen(Umlayelo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and imonitha_umzila.exists()):
                if self.Inqubo_inani.poll() is not None:
                    raise AssertionError(self.Inqubo_inani.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Sebenzisa 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.imonitha_inani.connect(str(imonitha_umzila))
            self.직렬.setblocking(False)
            self.imonitha_inani.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Vala()
            raise

    def 기다림(self, 문구, Sebenzisa=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.loga_umugqa[Sebenzisa:]:
                return self.loga_umugqa[Sebenzisa:].decode('utf-8', 'replace')
            Funda, _, _ = select.select([self.직렬], [], [], 0.1)
            if Funda:
                imininingwane = self.직렬.recv(65536)
                if not imininingwane: break
                self.loga_umugqa.extend(imininingwane)
            if self.Inqubo_inani.poll() is not None: break
        raise AssertionError('대기 ukwehluleka_inani: ' + 문구 + '\n' + self.loga_umugqa.decode('utf-8', 'replace'))

    def Umlayelo(self, uchunge_inani, 기대):
        Sebenzisa = len(self.loga_umugqa)
        self.직렬.sendall((uchunge_inani + '\n').encode())
        결과 = self.기다림('jkoros> ', Sebenzisa)
        for 문구 in 기대:
            assert 문구 in 결과, (uchunge_inani, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Vala(self):
        self.직렬.close()
        self.imonitha_inani.close()
        if self.Inqubo_inani.poll() is None:
            self.Inqubo_inani.terminate()
            try: self.Inqubo_inani.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Inqubo_inani.kill()
                self.Inqubo_inani.wait()
        self.Inqubo_inani.communicate()
        self.임시.cleanup()


def 보호커널(umkhombandlela_inani):
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
    for Igama, Okuqukethwe_inani in 사례들.items():
        umthombo = umkhombandlela_inani / (Igama + '.s')
        umthombo.write_text('.code32\n.text\n.globl _start\n_start:\n' + Okuqukethwe_inani +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(umkhombandlela_inani / (Igama + '.o')), str(umthombo)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/umsebenzisi_xhuma_I_layout.ld'),
                        '-o', str(umkhombandlela_inani / (Igama + '.elf')), str(umkhombandlela_inani / (Igama + '.o'))], check=True)
        항목들.append(Igama + '=' + str(umkhombandlela_inani / (Igama + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Igama, imininingwane in 변형들.items():
        Ihele = umkhombandlela_inani / (Igama + '.elf'); Ihele.write_bytes(imininingwane)
        항목들.append(Igama + '=' + str(Ihele))
    subprocess.run([sys.executable, str(위치 / 'Amathuluzi/묶기.py'), '-o', str(umkhombandlela_inani / 'apps.bin')] + 항목들, check=True)
    umthombo = umkhombandlela_inani / 'apps.s'
    umthombo.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(umkhombandlela_inani / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(umkhombandlela_inani / 'apps.o'), str(umthombo)], check=True)
    ikhenela_inani = umkhombandlela_inani / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/xhuma_I_layout.ld'), '-o', str(ikhenela_inani),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(umkhombandlela_inani / 'apps.o')], check=True)
    return ikhenela_inani


def yenza_umyalo():
    결과 = {}
    Iseva_inani = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Iseva_inani.bind(('127.0.0.1', 0))
    Iseva_inani.settimeout(0.1)
    intuba_inani = Iseva_inani.getsockname()[1]
    받은것 = []
    phuma_i_app = threading.Event()
    def 되보내기():
        while not phuma_i_app.is_set():
            try: imininingwane, untanga_inani = Iseva_inani.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(imininingwane)
            if imininingwane != b'drop-me': Iseva_inani.sendto(imininingwane, untanga_inani)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            umshini = utalagu_umshini(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                umshini.Umlayelo('apps', ['hello', 'udp', 'netcheck', 'stress'])
                umshini.Umlayelo('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                umshini.Umlayelo('run missing', ['Exit: -2'])
                umshini.Umlayelo('net', ['NET RTL8139'])
                umshini.Umlayelo('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Okuqukethwe_inani in ('hello-network', 'odd', 'even', 'repeat-123'):
                    umshini.Umlayelo('run udp 10.0.2.2 {} {}'.format(intuba_inani, Okuqukethwe_inani), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Okuqukethwe_inani.encode() in 받은것, 'singatha 서버에서 자료를 받지 못함'
                umshini.Umlayelo('run stress {}'.format(intuba_inani), ['UDP STRESS PASS', 'Exit: 0'])
                umshini.Umlayelo('run udp 10.0.2.2 {} drop-me'.format(intuba_inani), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                umshini.Umlayelo('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = umshini.loga_umugqa.decode('utf-8', 'replace')
                print('PASS: {} umsebenzisi ELF/ring 3/인수/UDP singatha 왕복/시간 초과/isihumushi_miyalelo 복귀'.format(종류), flush=True)
            finally:
                try: umshini.Umlayelo('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(umshini.loga_umugqa)
                umshini.Vala()
        umshini = utalagu_umshini(위치 / 'build/kernel.elf', iNethiwekhi_inani=False)
        try:
            umshini.Umlayelo('net', ['NET unavailable'])
            umshini.Umlayelo('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            umshini.Umlayelo('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = umshini.loga_umugqa.decode()
        finally: umshini.Vala()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            umshini = utalagu_umshini(보호커널(Path(임시)), iNethiwekhi_inani=False)
            try:
                for Igama, isimo_inani in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    umshini.Umlayelo('run ' + Igama, ['Exit: ' + str(isimo_inani)])
                    umshini.Umlayelo('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = umshini.loga_umugqa.decode()
                print('PASS: umsebenzisi inkumbulo_imininingwane/포트 격리, 잘못된 isikhombi/ELF, CPU 예외, 무한 impinda_inani 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(umshini.loga_umugqa)
                umshini.Vala()
    finally:
        phuma_i_app.set()
        일꾼.join(timeout=2)
        Iseva_inani.close()
    결과['host_udp_received'] = [{'length': len(imininingwane), 'sha256': hashlib.sha256(imininingwane).hexdigest()} for imininingwane in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    yenza_umyalo()
