#!/usr/bin/env python3
"""datosEfectivo ring 3 ELF/Anfitrión UDP 왕복/protegerValor error/valorTiempo valorLímite/잘못된 ELF를 검증한다."""
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

posición = Path(__file__).resolve().parents[1]


class MáquinaVirtual:
    def __init__(self, ruta, valorClaseTipo='elf', valorRed=True, medianoAlmacenamiento=None):
        self.valorTemporal = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        valorDirectorio = Path(self.valorTemporal.name)
        self.registroEntradaDiario = bytearray()
        self.valorSerie = socket.socket(socket.AF_UNIX)
        self.valorMonitor = socket.socket(socket.AF_UNIX)
        rutaSerie, rutaMonitor = valorDirectorio / 'serial.sock', valorDirectorio / 'monitor.sock'
        comando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(rutaSerie) + ',server,nowait',
                '-monitor', 'unix:' + str(rutaMonitor) + ',server,nowait']
        comando += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if valorRed else ['-net', 'none']
        comando += ['-kernel', str(ruta)] if valorClaseTipo == 'elf' else ['-cdrom', str(ruta), '-boot', 'd']
        if medianoAlmacenamiento is not None:
            comando += ['-drive', 'file=' + str(medianoAlmacenamiento) + ',format=raw,if=ide,index=0']
        self.valorProceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            terminación = time.monotonic() + 10
            while not (rutaSerie.exists() and rutaMonitor.exists()):
                if self.valorProceso.poll() is not None:
                    raise AssertionError(self.valorProceso.stderr.read().decode())
                if time.monotonic() > terminación: raise AssertionError('QEMU ponerEnMarcha valorTiempo 초과')
                time.sleep(0.03)
            self.valorSerie.connect(str(rutaSerie))
            self.valorMonitor.connect(str(rutaMonitor))
            self.valorSerie.setblocking(False)
            self.valorMonitor.sendall(b'cont\n')
            self.esperarEstadoValor('jkoros> ')
        except BaseException:
            self.cerrar()
            raise

    def esperarEstadoValor(self, valorExpresiónFrase, ponerEnMarcha=0, valorLímite=15):
        terminación = time.monotonic() + valorLímite
        while time.monotonic() < terminación:
            if valorExpresiónFrase.encode() in self.registroEntradaDiario[ponerEnMarcha:]:
                return self.registroEntradaDiario[ponerEnMarcha:].decode('utf-8', 'replace')
            leer, _, _ = select.select([self.valorSerie], [], [], 0.1)
            if leer:
                Datos = self.valorSerie.recv(65536)
                if not Datos: break
                self.registroEntradaDiario.extend(Datos)
            if self.valorProceso.poll() is not None: break
        raise AssertionError('esperarValor valorFallo: ' + valorExpresiónFrase + '\n' + self.registroEntradaDiario.decode('utf-8', 'replace'))

    def comando(self, Cadena, expectativa):
        ponerEnMarcha = len(self.registroEntradaDiario)
        self.valorSerie.sendall((Cadena + '\n').encode())
        resultado = self.esperarEstadoValor('jkoros> ', ponerEnMarcha)
        for valorExpresiónFrase in expectativa:
            assert valorExpresiónFrase in resultado, (Cadena, valorExpresiónFrase, resultado)
        assert 'PANIC' not in resultado, resultado
        return resultado

    def cerrar(self):
        self.valorSerie.close()
        self.valorMonitor.close()
        if self.valorProceso.poll() is None:
            self.valorProceso.terminate()
            try: self.valorProceso.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.valorProceso.kill()
                self.valorProceso.wait()
        self.valorProceso.communicate()
        self.valorTemporal.cleanup()


def núcleoProtegido(valorDirectorio):
    listaCasos = {
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
    listaEntradas = ['hello=' + str(posición / 'build/apps/hello.elf')]
    for nombre, valorContenidoValor in listaCasos.items():
        fuente = valorDirectorio / (nombre + '.s')
        fuente.write_text('.code32\n.text\n.globl _start\n_start:\n' + valorContenidoValor +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(valorDirectorio / (nombre + '.o')), str(fuente)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posición.parent / 'compiler/disposiciónEnlazarUsuario.ld'),
                        '-o', str(valorDirectorio / (nombre + '.elf')), str(valorDirectorio / (nombre + '.o'))], check=True)
        listaEntradas.append(nombre + '=' + str(valorDirectorio / (nombre + '.elf')))
    esNormal = bytearray((posición / 'build/apps/hello.elf').read_bytes())
    listaVariantes = {}
    resultadoInválido = bytearray(esNormal); resultadoInválido[0] = 0; listaVariantes['badelf'] = resultadoInválido
    resultadoInválido = bytearray(esNormal); struct.pack_into('<I', resultadoInválido, 24, 0x00100000); listaVariantes['badentry'] = resultadoInválido
    resultadoInválido = bytearray(esNormal); struct.pack_into('<I', resultadoInválido, 28, 0x7fffffff); listaVariantes['badtable'] = resultadoInválido
    resultadoInválido = bytearray(esNormal); Tabla = struct.unpack_from('<I', resultadoInválido, 28)[0]
    struct.pack_into('<I', resultadoInválido, Tabla + 20, 0x7fffffff); listaVariantes['badsize'] = resultadoInválido
    for nombre, Datos in listaVariantes.items():
        Archivo = valorDirectorio / (nombre + '.elf'); Archivo.write_bytes(Datos)
        listaEntradas.append(nombre + '=' + str(Archivo))
    subprocess.run([sys.executable, str(posición / 'Herramientas/EmpaquetarEjecutables.py'), '-o', str(valorDirectorio / 'apps.bin')] + listaEntradas, check=True)
    fuente = valorDirectorio / 'apps.s'
    fuente.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(valorDirectorio / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(valorDirectorio / 'apps.o'), str(fuente)], check=True)
    valorNúcleo = valorDirectorio / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posición / 'Arranque/DisposiciónEnlace.ld'), '-o', str(valorNúcleo),
                    str(posición / 'build/boot.o'), str(posición / 'build/java.o'), str(posición / 'build/user.o'), str(valorDirectorio / 'apps.o')], check=True)
    return valorNúcleo


def ejecutarComando():
    resultado = {}
    valorServidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    valorServidor.bind(('127.0.0.1', 0))
    valorServidor.settimeout(0.1)
    valorPuerto = valorServidor.getsockname()[1]
    elementoListaRecibido = []
    programaSalir = threading.Event()
    def respuestaRepetirEntrada():
        while not programaSalir.is_set():
            try: Datos, valorParRed = valorServidor.recvfrom(4096)
            except socket.timeout: continue
            elementoListaRecibido.append(Datos)
            if Datos != b'drop-me': valorServidor.sendto(Datos, valorParRed)
    valorTareaFondo = threading.Thread(target=respuestaRepetirEntrada, daemon=True)
    valorTareaFondo.start()
    try:
        for valorClaseTipo in ('elf', 'iso'):
            máquina = MáquinaVirtual(posición / ('build/kernel.elf' if valorClaseTipo == 'elf' else 'build/kernel.iso'), valorClaseTipo)
            try:
                máquina.comando('apps', ['hello', 'udp', 'netcheck', 'stress'])
                máquina.comando('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                máquina.comando('run missing', ['Exit: -2'])
                máquina.comando('net', ['NET RTL8139'])
                máquina.comando('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for valorContenidoValor in ('hello-network', 'odd', 'even', 'repeat-123'):
                    máquina.comando('run udp 10.0.2.2 {} {}'.format(valorPuerto, valorContenidoValor), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert valorContenidoValor.encode() in elementoListaRecibido, 'Anfitrión 서버에서 자료를 받지 못함'
                máquina.comando('run stress {}'.format(valorPuerto), ['UDP STRESS PASS', 'Exit: 0'])
                máquina.comando('run udp 10.0.2.2 {} drop-me'.format(valorPuerto), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                máquina.comando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                resultado[valorClaseTipo] = máquina.registroEntradaDiario.decode('utf-8', 'replace')
                print('PASS: {} Usuario ELF/ring 3/argumentos/UDP Anfitrión 왕복/valorTiempo 초과/intérpreteComandos 복귀'.format(valorClaseTipo), flush=True)
            finally:
                try: máquina.comando('net', [])
                except Exception: pass
                (posición / 'build/사용자통신-last.log').write_bytes(máquina.registroEntradaDiario)
                máquina.cerrar()
        máquina = MáquinaVirtual(posición / 'build/kernel.elf', valorRed=False)
        try:
            máquina.comando('net', ['NET unavailable'])
            máquina.comando('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            máquina.comando('run hello', ['USER MODE ring 3', 'Exit: 0'])
            resultado['no_nic'] = máquina.registroEntradaDiario.decode()
        finally: máquina.cerrar()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as valorTemporal:
            máquina = MáquinaVirtual(núcleoProtegido(Path(valorTemporal)), valorRed=False)
            try:
                for nombre, valorEstadoValor in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    máquina.comando('run ' + nombre, ['Exit: ' + str(valorEstadoValor)])
                    máquina.comando('run hello', ['USER MODE ring 3', 'Exit: 0'])
                resultado['protection'] = máquina.registroEntradaDiario.decode()
                print('PASS: Usuario datosMemoria/puertoEquipoFísico 격리, 잘못된 puntero/ELF, CPU excepción, 무한 valorIteración valorLímite', flush=True)
            finally:
                (posición / 'build/PruebaProtección-last.log').write_bytes(máquina.registroEntradaDiario)
                máquina.cerrar()
    finally:
        programaSalir.set()
        valorTareaFondo.join(timeout=2)
        valorServidor.close()
    resultado['host_udp_received'] = [{'length': len(Datos), 'sha256': hashlib.sha256(Datos).hexdigest()} for Datos in elementoListaRecibido]
    (posición / 'build/pruebaRedUsuario.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ejecutarComando()
