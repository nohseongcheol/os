#!/usr/bin/env python3
"""taannallarik_titiqqat ring 3 ELF/tuttarvik UDP 왕복/pijjairli_atuutilik tammarniq/시간 제한/잘못된 ELF를 검증한다."""
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
    def __init__(self, aqqut, 종류='elf', Kasuqatigiitsimajut_atuutilik=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        tukimuagutiit_atuutilik = Path(self.임시.name)
        self.papattivik_sanimukutaak = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.qarasaujaup_saqqijaarutinga_atuutilik = socket.socket(socket.AF_UNIX)
        직렬경로, qarasaujaup_saqqijaarutinga_aqqut = tukimuagutiit_atuutilik / 'serial.sock', tukimuagutiit_atuutilik / 'monitor.sock'
        piqujijjut = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(qarasaujaup_saqqijaarutinga_aqqut) + ',server,nowait']
        piqujijjut += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Kasuqatigiitsimajut_atuutilik else ['-net', 'none']
        piqujijjut += ['-kernel', str(aqqut)] if 종류 == 'elf' else ['-cdrom', str(aqqut), '-boot', 'd']
        if 저장매체 is not None:
            piqujijjut += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Pivallianiq_atuutilik = subprocess.Popen(piqujijjut, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and qarasaujaup_saqqijaarutinga_aqqut.exists()):
                if self.Pivallianiq_atuutilik.poll() is not None:
                    raise AssertionError(self.Pivallianiq_atuutilik.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU 시작 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.qarasaujaup_saqqijaarutinga_atuutilik.connect(str(qarasaujaup_saqqijaarutinga_aqqut))
            self.직렬.setblocking(False)
            self.qarasaujaup_saqqijaarutinga_atuutilik.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.matuli()
            raise

    def 기다림(self, 문구, 시작=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.papattivik_sanimukutaak[시작:]:
                return self.papattivik_sanimukutaak[시작:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                titiqqat = self.직렬.recv(65536)
                if not titiqqat: break
                self.papattivik_sanimukutaak.extend(titiqqat)
            if self.Pivallianiq_atuutilik.poll() is not None: break
        raise AssertionError('대기 itigaqtuq_atuutilik: ' + 문구 + '\n' + self.papattivik_sanimukutaak.decode('utf-8', 'replace'))

    def piqujijjut(self, qimiaq_atuutilik, 기대):
        시작 = len(self.papattivik_sanimukutaak)
        self.직렬.sendall((qimiaq_atuutilik + '\n').encode())
        결과 = self.기다림('jkoros> ', 시작)
        for 문구 in 기대:
            assert 문구 in 결과, (qimiaq_atuutilik, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def matuli(self):
        self.직렬.close()
        self.qarasaujaup_saqqijaarutinga_atuutilik.close()
        if self.Pivallianiq_atuutilik.poll() is None:
            self.Pivallianiq_atuutilik.terminate()
            try: self.Pivallianiq_atuutilik.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Pivallianiq_atuutilik.kill()
                self.Pivallianiq_atuutilik.wait()
        self.Pivallianiq_atuutilik.communicate()
        self.임시.cleanup()


def 보호커널(tukimuagutiit_atuutilik):
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
    for atiq, Ilulingit_atuutilik in 사례들.items():
        pivviujuq = tukimuagutiit_atuutilik / (atiq + '.s')
        pivviujuq.write_text('.code32\n.text\n.globl _start\n_start:\n' + Ilulingit_atuutilik +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(tukimuagutiit_atuutilik / (atiq + '.o')), str(pivviujuq)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/atuqtuq_kasurvik_ilinganinga.ld'),
                        '-o', str(tukimuagutiit_atuutilik / (atiq + '.elf')), str(tukimuagutiit_atuutilik / (atiq + '.o'))], check=True)
        항목들.append(atiq + '=' + str(tukimuagutiit_atuutilik / (atiq + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for atiq, titiqqat in 변형들.items():
        ini = tukimuagutiit_atuutilik / (atiq + '.elf'); ini.write_bytes(titiqqat)
        항목들.append(atiq + '=' + str(ini))
    subprocess.run([sys.executable, str(위치 / '도구/묶기.py'), '-o', str(tukimuagutiit_atuutilik / 'apps.bin')] + 항목들, check=True)
    pivviujuq = tukimuagutiit_atuutilik / 'apps.s'
    pivviujuq.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(tukimuagutiit_atuutilik / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(tukimuagutiit_atuutilik / 'apps.o'), str(pivviujuq)], check=True)
    kernel_atuutilik = tukimuagutiit_atuutilik / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/kasurvik_ilinganinga.ld'), '-o', str(kernel_atuutilik),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(tukimuagutiit_atuutilik / 'apps.o')], check=True)
    return kernel_atuutilik


def 실행():
    결과 = {}
    ikiaqqitittivik_atuutilik = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ikiaqqitittivik_atuutilik.bind(('127.0.0.1', 0))
    ikiaqqitittivik_atuutilik.settimeout(0.1)
    kapputigaq_atuutilik = ikiaqqitittivik_atuutilik.getsockname()[1]
    받은것 = []
    taima_pilirijjut = threading.Event()
    def 되보내기():
        while not taima_pilirijjut.is_set():
            try: titiqqat, ilagijaujuq_atuutilik = ikiaqqitittivik_atuutilik.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(titiqqat)
            if titiqqat != b'drop-me': ikiaqqitittivik_atuutilik.sendto(titiqqat, ilagijaujuq_atuutilik)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                기계.piqujijjut('apps', ['hello', 'udp', 'netcheck', 'stress'])
                기계.piqujijjut('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                기계.piqujijjut('run missing', ['Exit: -2'])
                기계.piqujijjut('net', ['NET RTL8139'])
                기계.piqujijjut('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Ilulingit_atuutilik in ('hello-network', 'odd', 'even', 'repeat-123'):
                    기계.piqujijjut('run udp 10.0.2.2 {} {}'.format(kapputigaq_atuutilik, Ilulingit_atuutilik), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Ilulingit_atuutilik.encode() in 받은것, 'tuttarvik 서버에서 자료를 받지 못함'
                기계.piqujijjut('run stress {}'.format(kapputigaq_atuutilik), ['UDP STRESS PASS', 'Exit: 0'])
                기계.piqujijjut('run udp 10.0.2.2 {} drop-me'.format(kapputigaq_atuutilik), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                기계.piqujijjut('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = 기계.papattivik_sanimukutaak.decode('utf-8', 'replace')
                print('PASS: {} atuqtuq ELF/ring 3/인수/UDP tuttarvik 왕복/시간 초과/piqujijjutiliriji 복귀'.format(종류), flush=True)
            finally:
                try: 기계.piqujijjut('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(기계.papattivik_sanimukutaak)
                기계.matuli()
        기계 = 가상기계(위치 / 'build/kernel.elf', Kasuqatigiitsimajut_atuutilik=False)
        try:
            기계.piqujijjut('net', ['NET unavailable'])
            기계.piqujijjut('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            기계.piqujijjut('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = 기계.papattivik_sanimukutaak.decode()
        finally: 기계.matuli()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            기계 = 가상기계(보호커널(Path(임시)), Kasuqatigiitsimajut_atuutilik=False)
            try:
                for atiq, qanuilinganiq_atuutilik in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    기계.piqujijjut('run ' + atiq, ['Exit: ' + str(qanuilinganiq_atuutilik)])
                    기계.piqujijjut('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = 기계.papattivik_sanimukutaak.decode()
                print('PASS: atuqtuq puigujjaikkut_titiqqat/포트 격리, 잘못된 포인터/ELF, CPU 예외, 무한 utiqtaqtuq_atuutilik 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(기계.papattivik_sanimukutaak)
                기계.matuli()
    finally:
        taima_pilirijjut.set()
        일꾼.join(timeout=2)
        ikiaqqitittivik_atuutilik.close()
    결과['host_udp_received'] = [{'length': len(titiqqat), 'sha256': hashlib.sha256(titiqqat).hexdigest()} for titiqqat in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    실행()
