#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instalar_VALOR·실행한다."""
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

Project_raíz = Path(__file__).resolve().parents[1]


def analizar_solicitude(solicitude):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', solicitude)
    if not 맞음:
        raise ValueError('paquete Nome 또는 Nome==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def validar_camiño(Nome, instalación_camiño=True):
    CAMIÑO = PurePosixPath(Nome)
    if CAMIÑO.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nome.split('/')):
        raise ValueError('허용하지 않는 paquete CAMIÑO: ' + Nome)
    if '\\' in Nome or any(ord(carácter_VALOR) < 32 or ord(carácter_VALOR) == 127 for carácter_VALOR in Nome):
        raise ValueError('잘못된 paquete CAMIÑO 문자')
    if instalación_camiño and (len(('/lib/' + Nome).encode()) > 63 or Nome in ('Galego.py', 'paquete.py')):
        raise ValueError('paquete CAMIÑO 제한 또는 valor_predefinido biblioteca 충돌: ' + Nome)
    return Nome


def 압축풀기(Ficheiro_introdución_nome, datos, Nome, versión_VALOR):
    파일들 = {}
    명세들 = []
    def Anexar_introdución(CAMIÑO, Contido_VALOR):
        validar_camiño(CAMIÑO)
        if CAMIÑO in 파일들:
            raise ValueError('중복 paquete CAMIÑO: ' + CAMIÑO)
        if len(Contido_VALOR) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + CAMIÑO)
        Contido_VALOR.decode('utf-8')
        파일들[CAMIÑO] = Contido_VALOR
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 fonte_árbore 16개·합계 64 KiB 이하여야 합니다.')
    if Ficheiro_introdución_nome.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(datos)) as paquete:
            항목들 = paquete.infolist()
            if len(항목들) > 256 or sum(introdución_VALOR.file_size for introdución_VALOR in 항목들) > 1048576:
                raise ValueError('Arquivo_VALOR liberar_Almacenamento Tamaño 제한 초과')
            caso_Lista = [introdución_VALOR for introdución_VALOR in 항목들 if introdución_VALOR.filename.endswith('.dist-info/WHEEL')]
            if len(caso_Lista) != 1:
                raise ValueError('wheel caso_VALOR 명세가 필요합니다.')
            caso_VALOR = email.parser.Parser().parsestr(paquete.read(caso_Lista[0]).decode())
            if caso_VALOR.get('Root-Is-Purelib', '').lower() != 'true' or not Ficheiro_introdución_nome.endswith('-none-any.whl'):
                raise ValueError('C extensión_VALOR·플랫폼 전용 wheel은 지원하지 않습니다.')
            for introdución_VALOR in 항목들:
                CAMIÑO = introdución_VALOR.filename.rstrip('/')
                validar_camiño(CAMIÑO, False)
                if (introdución_VALOR.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if introdución_VALOR.filename.endswith('/'):
                    continue
                if '.dist-info/' in CAMIÑO:
                    if CAMIÑO.endswith('/METADATA'):
                        명세들.append(paquete.read(introdución_VALOR).decode())
                    continue
                if not CAMIÑO.endswith('.py') or '.data/' in CAMIÑO:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + CAMIÑO)
                Anexar_introdución(CAMIÑO, paquete.read(introdución_VALOR))
    elif Ficheiro_introdución_nome.endswith('.tar.gz') and Nome.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py executar_comando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(datos), mode='r|gz') as paquete:
            뿌리들 = set()
            introdución_CONTAR = 0
            전체크기 = 0
            for introdución_VALOR in paquete:
                introdución_CONTAR += 1
                전체크기 += introdución_VALOR.size
                if introdución_CONTAR > 256 or 전체크기 > 1048576:
                    raise ValueError('Arquivo_VALOR liberar_Almacenamento Tamaño 제한 초과')
                validar_camiño(introdución_VALOR.name, False)
                부분들 = introdución_VALOR.name.split('/')
                뿌리들.add(부분들[0])
                if introdución_VALOR.isdir():
                    continue
                if not introdución_VALOR.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython fonte_árbore 배포형')
                CAMIÑO = '/'.join(부분들[1:])
                Contido_VALOR = paquete.extractfile(introdución_VALOR).read()
                if CAMIÑO.endswith('PKG-INFO'):
                    명세들.append(Contido_VALOR.decode())
                elif CAMIÑO.endswith('.py') and CAMIÑO not in ('setup.py',):
                    Anexar_introdución(CAMIÑO, Contido_VALOR)
                elif '.egg-info/' not in CAMIÑO and not CAMIÑO.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + CAMIÑO)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 raíz_VALOR 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* fonte_árbore 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if analizar_solicitude(명세.get('Name', ''))[0] != Nome or 명세.get('Version') != versión_VALOR:
        raise ValueError('배포 메타데이터의 Nome·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ENDEREZO, 한도):
    if not ENDEREZO.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ENDEREZO, timeout=30) as resposta:
        if not resposta.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ENDEREZO mover_VALOR')
        datos = resposta.read(한도 + 1)
    if len(datos) > 한도:
        raise ValueError('배포 Ficheiro Tamaño 제한 초과')
    return datos


def Transferir_paquete(Nome, versión_VALOR, 파일들, 출처):
    명세 = {'name': Nome, 'version': versión_VALOR, 'source': 출처, 'files': [
        {'path': CAMIÑO, 'size': len(datos), 'sha256': hashlib.sha256(datos).hexdigest()}
        for CAMIÑO, datos in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('paquete 명세 Tamaño 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[introdución_VALOR['path']] for introdución_VALOR in 명세['files'])


class paquete_repositorio:
    def __init__(자신, CAMIÑO, Tecnoloxía_da_información_TI_Desconectado=False):
        자신.CAMIÑO = Path(CAMIÑO)
        자신.CAMIÑO.mkdir(parents=True, exist_ok=True)
        자신.Tecnoloxía_da_información_TI_Desconectado = Tecnoloxía_da_información_TI_Desconectado

    def 준비(자신, solicitude):
        Nome, versión_VALOR = analizar_solicitude(solicitude)
        열쇠 = Nome + ('==' + versión_VALOR if versión_VALOR else '')
        LOG_camiño = 자신.CAMIÑO / (열쇠 + '.json')
        배포경로 = 자신.CAMIÑO / (열쇠 + '.archive')
        if LOG_camiño.is_file() and 배포경로.is_file():
            LOG_fila = json.loads(LOG_camiño.read_text())
            datos = 배포경로.read_bytes()
            if hashlib.sha256(datos).hexdigest() != LOG_fila['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.Tecnoloxía_da_información_TI_Desconectado:
                raise ValueError('Tecnoloxía_da_información_TI_Desconectado 저장소에 없는 paquete: ' + solicitude)
            ENDEREZO = 'https://pypi.org/pypi/' + Nome + ('/' + versión_VALOR if versión_VALOR else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ENDEREZO, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [introdución_VALOR for introdución_VALOR in msinfo32_exe['urls'] if not introdución_VALOR.get('yanked') and introdución_VALOR['filename'].endswith('-none-any.whl')]
            if not 후보 and Nome.startswith('micropython-'):
                후보 = [introdución_VALOR for introdución_VALOR in msinfo32_exe['urls'] if not introdución_VALOR.get('yanked') and introdución_VALOR['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            selección_VALOR = 후보[0]
            datos = 웹읽기(selección_VALOR['url'], 4194304)
            if hashlib.sha256(datos).hexdigest() != selección_VALOR['digests']['sha256']:
                raise ValueError('PyPI 배포 Ficheiro SHA-256 불일치')
            LOG_fila = {'name': Nome, 'version': msinfo32_exe['info']['version'], 'filename': selección_VALOR['filename'],
                    'url': selección_VALOR['url'], 'sha256': selección_VALOR['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_fila['filename'], datos, Nome, LOG_fila['version'])
            배포경로.write_bytes(datos)
            LOG_camiño.write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2) + '\n')
        if LOG_fila['name'] != Nome or versión_VALOR and LOG_fila['version'] != versión_VALOR:
            raise ValueError('repositorio_raíz Nome·버전 불일치')
        파일들 = 압축풀기(LOG_fila['filename'], datos, Nome, LOG_fila['version'])
        return Transferir_paquete(Nome, LOG_fila['version'], 파일들, LOG_fila['url'])


class paquete_solicitude(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            solicitude = bytearray()
            while b'\n' not in solicitude and len(solicitude) < 100:
                조각 = 자신.request.recv(100 - len(solicitude))
                if not 조각:
                    return
                solicitude.extend(조각)
            if not solicitude.endswith(b'\n') or solicitude.count(b'\n') != 1:
                raise ValueError('잘못된 paquete solicitude')
            resposta = 자신.server.repositorio_raíz.준비(solicitude[:-1].decode('ascii'))
        except Exception as ERRO:
            머리 = json.dumps({'error': str(ERRO)[:500]}, ensure_ascii=False).encode()
            resposta = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(resposta)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, número_do_porto=8027, CAMIÑO=None, Tecnoloxía_da_información_TI_Desconectado=False):
        자신.servidor_VALOR = socketserver.TCPServer(('127.0.0.1', número_do_porto), paquete_solicitude, bind_and_activate=False)
        자신.servidor_VALOR.allow_reuse_address = True
        자신.servidor_VALOR.server_bind()
        자신.servidor_VALOR.server_activate()
        자신.servidor_VALOR.repositorio_raíz = paquete_repositorio(CAMIÑO or Project_raíz/'build/pip-cache', Tecnoloxía_da_información_TI_Desconectado)
        자신.número_do_porto = 자신.servidor_VALOR.server_address[1]
        자신.tema_VALOR = threading.Thread(target=자신.servidor_VALOR.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.tema_VALOR.start()
        return 자신

    def __exit__(자신, *Argumentos):
        자신.servidor_VALOR.shutdown()
        자신.servidor_VALOR.server_close()
        자신.tema_VALOR.join(timeout=2)


def Executar_2():
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('--port', type=int, default=8027)
    analizador_48ee4b1b.add_argument('--cache', type=Path, default=Project_raíz/'build/pip-cache')
    analizador_48ee4b1b.add_argument('--offline', action='store_true')
    analizador_48ee4b1b.add_argument('--fetch', help='executar_comando 없이 호환 배포 파일을 내려받아 검사·Store_VALOR')
    Argumentos = analizador_48ee4b1b.parse_args()
    if Argumentos.fetch:
        datos = paquete_repositorio(Argumentos.cache, Argumentos.offline).준비(Argumentos.fetch)
        print('paquete 준비 완료:', Argumentos.fetch, len(datos), 'byte_VALOR')
        return
    with 꾸러미중계(Argumentos.port, Argumentos.cache, Argumentos.offline) as 중계:
        print('paquete 중계: 127.0.0.1:' + str(중계.número_do_porto), flush=True)
        try:
            중계.tema_VALOR.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Executar_2()
