#!/usr/bin/env python3
"""faktiki_verilənlər ring 3 ELF/host UDP 왕복/qorumaq_VALUE XƏTA/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

yerinə_qoymaq = Path(__file__).resolve().parents[1]


class virtual_maşın:
    def __init__(self, Cığır, 종류='elf', Şəbəkə_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        kataloq_VALUE = Path(self.임시.name)
        self.LOG_yaz = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_yol = kataloq_VALUE / 'serial.sock', kataloq_VALUE / 'monitor.sock'
        Əmr = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_yol) + ',server,nowait']
        Əmr += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Şəbəkə_VALUE else ['-net', 'none']
        Əmr += ['-kernel', str(Cığır)] if 종류 == 'elf' else ['-cdrom', str(Cığır), '-boot', 'd']
        if 저장매체 is not None:
            Əmr += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Proses_VALUE = subprocess.Popen(Əmr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_yol.exists()):
                if self.Proses_VALUE.poll() is not None:
                    raise AssertionError(self.Proses_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU İcra_Et TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_yol))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.gözlə_vəziyyət('jkoros> ')
        except BaseException:
            self.Bağla()
            raise

    def gözlə_vəziyyət(self, 문구, İcra_Et=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_yaz[İcra_Et:]:
                return self.LOG_yaz[İcra_Et:].decode('utf-8', 'replace')
            Oxuma, _, _ = select.select([self.직렬], [], [], 0.1)
            if Oxuma:
                verilənlər = self.직렬.recv(65536)
                if not verilənlər: break
                self.LOG_yaz.extend(verilənlər)
            if self.Proses_VALUE.poll() is not None: break
        raise AssertionError('gözlə_VALUE xəta_VALUE: ' + 문구 + '\n' + self.LOG_yaz.decode('utf-8', 'replace'))

    def Əmr(self, sətir_VALUE, 기대):
        İcra_Et = len(self.LOG_yaz)
        self.직렬.sendall((sətir_VALUE + '\n').encode())
        ölçü = self.gözlə_vəziyyət('jkoros> ', İcra_Et)
        for 문구 in 기대:
            assert 문구 in ölçü, (sətir_VALUE, 문구, ölçü)
        assert 'PANIC' not in ölçü, ölçü
        return ölçü

    def Bağla(self):
        self.직렬.close()
        self.monitor_VALUE.close()
        if self.Proses_VALUE.poll() is None:
            self.Proses_VALUE.terminate()
            try: self.Proses_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proses_VALUE.kill()
                self.Proses_VALUE.wait()
        self.Proses_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(kataloq_VALUE):
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
    항목들 = ['hello=' + str(yerinə_qoymaq / 'build/apps/hello.elf')]
    for Ad, Məzmun_VALUE in 사례들.items():
        QAYNAQ = kataloq_VALUE / (Ad + '.s')
        QAYNAQ.write_text('.code32\n.text\n.globl _start\n_start:\n' + Məzmun_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(kataloq_VALUE / (Ad + '.o')), str(QAYNAQ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(yerinə_qoymaq.parent / 'compiler/istifadəçi_keçid_Düzüm.ld'),
                        '-o', str(kataloq_VALUE / (Ad + '.elf')), str(kataloq_VALUE / (Ad + '.o'))], check=True)
        항목들.append(Ad + '=' + str(kataloq_VALUE / (Ad + '.elf')))
    정상 = bytearray((yerinə_qoymaq / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    yanlış_ölçü = bytearray(정상); yanlış_ölçü[0] = 0; 변형들['badelf'] = yanlış_ölçü
    yanlış_ölçü = bytearray(정상); struct.pack_into('<I', yanlış_ölçü, 24, 0x00100000); 변형들['badentry'] = yanlış_ölçü
    yanlış_ölçü = bytearray(정상); struct.pack_into('<I', yanlış_ölçü, 28, 0x7fffffff); 변형들['badtable'] = yanlış_ölçü
    yanlış_ölçü = bytearray(정상); LOOKUP_cədvəl = struct.unpack_from('<I', yanlış_ölçü, 28)[0]
    struct.pack_into('<I', yanlış_ölçü, LOOKUP_cədvəl + 20, 0x7fffffff); 변형들['badsize'] = yanlış_ölçü
    for Ad, verilənlər in 변형들.items():
        FAYL = kataloq_VALUE / (Ad + '.elf'); FAYL.write_bytes(verilənlər)
        항목들.append(Ad + '=' + str(FAYL))
    subprocess.run([sys.executable, str(yerinə_qoymaq / 'Alətlər/묶기.py'), '-o', str(kataloq_VALUE / 'apps.bin')] + 항목들, check=True)
    QAYNAQ = kataloq_VALUE / 'apps.s'
    QAYNAQ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(kataloq_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(kataloq_VALUE / 'apps.o'), str(QAYNAQ)], check=True)
    nüvə_VALUE = kataloq_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(yerinə_qoymaq / '부팅/keçid_Düzüm.ld'), '-o', str(nüvə_VALUE),
                    str(yerinə_qoymaq / 'build/boot.o'), str(yerinə_qoymaq / 'build/java.o'), str(yerinə_qoymaq / 'build/user.o'), str(kataloq_VALUE / 'apps.o')], check=True)
    return nüvə_VALUE


def icra_etmək_əmr():
    ölçü = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_element = []
    Çıxış_proqram = threading.Event()
    def 되보내기():
        while not Çıxış_proqram.is_set():
            try: verilənlər, eynisəviyyəli_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_element.append(verilənlər)
            if verilənlər != b'drop-me': server_VALUE.sendto(verilənlər, eynisəviyyəli_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            maşın = virtual_maşın(yerinə_qoymaq / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                maşın.Əmr('apps', ['hello', 'udp', 'netcheck', 'stress'])
                maşın.Əmr('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                maşın.Əmr('run missing', ['Exit: -2'])
                maşın.Əmr('net', ['NET RTL8139'])
                maşın.Əmr('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Məzmun_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    maşın.Əmr('run udp 10.0.2.2 {} {}'.format(port_VALUE, Məzmun_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Məzmun_VALUE.encode() in RECEIVED_element, 'host 서버에서 자료를 받지 못함'
                maşın.Əmr('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                maşın.Əmr('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                maşın.Əmr('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ölçü[종류] = maşın.LOG_yaz.decode('utf-8', 'replace')
                print('PASS: {} istifadəçi ELF/ring 3/인수/UDP host 왕복/TIME_VALUE 초과/örtük 복귀'.format(종류), flush=True)
            finally:
                try: maşın.Əmr('net', [])
                except Exception: pass
                (yerinə_qoymaq / 'build/사용자통신-last.log').write_bytes(maşın.LOG_yaz)
                maşın.Bağla()
        maşın = virtual_maşın(yerinə_qoymaq / 'build/kernel.elf', Şəbəkə_VALUE=False)
        try:
            maşın.Əmr('net', ['NET unavailable'])
            maşın.Əmr('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            maşın.Əmr('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ölçü['no_nic'] = maşın.LOG_yaz.decode()
        finally: maşın.Bağla()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            maşın = virtual_maşın(보호커널(Path(임시)), Şəbəkə_VALUE=False)
            try:
                for Ad, vəziyyət_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    maşın.Əmr('run ' + Ad, ['Exit: ' + str(vəziyyət_VALUE)])
                    maşın.Əmr('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ölçü['protection'] = maşın.LOG_yaz.decode()
                print('PASS: istifadəçi Yaddaş_verilənlər/포트 격리, 잘못된 göstərici/ELF, CPU istisna, 무한 iterasiya_VALUE 제한', flush=True)
            finally:
                (yerinə_qoymaq / 'build/보호시험-last.log').write_bytes(maşın.LOG_yaz)
                maşın.Bağla()
    finally:
        Çıxış_proqram.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    ölçü['host_udp_received'] = [{'length': len(verilənlər), 'sha256': hashlib.sha256(verilənlər).hexdigest()} for verilənlər in RECEIVED_element]
    (yerinə_qoymaq / 'build/사용자통신시험.json').write_text(json.dumps(ölçü, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    icra_etmək_əmr()
