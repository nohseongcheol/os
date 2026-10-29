#!/usr/bin/env python3
"""benetako_datuak ring 3 ELF/Ostalari UDP 왕복/babestu_balio errorea/ordua_balio 제한/잘못된 ELF를 검증한다."""
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

Posizioa = Path(__file__).resolve().parents[1]


class makina_birtual:
    def __init__(self, Bide_izena, 종류='elf', sare_balio=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        direktorio_balio = Path(self.임시.name)
        self.LOG_marka = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitore_balio = socket.socket(socket.AF_UNIX)
        직렬경로, monitore_bide_izen = direktorio_balio / 'serial.sock', direktorio_balio / 'monitor.sock'
        Komandoa = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitore_bide_izen) + ',server,nowait']
        Komandoa += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if sare_balio else ['-net', 'none']
        Komandoa += ['-kernel', str(Bide_izena)] if 종류 == 'elf' else ['-cdrom', str(Bide_izena), '-boot', 'd']
        if 저장매체 is not None:
            Komandoa += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.prozesu_balio = subprocess.Popen(Komandoa, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitore_bide_izen.exists()):
                if self.prozesu_balio.poll() is not None:
                    raise AssertionError(self.prozesu_balio.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Exekutatu_2 ordua_balio 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitore_balio.connect(str(monitore_bide_izen))
            self.직렬.setblocking(False)
            self.monitore_balio.sendall(b'cont\n')
            self.itxaron_Egoera('jkoros> ')
        except BaseException:
            self.Itxi()
            raise

    def itxaron_Egoera(self, 문구, Exekutatu_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_marka[Exekutatu_2:]:
                return self.LOG_marka[Exekutatu_2:].decode('utf-8', 'replace')
            Irakurri, _, _ = select.select([self.직렬], [], [], 0.1)
            if Irakurri:
                datuak = self.직렬.recv(65536)
                if not datuak: break
                self.LOG_marka.extend(datuak)
            if self.prozesu_balio.poll() is not None: break
        raise AssertionError('itxaron_balio hutsegite_balio: ' + 문구 + '\n' + self.LOG_marka.decode('utf-8', 'replace'))

    def Komandoa(self, kate_balio, 기대):
        Exekutatu_2 = len(self.LOG_marka)
        self.직렬.sendall((kate_balio + '\n').encode())
        EMAITZA = self.itxaron_Egoera('jkoros> ', Exekutatu_2)
        for 문구 in 기대:
            assert 문구 in EMAITZA, (kate_balio, 문구, EMAITZA)
        assert 'PANIC' not in EMAITZA, EMAITZA
        return EMAITZA

    def Itxi(self):
        self.직렬.close()
        self.monitore_balio.close()
        if self.prozesu_balio.poll() is None:
            self.prozesu_balio.terminate()
            try: self.prozesu_balio.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.prozesu_balio.kill()
                self.prozesu_balio.wait()
        self.prozesu_balio.communicate()
        self.임시.cleanup()


def 보호커널(direktorio_balio):
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
    항목들 = ['hello=' + str(Posizioa / 'build/apps/hello.elf')]
    for Izena, eduki_balio in 사례들.items():
        ITURBURUA = direktorio_balio / (Izena + '.s')
        ITURBURUA.write_text('.code32\n.text\n.globl _start\n_start:\n' + eduki_balio +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(direktorio_balio / (Izena + '.o')), str(ITURBURUA)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posizioa.parent / 'compiler/erabiltzaile_lotu_diseinu.ld'),
                        '-o', str(direktorio_balio / (Izena + '.elf')), str(direktorio_balio / (Izena + '.o'))], check=True)
        항목들.append(Izena + '=' + str(direktorio_balio / (Izena + '.elf')))
    정상 = bytearray((Posizioa / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    baliogabe_neurria = bytearray(정상); baliogabe_neurria[0] = 0; 변형들['badelf'] = baliogabe_neurria
    baliogabe_neurria = bytearray(정상); struct.pack_into('<I', baliogabe_neurria, 24, 0x00100000); 변형들['badentry'] = baliogabe_neurria
    baliogabe_neurria = bytearray(정상); struct.pack_into('<I', baliogabe_neurria, 28, 0x7fffffff); 변형들['badtable'] = baliogabe_neurria
    baliogabe_neurria = bytearray(정상); BEGIRATU_taula = struct.unpack_from('<I', baliogabe_neurria, 28)[0]
    struct.pack_into('<I', baliogabe_neurria, BEGIRATU_taula + 20, 0x7fffffff); 변형들['badsize'] = baliogabe_neurria
    for Izena, datuak in 변형들.items():
        Fitxategia = direktorio_balio / (Izena + '.elf'); Fitxategia.write_bytes(datuak)
        항목들.append(Izena + '=' + str(Fitxategia))
    subprocess.run([sys.executable, str(Posizioa / 'Tresnak/lotu_amaiera_puntu.py'), '-o', str(direktorio_balio / 'apps.bin')] + 항목들, check=True)
    ITURBURUA = direktorio_balio / 'apps.s'
    ITURBURUA.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(direktorio_balio / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(direktorio_balio / 'apps.o'), str(ITURBURUA)], check=True)
    nukleo_balio = direktorio_balio / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posizioa / '부팅/lotu_diseinu.ld'), '-o', str(nukleo_balio),
                    str(Posizioa / 'build/boot.o'), str(Posizioa / 'build/java.o'), str(Posizioa / 'build/user.o'), str(direktorio_balio / 'apps.o')], check=True)
    return nukleo_balio


def exekutatu_komando():
    EMAITZA = {}
    zerbitzari_balio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    zerbitzari_balio.bind(('127.0.0.1', 0))
    zerbitzari_balio.settimeout(0.1)
    ataka_balio = zerbitzari_balio.getsockname()[1]
    RECEIVED_elementu = []
    irten_aplik = threading.Event()
    def atzeko_planoko_eguneratze_erantzun():
        while not irten_aplik.is_set():
            try: datuak, pareko_balio = zerbitzari_balio.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_elementu.append(datuak)
            if datuak != b'drop-me': zerbitzari_balio.sendto(datuak, pareko_balio)
    일꾼 = threading.Thread(target=atzeko_planoko_eguneratze_erantzun, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            gailu = makina_birtual(Posizioa / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                gailu.Komandoa('apps', ['hello', 'udp', 'netcheck', 'stress'])
                gailu.Komandoa('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                gailu.Komandoa('run missing', ['Exit: -2'])
                gailu.Komandoa('net', ['NET RTL8139'])
                gailu.Komandoa('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for eduki_balio in ('hello-network', 'odd', 'even', 'repeat-123'):
                    gailu.Komandoa('run udp 10.0.2.2 {} {}'.format(ataka_balio, eduki_balio), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert eduki_balio.encode() in RECEIVED_elementu, 'Ostalari 서버에서 자료를 받지 못함'
                gailu.Komandoa('run stress {}'.format(ataka_balio), ['UDP STRESS PASS', 'Exit: 0'])
                gailu.Komandoa('run udp 10.0.2.2 {} drop-me'.format(ataka_balio), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                gailu.Komandoa('run hello recovered', ['arg: recovered', 'Exit: 0'])
                EMAITZA[종류] = gailu.LOG_marka.decode('utf-8', 'replace')
                print('PASS: {} erabiltzaile ELF/ring 3/Argumentuak/UDP Ostalari 왕복/ordua_balio 초과/shell 복귀'.format(종류), flush=True)
            finally:
                try: gailu.Komandoa('net', [])
                except Exception: pass
                (Posizioa / 'build/사용자통신-last.log').write_bytes(gailu.LOG_marka)
                gailu.Itxi()
        gailu = makina_birtual(Posizioa / 'build/kernel.elf', sare_balio=False)
        try:
            gailu.Komandoa('net', ['NET unavailable'])
            gailu.Komandoa('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            gailu.Komandoa('run hello', ['USER MODE ring 3', 'Exit: 0'])
            EMAITZA['no_nic'] = gailu.LOG_marka.decode()
        finally: gailu.Itxi()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            gailu = makina_birtual(보호커널(Path(임시)), sare_balio=False)
            try:
                for Izena, Egoera_balio in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    gailu.Komandoa('run ' + Izena, ['Exit: ' + str(Egoera_balio)])
                    gailu.Komandoa('run hello', ['USER MODE ring 3', 'Exit: 0'])
                EMAITZA['protection'] = gailu.LOG_marka.decode()
                print('PASS: erabiltzaile Memoria_datuak/포트 격리, 잘못된 erakusle/ELF, CPU salbuespen, 무한 iterazio_balio 제한', flush=True)
            finally:
                (Posizioa / 'build/보호시험-last.log').write_bytes(gailu.LOG_marka)
                gailu.Itxi()
    finally:
        irten_aplik.set()
        일꾼.join(timeout=2)
        zerbitzari_balio.close()
    EMAITZA['host_udp_received'] = [{'length': len(datuak), 'sha256': hashlib.sha256(datuak).hexdigest()} for datuak in RECEIVED_elementu]
    (Posizioa / 'build/사용자통신시험.json').write_text(json.dumps(EMAITZA, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    exekutatu_komando()
