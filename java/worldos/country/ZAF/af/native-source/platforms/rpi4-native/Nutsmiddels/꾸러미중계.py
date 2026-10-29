#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installeer_VALUE·실행한다."""
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

Project_wortel = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('bondel Naam 또는 Naam==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def valideer_pad(Naam, installering_pad=True):
    Pad = PurePosixPath(Naam)
    if Pad.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Naam.split('/')):
        raise ValueError('허용하지 않는 bondel Pad: ' + Naam)
    if '\\' in Naam or any(ord(karakter_VALUE) < 32 or ord(karakter_VALUE) == 127 for karakter_VALUE in Naam):
        raise ValueError('잘못된 bondel Pad 문자')
    if installering_pad and (len(('/lib/' + Naam).encode()) > 63 or Naam in ('한국어.py', 'bondel.py')):
        raise ValueError('bondel Pad 제한 또는 verstekwaarde biblioteek 충돌: ' + Naam)
    return Naam


def 압축풀기(lêer_inskrywing_naam, data, Naam, weergawe_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(Pad, Inhoud_VALUE):
        valideer_pad(Pad)
        if Pad in 파일들:
            raise ValueError('중복 bondel Pad: ' + Pad)
        if len(Inhoud_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Pad)
        Inhoud_VALUE.decode('utf-8')
        파일들[Pad] = Inhoud_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 bron_boom 16개·합계 64 KiB 이하여야 합니다.')
    if lêer_inskrywing_naam.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as bondel:
            항목들 = bondel.infolist()
            if len(항목들) > 256 or sum(inskrywing_VALUE.file_size for inskrywing_VALUE in 항목들) > 1048576:
                raise ValueError('Argief_VALUE stel_vry_Berging Grootte 제한 초과')
            saak_Lys = [inskrywing_VALUE for inskrywing_VALUE in 항목들 if inskrywing_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(saak_Lys) != 1:
                raise ValueError('wheel saak_VALUE 명세가 필요합니다.')
            saak_VALUE = email.parser.Parser().parsestr(bondel.read(saak_Lys[0]).decode())
            if saak_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not lêer_inskrywing_naam.endswith('-none-any.whl'):
                raise ValueError('C uitbreiding_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for inskrywing_VALUE in 항목들:
                Pad = inskrywing_VALUE.filename.rstrip('/')
                valideer_pad(Pad, False)
                if (inskrywing_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if inskrywing_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in Pad:
                    if Pad.endswith('/METADATA'):
                        명세들.append(bondel.read(inskrywing_VALUE).decode())
                    continue
                if not Pad.endswith('.py') or '.data/' in Pad:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Pad)
                추가(Pad, bondel.read(inskrywing_VALUE))
    elif lêer_inskrywing_naam.endswith('.tar.gz') and Naam.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py uitvoer_bevel 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as bondel:
            뿌리들 = set()
            inskrywing_COUNT = 0
            전체크기 = 0
            for inskrywing_VALUE in bondel:
                inskrywing_COUNT += 1
                전체크기 += inskrywing_VALUE.size
                if inskrywing_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Argief_VALUE stel_vry_Berging Grootte 제한 초과')
                valideer_pad(inskrywing_VALUE.name, False)
                부분들 = inskrywing_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if inskrywing_VALUE.isdir():
                    continue
                if not inskrywing_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython bron_boom 배포형')
                Pad = '/'.join(부분들[1:])
                Inhoud_VALUE = bondel.extractfile(inskrywing_VALUE).read()
                if Pad.endswith('PKG-INFO'):
                    명세들.append(Inhoud_VALUE.decode())
                elif Pad.endswith('.py') and Pad not in ('setup.py',):
                    추가(Pad, Inhoud_VALUE)
                elif '.egg-info/' not in Pad and not Pad.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Pad)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 wortel_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* bron_boom 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Naam or 명세.get('Version') != weergawe_VALUE:
        raise ValueError('배포 메타데이터의 Naam·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(adres, 한도):
    if not adres.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(adres, timeout=30) as antwoord:
        if not antwoord.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 adres skuif_VALUE')
        data = antwoord.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 Lêer Grootte 제한 초과')
    return data


def oordra_bondel(Naam, weergawe_VALUE, 파일들, 출처):
    명세 = {'name': Naam, 'version': weergawe_VALUE, 'source': 출처, 'files': [
        {'path': Pad, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for Pad, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('bondel 명세 Grootte 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[inskrywing_VALUE['path']] for inskrywing_VALUE in 명세['files'])


class bondel_bewaarplek:
    def __init__(자신, Pad, 오프라인=False):
        자신.Pad = Path(Pad)
        자신.Pad.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Maak_gereed(자신, 요청):
        Naam, weergawe_VALUE = 요청해석(요청)
        열쇠 = Naam + ('==' + weergawe_VALUE if weergawe_VALUE else '')
        LOG_pad = 자신.Pad / (열쇠 + '.json')
        배포경로 = 자신.Pad / (열쇠 + '.archive')
        if LOG_pad.is_file() and 배포경로.is_file():
            LOG_ry = json.loads(LOG_pad.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_ry['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 bondel: ' + 요청)
            adres = 'https://pypi.org/pypi/' + Naam + ('/' + weergawe_VALUE if weergawe_VALUE else '') + '/json'
            Stelselinfo = json.loads(웹읽기(adres, 4194304).decode())
            if Stelselinfo['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [inskrywing_VALUE for inskrywing_VALUE in Stelselinfo['urls'] if not inskrywing_VALUE.get('yanked') and inskrywing_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Naam.startswith('micropython-'):
                후보 = [inskrywing_VALUE for inskrywing_VALUE in Stelselinfo['urls'] if not inskrywing_VALUE.get('yanked') and inskrywing_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            seleksie_VALUE = 후보[0]
            data = 웹읽기(seleksie_VALUE['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != seleksie_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Lêer SHA-256 불일치')
            LOG_ry = {'name': Naam, 'version': Stelselinfo['info']['version'], 'filename': seleksie_VALUE['filename'],
                    'url': seleksie_VALUE['url'], 'sha256': seleksie_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_ry['filename'], data, Naam, LOG_ry['version'])
            배포경로.write_bytes(data)
            LOG_pad.write_text(json.dumps(LOG_ry, ensure_ascii=False, indent=2) + '\n')
        if LOG_ry['name'] != Naam or weergawe_VALUE and LOG_ry['version'] != weergawe_VALUE:
            raise ValueError('bewaarplek_wortel Naam·버전 불일치')
        파일들 = 압축풀기(LOG_ry['filename'], data, Naam, LOG_ry['version'])
        return oordra_bondel(Naam, LOG_ry['version'], 파일들, LOG_ry['url'])


class 꾸러미요청(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            요청 = bytearray()
            while b'\n' not in 요청 and len(요청) < 100:
                조각 = 자신.request.recv(100 - len(요청))
                if not 조각:
                    return
                요청.extend(조각)
            if not 요청.endswith(b'\n') or 요청.count(b'\n') != 1:
                raise ValueError('잘못된 bondel 요청')
            antwoord = 자신.server.bewaarplek_wortel.Maak_gereed(요청[:-1].decode('ascii'))
        except Exception as Fout:
            머리 = json.dumps({'error': str(Fout)[:500]}, ensure_ascii=False).encode()
            antwoord = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(antwoord)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Pad=None, 오프라인=False):
        자신.bediener_VALUE = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.bediener_VALUE.allow_reuse_address = True
        자신.bediener_VALUE.server_bind()
        자신.bediener_VALUE.server_activate()
        자신.bediener_VALUE.bewaarplek_wortel = bondel_bewaarplek(Pad or Project_wortel/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.bediener_VALUE.server_address[1]
        자신.draad_VALUE = threading.Thread(target=자신.bediener_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.draad_VALUE.start()
        return 자신

    def __exit__(자신, *인수):
        자신.bediener_VALUE.shutdown()
        자신.bediener_VALUE.server_close()
        자신.draad_VALUE.join(timeout=2)


def Loop():
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('--port', type=int, default=8027)
    ontleder_48ee4b1b.add_argument('--cache', type=Path, default=Project_wortel/'build/pip-cache')
    ontleder_48ee4b1b.add_argument('--offline', action='store_true')
    ontleder_48ee4b1b.add_argument('--fetch', help='uitvoer_bevel 없이 호환 배포 파일을 내려받아 검사·bêre_VALUE')
    인수 = ontleder_48ee4b1b.parse_args()
    if 인수.fetch:
        data = bondel_bewaarplek(인수.cache, 인수.offline).Maak_gereed(인수.fetch)
        print('bondel Maak_gereed 완료:', 인수.fetch, len(data), 'greep_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('bondel 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.draad_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Loop()
