#!/usr/bin/env python3
"""hakyky_maglumat ring 3 ELF/esasy UDP 왕복/gora_baha Hata/시간 제한/잘못된 ELF를 검증한다."""
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


class hyýaly_kompýuter:
    def __init__(self, Ýol, 종류='elf', Tor_baha=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        katalog_baha = Path(self.임시.name)
        self.hasaba_alyş_setir = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_baha = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_ýol = katalog_baha / 'serial.sock', katalog_baha / 'monitor.sock'
        buýruk = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_ýol) + ',server,nowait']
        buýruk += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Tor_baha else ['-net', 'none']
        buýruk += ['-kernel', str(Ýol)] if 종류 == 'elf' else ['-cdrom', str(Ýol), '-boot', 'd']
        if 저장매체 is not None:
            buýruk += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Proses_baha = subprocess.Popen(buýruk, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_ýol.exists()):
                if self.Proses_baha.poll() is not None:
                    raise AssertionError(self.Proses_baha.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Bitir 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_baha.connect(str(monitor_ýol))
            self.직렬.setblocking(False)
            self.monitor_baha.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Ýap()
            raise

    def 기다림(self, 문구, Bitir=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.hasaba_alyş_setir[Bitir:]:
                return self.hasaba_alyş_setir[Bitir:].decode('utf-8', 'replace')
            Oka, _, _ = select.select([self.직렬], [], [], 0.1)
            if Oka:
                maglumat = self.직렬.recv(65536)
                if not maglumat: break
                self.hasaba_alyş_setir.extend(maglumat)
            if self.Proses_baha.poll() is not None: break
        raise AssertionError('대기 näsazlyk_baha: ' + 문구 + '\n' + self.hasaba_alyş_setir.decode('utf-8', 'replace'))

    def buýruk(self, setir_baha_6ca8363c, 기대):
        Bitir = len(self.hasaba_alyş_setir)
        self.직렬.sendall((setir_baha_6ca8363c + '\n').encode())
        결과 = self.기다림('jkoros> ', Bitir)
        for 문구 in 기대:
            assert 문구 in 결과, (setir_baha_6ca8363c, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Ýap(self):
        self.직렬.close()
        self.monitor_baha.close()
        if self.Proses_baha.poll() is None:
            self.Proses_baha.terminate()
            try: self.Proses_baha.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proses_baha.kill()
                self.Proses_baha.wait()
        self.Proses_baha.communicate()
        self.임시.cleanup()


def 보호커널(katalog_baha):
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
    for Ad, Mazmun_baha in 사례들.items():
        Çeşme = katalog_baha / (Ad + '.s')
        Çeşme.write_text('.code32\n.text\n.globl _start\n_start:\n' + Mazmun_baha +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(katalog_baha / (Ad + '.o')), str(Çeşme)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/ulanyjy_Bag_Ýerleşiş.ld'),
                        '-o', str(katalog_baha / (Ad + '.elf')), str(katalog_baha / (Ad + '.o'))], check=True)
        항목들.append(Ad + '=' + str(katalog_baha / (Ad + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Ad, maglumat in 변형들.items():
        Faýl = katalog_baha / (Ad + '.elf'); Faýl.write_bytes(maglumat)
        항목들.append(Ad + '=' + str(Faýl))
    subprocess.run([sys.executable, str(위치 / 'Gurallar/묶기.py'), '-o', str(katalog_baha / 'apps.bin')] + 항목들, check=True)
    Çeşme = katalog_baha / 'apps.s'
    Çeşme.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(katalog_baha / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(katalog_baha / 'apps.o'), str(Çeşme)], check=True)
    ýadro_baha = katalog_baha / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Bag_Ýerleşiş.ld'), '-o', str(ýadro_baha),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(katalog_baha / 'apps.o')], check=True)
    return ýadro_baha


def ýerine_ýetir_buýruk():
    결과 = {}
    serwer_baha = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serwer_baha.bind(('127.0.0.1', 0))
    serwer_baha.settimeout(0.1)
    port_baha = serwer_baha.getsockname()[1]
    받은것 = []
    çyk_programma = threading.Event()
    def 되보내기():
        while not çyk_programma.is_set():
            try: maglumat, deň_derejeli_düwün_baha = serwer_baha.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(maglumat)
            if maglumat != b'drop-me': serwer_baha.sendto(maglumat, deň_derejeli_düwün_baha)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            kompýuter = hyýaly_kompýuter(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                kompýuter.buýruk('apps', ['hello', 'udp', 'netcheck', 'stress'])
                kompýuter.buýruk('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                kompýuter.buýruk('run missing', ['Exit: -2'])
                kompýuter.buýruk('net', ['NET RTL8139'])
                kompýuter.buýruk('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Mazmun_baha in ('hello-network', 'odd', 'even', 'repeat-123'):
                    kompýuter.buýruk('run udp 10.0.2.2 {} {}'.format(port_baha, Mazmun_baha), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Mazmun_baha.encode() in 받은것, 'esasy 서버에서 자료를 받지 못함'
                kompýuter.buýruk('run stress {}'.format(port_baha), ['UDP STRESS PASS', 'Exit: 0'])
                kompýuter.buýruk('run udp 10.0.2.2 {} drop-me'.format(port_baha), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                kompýuter.buýruk('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = kompýuter.hasaba_alyş_setir.decode('utf-8', 'replace')
                print('PASS: {} ulanyjy ELF/ring 3/인수/UDP esasy 왕복/시간 초과/gabyjak 복귀'.format(종류), flush=True)
            finally:
                try: kompýuter.buýruk('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(kompýuter.hasaba_alyş_setir)
                kompýuter.Ýap()
        kompýuter = hyýaly_kompýuter(위치 / 'build/kernel.elf', Tor_baha=False)
        try:
            kompýuter.buýruk('net', ['NET unavailable'])
            kompýuter.buýruk('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            kompýuter.buýruk('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = kompýuter.hasaba_alyş_setir.decode()
        finally: kompýuter.Ýap()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            kompýuter = hyýaly_kompýuter(보호커널(Path(임시)), Tor_baha=False)
            try:
                for Ad, ýagdaý_baha in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    kompýuter.buýruk('run ' + Ad, ['Exit: ' + str(ýagdaý_baha)])
                    kompýuter.buýruk('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = kompýuter.hasaba_alyş_setir.decode()
                print('PASS: ulanyjy ýat_maglumat/포트 격리, 잘못된 görkeziji/ELF, CPU 예외, 무한 iterasiýa_baha 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(kompýuter.hasaba_alyş_setir)
                kompýuter.Ýap()
    finally:
        çyk_programma.set()
        일꾼.join(timeout=2)
        serwer_baha.close()
    결과['host_udp_received'] = [{'length': len(maglumat), 'sha256': hashlib.sha256(maglumat).hexdigest()} for maglumat in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ýerine_ýetir_buýruk()
