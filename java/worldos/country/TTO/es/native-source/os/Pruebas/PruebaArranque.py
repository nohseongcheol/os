#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 valorSerie/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

posición = Path(__file__).resolve().parents[1]


def esperarFin(Comprobaciones, descripción, valorLímite=15):
    terminación = time.monotonic() + valorLímite
    while time.monotonic() < terminación:
        resultado = Comprobaciones()
        if resultado:
            return resultado
        time.sleep(0.05)
    raise AssertionError('valorTiempo 초과: ' + descripción)


def Pruebas(valorClaseTipo):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as valorTemporal:
        valorTemporal = Path(valorTemporal)
        rutaSerie = valorTemporal / 'serial.sock'
        rutaMonitor = valorTemporal / 'monitor.sock'
        comando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(rutaSerie) + ',server,nowait',
                '-monitor', 'unix:' + str(rutaMonitor) + ',server,nowait']
        comando += ['-kernel', str(posición / 'build/kernel.elf')] if valorClaseTipo == 'elf' else [
            '-cdrom', str(posición / 'build/kernel.iso'), '-boot', 'd']
        # valorSerie 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        comando += ['-S']
        valorProceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        valorSerie = socket.socket(socket.AF_UNIX)
        valorMonitor = socket.socket(socket.AF_UNIX)
        registroEntradaDiario = bytearray()
        try:
            def prepararConectorRed():
                if valorProceso.poll() is not None:
                    raise AssertionError(valorProceso.stderr.read().decode('utf-8', 'replace'))
                return rutaSerie.exists() and rutaMonitor.exists()
            esperarFin(prepararConectorRed, 'QEMU valorConectorRed')
            valorSerie.connect(str(rutaSerie))
            valorMonitor.connect(str(rutaMonitor))
            valorSerie.setblocking(False)
            valorMonitor.sendall(b'cont\n')

            def Encabezados(Cadena, ponerEnMarcha=0):
                leer, _, _ = select.select([valorSerie], [], [], 0.1)
                if leer:
                    Datos = valorSerie.recv(65536)
                    if not Datos:
                        raise AssertionError('valorSerie conectar programaSalir')
                    registroEntradaDiario.extend(Datos)
                if valorProceso.poll() is not None:
                    raise AssertionError('QEMU 비정상 programaSalir: ' + str(valorProceso.returncode))
                return Cadena.encode('utf-8') in registroEntradaDiario[ponerEnMarcha:]

            def pruebaComandos(valorEntrada, expectativa):
                ponerEnMarcha = len(registroEntradaDiario)
                valorSerie.sendall(valorEntrada.encode('ascii'))
                esperarFin(lambda: Encabezados(expectativa, ponerEnMarcha), expectativa)
                esperarFin(lambda: Encabezados('jkoros> ', ponerEnMarcha), 'comando estadoValorDespués 프롬프트')

            esperarFin(lambda: Encabezados('READY'), valorClaseTipo + ' Arranque')
            assert b'JAVA SELFTEST PASS' in registroEntradaDiario
            assert 'Java 기계어 valorNúcleo ponerEnMarcha'.encode() in registroEntradaDiario
            pruebaComandos('info\r\n', 'embedded subset JVM / polling kernel')
            pruebaComandos('help\n', 'free N | echo TEXT')
            pruebaComandos('mem\n', ' / 8 (각 4096바이트)')
            pruebaComandos('echo natix\bve\n', 'native\r\n')
            for número in range(8):
                pruebaComandos('alloc\n', 'valorSección número: ' + str(número))
            pruebaComandos('alloc\n', 'valorSección número: -1')
            pruebaComandos('free 3\n', '반환됨')
            pruebaComandos('free 3\n', '할당되지 않은 valorSección')
            pruebaComandos('free 99\n', '사용법: free 0..7')
            pruebaComandos('alloc\n', 'valorSección número: 3')
            pruebaComandos('free 0\n', '반환됨')
            pruebaComandos('test\n', 'JAVA SELFTEST PASS')
            pruebaComandos('unknown\n', '알 númeroValor 없는 명령입니다')
            pruebaComandos('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ponerEnMarcha = len(registroEntradaDiario)
            for valorTecla in ('i', 'n', 'f', 'o', 'ret'):
                valorMonitor.sendall(('sendkey ' + valorTecla + ' 30\n').encode())
                time.sleep(0.09)
            esperarFin(lambda: Encabezados('embedded subset JVM / polling kernel', ponerEnMarcha), 'PS/2 info valorEntrada')
            pruebaComandos('echo ' + 'a' * 150 + '\n', 'a' * 123)
            valorSerie.sendall(b'halt\n')
            esperarFin(lambda: Encabezados('HALTED'), 'ejecuciónDetenerMáquina comando')
            assert b'PANIC' not in registroEntradaDiario and b'SELFTEST FAIL' not in registroEntradaDiario
            print('PASS: {} Arranque, Java propio Pruebas, valorSerie comando, PS/2 valorEntrada, asignarMemoriaAlmacenamiento/resultadoRetornar, ejecuciónDetenerMáquina'.format(valorClaseTipo))
            return registroEntradaDiario.decode('utf-8', 'replace')
        finally:
            valorSerie.close()
            valorMonitor.close()
            valorProceso.terminate()
            try:
                valorProceso.wait(timeout=3)
            except subprocess.TimeoutExpired:
                valorProceso.kill()
                valorProceso.wait()


if __name__ == '__main__':
    resultado = {valorClaseTipo: Pruebas(valorClaseTipo) for valorClaseTipo in ('elf', 'iso')}
    (posición / 'build/PruebaArranque.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
