#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost retransmitirValor. 게스트는 TCP로 받은 소스를 직접 instalarValor·실행한다."""
import argparse
import email.parser
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import socketserver
import struct
import tarfile
import threading
import urllib.request
import zipfile

raízProyecto = Path(__file__).resolve().parents[1]


def analizarPetición(petición):
    esCoincidente = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', petición)
    if not esCoincidente:
        raise ValueError('Paquete nombre 또는 nombre==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', esCoincidente[1]).lower(), esCoincidente[2]


def validarRuta(nombre, rutaInstalación=True):
    ruta = PurePosixPath(nombre)
    if ruta.is_absolute() or any(valorSubparte in ('', '.', '..') or valorSubparte.startswith('.') for valorSubparte in nombre.split('/')):
        raise ValueError('허용하지 않는 Paquete ruta: ' + nombre)
    if '\\' in nombre or any(ord(valorCarácter) < 32 or ord(valorCarácter) == 127 for valorCarácter in nombre):
        raise ValueError('잘못된 Paquete ruta Caracteres')
    if rutaInstalación and (len(('/lib/' + nombre).encode()) > 63 or nombre in ('español.py', 'Paquete.py')):
        raise ValueError('Paquete ruta valorLímite 또는 valorPredeterminado biblioteca 충돌: ' + nombre)
    return nombre


def descomprimir(nombreEntradaElementoArchivo, Datos, nombre, valorVersión):
    entradasArchivo = {}
    especificaciones = []
    def añadirFinalEntradaElemento(ruta, valorContenidoValor):
        validarRuta(ruta)
        if ruta in entradasArchivo:
            raise ValueError('중복 Paquete ruta: ' + ruta)
        if len(valorContenidoValor) > 16384:
            raise ValueError('파일당 16 KiB valorLímite 초과: ' + ruta)
        valorContenidoValor.decode('utf-8')
        entradasArchivo[ruta] = valorContenidoValor
        if len(entradasArchivo) > 16 or sum(map(len, entradasArchivo.values())) > 65536:
            raise ValueError('꾸러미는 árbolFuente 16개·valorTotal 64 KiB 이하여야 합니다.')
    if nombreEntradaElementoArchivo.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(Datos)) as Paquete:
            listaEntradas = Paquete.infolist()
            if len(listaEntradas) > 256 or sum(valorEntradaElemento.file_size for valorEntradaElemento in listaEntradas) > 1048576:
                raise ValueError('valorArchivoComprimido liberarAlmacenamiento tamaño valorLímite 초과')
            listaContrato = [valorEntradaElemento for valorEntradaElemento in listaEntradas if valorEntradaElemento.filename.endswith('.dist-info/WHEEL')]
            if len(listaContrato) != 1:
                raise ValueError('wheel valorContrato 명세가 필요합니다.')
            valorContrato = email.parser.Parser().parsestr(Paquete.read(listaContrato[0]).decode())
            if valorContrato.get('Root-Is-Purelib', '').lower() != 'true' or not nombreEntradaElementoArchivo.endswith('-none-any.whl'):
                raise ValueError('C valorExtensión·플랫폼 전용 wheel은 지원하지 않습니다.')
            for valorEntradaElemento in listaEntradas:
                ruta = valorEntradaElemento.filename.rstrip('/')
                validarRuta(ruta, False)
                if (valorEntradaElemento.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 númeroValor 없습니다.')
                if valorEntradaElemento.filename.endswith('/'):
                    continue
                if '.dist-info/' in ruta:
                    if ruta.endswith('/METADATA'):
                        especificaciones.append(Paquete.read(valorEntradaElemento).decode())
                    continue
                if not ruta.endswith('.py') or '.data/' in ruta:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ruta)
                añadirFinalEntradaElemento(ruta, Paquete.read(valorEntradaElemento))
    elif nombreEntradaElementoArchivo.endswith('.tar.gz') and nombre.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ejecutarComando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(Datos), mode='r|gz') as Paquete:
            listaRaíces = set()
            númeroElementosEntradaElemento = 0
            tamañoTotal = 0
            for valorEntradaElemento in Paquete:
                númeroElementosEntradaElemento += 1
                tamañoTotal += valorEntradaElemento.size
                if númeroElementosEntradaElemento > 256 or tamañoTotal > 1048576:
                    raise ValueError('valorArchivoComprimido liberarAlmacenamiento tamaño valorLímite 초과')
                validarRuta(valorEntradaElemento.name, False)
                partes = valorEntradaElemento.name.split('/')
                listaRaíces.add(partes[0])
                if valorEntradaElemento.isdir():
                    continue
                if not valorEntradaElemento.isfile() or len(partes) < 2:
                    raise ValueError('잘못된 MicroPython árbolFuente 배포형')
                ruta = '/'.join(partes[1:])
                valorContenidoValor = Paquete.extractfile(valorEntradaElemento).read()
                if ruta.endswith('PKG-INFO'):
                    especificaciones.append(valorContenidoValor.decode())
                elif ruta.endswith('.py') and ruta not in ('setup.py',):
                    añadirFinalEntradaElemento(ruta, valorContenidoValor)
                elif '.egg-info/' not in ruta and not ruta.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ruta)
            if len(listaRaíces) != 1:
                raise ValueError('MicroPython 소스의 valorRaíz 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* árbolFuente 배포형이 필요합니다.')
    if not entradasArchivo or len(especificaciones) != 1:
        raise ValueError('소스와 valorDistribución 메타데이터가 필요합니다.')
    especificación = email.parser.Parser().parsestr(especificaciones[0])
    if analizarPetición(especificación.get('Name', ''))[0] != nombre or especificación.get('Version') != valorVersión:
        raise ValueError('valorDistribución 메타데이터의 nombre·버전 불일치')
    if especificación.get_all('Requires-Dist') or especificación.get_all('Requires'):
        raise ValueError('자동 dependencias 해결은 아직 지원하지 않습니다. dependencias 없는 호환 꾸러미를 사용하십시오.')
    return entradasArchivo


def leerWeb(dirección, límiteCapacidad):
    if not dirección.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS valorDistribución 주소만 허용합니다.')
    with urllib.request.urlopen(dirección, timeout=30) as respuesta:
        if not respuesta.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 valorDistribución dirección valorMover')
        Datos = respuesta.read(límiteCapacidad + 1)
    if len(Datos) > límiteCapacidad:
        raise ValueError('valorDistribución Archivo tamaño valorLímite 초과')
    return Datos


def paqueteTransferencia(nombre, valorVersión, entradasArchivo, valorOrigen):
    especificación = {'name': nombre, 'version': valorVersión, 'source': valorOrigen, 'files': [
        {'path': ruta, 'size': len(Datos), 'sha256': hashlib.sha256(Datos).hexdigest()}
        for ruta, Datos in sorted(entradasArchivo.items())]}
    valorCabecera = json.dumps(especificación, ensure_ascii=False).encode()
    if len(valorCabecera) > 8192:
        raise ValueError('Paquete especificación tamaño 초과')
    return b'JKP1' + struct.pack('>I', len(valorCabecera)) + valorCabecera + b''.join(entradasArchivo[valorEntradaElemento['path']] for valorEntradaElemento in especificación['files'])


class repositorioPaquete:
    def __init__(valorPropio, ruta, esSinConexión=False):
        valorPropio.ruta = Path(ruta)
        valorPropio.ruta.mkdir(parents=True, exist_ok=True)
        valorPropio.esSinConexión = esSinConexión

    def preparar(valorPropio, petición):
        nombre, valorVersión = analizarPetición(petición)
        materialTecla = nombre + ('==' + valorVersión if valorVersión else '')
        rutaDiario = valorPropio.ruta / (materialTecla + '.json')
        rutaDistribución = valorPropio.ruta / (materialTecla + '.archive')
        if rutaDiario.is_file() and rutaDistribución.is_file():
            registroEntradaDiario = json.loads(rutaDiario.read_text())
            Datos = rutaDistribución.read_bytes()
            if hashlib.sha256(Datos).hexdigest() != registroEntradaDiario['sha256']:
                raise ValueError('저장된 valorDistribución 파일의 SHA-256 불일치')
        else:
            if valorPropio.esSinConexión:
                raise ValueError('esSinConexión 저장소에 없는 Paquete: ' + petición)
            dirección = 'https://pypi.org/pypi/' + nombre + ('/' + valorVersión if valorVersión else '') + '/json'
            informaciónSistema = json.loads(leerWeb(dirección, 4194304).decode())
            if informaciónSistema['info'].get('requires_dist'):
                raise ValueError('자동 dependencias 해결은 아직 지원하지 않습니다.')
            candidato = [valorEntradaElemento for valorEntradaElemento in informaciónSistema['urls'] if not valorEntradaElemento.get('yanked') and valorEntradaElemento['filename'].endswith('-none-any.whl')]
            if not candidato and nombre.startswith('micropython-'):
                candidato = [valorEntradaElemento for valorEntradaElemento in informaciónSistema['urls'] if not valorEntradaElemento.get('yanked') and valorEntradaElemento['filename'].endswith('.tar.gz')]
            if not candidato:
                raise ValueError('지원되는 순수 Python valorDistribución 파일이 없습니다.')
            valorSelección = candidato[0]
            Datos = leerWeb(valorSelección['url'], 4194304)
            if hashlib.sha256(Datos).hexdigest() != valorSelección['digests']['sha256']:
                raise ValueError('PyPI valorDistribución Archivo SHA-256 불일치')
            registroEntradaDiario = {'name': nombre, 'version': informaciónSistema['info']['version'], 'filename': valorSelección['filename'],
                    'url': valorSelección['url'], 'sha256': valorSelección['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            descomprimir(registroEntradaDiario['filename'], Datos, nombre, registroEntradaDiario['version'])
            rutaDistribución.write_bytes(Datos)
            rutaDiario.write_text(json.dumps(registroEntradaDiario, ensure_ascii=False, indent=2) + '\n')
        if registroEntradaDiario['name'] != nombre or valorVersión and registroEntradaDiario['version'] != valorVersión:
            raise ValueError('raízRepositorio nombre·버전 불일치')
        entradasArchivo = descomprimir(registroEntradaDiario['filename'], Datos, nombre, registroEntradaDiario['version'])
        return paqueteTransferencia(nombre, registroEntradaDiario['version'], entradasArchivo, registroEntradaDiario['url'])


class peticiónPaquete(socketserver.BaseRequestHandler):
    def handle(valorPropio):
        valorPropio.request.settimeout(10)
        try:
            petición = bytearray()
            while b'\n' not in petición and len(petición) < 100:
                valorFragmento = valorPropio.request.recv(100 - len(petición))
                if not valorFragmento:
                    return
                petición.extend(valorFragmento)
            if not petición.endswith(b'\n') or petición.count(b'\n') != 1:
                raise ValueError('잘못된 Paquete petición')
            respuesta = valorPropio.server.raízRepositorio.preparar(petición[:-1].decode('ascii'))
        except Exception as error:
            valorCabecera = json.dumps({'error': str(error)[:500]}, ensure_ascii=False).encode()
            respuesta = b'JKP1' + struct.pack('>I', len(valorCabecera)) + valorCabecera
        try:
            valorPropio.request.sendall(respuesta)
        except OSError:
            pass


class retransmitirPaquete:
    def __init__(valorPropio, númeroPuerto=8027, ruta=None, esSinConexión=False):
        valorPropio.valorServidor = socketserver.TCPServer(('127.0.0.1', númeroPuerto), peticiónPaquete, bind_and_activate=False)
        valorPropio.valorServidor.allow_reuse_address = True
        valorPropio.valorServidor.server_bind()
        valorPropio.valorServidor.server_activate()
        valorPropio.valorServidor.raízRepositorio = repositorioPaquete(ruta or raízProyecto/'build/pip-cache', esSinConexión)
        valorPropio.númeroPuerto = valorPropio.valorServidor.server_address[1]
        valorPropio.valorHiloEjecución = threading.Thread(target=valorPropio.valorServidor.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(valorPropio):
        valorPropio.valorHiloEjecución.start()
        return valorPropio

    def __exit__(valorPropio, *argumentos):
        valorPropio.valorServidor.shutdown()
        valorPropio.valorServidor.server_close()
        valorPropio.valorHiloEjecución.join(timeout=2)


def ponerEnMarcha():
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('--port', type=int, default=8027)
    Analizador.add_argument('--cache', type=Path, default=raízProyecto/'build/pip-cache')
    Analizador.add_argument('--offline', action='store_true')
    Analizador.add_argument('--fetch', help='ejecutarComando 없이 호환 valorDistribución 파일을 내려받아 Comprobaciones·valorAlmacenar')
    argumentos = Analizador.parse_args()
    if argumentos.fetch:
        Datos = repositorioPaquete(argumentos.cache, argumentos.offline).preparar(argumentos.fetch)
        print('Paquete preparar esTerminado:', argumentos.fetch, len(Datos), 'valorByte')
        return
    with retransmitirPaquete(argumentos.port, argumentos.cache, argumentos.offline) as retransmitirValor:
        print('Paquete retransmitirValor: 127.0.0.1:' + str(retransmitirValor.númeroPuerto), flush=True)
        try:
            retransmitirValor.valorHiloEjecución.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ponerEnMarcha()
