#!/usr/bin/env python3
"""real_dades ring 3 ELF/allotjar UDP 왕복/protegir_VALOR s_ha_produït_un_error/Hora_VALOR 제한/잘못된 ELF를 검증한다."""
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

Posició = Path(__file__).resolve().parents[1]


class màquina_virtual:
    def __init__(self, Camí, 종류='elf', xarxa_VALOR=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        directori_VALOR = Path(self.임시.name)
        self.LOG_fila = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALOR = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_camí = directori_VALOR / 'serial.sock', directori_VALOR / 'monitor.sock'
        Ordre = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_camí) + ',server,nowait']
        Ordre += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if xarxa_VALOR else ['-net', 'none']
        Ordre += ['-kernel', str(Camí)] if 종류 == 'elf' else ['-cdrom', str(Camí), '-boot', 'd']
        if 저장매체 is not None:
            Ordre += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Procés_VALOR = subprocess.Popen(Ordre, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_camí.exists()):
                if self.Procés_VALOR.poll() is not None:
                    raise AssertionError(self.Procés_VALOR.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Executa_2 Hora_VALOR 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALOR.connect(str(monitor_camí))
            self.직렬.setblocking(False)
            self.monitor_VALOR.sendall(b'cont\n')
            self.Espera_Estat('jkoros> ')
        except BaseException:
            self.Tanca()
            raise

    def Espera_Estat(self, 문구, Executa_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_fila[Executa_2:]:
                return self.LOG_fila[Executa_2:].decode('utf-8', 'replace')
            Lectura, _, _ = select.select([self.직렬], [], [], 0.1)
            if Lectura:
                dades = self.직렬.recv(65536)
                if not dades: break
                self.LOG_fila.extend(dades)
            if self.Procés_VALOR.poll() is not None: break
        raise AssertionError('Espera_VALOR error_VALOR: ' + 문구 + '\n' + self.LOG_fila.decode('utf-8', 'replace'))

    def Ordre(self, cadena_VALOR, 기대):
        Executa_2 = len(self.LOG_fila)
        self.직렬.sendall((cadena_VALOR + '\n').encode())
        RESULTAT = self.Espera_Estat('jkoros> ', Executa_2)
        for 문구 in 기대:
            assert 문구 in RESULTAT, (cadena_VALOR, 문구, RESULTAT)
        assert 'PANIC' not in RESULTAT, RESULTAT
        return RESULTAT

    def Tanca(self):
        self.직렬.close()
        self.monitor_VALOR.close()
        if self.Procés_VALOR.poll() is None:
            self.Procés_VALOR.terminate()
            try: self.Procés_VALOR.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Procés_VALOR.kill()
                self.Procés_VALOR.wait()
        self.Procés_VALOR.communicate()
        self.임시.cleanup()


def 보호커널(directori_VALOR):
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
    항목들 = ['hello=' + str(Posició / 'build/apps/hello.elf')]
    for Nom, contingut_VALOR in 사례들.items():
        FONT = directori_VALOR / (Nom + '.s')
        FONT.write_text('.code32\n.text\n.globl _start\n_start:\n' + contingut_VALOR +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(directori_VALOR / (Nom + '.o')), str(FONT)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posició.parent / 'compiler/usuari_enllaç_disseny.ld'),
                        '-o', str(directori_VALOR / (Nom + '.elf')), str(directori_VALOR / (Nom + '.o'))], check=True)
        항목들.append(Nom + '=' + str(directori_VALOR / (Nom + '.elf')))
    정상 = bytearray((Posició / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    invàlid_mesura = bytearray(정상); invàlid_mesura[0] = 0; 변형들['badelf'] = invàlid_mesura
    invàlid_mesura = bytearray(정상); struct.pack_into('<I', invàlid_mesura, 24, 0x00100000); 변형들['badentry'] = invàlid_mesura
    invàlid_mesura = bytearray(정상); struct.pack_into('<I', invàlid_mesura, 28, 0x7fffffff); 변형들['badtable'] = invàlid_mesura
    invàlid_mesura = bytearray(정상); Cerca_taula = struct.unpack_from('<I', invàlid_mesura, 28)[0]
    struct.pack_into('<I', invàlid_mesura, Cerca_taula + 20, 0x7fffffff); 변형들['badsize'] = invàlid_mesura
    for Nom, dades in 변형들.items():
        Fitxer = directori_VALOR / (Nom + '.elf'); Fitxer.write_bytes(dades)
        항목들.append(Nom + '=' + str(Fitxer))
    subprocess.run([sys.executable, str(Posició / 'Eines/enllaçar_extrem.py'), '-o', str(directori_VALOR / 'apps.bin')] + 항목들, check=True)
    FONT = directori_VALOR / 'apps.s'
    FONT.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(directori_VALOR / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(directori_VALOR / 'apps.o'), str(FONT)], check=True)
    nucli_VALOR = directori_VALOR / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posició / '부팅/enllaç_disseny.ld'), '-o', str(nucli_VALOR),
                    str(Posició / 'build/boot.o'), str(Posició / 'build/java.o'), str(Posició / 'build/user.o'), str(directori_VALOR / 'apps.o')], check=True)
    return nucli_VALOR


def Executa_ordre():
    RESULTAT = {}
    servidor_VALOR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_VALOR.bind(('127.0.0.1', 0))
    servidor_VALOR.settimeout(0.1)
    port_VALOR = servidor_VALOR.getsockname()[1]
    CANTIDAD_RECIBIDA_element = []
    Surt_programa = threading.Event()
    def eco_resposta():
        while not Surt_programa.is_set():
            try: dades, homòleg_VALOR = servidor_VALOR.recvfrom(4096)
            except socket.timeout: continue
            CANTIDAD_RECIBIDA_element.append(dades)
            if dades != b'drop-me': servidor_VALOR.sendto(dades, homòleg_VALOR)
    일꾼 = threading.Thread(target=eco_resposta, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            màquina = màquina_virtual(Posició / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                màquina.Ordre('apps', ['hello', 'udp', 'netcheck', 'stress'])
                màquina.Ordre('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                màquina.Ordre('run missing', ['Exit: -2'])
                màquina.Ordre('net', ['NET RTL8139'])
                màquina.Ordre('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for contingut_VALOR in ('hello-network', 'odd', 'even', 'repeat-123'):
                    màquina.Ordre('run udp 10.0.2.2 {} {}'.format(port_VALOR, contingut_VALOR), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert contingut_VALOR.encode() in CANTIDAD_RECIBIDA_element, 'allotjar 서버에서 자료를 받지 못함'
                màquina.Ordre('run stress {}'.format(port_VALOR), ['UDP STRESS PASS', 'Exit: 0'])
                màquina.Ordre('run udp 10.0.2.2 {} drop-me'.format(port_VALOR), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                màquina.Ordre('run hello recovered', ['arg: recovered', 'Exit: 0'])
                RESULTAT[종류] = màquina.LOG_fila.decode('utf-8', 'replace')
                print('PASS: {} usuari ELF/ring 3/인수/UDP allotjar 왕복/Hora_VALOR 초과/shell 복귀'.format(종류), flush=True)
            finally:
                try: màquina.Ordre('net', [])
                except Exception: pass
                (Posició / 'build/사용자통신-last.log').write_bytes(màquina.LOG_fila)
                màquina.Tanca()
        màquina = màquina_virtual(Posició / 'build/kernel.elf', xarxa_VALOR=False)
        try:
            màquina.Ordre('net', ['NET unavailable'])
            màquina.Ordre('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            màquina.Ordre('run hello', ['USER MODE ring 3', 'Exit: 0'])
            RESULTAT['no_nic'] = màquina.LOG_fila.decode()
        finally: màquina.Tanca()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            màquina = màquina_virtual(보호커널(Path(임시)), xarxa_VALOR=False)
            try:
                for Nom, Estat_VALOR in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    màquina.Ordre('run ' + Nom, ['Exit: ' + str(Estat_VALOR)])
                    màquina.Ordre('run hello', ['USER MODE ring 3', 'Exit: 0'])
                RESULTAT['protection'] = màquina.LOG_fila.decode()
                print('PASS: usuari Memòria_dades/포트 격리, 잘못된 punter/ELF, CPU excepció, 무한 esprint_VALOR 제한', flush=True)
            finally:
                (Posició / 'build/보호시험-last.log').write_bytes(màquina.LOG_fila)
                màquina.Tanca()
    finally:
        Surt_programa.set()
        일꾼.join(timeout=2)
        servidor_VALOR.close()
    RESULTAT['host_udp_received'] = [{'length': len(dades), 'sha256': hashlib.sha256(dades).hexdigest()} for dades in CANTIDAD_RECIBIDA_element]
    (Posició / 'build/사용자통신시험.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Executa_ordre()
