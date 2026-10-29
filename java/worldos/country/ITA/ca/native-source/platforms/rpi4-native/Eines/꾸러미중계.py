#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instal_lar_VALOR·실행한다."""
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

Project_rel = Path(__file__).resolve().parents[1]


def analitzar_sol_licitud(sol_licitud):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', sol_licitud)
    if not 맞음:
        raise ValueError('paquet Nom 또는 Nom==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def validar_camí(Nom, instal_lació_camí=True):
    Camí = PurePosixPath(Nom)
    if Camí.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nom.split('/')):
        raise ValueError('허용하지 않는 paquet Camí: ' + Nom)
    if '\\' in Nom or any(ord(caràcter_VALOR) < 32 or ord(caràcter_VALOR) == 127 for caràcter_VALOR in Nom):
        raise ValueError('잘못된 paquet Camí 문자')
    if instal_lació_camí and (len(('/lib/' + Nom).encode()) > 63 or Nom in ('Català.py', 'paquet.py')):
        raise ValueError('paquet Camí 제한 또는 valor_per_defecte biblioteca 충돌: ' + Nom)
    return Nom


def 압축풀기(arxiu_introducció_nom, dades, Nom, versió_VALOR):
    파일들 = {}
    명세들 = []
    def Annexa_introducció(Camí, contingut_VALOR):
        validar_camí(Camí)
        if Camí in 파일들:
            raise ValueError('중복 paquet Camí: ' + Camí)
        if len(contingut_VALOR) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Camí)
        contingut_VALOR.decode('utf-8')
        파일들[Camí] = contingut_VALOR
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 font_arbre 16개·total_VALOR 64 KiB 이하여야 합니다.')
    if arxiu_introducció_nom.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(dades)) as paquet:
            항목들 = paquet.infolist()
            if len(항목들) > 256 or sum(introducció_VALOR.file_size for introducció_VALOR in 항목들) > 1048576:
                raise ValueError('Arxiu_VALOR versió_Emmagatzematge Mida 제한 초과')
            cas_Llista = [introducció_VALOR for introducció_VALOR in 항목들 if introducció_VALOR.filename.endswith('.dist-info/WHEEL')]
            if len(cas_Llista) != 1:
                raise ValueError('wheel cas_VALOR 명세가 필요합니다.')
            cas_VALOR = email.parser.Parser().parsestr(paquet.read(cas_Llista[0]).decode())
            if cas_VALOR.get('Root-Is-Purelib', '').lower() != 'true' or not arxiu_introducció_nom.endswith('-none-any.whl'):
                raise ValueError('C extensió_VALOR·플랫폼 전용 wheel은 지원하지 않습니다.')
            for introducció_VALOR in 항목들:
                Camí = introducció_VALOR.filename.rstrip('/')
                validar_camí(Camí, False)
                if (introducció_VALOR.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if introducció_VALOR.filename.endswith('/'):
                    continue
                if '.dist-info/' in Camí:
                    if Camí.endswith('/METADATA'):
                        명세들.append(paquet.read(introducció_VALOR).decode())
                    continue
                if not Camí.endswith('.py') or '.data/' in Camí:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Camí)
                Annexa_introducció(Camí, paquet.read(introducció_VALOR))
    elif arxiu_introducció_nom.endswith('.tar.gz') and Nom.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Executa_ordre 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(dades), mode='r|gz') as paquet:
            뿌리들 = set()
            introducció_COMPT = 0
            total_canviar_la_mida = 0
            for introducció_VALOR in paquet:
                introducció_COMPT += 1
                total_canviar_la_mida += introducció_VALOR.size
                if introducció_COMPT > 256 or total_canviar_la_mida > 1048576:
                    raise ValueError('Arxiu_VALOR versió_Emmagatzematge Mida 제한 초과')
                validar_camí(introducció_VALOR.name, False)
                부분들 = introducció_VALOR.name.split('/')
                뿌리들.add(부분들[0])
                if introducció_VALOR.isdir():
                    continue
                if not introducció_VALOR.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython font_arbre 배포형')
                Camí = '/'.join(부분들[1:])
                contingut_VALOR = paquet.extractfile(introducció_VALOR).read()
                if Camí.endswith('PKG-INFO'):
                    명세들.append(contingut_VALOR.decode())
                elif Camí.endswith('.py') and Camí not in ('setup.py',):
                    Annexa_introducció(Camí, contingut_VALOR)
                elif '.egg-info/' not in Camí and not Camí.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Camí)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 rel_VALOR 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* font_arbre 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if analitzar_sol_licitud(명세.get('Name', ''))[0] != Nom or 명세.get('Version') != versió_VALOR:
        raise ValueError('배포 메타데이터의 Nom·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def tancar_WWW(Adreça, 한도):
    if not Adreça.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(Adreça, timeout=30) as resposta:
        if not resposta.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 Adreça moure_VALOR')
        dades = resposta.read(한도 + 1)
    if len(dades) > 한도:
        raise ValueError('배포 Fitxer Mida 제한 초과')
    return dades


def transferir_paquet(Nom, versió_VALOR, 파일들, 출처):
    명세 = {'name': Nom, 'version': versió_VALOR, 'source': 출처, 'files': [
        {'path': Camí, 'size': len(dades), 'sha256': hashlib.sha256(dades).hexdigest()}
        for Camí, dades in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('paquet 명세 Mida 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[introducció_VALOR['path']] for introducció_VALOR in 명세['files'])


class paquet_dipòsit:
    def __init__(자신, Camí, tecnologies_de_la_informació_Desconnectat=False):
        자신.Camí = Path(Camí)
        자신.Camí.mkdir(parents=True, exist_ok=True)
        자신.tecnologies_de_la_informació_Desconnectat = tecnologies_de_la_informació_Desconnectat

    def Prepara(자신, sol_licitud):
        Nom, versió_VALOR = analitzar_sol_licitud(sol_licitud)
        열쇠 = Nom + ('==' + versió_VALOR if versió_VALOR else '')
        LOG_camí = 자신.Camí / (열쇠 + '.json')
        배포경로 = 자신.Camí / (열쇠 + '.archive')
        if LOG_camí.is_file() and 배포경로.is_file():
            LOG_fila = json.loads(LOG_camí.read_text())
            dades = 배포경로.read_bytes()
            if hashlib.sha256(dades).hexdigest() != LOG_fila['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.tecnologies_de_la_informació_Desconnectat:
                raise ValueError('tecnologies_de_la_informació_Desconnectat 저장소에 없는 paquet: ' + sol_licitud)
            Adreça = 'https://pypi.org/pypi/' + Nom + ('/' + versió_VALOR if versió_VALOR else '') + '/json'
            msinfo32_exe = json.loads(tancar_WWW(Adreça, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [introducció_VALOR for introducció_VALOR in msinfo32_exe['urls'] if not introducció_VALOR.get('yanked') and introducció_VALOR['filename'].endswith('-none-any.whl')]
            if not 후보 and Nom.startswith('micropython-'):
                후보 = [introducció_VALOR for introducció_VALOR in msinfo32_exe['urls'] if not introducció_VALOR.get('yanked') and introducció_VALOR['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            selecció_VALOR = 후보[0]
            dades = tancar_WWW(selecció_VALOR['url'], 4194304)
            if hashlib.sha256(dades).hexdigest() != selecció_VALOR['digests']['sha256']:
                raise ValueError('PyPI 배포 Fitxer SHA-256 불일치')
            LOG_fila = {'name': Nom, 'version': msinfo32_exe['info']['version'], 'filename': selecció_VALOR['filename'],
                    'url': selecció_VALOR['url'], 'sha256': selecció_VALOR['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_fila['filename'], dades, Nom, LOG_fila['version'])
            배포경로.write_bytes(dades)
            LOG_camí.write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2) + '\n')
        if LOG_fila['name'] != Nom or versió_VALOR and LOG_fila['version'] != versió_VALOR:
            raise ValueError('dipòsit_rel Nom·버전 불일치')
        파일들 = 압축풀기(LOG_fila['filename'], dades, Nom, LOG_fila['version'])
        return transferir_paquet(Nom, LOG_fila['version'], 파일들, LOG_fila['url'])


class paquet_sol_licitud(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            sol_licitud = bytearray()
            while b'\n' not in sol_licitud and len(sol_licitud) < 100:
                조각 = 자신.request.recv(100 - len(sol_licitud))
                if not 조각:
                    return
                sol_licitud.extend(조각)
            if not sol_licitud.endswith(b'\n') or sol_licitud.count(b'\n') != 1:
                raise ValueError('잘못된 paquet sol_licitud')
            resposta = 자신.server.dipòsit_rel.Prepara(sol_licitud[:-1].decode('ascii'))
        except Exception as s_ha_produït_un_error:
            머리 = json.dumps({'error': str(s_ha_produït_un_error)[:500]}, ensure_ascii=False).encode()
            resposta = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(resposta)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, número_de_port=8027, Camí=None, tecnologies_de_la_informació_Desconnectat=False):
        자신.servidor_VALOR = socketserver.TCPServer(('127.0.0.1', número_de_port), paquet_sol_licitud, bind_and_activate=False)
        자신.servidor_VALOR.allow_reuse_address = True
        자신.servidor_VALOR.server_bind()
        자신.servidor_VALOR.server_activate()
        자신.servidor_VALOR.dipòsit_rel = paquet_dipòsit(Camí or Project_rel/'build/pip-cache', tecnologies_de_la_informació_Desconnectat)
        자신.número_de_port = 자신.servidor_VALOR.server_address[1]
        자신.fil_VALOR = threading.Thread(target=자신.servidor_VALOR.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.fil_VALOR.start()
        return 자신

    def __exit__(자신, *인수):
        자신.servidor_VALOR.shutdown()
        자신.servidor_VALOR.server_close()
        자신.fil_VALOR.join(timeout=2)


def Executa_2():
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('--port', type=int, default=8027)
    analitzador_48ee4b1b.add_argument('--cache', type=Path, default=Project_rel/'build/pip-cache')
    analitzador_48ee4b1b.add_argument('--offline', action='store_true')
    analitzador_48ee4b1b.add_argument('--fetch', help='Executa_ordre 없이 호환 배포 파일을 내려받아 검사·Store_VALOR')
    인수 = analitzador_48ee4b1b.parse_args()
    if 인수.fetch:
        dades = paquet_dipòsit(인수.cache, 인수.offline).Prepara(인수.fetch)
        print('paquet Prepara 완료:', 인수.fetch, len(dades), 'byte_VALOR')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('paquet 중계: 127.0.0.1:' + str(중계.número_de_port), flush=True)
        try:
            중계.fil_VALOR.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Executa_2()
