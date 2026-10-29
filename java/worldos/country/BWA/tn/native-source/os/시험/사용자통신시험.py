#!/usr/bin/env python3
"""tota_tshedimosetso ring 3 ELF/pinagare UDP 왕복/sireletsa_Boleng phoso/시간 제한/잘못된 ELF를 검증한다."""
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


class seka_motšhine:
    def __init__(self, tsela, 종류='elf', Neteweke_Boleng=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Lenaneofaele_Boleng = Path(self.임시.name)
        self.rekota_mola = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monithara_Boleng = socket.socket(socket.AF_UNIX)
        직렬경로, monithara_tsela = Lenaneofaele_Boleng / 'serial.sock', Lenaneofaele_Boleng / 'monitor.sock'
        Taelo = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monithara_tsela) + ',server,nowait']
        Taelo += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Neteweke_Boleng else ['-net', 'none']
        Taelo += ['-kernel', str(tsela)] if 종류 == 'elf' else ['-cdrom', str(tsela), '-boot', 'd']
        if 저장매체 is not None:
            Taelo += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Thulaganyo_Boleng = subprocess.Popen(Taelo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monithara_tsela.exists()):
                if self.Thulaganyo_Boleng.poll() is not None:
                    raise AssertionError(self.Thulaganyo_Boleng.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU dirisa 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monithara_Boleng.connect(str(monithara_tsela))
            self.직렬.setblocking(False)
            self.monithara_Boleng.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.tswala()
            raise

    def 기다림(self, 문구, dirisa=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.rekota_mola[dirisa:]:
                return self.rekota_mola[dirisa:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                tshedimosetso = self.직렬.recv(65536)
                if not tshedimosetso: break
                self.rekota_mola.extend(tshedimosetso)
            if self.Thulaganyo_Boleng.poll() is not None: break
        raise AssertionError('대기 palelo_Boleng: ' + 문구 + '\n' + self.rekota_mola.decode('utf-8', 'replace'))

    def Taelo(self, dikwalwa_Boleng, 기대):
        dirisa = len(self.rekota_mola)
        self.직렬.sendall((dikwalwa_Boleng + '\n').encode())
        결과 = self.기다림('jkoros> ', dirisa)
        for 문구 in 기대:
            assert 문구 in 결과, (dikwalwa_Boleng, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def tswala(self):
        self.직렬.close()
        self.monithara_Boleng.close()
        if self.Thulaganyo_Boleng.poll() is None:
            self.Thulaganyo_Boleng.terminate()
            try: self.Thulaganyo_Boleng.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Thulaganyo_Boleng.kill()
                self.Thulaganyo_Boleng.wait()
        self.Thulaganyo_Boleng.communicate()
        self.임시.cleanup()


def 보호커널(Lenaneofaele_Boleng):
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
    for leina, Diteng_Boleng in 사례들.items():
        Motswedi = Lenaneofaele_Boleng / (leina + '.s')
        Motswedi.write_text('.code32\n.text\n.globl _start\n_start:\n' + Diteng_Boleng +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Lenaneofaele_Boleng / (leina + '.o')), str(Motswedi)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/modirisi_Kgokagano_Boalo.ld'),
                        '-o', str(Lenaneofaele_Boleng / (leina + '.elf')), str(Lenaneofaele_Boleng / (leina + '.o'))], check=True)
        항목들.append(leina + '=' + str(Lenaneofaele_Boleng / (leina + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for leina, tshedimosetso in 변형들.items():
        faele = Lenaneofaele_Boleng / (leina + '.elf'); faele.write_bytes(tshedimosetso)
        항목들.append(leina + '=' + str(faele))
    subprocess.run([sys.executable, str(위치 / 'Thuluse/묶기.py'), '-o', str(Lenaneofaele_Boleng / 'apps.bin')] + 항목들, check=True)
    Motswedi = Lenaneofaele_Boleng / 'apps.s'
    Motswedi.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Lenaneofaele_Boleng / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Lenaneofaele_Boleng / 'apps.o'), str(Motswedi)], check=True)
    Khenele_Boleng = Lenaneofaele_Boleng / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Kgokagano_Boalo.ld'), '-o', str(Khenele_Boleng),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(Lenaneofaele_Boleng / 'apps.o')], check=True)
    return Khenele_Boleng


def diragatsa_Taelo():
    결과 = {}
    sefara_Boleng = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sefara_Boleng.bind(('127.0.0.1', 0))
    sefara_Boleng.settimeout(0.1)
    gorogisetsa_Boleng = sefara_Boleng.getsockname()[1]
    받은것 = []
    tswaya_Tiriso = threading.Event()
    def 되보내기():
        while not tswaya_Tiriso.is_set():
            try: tshedimosetso, semphato_Boleng = sefara_Boleng.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(tshedimosetso)
            if tshedimosetso != b'drop-me': sefara_Boleng.sendto(tshedimosetso, semphato_Boleng)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            motšhine = seka_motšhine(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                motšhine.Taelo('apps', ['hello', 'udp', 'netcheck', 'stress'])
                motšhine.Taelo('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                motšhine.Taelo('run missing', ['Exit: -2'])
                motšhine.Taelo('net', ['NET RTL8139'])
                motšhine.Taelo('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Diteng_Boleng in ('hello-network', 'odd', 'even', 'repeat-123'):
                    motšhine.Taelo('run udp 10.0.2.2 {} {}'.format(gorogisetsa_Boleng, Diteng_Boleng), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Diteng_Boleng.encode() in 받은것, 'pinagare 서버에서 자료를 받지 못함'
                motšhine.Taelo('run stress {}'.format(gorogisetsa_Boleng), ['UDP STRESS PASS', 'Exit: 0'])
                motšhine.Taelo('run udp 10.0.2.2 {} drop-me'.format(gorogisetsa_Boleng), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                motšhine.Taelo('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = motšhine.rekota_mola.decode('utf-8', 'replace')
                print('PASS: {} modirisi ELF/ring 3/인수/UDP pinagare 왕복/시간 초과/setlhalosataelo 복귀'.format(종류), flush=True)
            finally:
                try: motšhine.Taelo('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(motšhine.rekota_mola)
                motšhine.tswala()
        motšhine = seka_motšhine(위치 / 'build/kernel.elf', Neteweke_Boleng=False)
        try:
            motšhine.Taelo('net', ['NET unavailable'])
            motšhine.Taelo('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            motšhine.Taelo('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = motšhine.rekota_mola.decode()
        finally: motšhine.tswala()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            motšhine = seka_motšhine(보호커널(Path(임시)), Neteweke_Boleng=False)
            try:
                for leina, kemo_Boleng in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    motšhine.Taelo('run ' + leina, ['Exit: ' + str(kemo_Boleng)])
                    motšhine.Taelo('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = motšhine.rekota_mola.decode()
                print('PASS: modirisi memori_tshedimosetso/포트 격리, 잘못된 sesupi/ELF, CPU 예외, 무한 poeletso_Boleng 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(motšhine.rekota_mola)
                motšhine.tswala()
    finally:
        tswaya_Tiriso.set()
        일꾼.join(timeout=2)
        sefara_Boleng.close()
    결과['host_udp_received'] = [{'length': len(tshedimosetso), 'sha256': hashlib.sha256(tshedimosetso).hexdigest()} for tshedimosetso in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    diragatsa_Taelo()
