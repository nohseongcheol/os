#!/usr/bin/env python3
"""liteew_mbir ring 3 ELF/dalal UDP 왕복/saama_xëyma njumte/시간 제한/잘못된 ELF를 검증한다."""
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


class luy_feeñ_te_jëmmadi_masin:
    def __init__(self, Yoonu_jëmale, 종류='elf', mbaal_xëyma=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        dàmb_xëyma = Path(self.임시.name)
        self.làq_Dënk = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.wonekaay_xëyma = socket.socket(socket.AF_UNIX)
        직렬경로, wonekaay_Yoonu_jëmale = dàmb_xëyma / 'serial.sock', dàmb_xëyma / 'monitor.sock'
        ndigel = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(wonekaay_Yoonu_jëmale) + ',server,nowait']
        ndigel += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if mbaal_xëyma else ['-net', 'none']
        ndigel += ['-kernel', str(Yoonu_jëmale)] if 종류 == 'elf' else ['-cdrom', str(Yoonu_jëmale), '-boot', 'd']
        if 저장매체 is not None:
            ndigel += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.yokkute_xëyma = subprocess.Popen(ndigel, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and wonekaay_Yoonu_jëmale.exists()):
                if self.yokkute_xëyma.poll() is not None:
                    raise AssertionError(self.yokkute_xëyma.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU daw 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.wonekaay_xëyma.connect(str(wonekaay_Yoonu_jëmale))
            self.직렬.setblocking(False)
            self.wonekaay_xëyma.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Tej()
            raise

    def 기다림(self, 문구, daw=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.làq_Dënk[daw:]:
                return self.làq_Dënk[daw:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                mbir = self.직렬.recv(65536)
                if not mbir: break
                self.làq_Dënk.extend(mbir)
            if self.yokkute_xëyma.poll() is not None: break
        raise AssertionError('대기 foo_xëyma: ' + 문구 + '\n' + self.làq_Dënk.decode('utf-8', 'replace'))

    def ndigel(self, araf_yu_bennoo_xëyma, 기대):
        daw = len(self.làq_Dënk)
        self.직렬.sendall((araf_yu_bennoo_xëyma + '\n').encode())
        결과 = self.기다림('jkoros> ', daw)
        for 문구 in 기대:
            assert 문구 in 결과, (araf_yu_bennoo_xëyma, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Tej(self):
        self.직렬.close()
        self.wonekaay_xëyma.close()
        if self.yokkute_xëyma.poll() is None:
            self.yokkute_xëyma.terminate()
            try: self.yokkute_xëyma.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.yokkute_xëyma.kill()
                self.yokkute_xëyma.wait()
        self.yokkute_xëyma.communicate()
        self.임시.cleanup()


def 보호커널(dàmb_xëyma):
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
    for tur_253d1510, Këmb_xëyma in 사례들.items():
        Cosaan = dàmb_xëyma / (tur_253d1510 + '.s')
        Cosaan.write_text('.code32\n.text\n.globl _start\n_start:\n' + Këmb_xëyma +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(dàmb_xëyma / (tur_253d1510 + '.o')), str(Cosaan)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/kiy_jariñoo_internet_lëkkale_Tëralin.ld'),
                        '-o', str(dàmb_xëyma / (tur_253d1510 + '.elf')), str(dàmb_xëyma / (tur_253d1510 + '.o'))], check=True)
        항목들.append(tur_253d1510 + '=' + str(dàmb_xëyma / (tur_253d1510 + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for tur_253d1510, mbir in 변형들.items():
        bara_denc = dàmb_xëyma / (tur_253d1510 + '.elf'); bara_denc.write_bytes(mbir)
        항목들.append(tur_253d1510 + '=' + str(bara_denc))
    subprocess.run([sys.executable, str(위치 / 'Jumtukaay_yi/묶기.py'), '-o', str(dàmb_xëyma / 'apps.bin')] + 항목들, check=True)
    Cosaan = dàmb_xëyma / 'apps.s'
    Cosaan.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(dàmb_xëyma / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(dàmb_xëyma / 'apps.o'), str(Cosaan)], check=True)
    xoox_xëyma = dàmb_xëyma / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/lëkkale_Tëralin.ld'), '-o', str(xoox_xëyma),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(dàmb_xëyma / 'apps.o')], check=True)
    return xoox_xëyma


def def_ndigel():
    결과 = {}
    dëggu_xëyma = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dëggu_xëyma.bind(('127.0.0.1', 0))
    dëggu_xëyma.settimeout(0.1)
    jël_xëyma = dëggu_xëyma.getsockname()[1]
    받은것 = []
    Génn_jëfekaay = threading.Event()
    def 되보내기():
        while not Génn_jëfekaay.is_set():
            try: mbir, Nàttangoo_xëyma = dëggu_xëyma.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(mbir)
            if mbir != b'drop-me': dëggu_xëyma.sendto(mbir, Nàttangoo_xëyma)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            masin = luy_feeñ_te_jëmmadi_masin(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                masin.ndigel('apps', ['hello', 'udp', 'netcheck', 'stress'])
                masin.ndigel('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                masin.ndigel('run missing', ['Exit: -2'])
                masin.ndigel('net', ['NET RTL8139'])
                masin.ndigel('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Këmb_xëyma in ('hello-network', 'odd', 'even', 'repeat-123'):
                    masin.ndigel('run udp 10.0.2.2 {} {}'.format(jël_xëyma, Këmb_xëyma), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Këmb_xëyma.encode() in 받은것, 'dalal 서버에서 자료를 받지 못함'
                masin.ndigel('run stress {}'.format(jël_xëyma), ['UDP STRESS PASS', 'Exit: 0'])
                masin.ndigel('run udp 10.0.2.2 {} drop-me'.format(jël_xëyma), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                masin.ndigel('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = masin.làq_Dënk.decode('utf-8', 'replace')
                print('PASS: {} kiy_jariñoo_internet ELF/ring 3/인수/UDP dalal 왕복/시간 초과/Wëreef 복귀'.format(종류), flush=True)
            finally:
                try: masin.ndigel('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(masin.làq_Dënk)
                masin.Tej()
        masin = luy_feeñ_te_jëmmadi_masin(위치 / 'build/kernel.elf', mbaal_xëyma=False)
        try:
            masin.ndigel('net', ['NET unavailable'])
            masin.ndigel('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            masin.ndigel('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = masin.làq_Dënk.decode()
        finally: masin.Tej()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            masin = luy_feeñ_te_jëmmadi_masin(보호커널(Path(임시)), mbaal_xëyma=False)
            try:
                for tur_253d1510, nekkin_xëyma in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    masin.ndigel('run ' + tur_253d1510, ['Exit: ' + str(nekkin_xëyma)])
                    masin.ndigel('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = masin.làq_Dënk.decode()
                print('PASS: kiy_jariñoo_internet fatlekookaay_mbir/jumtukaay_jël 격리, 잘못된 joxañukaay/ELF, CPU 예외, 무한 baamtu_xëyma 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(masin.làq_Dënk)
                masin.Tej()
    finally:
        Génn_jëfekaay.set()
        일꾼.join(timeout=2)
        dëggu_xëyma.close()
    결과['host_udp_received'] = [{'length': len(mbir), 'sha256': hashlib.sha256(mbir).hexdigest()} for mbir in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    def_ndigel()
