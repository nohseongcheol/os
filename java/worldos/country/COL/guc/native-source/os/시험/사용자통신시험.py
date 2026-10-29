#!/usr/bin/env python3
"""실제 ring 3 ELF/epiajatü UDP 왕복/aa_inmajaa_ajutuu ajachitia/시간 제한/잘못된 ELF를 검증한다."""
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


class 가상기계:
    def __init__(self, wopu_a_ttaaleemüin, 종류='elf', kusu_ajutuu=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        anaajaalee_ajutuu = Path(self.임시.name)
        self.aa_innachikimaajatü_aparatsee = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.anajia_ajutuu = socket.socket(socket.AF_UNIX)
        직렬경로, anajia_wopu_a_ttaaleemüin = anaajaalee_ajutuu / 'serial.sock', anaajaalee_ajutuu / 'monitor.sock'
        aluwataaya = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(anajia_wopu_a_ttaaleemüin) + ',server,nowait']
        aluwataaya += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if kusu_ajutuu else ['-net', 'none']
        aluwataaya += ['-kernel', str(wopu_a_ttaaleemüin)] if 종류 == 'elf' else ['-cdrom', str(wopu_a_ttaaleemüin), '-boot', 'd']
        if 저장매체 is not None:
            aluwataaya += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.과정 = subprocess.Popen(aluwataaya, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and anajia_wopu_a_ttaaleemüin.exists()):
                if self.과정.poll() is not None:
                    raise AssertionError(self.과정.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU 시작 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.anajia_ajutuu.connect(str(anajia_wopu_a_ttaaleemüin))
            self.직렬.setblocking(False)
            self.anajia_ajutuu.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.asürülaa()
            raise

    def 기다림(self, 문구, 시작=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.aa_innachikimaajatü_aparatsee[시작:]:
                return self.aa_innachikimaajatü_aparatsee[시작:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                atijaaya = self.직렬.recv(65536)
                if not atijaaya: break
                self.aa_innachikimaajatü_aparatsee.extend(atijaaya)
            if self.과정.poll() is not None: break
        raise AssertionError('대기 ajachitia_ajutuu: ' + 문구 + '\n' + self.aa_innachikimaajatü_aparatsee.decode('utf-8', 'replace'))

    def aluwataaya(self, kaleena_ajutuu, 기대):
        시작 = len(self.aa_innachikimaajatü_aparatsee)
        self.직렬.sendall((kaleena_ajutuu + '\n').encode())
        결과 = self.기다림('jkoros> ', 시작)
        for 문구 in 기대:
            assert 문구 in 결과, (kaleena_ajutuu, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def asürülaa(self):
        self.직렬.close()
        self.anajia_ajutuu.close()
        if self.과정.poll() is None:
            self.과정.terminate()
            try: self.과정.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.과정.kill()
                self.과정.wait()
        self.과정.communicate()
        self.임시.cleanup()


def 보호커널(anaajaalee_ajutuu):
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
    for 이름, alu_ujatüü_ajutuu in 사례들.items():
        eejeejetülein = anaajaalee_ajutuu / (이름 + '.s')
        eejeejetülein.write_text('.code32\n.text\n.globl _start\n_start:\n' + alu_ujatüü_ajutuu +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(anaajaalee_ajutuu / (이름 + '.o')), str(eejeejetülein)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/ka_yataayakalü_wopu_akumajiakuai_pa.ld'),
                        '-o', str(anaajaalee_ajutuu / (이름 + '.elf')), str(anaajaalee_ajutuu / (이름 + '.o'))], check=True)
        항목들.append(이름 + '=' + str(anaajaalee_ajutuu / (이름 + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for 이름, atijaaya in 변형들.items():
        anaajaalaa = anaajaalee_ajutuu / (이름 + '.elf'); anaajaalaa.write_bytes(atijaaya)
        항목들.append(이름 + '=' + str(anaajaalaa))
    subprocess.run([sys.executable, str(위치 / '도구/묶기.py'), '-o', str(anaajaalee_ajutuu / 'apps.bin')] + 항목들, check=True)
    eejeejetülein = anaajaalee_ajutuu / 'apps.s'
    eejeejetülein.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(anaajaalee_ajutuu / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(anaajaalee_ajutuu / 'apps.o'), str(eejeejetülein)], check=True)
    keetnerü_ajutuu = anaajaalee_ajutuu / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/wopu_akumajiakuai_pa.ld'), '-o', str(keetnerü_ajutuu),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(anaajaalee_ajutuu / 'apps.o')], check=True)
    return keetnerü_ajutuu


def 실행():
    결과 = {}
    서버 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    서버.bind(('127.0.0.1', 0))
    서버.settimeout(0.1)
    outtülee_ajutuu = 서버.getsockname()[1]
    받은것 = []
    aju_itaa_akumajiaa = threading.Event()
    def 되보내기():
        while not aju_itaa_akumajiaa.is_set():
            try: atijaaya, wanaawasü_ajutuu = 서버.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(atijaaya)
            if atijaaya != b'drop-me': 서버.sendto(atijaaya, wanaawasü_ajutuu)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                기계.aluwataaya('apps', ['hello', 'udp', 'netcheck', 'stress'])
                기계.aluwataaya('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                기계.aluwataaya('run missing', ['Exit: -2'])
                기계.aluwataaya('net', ['NET RTL8139'])
                기계.aluwataaya('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for alu_ujatüü_ajutuu in ('hello-network', 'odd', 'even', 'repeat-123'):
                    기계.aluwataaya('run udp 10.0.2.2 {} {}'.format(outtülee_ajutuu, alu_ujatüü_ajutuu), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert alu_ujatüü_ajutuu.encode() in 받은것, 'epiajatü 서버에서 자료를 받지 못함'
                기계.aluwataaya('run stress {}'.format(outtülee_ajutuu), ['UDP STRESS PASS', 'Exit: 0'])
                기계.aluwataaya('run udp 10.0.2.2 {} drop-me'.format(outtülee_ajutuu), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                기계.aluwataaya('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.aa_innachikimaajatü_aparatsee.decode('utf-8', 'replace')
                print('PASS: {} ka_yataayakalü ELF/ring 3/인수/UDP epiajatü 왕복/시간 초과/aluwataalapu_u 복귀'.format(종류), flush=True)
            finally:
                try: 기계.aluwataaya('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(기계.aa_innachikimaajatü_aparatsee)
                기계.asürülaa()
        기계 = 가상기계(위치 / 'build/kernel.elf', kusu_ajutuu=False)
        try:
            기계.aluwataaya('net', ['NET unavailable'])
            기계.aluwataaya('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            기계.aluwataaya('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = 기계.aa_innachikimaajatü_aparatsee.decode()
        finally: 기계.asürülaa()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            기계 = 가상기계(보호커널(Path(임시)), kusu_ajutuu=False)
            try:
                for 이름, jamakua_iparülein_ajutuu in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    기계.aluwataaya('run ' + 이름, ['Exit: ' + str(jamakua_iparülein_ajutuu)])
                    기계.aluwataaya('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = 기계.aa_innachikimaajatü_aparatsee.decode()
                print('PASS: ka_yataayakalü 메모리/포트 격리, 잘못된 포인터/ELF, CPU 예외, 무한 a_lakaa_ajutuu 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(기계.aa_innachikimaajatü_aparatsee)
                기계.asürülaa()
    finally:
        aju_itaa_akumajiaa.set()
        일꾼.join(timeout=2)
        서버.close()
    결과['host_udp_received'] = [{'length': len(atijaaya), 'sha256': hashlib.sha256(atijaaya).hexdigest()} for atijaaya in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    실행()
