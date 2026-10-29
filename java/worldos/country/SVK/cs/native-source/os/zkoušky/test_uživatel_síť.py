#!/usr/bin/env python3
"""skutečný_data ring 3 ELF/hostit UDP 왕복/chránit_HODNOTA chyba/časová_hodnota 제한/잘못된 ELF를 검증한다."""
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

pozice = Path(__file__).resolve().parents[1]


class virtuální_počítač:
    def __init__(self, cesta_2, Druh_HODNOTA='elf', síť_HODNOTA=True, Storage_médium=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Adresář_HODNOTA = Path(self.임시.name)
        self.LOGZ_ZÁZNAM = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_HODNOTA = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_cesta = Adresář_HODNOTA / 'serial.sock', Adresář_HODNOTA / 'monitor.sock'
        příkaz = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_cesta) + ',server,nowait']
        příkaz += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if síť_HODNOTA else ['-net', 'none']
        příkaz += ['-kernel', str(cesta_2)] if Druh_HODNOTA == 'elf' else ['-cdrom', str(cesta_2), '-boot', 'd']
        if Storage_médium is not None:
            příkaz += ['-drive', 'file=' + str(Storage_médium) + ',format=raw,if=ide,index=0']
        self.Proces_HODNOTA = subprocess.Popen(příkaz, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_cesta.exists()):
                if self.Proces_HODNOTA.poll() is not None:
                    raise AssertionError(self.Proces_HODNOTA.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Spustit_2 časová_hodnota 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_HODNOTA.connect(str(monitor_cesta))
            self.직렬.setblocking(False)
            self.monitor_HODNOTA.sendall(b'cont\n')
            self.čekací_stav('jkoros> ')
        except BaseException:
            self.Zavřené()
            raise

    def čekací_stav(self, 문구, Spustit_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOGZ_ZÁZNAM[Spustit_2:]:
                return self.LOGZ_ZÁZNAM[Spustit_2:].decode('utf-8', 'replace')
            Čtení, _, _ = select.select([self.직렬], [], [], 0.1)
            if Čtení:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOGZ_ZÁZNAM.extend(data)
            if self.Proces_HODNOTA.poll() is not None: break
        raise AssertionError('počkej_HODNOTA selhání_HODNOTA: ' + 문구 + '\n' + self.LOGZ_ZÁZNAM.decode('utf-8', 'replace'))

    def příkaz(self, řetězec_HODNOTA, 기대):
        Spustit_2 = len(self.LOGZ_ZÁZNAM)
        self.직렬.sendall((řetězec_HODNOTA + '\n').encode())
        VÝSLEDEK = self.čekací_stav('jkoros> ', Spustit_2)
        for 문구 in 기대:
            assert 문구 in VÝSLEDEK, (řetězec_HODNOTA, 문구, VÝSLEDEK)
        assert 'PANIC' not in VÝSLEDEK, VÝSLEDEK
        return VÝSLEDEK

    def Zavřené(self):
        self.직렬.close()
        self.monitor_HODNOTA.close()
        if self.Proces_HODNOTA.poll() is None:
            self.Proces_HODNOTA.terminate()
            try: self.Proces_HODNOTA.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proces_HODNOTA.kill()
                self.Proces_HODNOTA.wait()
        self.Proces_HODNOTA.communicate()
        self.임시.cleanup()


def 보호커널(Adresář_HODNOTA):
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
    항목들 = ['hello=' + str(pozice / 'build/apps/hello.elf')]
    for Název, Obsah_HODNOTA in 사례들.items():
        zdrojový_soubor = Adresář_HODNOTA / (Název + '.s')
        zdrojový_soubor.write_text('.code32\n.text\n.globl _start\n_start:\n' + Obsah_HODNOTA +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Adresář_HODNOTA / (Název + '.o')), str(zdrojový_soubor)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozice.parent / 'compiler/uživatel_Odkaz_Navigace.ld'),
                        '-o', str(Adresář_HODNOTA / (Název + '.elf')), str(Adresář_HODNOTA / (Název + '.o'))], check=True)
        항목들.append(Název + '=' + str(Adresář_HODNOTA / (Název + '.elf')))
    informační_systémy_normální = bytearray((pozice / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    neplatný_KV = bytearray(informační_systémy_normální); neplatný_KV[0] = 0; 변형들['badelf'] = neplatný_KV
    neplatný_KV = bytearray(informační_systémy_normální); struct.pack_into('<I', neplatný_KV, 24, 0x00100000); 변형들['badentry'] = neplatný_KV
    neplatný_KV = bytearray(informační_systémy_normální); struct.pack_into('<I', neplatný_KV, 28, 0x7fffffff); 변형들['badtable'] = neplatný_KV
    neplatný_KV = bytearray(informační_systémy_normální); VYHLEDAT_tabulka = struct.unpack_from('<I', neplatný_KV, 28)[0]
    struct.pack_into('<I', neplatný_KV, VYHLEDAT_tabulka + 20, 0x7fffffff); 변형들['badsize'] = neplatný_KV
    for Název, data in 변형들.items():
        název_souboru = Adresář_HODNOTA / (Název + '.elf'); název_souboru.write_bytes(data)
        항목들.append(Název + '=' + str(název_souboru))
    subprocess.run([sys.executable, str(pozice / 'nástroje/vázat_účastník.py'), '-o', str(Adresář_HODNOTA / 'apps.bin')] + 항목들, check=True)
    zdrojový_soubor = Adresář_HODNOTA / 'apps.s'
    zdrojový_soubor.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Adresář_HODNOTA / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Adresář_HODNOTA / 'apps.o'), str(zdrojový_soubor)], check=True)
    jádro_HODNOTA = Adresář_HODNOTA / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozice / 'spuštění_stroje/rozvržení_spojování.ld'), '-o', str(jádro_HODNOTA),
                    str(pozice / 'build/boot.o'), str(pozice / 'build/java.o'), str(pozice / 'build/user.o'), str(Adresář_HODNOTA / 'apps.o')], check=True)
    return jádro_HODNOTA


def Provést_příkaz():
    VÝSLEDEK = {}
    server_HODNOTA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_HODNOTA.bind(('127.0.0.1', 0))
    server_HODNOTA.settimeout(0.1)
    port_HODNOTA = server_HODNOTA.getsockname()[1]
    RECEIVED_zboží = []
    Konec_program = threading.Event()
    def zobrazení_výsledků_odezva():
        while not Konec_program.is_set():
            try: data, partner_HODNOTA = server_HODNOTA.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_zboží.append(data)
            if data != b'drop-me': server_HODNOTA.sendto(data, partner_HODNOTA)
    pracovník_HODNOTA = threading.Thread(target=zobrazení_výsledků_odezva, daemon=True)
    pracovník_HODNOTA.start()
    try:
        for Druh_HODNOTA in ('elf', 'iso'):
            počítač = virtuální_počítač(pozice / ('build/kernel.elf' if Druh_HODNOTA == 'elf' else 'build/kernel.iso'), Druh_HODNOTA)
            try:
                počítač.příkaz('apps', ['hello', 'udp', 'netcheck', 'stress'])
                počítač.příkaz('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                počítač.příkaz('run missing', ['Exit: -2'])
                počítač.příkaz('net', ['NET RTL8139'])
                počítač.příkaz('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Obsah_HODNOTA in ('hello-network', 'odd', 'even', 'repeat-123'):
                    počítač.příkaz('run udp 10.0.2.2 {} {}'.format(port_HODNOTA, Obsah_HODNOTA), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Obsah_HODNOTA.encode() in RECEIVED_zboží, 'hostit 서버에서 자료를 받지 못함'
                počítač.příkaz('run stress {}'.format(port_HODNOTA), ['UDP STRESS PASS', 'Exit: 0'])
                počítač.příkaz('run udp 10.0.2.2 {} drop-me'.format(port_HODNOTA), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                počítač.příkaz('run hello recovered', ['arg: recovered', 'Exit: 0'])
                VÝSLEDEK[Druh_HODNOTA] = počítač.LOGZ_ZÁZNAM.decode('utf-8', 'replace')
                print('PASS: {} uživatelský_prostor ELF/ring 3/argumenty/UDP hostit 왕복/časová_hodnota 초과/prostředí 복귀'.format(Druh_HODNOTA), flush=True)
            finally:
                try: počítač.příkaz('net', [])
                except Exception: pass
                (pozice / 'build/사용자통신-last.log').write_bytes(počítač.LOGZ_ZÁZNAM)
                počítač.Zavřené()
        počítač = virtuální_počítač(pozice / 'build/kernel.elf', síť_HODNOTA=False)
        try:
            počítač.příkaz('net', ['NET unavailable'])
            počítač.příkaz('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            počítač.příkaz('run hello', ['USER MODE ring 3', 'Exit: 0'])
            VÝSLEDEK['no_nic'] = počítač.LOGZ_ZÁZNAM.decode()
        finally: počítač.Zavřené()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            počítač = virtuální_počítač(보호커널(Path(임시)), síť_HODNOTA=False)
            try:
                for Název, Stav_HODNOTA in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    počítač.příkaz('run ' + Název, ['Exit: ' + str(Stav_HODNOTA)])
                    počítač.příkaz('run hello', ['USER MODE ring 3', 'Exit: 0'])
                VÝSLEDEK['protection'] = počítač.LOGZ_ZÁZNAM.decode()
                print('PASS: uživatelský_prostor Paměť_data/hardware_port 격리, 잘못된 ukazatel/ELF, CPU výjimka, 무한 sprint_HODNOTA 제한', flush=True)
            finally:
                (pozice / 'build/Ochrana_test-last.log').write_bytes(počítač.LOGZ_ZÁZNAM)
                počítač.Zavřené()
    finally:
        Konec_program.set()
        pracovník_HODNOTA.join(timeout=2)
        server_HODNOTA.close()
    VÝSLEDEK['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in RECEIVED_zboží]
    (pozice / 'build/test_uživatel_síť.json').write_text(json.dumps(VÝSLEDEK, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Provést_příkaz()
