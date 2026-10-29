#!/usr/bin/env python3
"""iarbhír_sonraí ring 3 ELF/óstach UDP 왕복/cosain_VALUE ERREÁID/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

suíomh = Path(__file__).resolve().parents[1]


class fíorúil_meaisín:
    def __init__(self, CONAIR, 종류='elf', Líonra_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        eolaire_VALUE = Path(self.임시.name)
        self.LOG_ró = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monatóir_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monatóir_cosán = eolaire_VALUE / 'serial.sock', eolaire_VALUE / 'monitor.sock'
        Ordú = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monatóir_cosán) + ',server,nowait']
        Ordú += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Líonra_VALUE else ['-net', 'none']
        Ordú += ['-kernel', str(CONAIR)] if 종류 == 'elf' else ['-cdrom', str(CONAIR), '-boot', 'd']
        if 저장매체 is not None:
            Ordú += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Próiseas_VALUE = subprocess.Popen(Ordú, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monatóir_cosán.exists()):
                if self.Próiseas_VALUE.poll() is not None:
                    raise AssertionError(self.Próiseas_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Rith_2 TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monatóir_VALUE.connect(str(monatóir_cosán))
            self.직렬.setblocking(False)
            self.monatóir_VALUE.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Dún()
            raise

    def 기다림(self, 문구, Rith_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_ró[Rith_2:]:
                return self.LOG_ró[Rith_2:].decode('utf-8', 'replace')
            Léigh, _, _ = select.select([self.직렬], [], [], 0.1)
            if Léigh:
                sonraí = self.직렬.recv(65536)
                if not sonraí: break
                self.LOG_ró.extend(sonraí)
            if self.Próiseas_VALUE.poll() is not None: break
        raise AssertionError('대기 teip_VALUE: ' + 문구 + '\n' + self.LOG_ró.decode('utf-8', 'replace'))

    def Ordú(self, teaghrán_VALUE, 기대):
        Rith_2 = len(self.LOG_ró)
        self.직렬.sendall((teaghrán_VALUE + '\n').encode())
        tomhas = self.기다림('jkoros> ', Rith_2)
        for 문구 in 기대:
            assert 문구 in tomhas, (teaghrán_VALUE, 문구, tomhas)
        assert 'PANIC' not in tomhas, tomhas
        return tomhas

    def Dún(self):
        self.직렬.close()
        self.monatóir_VALUE.close()
        if self.Próiseas_VALUE.poll() is None:
            self.Próiseas_VALUE.terminate()
            try: self.Próiseas_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Próiseas_VALUE.kill()
                self.Próiseas_VALUE.wait()
        self.Próiseas_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(eolaire_VALUE):
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
    항목들 = ['hello=' + str(suíomh / 'build/apps/hello.elf')]
    for Ainm, Inneachar_VALUE in 사례들.items():
        FOINSE = eolaire_VALUE / (Ainm + '.s')
        FOINSE.write_text('.code32\n.text\n.globl _start\n_start:\n' + Inneachar_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(eolaire_VALUE / (Ainm + '.o')), str(FOINSE)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(suíomh.parent / 'compiler/úsáideoir_Nasc_dáileadh.ld'),
                        '-o', str(eolaire_VALUE / (Ainm + '.elf')), str(eolaire_VALUE / (Ainm + '.o'))], check=True)
        항목들.append(Ainm + '=' + str(eolaire_VALUE / (Ainm + '.elf')))
    정상 = bytearray((suíomh / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    neamhbhailí_tomhas = bytearray(정상); neamhbhailí_tomhas[0] = 0; 변형들['badelf'] = neamhbhailí_tomhas
    neamhbhailí_tomhas = bytearray(정상); struct.pack_into('<I', neamhbhailí_tomhas, 24, 0x00100000); 변형들['badentry'] = neamhbhailí_tomhas
    neamhbhailí_tomhas = bytearray(정상); struct.pack_into('<I', neamhbhailí_tomhas, 28, 0x7fffffff); 변형들['badtable'] = neamhbhailí_tomhas
    neamhbhailí_tomhas = bytearray(정상); LOOKUP_tábla = struct.unpack_from('<I', neamhbhailí_tomhas, 28)[0]
    struct.pack_into('<I', neamhbhailí_tomhas, LOOKUP_tábla + 20, 0x7fffffff); 변형들['badsize'] = neamhbhailí_tomhas
    for Ainm, sonraí in 변형들.items():
        Comhad = eolaire_VALUE / (Ainm + '.elf'); Comhad.write_bytes(sonraí)
        항목들.append(Ainm + '=' + str(Comhad))
    subprocess.run([sys.executable, str(suíomh / 'Uirlisí/묶기.py'), '-o', str(eolaire_VALUE / 'apps.bin')] + 항목들, check=True)
    FOINSE = eolaire_VALUE / 'apps.s'
    FOINSE.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(eolaire_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(eolaire_VALUE / 'apps.o'), str(FOINSE)], check=True)
    eithne_VALUE = eolaire_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(suíomh / '부팅/Nasc_dáileadh.ld'), '-o', str(eithne_VALUE),
                    str(suíomh / 'build/boot.o'), str(suíomh / 'build/java.o'), str(suíomh / 'build/user.o'), str(eolaire_VALUE / 'apps.o')], check=True)
    return eithne_VALUE


def Rith_ordú():
    tomhas = {}
    freastalaí_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    freastalaí_VALUE.bind(('127.0.0.1', 0))
    freastalaí_VALUE.settimeout(0.1)
    port_VALUE = freastalaí_VALUE.getsockname()[1]
    RECEIVED_mír = []
    scoir_clár = threading.Event()
    def 되보내기():
        while not scoir_clár.is_set():
            try: sonraí, piara_VALUE = freastalaí_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_mír.append(sonraí)
            if sonraí != b'drop-me': freastalaí_VALUE.sendto(sonraí, piara_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            meaisín = fíorúil_meaisín(suíomh / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                meaisín.Ordú('apps', ['hello', 'udp', 'netcheck', 'stress'])
                meaisín.Ordú('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                meaisín.Ordú('run missing', ['Exit: -2'])
                meaisín.Ordú('net', ['NET RTL8139'])
                meaisín.Ordú('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Inneachar_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    meaisín.Ordú('run udp 10.0.2.2 {} {}'.format(port_VALUE, Inneachar_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Inneachar_VALUE.encode() in RECEIVED_mír, 'óstach 서버에서 자료를 받지 못함'
                meaisín.Ordú('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                meaisín.Ordú('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                meaisín.Ordú('run hello recovered', ['arg: recovered', 'Exit: 0'])
                tomhas[종류] = meaisín.LOG_ró.decode('utf-8', 'replace')
                print('PASS: {} úsáideoir ELF/ring 3/Argóintí/UDP óstach 왕복/TIME_VALUE 초과/blaosc 복귀'.format(종류), flush=True)
            finally:
                try: meaisín.Ordú('net', [])
                except Exception: pass
                (suíomh / 'build/사용자통신-last.log').write_bytes(meaisín.LOG_ró)
                meaisín.Dún()
        meaisín = fíorúil_meaisín(suíomh / 'build/kernel.elf', Líonra_VALUE=False)
        try:
            meaisín.Ordú('net', ['NET unavailable'])
            meaisín.Ordú('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            meaisín.Ordú('run hello', ['USER MODE ring 3', 'Exit: 0'])
            tomhas['no_nic'] = meaisín.LOG_ró.decode()
        finally: meaisín.Dún()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            meaisín = fíorúil_meaisín(보호커널(Path(임시)), Líonra_VALUE=False)
            try:
                for Ainm, staid_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    meaisín.Ordú('run ' + Ainm, ['Exit: ' + str(staid_VALUE)])
                    meaisín.Ordú('run hello', ['USER MODE ring 3', 'Exit: 0'])
                tomhas['protection'] = meaisín.LOG_ró.decode()
                print('PASS: úsáideoir Cuimhne_sonraí/포트 격리, 잘못된 pointeoir/ELF, CPU eisceacht, 무한 atriall_VALUE 제한', flush=True)
            finally:
                (suíomh / 'build/보호시험-last.log').write_bytes(meaisín.LOG_ró)
                meaisín.Dún()
    finally:
        scoir_clár.set()
        일꾼.join(timeout=2)
        freastalaí_VALUE.close()
    tomhas['host_udp_received'] = [{'length': len(sonraí), 'sha256': hashlib.sha256(sonraí).hexdigest()} for sonraí in RECEIVED_mír]
    (suíomh / 'build/사용자통신시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Rith_ordú()
