#!/usr/bin/env python3
"""tegelik_andmed ring 3 ELF/host UDP 왕복/kaitsma_VALUE VIGA/Aeg_VALUE 제한/잘못된 ELF를 검증한다."""
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

Asukoht = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, RADA, 종류='elf', võrk_VALUE=True, salvesti_kandja=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        kaust_VALUE = Path(self.임시.name)
        self.LOG_kirje = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.kuvar_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, kuvar_tee = kaust_VALUE / 'serial.sock', kaust_VALUE / 'monitor.sock'
        Käsk = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(kuvar_tee) + ',server,nowait']
        Käsk += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if võrk_VALUE else ['-net', 'none']
        Käsk += ['-kernel', str(RADA)] if 종류 == 'elf' else ['-cdrom', str(RADA), '-boot', 'd']
        if salvesti_kandja is not None:
            Käsk += ['-drive', 'file=' + str(salvesti_kandja) + ',format=raw,if=ide,index=0']
        self.Joonis_VALUE = subprocess.Popen(Käsk, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and kuvar_tee.exists()):
                if self.Joonis_VALUE.poll() is not None:
                    raise AssertionError(self.Joonis_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Käivita_2 Aeg_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.kuvar_VALUE.connect(str(kuvar_tee))
            self.직렬.setblocking(False)
            self.kuvar_VALUE.sendall(b'cont\n')
            self.ooteolek('jkoros> ')
        except BaseException:
            self.Suletud()
            raise

    def ooteolek(self, 문구, Käivita_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_kirje[Käivita_2:]:
                return self.LOG_kirje[Käivita_2:].decode('utf-8', 'replace')
            Lugemine, _, _ = select.select([self.직렬], [], [], 0.1)
            if Lugemine:
                andmed = self.직렬.recv(65536)
                if not andmed: break
                self.LOG_kirje.extend(andmed)
            if self.Joonis_VALUE.poll() is not None: break
        raise AssertionError('Oota_VALUE tõrge_VALUE: ' + 문구 + '\n' + self.LOG_kirje.decode('utf-8', 'replace'))

    def Käsk(self, string_VALUE, 기대):
        Käivita_2 = len(self.LOG_kirje)
        self.직렬.sendall((string_VALUE + '\n').encode())
        TULEMUS = self.ooteolek('jkoros> ', Käivita_2)
        for 문구 in 기대:
            assert 문구 in TULEMUS, (string_VALUE, 문구, TULEMUS)
        assert 'PANIC' not in TULEMUS, TULEMUS
        return TULEMUS

    def Suletud(self):
        self.직렬.close()
        self.kuvar_VALUE.close()
        if self.Joonis_VALUE.poll() is None:
            self.Joonis_VALUE.terminate()
            try: self.Joonis_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Joonis_VALUE.kill()
                self.Joonis_VALUE.wait()
        self.Joonis_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(kaust_VALUE):
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
    항목들 = ['hello=' + str(Asukoht / 'build/apps/hello.elf')]
    for Nimi_2, Sisu_VALUE in 사례들.items():
        ALLIKAS = kaust_VALUE / (Nimi_2 + '.s')
        ALLIKAS.write_text('.code32\n.text\n.globl _start\n_start:\n' + Sisu_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(kaust_VALUE / (Nimi_2 + '.o')), str(ALLIKAS)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Asukoht.parent / 'compiler/kasutaja_Link_küljend.ld'),
                        '-o', str(kaust_VALUE / (Nimi_2 + '.elf')), str(kaust_VALUE / (Nimi_2 + '.o'))], check=True)
        항목들.append(Nimi_2 + '=' + str(kaust_VALUE / (Nimi_2 + '.elf')))
    정상 = bytearray((Asukoht / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    kehtetu_näitaja = bytearray(정상); kehtetu_näitaja[0] = 0; 변형들['badelf'] = kehtetu_näitaja
    kehtetu_näitaja = bytearray(정상); struct.pack_into('<I', kehtetu_näitaja, 24, 0x00100000); 변형들['badentry'] = kehtetu_näitaja
    kehtetu_näitaja = bytearray(정상); struct.pack_into('<I', kehtetu_näitaja, 28, 0x7fffffff); 변형들['badtable'] = kehtetu_näitaja
    kehtetu_näitaja = bytearray(정상); LOOKUP_tabel = struct.unpack_from('<I', kehtetu_näitaja, 28)[0]
    struct.pack_into('<I', kehtetu_näitaja, LOOKUP_tabel + 20, 0x7fffffff); 변형들['badsize'] = kehtetu_näitaja
    for Nimi_2, andmed in 변형들.items():
        Fail = kaust_VALUE / (Nimi_2 + '.elf'); Fail.write_bytes(andmed)
        항목들.append(Nimi_2 + '=' + str(Fail))
    subprocess.run([sys.executable, str(Asukoht / 'Tööriistad/BIND_osaleja.py'), '-o', str(kaust_VALUE / 'apps.bin')] + 항목들, check=True)
    ALLIKAS = kaust_VALUE / 'apps.s'
    ALLIKAS.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(kaust_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(kaust_VALUE / 'apps.o'), str(ALLIKAS)], check=True)
    tuum_VALUE = kaust_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Asukoht / '부팅/Link_küljend.ld'), '-o', str(tuum_VALUE),
                    str(Asukoht / 'build/boot.o'), str(Asukoht / 'build/java.o'), str(Asukoht / 'build/user.o'), str(kaust_VALUE / 'apps.o')], check=True)
    return tuum_VALUE


def Täida_käsk():
    TULEMUS = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_kaup = []
    Välju_programm = threading.Event()
    def kaja_vastus():
        while not Välju_programm.is_set():
            try: andmed, partner_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_kaup.append(andmed)
            if andmed != b'drop-me': server_VALUE.sendto(andmed, partner_VALUE)
    töötaja_VALUE = threading.Thread(target=kaja_vastus, daemon=True)
    töötaja_VALUE.start()
    try:
        for 종류 in ('elf', 'iso'):
            arvuti = VM(Asukoht / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                arvuti.Käsk('apps', ['hello', 'udp', 'netcheck', 'stress'])
                arvuti.Käsk('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                arvuti.Käsk('run missing', ['Exit: -2'])
                arvuti.Käsk('net', ['NET RTL8139'])
                arvuti.Käsk('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Sisu_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    arvuti.Käsk('run udp 10.0.2.2 {} {}'.format(port_VALUE, Sisu_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Sisu_VALUE.encode() in RECEIVED_kaup, 'host 서버에서 자료를 받지 못함'
                arvuti.Käsk('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                arvuti.Käsk('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                arvuti.Käsk('run hello recovered', ['arg: recovered', 'Exit: 0'])
                TULEMUS[종류] = arvuti.LOG_kirje.decode('utf-8', 'replace')
                print('PASS: {} kasutaja ELF/ring 3/Argumendid/UDP host 왕복/Aeg_VALUE 초과/kest 복귀'.format(종류), flush=True)
            finally:
                try: arvuti.Käsk('net', [])
                except Exception: pass
                (Asukoht / 'build/사용자통신-last.log').write_bytes(arvuti.LOG_kirje)
                arvuti.Suletud()
        arvuti = VM(Asukoht / 'build/kernel.elf', võrk_VALUE=False)
        try:
            arvuti.Käsk('net', ['NET unavailable'])
            arvuti.Käsk('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            arvuti.Käsk('run hello', ['USER MODE ring 3', 'Exit: 0'])
            TULEMUS['no_nic'] = arvuti.LOG_kirje.decode()
        finally: arvuti.Suletud()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            arvuti = VM(보호커널(Path(임시)), võrk_VALUE=False)
            try:
                for Nimi_2, Olek_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    arvuti.Käsk('run ' + Nimi_2, ['Exit: ' + str(Olek_VALUE)])
                    arvuti.Käsk('run hello', ['USER MODE ring 3', 'Exit: 0'])
                TULEMUS['protection'] = arvuti.LOG_kirje.decode()
                print('PASS: kasutaja Mälu_andmed/포트 격리, 잘못된 kursor/ELF, CPU erand, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (Asukoht / 'build/보호시험-last.log').write_bytes(arvuti.LOG_kirje)
                arvuti.Suletud()
    finally:
        Välju_programm.set()
        töötaja_VALUE.join(timeout=2)
        server_VALUE.close()
    TULEMUS['host_udp_received'] = [{'length': len(andmed), 'sha256': hashlib.sha256(andmed).hexdigest()} for andmed in RECEIVED_kaup]
    (Asukoht / 'build/사용자통신시험.json').write_text(json.dumps(TULEMUS, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Täida_käsk()
