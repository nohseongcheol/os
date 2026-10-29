#!/usr/bin/env python3
"""datosEfectivo raspi4b Arranque, UART valorEntrada, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from ejecutarComando import raízProyecto, comando


def ponerEnMarcha():
    salida = raízProyecto / 'build/verification'
    salida.mkdir(parents=True, exist_ok=True)
    transcripción = bytearray()
    informeValidación = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as rutaTrabajoEnCurso:
        rutaQMP = Path(rutaTrabajoEnCurso) / 'qmp.sock'
        argumentosComando = comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(rutaQMP),
                           '-vnc', 'unix:{}'.format(Path(rutaTrabajoEnCurso) / 'vnc.sock')]
        informeValidación['command'] = argumentosComando
        proceso = subprocess.Popen(argumentosComando, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selector = selectors.DefaultSelector()
        selector.register(proceso.stdout, selectors.EVENT_READ)
        def recibirHasta(marcador, valorDesfase=0, tiempoEsperaEjecución=45):
            tiempoPlazo = time.monotonic() + tiempoEsperaEjecución
            while marcador not in transcripción[valorDesfase:]:
                if time.monotonic() > tiempoPlazo:
                    raise AssertionError('UART timeout: ' + repr(marcador))
                for valorPulsado, _ in selector.select(0.2):
                    bloqueDatos = valorPulsado.fileobj.read(4096)
                    if bloqueDatos:
                        transcripción.extend(bloqueDatos)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transcripción):
                    raise AssertionError('kernel failure')
                if proceso.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(proceso.returncode))
        try:
            recibirHasta(b'jkoros-native> ')
            marcadores = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for marcador in marcadores:
                assert marcador in transcripción, marcador
            # GTK 없는 elementoListaActual 호스트에서도 VNC로 datosEfectivo GUI를 볼 númeroValor 있어야 한다.
            with socket.socket(socket.AF_UNIX) as clientePantalla:
                clientePantalla.settimeout(5); clientePantalla.connect(str(Path(rutaTrabajoEnCurso) / 'vnc.sock'))
                def valorExacto(tamaño):
                    resultado = b''
                    while len(resultado) < tamaño:
                        valorFragmento = clientePantalla.recv(tamaño - len(resultado))
                        if not valorFragmento: raise AssertionError('VNC disconnected')
                        resultado += valorFragmento
                    return resultado
                assert valorExacto(12) == b'RFB 003.008\n'
                clientePantalla.sendall(b'RFB 003.008\n')
                assert 1 in valorExacto(valorExacto(1)[0]); clientePantalla.sendall(b'\x01')
                assert valorExacto(4) == b'\x00\x00\x00\x00'; clientePantalla.sendall(b'\x01')
                valorServidor = valorExacto(24)
                assert int.from_bytes(valorServidor[:2], 'big') == 640 and int.from_bytes(valorServidor[2:4], 'big') == 480
                valorExacto(int.from_bytes(valorServidor[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for byteComando, marcador in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'Pruebas.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                valorDesfase = len(transcripción)
                proceso.stdin.write(byteComando + b'\n')
                proceso.stdin.flush()
                recibirHasta(b'jkoros-native> ', valorDesfase)
                assert marcador in transcripción[valorDesfase:], marcador
            def intérpreteComandos(línea, esperado):
                valorDesfase = len(transcripción)
                proceso.stdin.write(línea.encode('utf-8') + b'\n'); proceso.stdin.flush()
                recibirHasta(b'jkoros-native> ', valorDesfase)
                respuestaRetorno = bytes(transcripción[valorDesfase:])
                for texto in esperado:
                    assert texto.encode('utf-8') in respuestaRetorno, (línea, texto, respuestaRetorno)
                return respuestaRetorno
            def entrar(línea, indicadorEntrada):
                valorDesfase = len(transcripción)
                proceso.stdin.write(línea.encode('utf-8') + b'\n'); proceso.stdin.flush()
                recibirHasta(indicadorEntrada, valorDesfase)
                return bytes(transcripción[valorDesfase:])
            def valorEditar(nombre, valorContenidoValor, operaciónCancelar=False):
                entrar('edit ' + nombre, b'edit> ')
                for línea in valorContenidoValor.splitlines(): entrar(línea, b'edit> ')
                if operaciónCancelar:
                    valorDesfase = len(transcripción)
                    proceso.stdin.write(b'\x03'); proceso.stdin.flush()
                    recibirHasta(b'jkoros-native> ', valorDesfase)
                    assert b'EDIT CANCELLED' in transcripción[valorDesfase:]
                else:
                    assert b'SAVED' in entrar('.', b'jkoros-native> ')
            def archivosSubir(nombre, Datos):
                assert len(Datos) <= 16384
                entrar('load ' + nombre, b'hex> ')
                for índiceOrdinal in range(0, len(Datos), 64): entrar(Datos[índiceOrdinal:índiceOrdinal+64].hex(), b'hex> ')
                assert b'LOADED' in entrar('.', b'jkoros-native> ')
            def descargar(nombre):
                respuestaRetorno = intérpreteComandos('hex ' + nombre, ['HEX BEGIN', 'HEX END'])
                esIgual = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', respuestaRetorno, re.S)
                Datos = bytes.fromhex(''.join(esIgual.group(2).decode('ascii').split()))
                assert len(Datos) == int(esIgual.group(1)); return Datos
            intérpreteComandos('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            intérpreteComandos('java -version', ['not OpenJDK', 'exit 0'])
            intérpreteComandos('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            intérpreteComandos('java Hello "한글 argumentos 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumentos 😀', 'exit 0'])
            intérpreteComandos('python --version', ['MicroPython 1.24.1', 'exit 0'])
            intérpreteComandos('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Archivo', 'exit 0'])
            intérpreteComandos('cat python.txt', ['한글 Archivo'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            claseJava = salida / 'Hello.class'; claseJava.write_bytes(descargar('Hello.class'))
            esperado = subprocess.check_output(['java', '-Xverify:all', '-cp', str(salida), 'Hello', '한글 argumentos 😀']).decode('utf-8')
            assert esperado.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumentos 😀'], esperado
            valorEditar('Saludo.java', 'public class Saludo { public static void main(String[] args) { int valor = 7; System.out.println("한글=" + valor); } }')
            intérpreteComandos('javac Saludo.java', ['Compiled: Saludo.class', 'exit 0'])
            intérpreteComandos('java Saludo', ['한글=7', 'exit 0'])
            (salida / 'Saludo.class').write_bytes(descargar('Saludo.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(salida), 'Saludo']).decode().strip() == '한글=7'
            valorEditar('Hello.java', 'broken', operaciónCancelar=True)
            intérpreteComandos('javac Hello.java', ['Compiled:', 'exit 0'])
            valorEditar('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            intérpreteComandos('javac Broken.java', ['javac error:', 'exit 1'])
            archivosSubir('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            intérpreteComandos('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            intérpreteComandos('rm Broken.java', [])
            importado = salida / 'Imported.java'
            importado.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(importado)])
            archivosSubir('Imported.class', (salida / 'Imported.class').read_bytes())
            intérpreteComandos('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            intérpreteComandos('rm Imported.class', [])
            valorEditar('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            intérpreteComandos('javac Loop.java', ['Compiled:', 'exit 0'])
            respuestaRetorno = intérpreteComandos('java Loop', ['exit '])
            assert b'instruction limit' in respuestaRetorno or b'exit -1004' in respuestaRetorno
            intérpreteComandos('rm Loop.java', []); intérpreteComandos('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            comprobacionesPython = """import gc, jkoros
assert len('한글😀') == 3
assert 2**100 == 1267650600228229401496703205376
class Counter:
    def __init__(self, n): self.n = n
    def value(self): return self.n + 1
keep = Counter(41)
for i in range(300):
    garbage = [str(j) for j in range(80)]
    gc.collect()
assert keep.value() == 42
try:
    1 // 0
except ZeroDivisionError:
    print('PY EXCEPTION OK')
a = jkoros.udp_open(9401)
b = jkoros.udp_open(9402)
assert jkoros.udp_send(a, 9402, b'udp-python') == 10
assert jkoros.udp_recv(b) == (b'udp-python', 9401)
try:
    jkoros.udp_recv(b)
except OSError as e:
    assert e.args[0] == 11
jkoros.udp_close(a)
jkoros.udp_close(b)
print('PY GC UNICODE MPZ CLASS UDP OK')
"""
            valorEditar('checks.py', comprobacionesPython)
            intérpreteComandos('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            intérpreteComandos('rm checks.py', [])
            valorEditar('helper.py', 'value = 321')
            intérpreteComandos("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            intérpreteComandos('rm helper.py', [])
            intérpreteComandos("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            intérpreteComandos("python -c 'while True: pass'", ['exit -1004'])
            for índiceOrdinal in range(4):
                intérpreteComandos('python hello.py', ['한글 Archivo', 'exit 0'])
                intérpreteComandos('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            archivosSubir('app.elf', (raízProyecto / 'build/user/demo.elf').read_bytes())
            assert descargar('app.elf') == (raízProyecto / 'build/user/demo.elf').read_bytes()
            intérpreteComandos('run app.elf', ['EL0 C++', 'exit 0'])
            archivosSubir('app.elf', b'not an ELF')
            intérpreteComandos('run app.elf', ['exit -8'])
            intérpreteComandos('rm app.elf', [])
            intérpreteComandos('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            rutaDibujo = salida / 'java-framebuffer'; rutaDibujo.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(raízProyecto / 'dist/jkoros-native-korean.jar'), '-d', str(rutaDibujo), str(raízProyecto / 'Pruebas/Java/pruebaPantalla.java')])
            archivosSubir('pruebaPantalla.class', (rutaDibujo / 'pruebaPantalla.class').read_bytes())
            intérpreteComandos('java pruebaPantalla', ['Pantalla recortar rechazarValor', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            intérpreteComandos('rm pruebaPantalla.class', [])
            with socket.socket(socket.AF_UNIX) as cliente:
                cliente.settimeout(10)
                cliente.connect(str(rutaQMP))
                with cliente.makefile('rwb') as valorFlujo:
                    Saludo = json.loads(valorFlujo.readline())
                    def conexiónControlDoblePrueba(ejecutarTarea, argumentoReenviado=None):
                        mensajeRed = {'execute': ejecutarTarea}
                        if argumentoReenviado: mensajeRed['arguments'] = argumentoReenviado
                        valorFlujo.write((json.dumps(mensajeRed) + '\n').encode())
                        valorFlujo.flush()
                        while True:
                            respuesta = json.loads(valorFlujo.readline())
                            if 'error' in respuesta: raise AssertionError(respuesta)
                            if 'return' in respuesta: return respuesta['return']
                    conexiónControlDoblePrueba('qmp_capabilities')
                    capturaPantalla = salida / 'framebuffer.ppm'
                    conexiónControlDoblePrueba('screendump', {'filename': str(capturaPantalla), 'format': 'ppm'})
                    def entradasEjemplo(ruta, puntos):
                        with ruta.open('rb') as archivoPíxel:
                            assert archivoPíxel.readline().strip() == b'P6'
                            assert archivoPíxel.readline().strip() == b'640 480'
                            assert archivoPíxel.readline().strip() == b'255'
                            datosPíxel = archivoPíxel.read()
                        assert len(datosPíxel) == 640 * 480 * 3
                        return [list(datosPíxel[(coordenadaCoordenadaVertical * 640 + coordenadaCoordenadaHorizontal) * 3:(coordenadaCoordenadaVertical * 640 + coordenadaCoordenadaHorizontal) * 3 + 3]) for coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical in puntos]
                    assert entradasEjemplo(capturaPantalla, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert entradasEjemplo(capturaPantalla, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def enviar(valorPulsado, marcador):
                        valorDesfase = len(transcripción)
                        proceso.stdin.write(valorPulsado); proceso.stdin.flush()
                        recibirHasta(marcador, valorDesfase)
                    enviar(b'gui\n', b'GUI READY:')
                    gUIPrimero = salida / 'gui-programs.ppm'
                    conexiónControlDoblePrueba('screendump', {'filename': str(gUIPrimero), 'format': 'ppm'})
                    conexiónControlDoblePrueba('screendump', {'filename': str(salida / 'gui-programs.png'), 'format': 'png'})
                    assert entradasEjemplo(gUIPrimero, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    enviar(b'\r', b'GUI ACTION 0 RESULT 0')
                    enviar(b'\t', b'GUI FOCUS 1')
                    enviar(b'\r', b'GUI ACTION 1 RESULT 0')
                    gUISegundo = salida / 'gui-network.ppm'
                    conexiónControlDoblePrueba('screendump', {'filename': str(gUISegundo), 'format': 'ppm'})
                    conexiónControlDoblePrueba('screendump', {'filename': str(salida / 'gui-network.png'), 'format': 'png'})
                    assert entradasEjemplo(gUISegundo, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    enviar(b'\t', b'GUI FOCUS 2')
                    enviar(b'\r', b'GUI ACTION 2 RESULT 0')
                    enviar(b'\t', b'GUI FOCUS 3')
                    enviar(b'\r', b'GUI ACTION 3 RESULT 0')
                    conexiónControlDoblePrueba('screendump', {'filename': str(salida / 'gui-python.png'), 'format': 'png'})
                    enviar(b'q', b'jkoros-native> ')
                    informeValidación['qemu'] = Saludo['QMP']['version']
                    conexiónControlDoblePrueba('quit')
            proceso.wait(timeout=10)
            # framebuffer 응답뿐 아니라 datosEfectivo scanout 픽셀도 확인한다.
            with capturaPantalla.open('rb') as entradaElementoArchivo:
                assert entradaElementoArchivo.readline().strip() == b'P6'
                valorDimensiones = entradaElementoArchivo.readline().strip()
                assert valorDimensiones == b'640 480', valorDimensiones
                assert entradaElementoArchivo.readline().strip() == b'255'
                listaPíxeles = entradaElementoArchivo.read()
            assert len(listaPíxeles) == 640 * 480 * 3
            def píxel(coordenadaCoordenadaHorizontal, coordenadaCoordenadaVertical): return list(listaPíxeles[(coordenadaCoordenadaVertical * 640 + coordenadaCoordenadaHorizontal) * 3:(coordenadaCoordenadaVertical * 640 + coordenadaCoordenadaHorizontal) * 3 + 3])
            entradasEjemplo = {'background': píxel(5, 5), 'panel': píxel(45, 85), 'tile': píxel(65, 115)}
            assert entradasEjemplo == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, entradasEjemplo
            informeValidación.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
                'UTF-8 Korean/Japanese/Arabic/emoji UART', 'C++ direct RAM file API (21 runs)',
                'cooperative independent stacks (4 runs)', 'line shell/UTF-8/quotes/edit/cancel/hex upload/download',
                'guest Java compiler/JVM and OpenJDK two-way class verification',
                'Korean Java framebuffer library bounds and actual scanout pixels',
                'Korean Java identifiers, UTF-8 validation, malformed source and bounded execution',
                'MicroPython GC/classes/Unicode/MPZ/imports/exceptions/files/UDP and timeout recovery',
                'load and run custom ELF with malformed image rejection', 'RGB32 framebuffer pixels',
                'ELF64 rejection fixtures: 22', 'EL0 C++ constructors/RAII/FP/files/heap/pointer validation',
                'kernel/text/MMIO/guard/NX/privileged instruction protection', 'timer terminates EL0 infinite loop',
                'repeated EL0 program exit closes leaked descriptors', 'UDP loopback payload/peer/reply/truncation/queue/zero datagram/errors/cleanup',
                'GUI focus/keyboard activation/C++/UDP/Java/MicroPython launch/exit and framebuffer pixels'],
                vnc='RFB 3.8 / 640x480 / UART input',
                framebuffer=entradasEjemplo, kernel_sha256=hashlib.sha256((raízProyecto / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if proceso.poll() is None:
                proceso.terminate()
                try: proceso.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proceso.kill(); proceso.wait(timeout=5)
            selector.close()
            proceso.stdin.close(); proceso.stdout.close()
            (salida / 'serial.log').write_bytes(transcripción)
            (salida / 'report.json').write_text(json.dumps(informeValidación, indent=2) + '\n')


if __name__ == '__main__':
    ponerEnMarcha()
