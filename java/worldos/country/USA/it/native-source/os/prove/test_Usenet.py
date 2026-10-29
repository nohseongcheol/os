#!/usr/bin/env python3
"""effettivo_dati ring 3 ELF/host UDP 왕복/proteggere_VALORE errore/valore 제한/잘못된 ELF를 검증한다."""
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

posizione = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, percorso, Kind_VALORE='elf', rete_VALORE=True, Memoria_Medio=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        elenco_VALORE = Path(self.임시.name)
        self.LOG_riga = bytearray()
        self.seriale_VALORE = socket.socket(socket.AF_UNIX)
        self.monitor_VALORE = socket.socket(socket.AF_UNIX)
        seriale_percorso, monitor_percorso = elenco_VALORE / 'serial.sock', elenco_VALORE / 'monitor.sock'
        comando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(seriale_percorso) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_percorso) + ',server,nowait']
        comando += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if rete_VALORE else ['-net', 'none']
        comando += ['-kernel', str(percorso)] if Kind_VALORE == 'elf' else ['-cdrom', str(percorso), '-boot', 'd']
        if Memoria_Medio is not None:
            comando += ['-drive', 'file=' + str(Memoria_Medio) + ',format=raw,if=ide,index=0']
        self.Processi_VALORE = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (seriale_percorso.exists() and monitor_percorso.exists()):
                if self.Processi_VALORE.poll() is not None:
                    raise AssertionError(self.Processi_VALORE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU avvia valore 초과')
                time.sleep(0.03)
            self.seriale_VALORE.connect(str(seriale_percorso))
            self.monitor_VALORE.connect(str(monitor_percorso))
            self.seriale_VALORE.setblocking(False)
            self.monitor_VALORE.sendall(b'cont\n')
            self.stato_di_attesa('jkoros> ')
        except BaseException:
            self.Chiudi()
            raise

    def stato_di_attesa(self, 문구, avvia=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_riga[avvia:]:
                return self.LOG_riga[avvia:].decode('utf-8', 'replace')
            Lettura, _, _ = select.select([self.seriale_VALORE], [], [], 0.1)
            if Lettura:
                dati = self.seriale_VALORE.recv(65536)
                if not dati: break
                self.LOG_riga.extend(dati)
            if self.Processi_VALORE.poll() is not None: break
        raise AssertionError('aspetta_VALORE errore_VALORE: ' + 문구 + '\n' + self.LOG_riga.decode('utf-8', 'replace'))

    def comando(self, stringa_VALORE, 기대):
        avvia = len(self.LOG_riga)
        self.seriale_VALORE.sendall((stringa_VALORE + '\n').encode())
        risultato = self.stato_di_attesa('jkoros> ', avvia)
        for 문구 in 기대:
            assert 문구 in risultato, (stringa_VALORE, 문구, risultato)
        assert 'PANIC' not in risultato, risultato
        return risultato

    def Chiudi(self):
        self.seriale_VALORE.close()
        self.monitor_VALORE.close()
        if self.Processi_VALORE.poll() is None:
            self.Processi_VALORE.terminate()
            try: self.Processi_VALORE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Processi_VALORE.kill()
                self.Processi_VALORE.wait()
        self.Processi_VALORE.communicate()
        self.임시.cleanup()


def 보호커널(elenco_VALORE):
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
    항목들 = ['hello=' + str(posizione / 'build/apps/hello.elf')]
    for Nome, Contenuto_VALORE in 사례들.items():
        codiceSorgente = elenco_VALORE / (Nome + '.s')
        codiceSorgente.write_text('.code32\n.text\n.globl _start\n_start:\n' + Contenuto_VALORE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(elenco_VALORE / (Nome + '.o')), str(codiceSorgente)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posizione.parent / 'compiler/USER_link_Layout.ld'),
                        '-o', str(elenco_VALORE / (Nome + '.elf')), str(elenco_VALORE / (Nome + '.o'))], check=True)
        항목들.append(Nome + '=' + str(elenco_VALORE / (Nome + '.elf')))
    reparto_IT_normale = bytearray((posizione / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    non_valida_KR = bytearray(reparto_IT_normale); non_valida_KR[0] = 0; 변형들['badelf'] = non_valida_KR
    non_valida_KR = bytearray(reparto_IT_normale); struct.pack_into('<I', non_valida_KR, 24, 0x00100000); 변형들['badentry'] = non_valida_KR
    non_valida_KR = bytearray(reparto_IT_normale); struct.pack_into('<I', non_valida_KR, 28, 0x7fffffff); 변형들['badtable'] = non_valida_KR
    non_valida_KR = bytearray(reparto_IT_normale); tabella_di_ricerca = struct.unpack_from('<I', non_valida_KR, 28)[0]
    struct.pack_into('<I', non_valida_KR, tabella_di_ricerca + 20, 0x7fffffff); 변형들['badsize'] = non_valida_KR
    for Nome, dati in 변형들.items():
        file = elenco_VALORE / (Nome + '.elf'); file.write_bytes(dati)
        항목들.append(Nome + '=' + str(file))
    subprocess.run([sys.executable, str(posizione / 'strumenti/BIND_endpoint.py'), '-o', str(elenco_VALORE / 'apps.bin')] + 항목들, check=True)
    codiceSorgente = elenco_VALORE / 'apps.s'
    codiceSorgente.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(elenco_VALORE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(elenco_VALORE / 'apps.o'), str(codiceSorgente)], check=True)
    kernel_VALORE = elenco_VALORE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posizione / 'avvio_macchina/disposizione_di_collegamento.ld'), '-o', str(kernel_VALORE),
                    str(posizione / 'build/boot.o'), str(posizione / 'build/java.o'), str(posizione / 'build/user.o'), str(elenco_VALORE / 'apps.o')], check=True)
    return kernel_VALORE


def Esegui_comando():
    risultato = {}
    server_VALORE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALORE.bind(('127.0.0.1', 0))
    server_VALORE.settimeout(0.1)
    porta_VALORE = server_VALORE.getsockname()[1]
    RICEV_SCAD_articolo = []
    Esci_app = threading.Event()
    def eco_schermo_replica():
        while not Esci_app.is_set():
            try: dati, peer_VALORE = server_VALORE.recvfrom(4096)
            except socket.timeout: continue
            RICEV_SCAD_articolo.append(dati)
            if dati != b'drop-me': server_VALORE.sendto(dati, peer_VALORE)
    lavoratore_VALORE = threading.Thread(target=eco_schermo_replica, daemon=True)
    lavoratore_VALORE.start()
    try:
        for Kind_VALORE in ('elf', 'iso'):
            computer = VM(posizione / ('build/kernel.elf' if Kind_VALORE == 'elf' else 'build/kernel.iso'), Kind_VALORE)
            try:
                computer.comando('apps', ['hello', 'udp', 'netcheck', 'stress'])
                computer.comando('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                computer.comando('run missing', ['Exit: -2'])
                computer.comando('net', ['NET RTL8139'])
                computer.comando('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Contenuto_VALORE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    computer.comando('run udp 10.0.2.2 {} {}'.format(porta_VALORE, Contenuto_VALORE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Contenuto_VALORE.encode() in RICEV_SCAD_articolo, 'host 서버에서 자료를 받지 못함'
                computer.comando('run stress {}'.format(porta_VALORE), ['UDP STRESS PASS', 'Exit: 0'])
                computer.comando('run udp 10.0.2.2 {} drop-me'.format(porta_VALORE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                computer.comando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                risultato[Kind_VALORE] = computer.LOG_riga.decode('utf-8', 'replace')
                print('PASS: {} spazio_utente ELF/ring 3/argomenti/UDP host 왕복/valore 초과/Shell 복귀'.format(Kind_VALORE), flush=True)
            finally:
                try: computer.comando('net', [])
                except Exception: pass
                (posizione / 'build/사용자통신-last.log').write_bytes(computer.LOG_riga)
                computer.Chiudi()
        computer = VM(posizione / 'build/kernel.elf', rete_VALORE=False)
        try:
            computer.comando('net', ['NET unavailable'])
            computer.comando('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            computer.comando('run hello', ['USER MODE ring 3', 'Exit: 0'])
            risultato['no_nic'] = computer.LOG_riga.decode()
        finally: computer.Chiudi()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            computer = VM(보호커널(Path(임시)), rete_VALORE=False)
            try:
                for Nome, Stato_VALORE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    computer.comando('run ' + Nome, ['Exit: ' + str(Stato_VALORE)])
                    computer.comando('run hello', ['USER MODE ring 3', 'Exit: 0'])
                risultato['protection'] = computer.LOG_riga.decode()
                print('PASS: spazio_utente Memoria_dati/hardware_porta 격리, 잘못된 puntatore/ELF, CPU eccezione, 무한 sprint_VALORE 제한', flush=True)
            finally:
                (posizione / 'build/Protezione_test-last.log').write_bytes(computer.LOG_riga)
                computer.Chiudi()
    finally:
        Esci_app.set()
        lavoratore_VALORE.join(timeout=2)
        server_VALORE.close()
    risultato['host_udp_received'] = [{'length': len(dati), 'sha256': hashlib.sha256(dati).hexdigest()} for dati in RICEV_SCAD_articolo]
    (posizione / 'build/test_Usenet.json').write_text(json.dumps(risultato, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Esegui_comando()
