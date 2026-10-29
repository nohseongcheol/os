#!/usr/bin/env python3
"""werkelijk_gegevens ring 3 ELF/host UDP 왕복/beschermen_WAARDE fout/TIJD_WAARDE 제한/잘못된 ELF를 검증한다."""
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

positie = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, pad, soort_WAARDE='elf', net_WAARDE=True, Opslag_medium=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        map_WAARDE = Path(self.임시.name)
        self.LOG_RECORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_WAARDE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_pad = map_WAARDE / 'serial.sock', map_WAARDE / 'monitor.sock'
        opdracht = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_pad) + ',server,nowait']
        opdracht += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if net_WAARDE else ['-net', 'none']
        opdracht += ['-kernel', str(pad)] if soort_WAARDE == 'elf' else ['-cdrom', str(pad), '-boot', 'd']
        if Opslag_medium is not None:
            opdracht += ['-drive', 'file=' + str(Opslag_medium) + ',format=raw,if=ide,index=0']
        self.Proces_WAARDE = subprocess.Popen(opdracht, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_pad.exists()):
                if self.Proces_WAARDE.poll() is not None:
                    raise AssertionError(self.Proces_WAARDE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU starten TIJD_WAARDE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_WAARDE.connect(str(monitor_pad))
            self.직렬.setblocking(False)
            self.monitor_WAARDE.sendall(b'cont\n')
            self.wachtstatus('jkoros> ')
        except BaseException:
            self.Sluiten()
            raise

    def wachtstatus(self, 문구, starten=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_RECORD[starten:]:
                return self.LOG_RECORD[starten:].decode('utf-8', 'replace')
            Lezen, _, _ = select.select([self.직렬], [], [], 0.1)
            if Lezen:
                gegevens = self.직렬.recv(65536)
                if not gegevens: break
                self.LOG_RECORD.extend(gegevens)
            if self.Proces_WAARDE.poll() is not None: break
        raise AssertionError('wachten_WAARDE fout_WAARDE: ' + 문구 + '\n' + self.LOG_RECORD.decode('utf-8', 'replace'))

    def opdracht(self, tekenreeks_WAARDE, 기대):
        starten = len(self.LOG_RECORD)
        self.직렬.sendall((tekenreeks_WAARDE + '\n').encode())
        resultaat = self.wachtstatus('jkoros> ', starten)
        for 문구 in 기대:
            assert 문구 in resultaat, (tekenreeks_WAARDE, 문구, resultaat)
        assert 'PANIC' not in resultaat, resultaat
        return resultaat

    def Sluiten(self):
        self.직렬.close()
        self.monitor_WAARDE.close()
        if self.Proces_WAARDE.poll() is None:
            self.Proces_WAARDE.terminate()
            try: self.Proces_WAARDE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proces_WAARDE.kill()
                self.Proces_WAARDE.wait()
        self.Proces_WAARDE.communicate()
        self.임시.cleanup()


def 보호커널(map_WAARDE):
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
    항목들 = ['hello=' + str(positie / 'build/apps/hello.elf')]
    for Naam, Inhoud_WAARDE in 사례들.items():
        broncode = map_WAARDE / (Naam + '.s')
        broncode.write_text('.code32\n.text\n.globl _start\n_start:\n' + Inhoud_WAARDE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(map_WAARDE / (Naam + '.o')), str(broncode)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(positie.parent / 'compiler/gebruiker_link_Indeling.ld'),
                        '-o', str(map_WAARDE / (Naam + '.elf')), str(map_WAARDE / (Naam + '.o'))], check=True)
        항목들.append(Naam + '=' + str(map_WAARDE / (Naam + '.elf')))
    informatie_normaal = bytearray((positie / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    nietig_HR = bytearray(informatie_normaal); nietig_HR[0] = 0; 변형들['badelf'] = nietig_HR
    nietig_HR = bytearray(informatie_normaal); struct.pack_into('<I', nietig_HR, 24, 0x00100000); 변형들['badentry'] = nietig_HR
    nietig_HR = bytearray(informatie_normaal); struct.pack_into('<I', nietig_HR, 28, 0x7fffffff); 변형들['badtable'] = nietig_HR
    nietig_HR = bytearray(informatie_normaal); opzoektabel = struct.unpack_from('<I', nietig_HR, 28)[0]
    struct.pack_into('<I', nietig_HR, opzoektabel + 20, 0x7fffffff); 변형들['badsize'] = nietig_HR
    for Naam, gegevens in 변형들.items():
        bestand = map_WAARDE / (Naam + '.elf'); bestand.write_bytes(gegevens)
        항목들.append(Naam + '=' + str(bestand))
    subprocess.run([sys.executable, str(positie / 'hulpmiddelen/BIND_eindpunt.py'), '-o', str(map_WAARDE / 'apps.bin')] + 항목들, check=True)
    broncode = map_WAARDE / 'apps.s'
    broncode.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(map_WAARDE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(map_WAARDE / 'apps.o'), str(broncode)], check=True)
    kernel_WAARDE = map_WAARDE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(positie / 'machineopstart/koppelindeling.ld'), '-o', str(kernel_WAARDE),
                    str(positie / 'build/boot.o'), str(positie / 'build/java.o'), str(positie / 'build/user.o'), str(map_WAARDE / 'apps.o')], check=True)
    return kernel_WAARDE


def Uitvoeren_opdracht():
    resultaat = {}
    server_WAARDE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_WAARDE.bind(('127.0.0.1', 0))
    server_WAARDE.settimeout(0.1)
    poort_WAARDE = server_WAARDE.getsockname()[1]
    OPBRENGST_item = []
    Einde_app = threading.Event()
    def echo_reactie():
        while not Einde_app.is_set():
            try: gegevens, peer_WAARDE = server_WAARDE.recvfrom(4096)
            except socket.timeout: continue
            OPBRENGST_item.append(gegevens)
            if gegevens != b'drop-me': server_WAARDE.sendto(gegevens, peer_WAARDE)
    werkrol_WAARDE = threading.Thread(target=echo_reactie, daemon=True)
    werkrol_WAARDE.start()
    try:
        for soort_WAARDE in ('elf', 'iso'):
            machine = VM(positie / ('build/kernel.elf' if soort_WAARDE == 'elf' else 'build/kernel.iso'), soort_WAARDE)
            try:
                machine.opdracht('apps', ['hello', 'udp', 'netcheck', 'stress'])
                machine.opdracht('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                machine.opdracht('run missing', ['Exit: -2'])
                machine.opdracht('net', ['NET RTL8139'])
                machine.opdracht('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Inhoud_WAARDE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    machine.opdracht('run udp 10.0.2.2 {} {}'.format(poort_WAARDE, Inhoud_WAARDE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Inhoud_WAARDE.encode() in OPBRENGST_item, 'host 서버에서 자료를 받지 못함'
                machine.opdracht('run stress {}'.format(poort_WAARDE), ['UDP STRESS PASS', 'Exit: 0'])
                machine.opdracht('run udp 10.0.2.2 {} drop-me'.format(poort_WAARDE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                machine.opdracht('run hello recovered', ['arg: recovered', 'Exit: 0'])
                resultaat[soort_WAARDE] = machine.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS: {} gebruikersruimte ELF/ring 3/argumenten/UDP host 왕복/TIJD_WAARDE 초과/Shell 복귀'.format(soort_WAARDE), flush=True)
            finally:
                try: machine.opdracht('net', [])
                except Exception: pass
                (positie / 'build/사용자통신-last.log').write_bytes(machine.LOG_RECORD)
                machine.Sluiten()
        machine = VM(positie / 'build/kernel.elf', net_WAARDE=False)
        try:
            machine.opdracht('net', ['NET unavailable'])
            machine.opdracht('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            machine.opdracht('run hello', ['USER MODE ring 3', 'Exit: 0'])
            resultaat['no_nic'] = machine.LOG_RECORD.decode()
        finally: machine.Sluiten()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            machine = VM(보호커널(Path(임시)), net_WAARDE=False)
            try:
                for Naam, Status_WAARDE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    machine.opdracht('run ' + Naam, ['Exit: ' + str(Status_WAARDE)])
                    machine.opdracht('run hello', ['USER MODE ring 3', 'Exit: 0'])
                resultaat['protection'] = machine.LOG_RECORD.decode()
                print('PASS: gebruikersruimte Geheugen_gegevens/hardware_poort 격리, 잘못된 wijzer/ELF, CPU uitzondering, 무한 sprint_WAARDE 제한', flush=True)
            finally:
                (positie / 'build/Beveiliging_test-last.log').write_bytes(machine.LOG_RECORD)
                machine.Sluiten()
    finally:
        Einde_app.set()
        werkrol_WAARDE.join(timeout=2)
        server_WAARDE.close()
    resultaat['host_udp_received'] = [{'length': len(gegevens), 'sha256': hashlib.sha256(gegevens).hexdigest()} for gegevens in OPBRENGST_item]
    (positie / 'build/test_gebruiker_net.json').write_text(json.dumps(resultaat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Uitvoeren_opdracht()
