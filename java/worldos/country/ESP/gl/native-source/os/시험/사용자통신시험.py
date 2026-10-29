#!/usr/bin/env python3
"""real_datos ring 3 ELF/hospedar UDP 왕복/protexer_VALOR ERRO/hora_VALOR 제한/잘못된 ELF를 검증한다."""
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

Posición = Path(__file__).resolve().parents[1]


class máquina_virtual:
    def __init__(self, CAMIÑO, 종류='elf', Rede_VALOR=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        directorio_VALOR = Path(self.임시.name)
        self.LOG_fila = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALOR = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_camiño = directorio_VALOR / 'serial.sock', directorio_VALOR / 'monitor.sock'
        Orde = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_camiño) + ',server,nowait']
        Orde += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Rede_VALOR else ['-net', 'none']
        Orde += ['-kernel', str(CAMIÑO)] if 종류 == 'elf' else ['-cdrom', str(CAMIÑO), '-boot', 'd']
        if 저장매체 is not None:
            Orde += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Proceso_VALOR = subprocess.Popen(Orde, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_camiño.exists()):
                if self.Proceso_VALOR.poll() is not None:
                    raise AssertionError(self.Proceso_VALOR.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Executar_2 hora_VALOR 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALOR.connect(str(monitor_camiño))
            self.직렬.setblocking(False)
            self.monitor_VALOR.sendall(b'cont\n')
            self.agarda_Estado('jkoros> ')
        except BaseException:
            self.Pechar()
            raise

    def agarda_Estado(self, 문구, Executar_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_fila[Executar_2:]:
                return self.LOG_fila[Executar_2:].decode('utf-8', 'replace')
            Lectura, _, _ = select.select([self.직렬], [], [], 0.1)
            if Lectura:
                datos = self.직렬.recv(65536)
                if not datos: break
                self.LOG_fila.extend(datos)
            if self.Proceso_VALOR.poll() is not None: break
        raise AssertionError('agarda_VALOR erro_VALOR: ' + 문구 + '\n' + self.LOG_fila.decode('utf-8', 'replace'))

    def Orde(self, cadea_VALOR, 기대):
        Executar_2 = len(self.LOG_fila)
        self.직렬.sendall((cadea_VALOR + '\n').encode())
        RESULTANTE = self.agarda_Estado('jkoros> ', Executar_2)
        for 문구 in 기대:
            assert 문구 in RESULTANTE, (cadea_VALOR, 문구, RESULTANTE)
        assert 'PANIC' not in RESULTANTE, RESULTANTE
        return RESULTANTE

    def Pechar(self):
        self.직렬.close()
        self.monitor_VALOR.close()
        if self.Proceso_VALOR.poll() is None:
            self.Proceso_VALOR.terminate()
            try: self.Proceso_VALOR.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proceso_VALOR.kill()
                self.Proceso_VALOR.wait()
        self.Proceso_VALOR.communicate()
        self.임시.cleanup()


def 보호커널(directorio_VALOR):
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
    항목들 = ['hello=' + str(Posición / 'build/apps/hello.elf')]
    for Nome, Contido_VALOR in 사례들.items():
        FONTE = directorio_VALOR / (Nome + '.s')
        FONTE.write_text('.code32\n.text\n.globl _start\n_start:\n' + Contido_VALOR +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(directorio_VALOR / (Nome + '.o')), str(FONTE)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posición.parent / 'compiler/usuario_Ligar_deseño.ld'),
                        '-o', str(directorio_VALOR / (Nome + '.elf')), str(directorio_VALOR / (Nome + '.o'))], check=True)
        항목들.append(Nome + '=' + str(directorio_VALOR / (Nome + '.elf')))
    정상 = bytearray((Posición / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    non_válido_medida = bytearray(정상); non_válido_medida[0] = 0; 변형들['badelf'] = non_válido_medida
    non_válido_medida = bytearray(정상); struct.pack_into('<I', non_válido_medida, 24, 0x00100000); 변형들['badentry'] = non_válido_medida
    non_válido_medida = bytearray(정상); struct.pack_into('<I', non_válido_medida, 28, 0x7fffffff); 변형들['badtable'] = non_válido_medida
    non_válido_medida = bytearray(정상); Busca_táboa = struct.unpack_from('<I', non_válido_medida, 28)[0]
    struct.pack_into('<I', non_válido_medida, Busca_táboa + 20, 0x7fffffff); 변형들['badsize'] = non_válido_medida
    for Nome, datos in 변형들.items():
        Ficheiro = directorio_VALOR / (Nome + '.elf'); Ficheiro.write_bytes(datos)
        항목들.append(Nome + '=' + str(Ficheiro))
    subprocess.run([sys.executable, str(Posición / 'Ferramentas/ligar_extremo.py'), '-o', str(directorio_VALOR / 'apps.bin')] + 항목들, check=True)
    FONTE = directorio_VALOR / 'apps.s'
    FONTE.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(directorio_VALOR / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(directorio_VALOR / 'apps.o'), str(FONTE)], check=True)
    kernel_VALOR = directorio_VALOR / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Posición / '부팅/Ligar_deseño.ld'), '-o', str(kernel_VALOR),
                    str(Posición / 'build/boot.o'), str(Posición / 'build/java.o'), str(Posición / 'build/user.o'), str(directorio_VALOR / 'apps.o')], check=True)
    return kernel_VALOR


def executar_comando():
    RESULTANTE = {}
    servidor_VALOR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_VALOR.bind(('127.0.0.1', 0))
    servidor_VALOR.settimeout(0.1)
    porto_VALOR = servidor_VALOR.getsockname()[1]
    RECIBIDO_elemento = []
    saír_apl = threading.Event()
    def eco_resposta():
        while not saír_apl.is_set():
            try: datos, punto_VALOR = servidor_VALOR.recvfrom(4096)
            except socket.timeout: continue
            RECIBIDO_elemento.append(datos)
            if datos != b'drop-me': servidor_VALOR.sendto(datos, punto_VALOR)
    일꾼 = threading.Thread(target=eco_resposta, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            máquina = máquina_virtual(Posición / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                máquina.Orde('apps', ['hello', 'udp', 'netcheck', 'stress'])
                máquina.Orde('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                máquina.Orde('run missing', ['Exit: -2'])
                máquina.Orde('net', ['NET RTL8139'])
                máquina.Orde('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Contido_VALOR in ('hello-network', 'odd', 'even', 'repeat-123'):
                    máquina.Orde('run udp 10.0.2.2 {} {}'.format(porto_VALOR, Contido_VALOR), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Contido_VALOR.encode() in RECIBIDO_elemento, 'hospedar 서버에서 자료를 받지 못함'
                máquina.Orde('run stress {}'.format(porto_VALOR), ['UDP STRESS PASS', 'Exit: 0'])
                máquina.Orde('run udp 10.0.2.2 {} drop-me'.format(porto_VALOR), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                máquina.Orde('run hello recovered', ['arg: recovered', 'Exit: 0'])
                RESULTANTE[종류] = máquina.LOG_fila.decode('utf-8', 'replace')
                print('PASS: {} usuario ELF/ring 3/Argumentos/UDP hospedar 왕복/hora_VALOR 초과/shell 복귀'.format(종류), flush=True)
            finally:
                try: máquina.Orde('net', [])
                except Exception: pass
                (Posición / 'build/사용자통신-last.log').write_bytes(máquina.LOG_fila)
                máquina.Pechar()
        máquina = máquina_virtual(Posición / 'build/kernel.elf', Rede_VALOR=False)
        try:
            máquina.Orde('net', ['NET unavailable'])
            máquina.Orde('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            máquina.Orde('run hello', ['USER MODE ring 3', 'Exit: 0'])
            RESULTANTE['no_nic'] = máquina.LOG_fila.decode()
        finally: máquina.Pechar()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            máquina = máquina_virtual(보호커널(Path(임시)), Rede_VALOR=False)
            try:
                for Nome, Estado_VALOR in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    máquina.Orde('run ' + Nome, ['Exit: ' + str(Estado_VALOR)])
                    máquina.Orde('run hello', ['USER MODE ring 3', 'Exit: 0'])
                RESULTANTE['protection'] = máquina.LOG_fila.decode()
                print('PASS: usuario Memoria_datos/포트 격리, 잘못된 punteiro/ELF, CPU excepción, 무한 sprint_VALOR 제한', flush=True)
            finally:
                (Posición / 'build/보호시험-last.log').write_bytes(máquina.LOG_fila)
                máquina.Pechar()
    finally:
        saír_apl.set()
        일꾼.join(timeout=2)
        servidor_VALOR.close()
    RESULTANTE['host_udp_received'] = [{'length': len(datos), 'sha256': hashlib.sha256(datos).hexdigest()} for datos in RECIBIDO_elemento]
    (Posición / 'build/사용자통신시험.json').write_text(json.dumps(RESULTANTE, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    executar_comando()
