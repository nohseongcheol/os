#!/usr/bin/env python3
"""PyPI equipoFísicoFísico 배포와 부정 valorEntrada·RAM 되돌림을 propio 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from retransmitirPaquete import repositorioPaquete, descomprimir
from ejecutarComando import raízProyecto


def pruebaRueda(nombre, entradasArchivo, valorContrato='Root-Is-Purelib: true\n', dependencias=''):
    Datos = io.BytesIO()
    with zipfile.ZipFile(Datos, 'w', zipfile.ZIP_DEFLATED) as Paquete:
        Paquete.writestr(nombre + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + valorContrato)
        Paquete.writestr(nombre + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + nombre + '\nVersion: 1.0\n' + dependencias)
        for ruta, valorContenidoValor in entradasArchivo.items():
            Paquete.writestr(ruta, valorContenidoValor)
    return Datos.getvalue()


def comprobarAnfitrión():
    esNormal = pruebaRueda('jkoros-fixture', {'mod.py': 'valor=42\n'})
    assert descomprimir('jkoros_fixture-1.0-py3-none-any.whl', esNormal, 'jkoros-fixture', '1.0') == {'mod.py': 'valor=42\n'.encode()}
    for Datos in (
            pruebaRueda('jkoros-fixture', {'../escape.py': ''}),
            pruebaRueda('jkoros-fixture', {'/abs.py': ''}),
            pruebaRueda('jkoros-fixture', {'big.py': 'x' * 16385}),
            pruebaRueda('jkoros-fixture', {'mod.so': ''}),
            pruebaRueda('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            pruebaRueda('jkoros-fixture', {'mod.py': ''}, dependencias='Requires-Dist: requests\n')):
        try:
            descomprimir('jkoros_fixture-1.0-py3-none-any.whl', Datos, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel ruta·tamaño·C valorExtensión·dependencias rechazarValor')


def númeroPuertoVacíoEstado():
    with socket.socket() as valorConectorRed:
        valorConectorRed.bind(('127.0.0.1', 0))
        return valorConectorRed.getsockname()[1]


def ponerEnMarcha():
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('--host-only', action='store_true')
    argumentos = Analizador.parse_args()
    comprobarAnfitrión()
    if argumentos.host_only:
        return
    rutaResultado = raízProyecto/'build/verification/pip'
    rutaResultado.mkdir(parents=True, exist_ok=True)
    rutaAlmacenamiento = rutaResultado/'cache'
    rutaAlmacenamiento.mkdir(exist_ok=True)
    # datosEfectivo PyPI valorDistribución Archivo. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    repositorioPaquete(raízProyecto/'build/pip-cache').preparar('micropython-bisect==3.3.3')
    for valorExtremoFinal in ('.archive', '.json'):
        shutil.copyfile(str(raízProyecto/'build/pip-cache'/('micropython-bisect==3.3.3'+valorExtremoFinal)), str(rutaAlmacenamiento/('micropython-bisect==3.3.3'+valorExtremoFinal)))
    diarioEquipoFísico = json.loads((rutaAlmacenamiento/'micropython-bisect==3.3.3.json').read_text())
    assert diarioEquipoFísico['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for nombre, entradasArchivo in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .resultadoCálculo import añadirValores\n', '검증꾸러미/resultadoCálculo.py': 'def añadirValores(operandoPrimero,operandoSegundo):\n return operandoPrimero+operandoSegundo\n'}),
            ('jkoros-space', {'space%d.py' % númeroValor: 'valor=1\n' for númeroValor in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        Datos = pruebaRueda(nombre, entradasArchivo)
        (rutaAlmacenamiento/(nombre+'==1.0.archive')).write_bytes(Datos)
        (rutaAlmacenamiento/(nombre+'==1.0.json')).write_text(json.dumps({'name': nombre, 'version': '1.0',
            'filename': nombre.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(Datos).hexdigest()}))
    validar = {'passed': False, 'kernel_sha256': hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': diarioEquipoFísico, 'checks': []}
    númeroPuerto = númeroPuertoVacíoEstado()
    proceso = subprocess.Popen(['python3', str(raízProyecto/'Herramientas/ejecutarComando.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(númeroPuerto), '--pip-cache', str(rutaAlmacenamiento), '--ftp-port', str(númeroPuertoVacíoEstado())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Selector = selectors.DefaultSelector()
    Selector.register(proceso.stdout, selectors.EVENT_READ)
    transcripción = bytearray()
    def esperarFin(mostrarValor=b'jkoros-native> '):
        valorContenidoValor = bytearray()
        terminación = time.monotonic()+120
        while mostrarValor not in valorContenidoValor:
            if time.monotonic() > terminación or proceso.poll() is not None:
                raise AssertionError('게스트 respuesta métodoAusente: '+valorContenidoValor.decode('utf-8','replace'))
            for valorEntradaElemento, _ in Selector.select(.1):
                valorFragmento = valorEntradaElemento.fileobj.read(4096)
                valorContenidoValor.extend(valorFragmento)
                transcripción.extend(valorFragmento)
        return valorContenidoValor.decode('utf-8', 'replace').replace('\r\n','\n')
    def intérpreteComandos(comando, mostrarValor=b'jkoros-native> '):
        proceso.stdin.write(comando.encode()+b'\n')
        proceso.stdin.flush()
        return esperarFin(mostrarValor)
    def ejecutarComando(comando, valoresEsperado, valorEstadoValor=0):
        valorContenidoValor = intérpreteComandos(comando)
        assert valoresEsperado in valorContenidoValor and '\nexit '+str(valorEstadoValor)+'\n' in valorContenidoValor, valorContenidoValor
        validar['checks'].append(comando)
        return valorContenidoValor
    def archivosSubir(nombre, Datos):
        intérpreteComandos('load '+nombre, b'hex> ')
        for índicePosición in range(0, len(Datos), 64):
            intérpreteComandos(Datos[índicePosición:índicePosición+64].hex(), b'hex> ')
        assert 'LOADED' in intérpreteComandos('.')
    try:
        esperarFin()
        ejecutarComando('pip --help', 'MicroPython árbolFuente 설치기')
        archivosSubir('오류시험.py', (raízProyecto/'Pruebas/Python/PruebaErrorCoreano.py').read_bytes())
        ejecutarComando('python 오류시험.py', 'español Archivo excepción verificar')
        ejecutarComando('pip install micropython-bisect==3.3.3 --port '+str(númeroPuerto), 'instalarValor esTerminado: micropython-bisect 3.3.3')
        ejecutarComando('python -c \'from bisect import insort as 순서대로넣기; valor=[1,5]; 순서대로넣기(valor,3); print(valor)\'', '[1, 3, 5]')
        ejecutarComando('python -m pip list', 'micropython-bisect 3.3.3')
        ejecutarComando('pip install micropython-bisect==3.3.3 --port '+str(númeroPuerto), '이미 설치됨:')
        ejecutarComando('pip install jkoros-fixture==1.0 --port '+str(númeroPuerto), 'instalarValor esTerminado: jkoros-fixture')
        ejecutarComando('python -c \'from 검증꾸러미 import añadirValores; print(añadirValores(20,22))\'', '\n42\n')
        ejecutarComando('pip install jkoros-syntax==1.0 --port '+str(númeroPuerto), 'Paquete error:', 1)
        ejecutarComando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 error 보존")\'', '구문 error 보존')
        archivosSubir('공간시험.py', (raízProyecto/'Pruebas/Python/PruebaEspacioNombresPaquete.py').read_bytes())
        ejecutarComando('python 공간시험.py '+str(númeroPuerto), 'Paquete regiónDirección 부족 puenteRetornar verificar')
        ejecutarComando('pip uninstall jkoros-fixture', 'eliminarEntradaElemento esTerminado: jkoros-fixture')
        ejecutarComando('pip uninstall micropython-bisect', 'eliminarEntradaElemento esTerminado: micropython-bisect')
        ejecutarComando('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("eliminarEntradaElemento verificar")\'', 'eliminarEntradaElemento verificar')
        validar['passed'] = True
        print('PASS: PyPI equipoFísicoFísico instalarValor·import·ejecutarComando, español excepción, 패키지 valorDirectorio, valorFallo puenteRetornar, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 programaSalir 키로 QEMU를 끝내면 실행기의 retransmitirValor 문맥도 정리된다.
            proceso.stdin.write(b'\x01x')
            proceso.stdin.flush()
            proceso.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            proceso.terminate()
            try:
                proceso.wait(timeout=8)
            except subprocess.TimeoutExpired:
                proceso.kill()
                proceso.wait()
        if proceso.poll() is None:
            proceso.kill()
            proceso.wait()
        Selector.close()
        proceso.stdin.close()
        proceso.stdout.close()
        (rutaResultado/'serial.log').write_bytes(transcripción)
        (rutaResultado/'report.json').write_text(json.dumps(validar, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ponerEnMarcha()
