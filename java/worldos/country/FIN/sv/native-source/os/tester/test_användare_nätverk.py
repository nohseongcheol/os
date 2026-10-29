#!/usr/bin/env python3
"""verklig_data ring 3 ELF/värd UDP 왕복/skydda_värde fel/tid_värde 제한/잘못된 ELF를 검증한다."""
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

position = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, sökväg_2, variant_värde='elf', nätverk_värde=True, minne_medel=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Katalog_värde = Path(self.임시.name)
        self.LOG_POST = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.övervaka_värde = socket.socket(socket.AF_UNIX)
        직렬경로, övervaka_väg = Katalog_värde / 'serial.sock', Katalog_värde / 'monitor.sock'
        kommando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(övervaka_väg) + ',server,nowait']
        kommando += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if nätverk_värde else ['-net', 'none']
        kommando += ['-kernel', str(sökväg_2)] if variant_värde == 'elf' else ['-cdrom', str(sökväg_2), '-boot', 'd']
        if minne_medel is not None:
            kommando += ['-drive', 'file=' + str(minne_medel) + ',format=raw,if=ide,index=0']
        self.Process_värde = subprocess.Popen(kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and övervaka_väg.exists()):
                if self.Process_värde.poll() is not None:
                    raise AssertionError(self.Process_värde.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Kör tid_värde 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.övervaka_värde.connect(str(övervaka_väg))
            self.직렬.setblocking(False)
            self.övervaka_värde.sendall(b'cont\n')
            self.tillståndet_Vänta('jkoros> ')
        except BaseException:
            self.Stäng()
            raise

    def tillståndet_Vänta(self, 문구, Kör=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_POST[Kör:]:
                return self.LOG_POST[Kör:].decode('utf-8', 'replace')
            Läs, _, _ = select.select([self.직렬], [], [], 0.1)
            if Läs:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_POST.extend(data)
            if self.Process_värde.poll() is not None: break
        raise AssertionError('vänta_värde fel_värde: ' + 문구 + '\n' + self.LOG_POST.decode('utf-8', 'replace'))

    def kommando(self, sträng_värde, 기대):
        Kör = len(self.LOG_POST)
        self.직렬.sendall((sträng_värde + '\n').encode())
        RESULTAT = self.tillståndet_Vänta('jkoros> ', Kör)
        for 문구 in 기대:
            assert 문구 in RESULTAT, (sträng_värde, 문구, RESULTAT)
        assert 'PANIC' not in RESULTAT, RESULTAT
        return RESULTAT

    def Stäng(self):
        self.직렬.close()
        self.övervaka_värde.close()
        if self.Process_värde.poll() is None:
            self.Process_värde.terminate()
            try: self.Process_värde.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Process_värde.kill()
                self.Process_värde.wait()
        self.Process_värde.communicate()
        self.임시.cleanup()


def 보호커널(Katalog_värde):
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
    항목들 = ['hello=' + str(position / 'build/apps/hello.elf')]
    for Namn, Innehåll_värde in 사례들.items():
        källfil = Katalog_värde / (Namn + '.s')
        källfil.write_text('.code32\n.text\n.globl _start\n_start:\n' + Innehåll_värde +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Katalog_värde / (Namn + '.o')), str(källfil)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position.parent / 'compiler/användare_Länk_Layout.ld'),
                        '-o', str(Katalog_värde / (Namn + '.elf')), str(Katalog_värde / (Namn + '.o'))], check=True)
        항목들.append(Namn + '=' + str(Katalog_värde / (Namn + '.elf')))
    informationsteknik_normal = bytearray((position / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ogiltig_KR = bytearray(informationsteknik_normal); ogiltig_KR[0] = 0; 변형들['badelf'] = ogiltig_KR
    ogiltig_KR = bytearray(informationsteknik_normal); struct.pack_into('<I', ogiltig_KR, 24, 0x00100000); 변형들['badentry'] = ogiltig_KR
    ogiltig_KR = bytearray(informationsteknik_normal); struct.pack_into('<I', ogiltig_KR, 28, 0x7fffffff); 변형들['badtable'] = ogiltig_KR
    ogiltig_KR = bytearray(informationsteknik_normal); LETAUPP_tabell = struct.unpack_from('<I', ogiltig_KR, 28)[0]
    struct.pack_into('<I', ogiltig_KR, LETAUPP_tabell + 20, 0x7fffffff); 변형들['badsize'] = ogiltig_KR
    for Namn, data in 변형들.items():
        filnamn = Katalog_värde / (Namn + '.elf'); filnamn.write_bytes(data)
        항목들.append(Namn + '=' + str(filnamn))
    subprocess.run([sys.executable, str(position / 'verktyg/BIND_deltagare.py'), '-o', str(Katalog_värde / 'apps.bin')] + 항목들, check=True)
    källfil = Katalog_värde / 'apps.s'
    källfil.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Katalog_värde / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Katalog_värde / 'apps.o'), str(källfil)], check=True)
    kärna_värde = Katalog_värde / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position / 'maskinstart/länkningslayout.ld'), '-o', str(kärna_värde),
                    str(position / 'build/boot.o'), str(position / 'build/java.o'), str(position / 'build/user.o'), str(Katalog_värde / 'apps.o')], check=True)
    return kärna_värde


def köra_kommando():
    RESULTAT = {}
    server_värde = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_värde.bind(('127.0.0.1', 0))
    server_värde.settimeout(0.1)
    port_värde = server_värde.getsockname()[1]
    BELOPP_objekt = []
    Utgång_app = threading.Event()
    def UppdateraSkärm_svara():
        while not Utgång_app.is_set():
            try: data, peer_värde = server_värde.recvfrom(4096)
            except socket.timeout: continue
            BELOPP_objekt.append(data)
            if data != b'drop-me': server_värde.sendto(data, peer_värde)
    arbete_värde = threading.Thread(target=UppdateraSkärm_svara, daemon=True)
    arbete_värde.start()
    try:
        for variant_värde in ('elf', 'iso'):
            dator = VM(position / ('build/kernel.elf' if variant_värde == 'elf' else 'build/kernel.iso'), variant_värde)
            try:
                dator.kommando('apps', ['hello', 'udp', 'netcheck', 'stress'])
                dator.kommando('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                dator.kommando('run missing', ['Exit: -2'])
                dator.kommando('net', ['NET RTL8139'])
                dator.kommando('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Innehåll_värde in ('hello-network', 'odd', 'even', 'repeat-123'):
                    dator.kommando('run udp 10.0.2.2 {} {}'.format(port_värde, Innehåll_värde), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Innehåll_värde.encode() in BELOPP_objekt, 'värd 서버에서 자료를 받지 못함'
                dator.kommando('run stress {}'.format(port_värde), ['UDP STRESS PASS', 'Exit: 0'])
                dator.kommando('run udp 10.0.2.2 {} drop-me'.format(port_värde), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                dator.kommando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                RESULTAT[variant_värde] = dator.LOG_POST.decode('utf-8', 'replace')
                print('PASS: {} användarutrymme ELF/ring 3/argument/UDP värd 왕복/tid_värde 초과/Shell 복귀'.format(variant_värde), flush=True)
            finally:
                try: dator.kommando('net', [])
                except Exception: pass
                (position / 'build/사용자통신-last.log').write_bytes(dator.LOG_POST)
                dator.Stäng()
        dator = VM(position / 'build/kernel.elf', nätverk_värde=False)
        try:
            dator.kommando('net', ['NET unavailable'])
            dator.kommando('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            dator.kommando('run hello', ['USER MODE ring 3', 'Exit: 0'])
            RESULTAT['no_nic'] = dator.LOG_POST.decode()
        finally: dator.Stäng()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            dator = VM(보호커널(Path(임시)), nätverk_värde=False)
            try:
                for Namn, status_värde in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    dator.kommando('run ' + Namn, ['Exit: ' + str(status_värde)])
                    dator.kommando('run hello', ['USER MODE ring 3', 'Exit: 0'])
                RESULTAT['protection'] = dator.LOG_POST.decode()
                print('PASS: användarutrymme Minne_data/maskinvara_port 격리, 잘못된 markör/ELF, CPU fel_31f743d2, 무한 sprint_värde 제한', flush=True)
            finally:
                (position / 'build/Säkerhet_test-last.log').write_bytes(dator.LOG_POST)
                dator.Stäng()
    finally:
        Utgång_app.set()
        arbete_värde.join(timeout=2)
        server_värde.close()
    RESULTAT['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in BELOPP_objekt]
    (position / 'build/test_användare_nätverk.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    köra_kommando()
