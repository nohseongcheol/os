#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instalatu_balio·실행한다."""
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

Project_erro = Path(__file__).resolve().parents[1]


def analizatu_eskaera(eskaera):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', eskaera)
    if not 맞음:
        raise ValueError('multzo Izena 또는 Izena==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def baliozkotu_bide_izen(Izena, instalazio_bide_izen=True):
    Bide_izena = PurePosixPath(Izena)
    if Bide_izena.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Izena.split('/')):
        raise ValueError('허용하지 않는 multzo Bide_izena: ' + Izena)
    if '\\' in Izena or any(ord(karaktere_balio) < 32 or ord(karaktere_balio) == 127 for karaktere_balio in Izena):
        raise ValueError('잘못된 multzo Bide_izena 문자')
    if instalazio_bide_izen and (len(('/lib/' + Izena).encode()) > 63 or Izena in ('Euskara.py', 'multzo.py')):
        raise ValueError('multzo Bide_izena 제한 또는 balio_lehenetsi liburutegi 충돌: ' + Izena)
    return Izena


def 압축풀기(fitxategi_sarrera_izen, datuak, Izena, bertsio_balio):
    파일들 = {}
    명세들 = []
    def Erantsi_sarrera(Bide_izena, eduki_balio):
        baliozkotu_bide_izen(Bide_izena)
        if Bide_izena in 파일들:
            raise ValueError('중복 multzo Bide_izena: ' + Bide_izena)
        if len(eduki_balio) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Bide_izena)
        eduki_balio.decode('utf-8')
        파일들[Bide_izena] = eduki_balio
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 iturburu_zuhaitz 16개·합계 64 KiB 이하여야 합니다.')
    if fitxategi_sarrera_izen.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(datuak)) as multzo:
            항목들 = multzo.infolist()
            if len(항목들) > 256 or sum(sarrera_balio.file_size for sarrera_balio in 항목들) > 1048576:
                raise ValueError('artxibo_balio askatu_biltegi Tamaina 제한 초과')
            kasu_Zerrenda = [sarrera_balio for sarrera_balio in 항목들 if sarrera_balio.filename.endswith('.dist-info/WHEEL')]
            if len(kasu_Zerrenda) != 1:
                raise ValueError('wheel kasu_balio 명세가 필요합니다.')
            kasu_balio = email.parser.Parser().parsestr(multzo.read(kasu_Zerrenda[0]).decode())
            if kasu_balio.get('Root-Is-Purelib', '').lower() != 'true' or not fitxategi_sarrera_izen.endswith('-none-any.whl'):
                raise ValueError('C luzapen_balio·플랫폼 전용 wheel은 지원하지 않습니다.')
            for sarrera_balio in 항목들:
                Bide_izena = sarrera_balio.filename.rstrip('/')
                baliozkotu_bide_izen(Bide_izena, False)
                if (sarrera_balio.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if sarrera_balio.filename.endswith('/'):
                    continue
                if '.dist-info/' in Bide_izena:
                    if Bide_izena.endswith('/METADATA'):
                        명세들.append(multzo.read(sarrera_balio).decode())
                    continue
                if not Bide_izena.endswith('.py') or '.data/' in Bide_izena:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Bide_izena)
                Erantsi_sarrera(Bide_izena, multzo.read(sarrera_balio))
    elif fitxategi_sarrera_izen.endswith('.tar.gz') and Izena.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py exekutatu_komando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(datuak), mode='r|gz') as multzo:
            뿌리들 = set()
            sarrera_ZENBATU = 0
            전체크기 = 0
            for sarrera_balio in multzo:
                sarrera_ZENBATU += 1
                전체크기 += sarrera_balio.size
                if sarrera_ZENBATU > 256 or 전체크기 > 1048576:
                    raise ValueError('artxibo_balio askatu_biltegi Tamaina 제한 초과')
                baliozkotu_bide_izen(sarrera_balio.name, False)
                부분들 = sarrera_balio.name.split('/')
                뿌리들.add(부분들[0])
                if sarrera_balio.isdir():
                    continue
                if not sarrera_balio.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython iturburu_zuhaitz 배포형')
                Bide_izena = '/'.join(부분들[1:])
                eduki_balio = multzo.extractfile(sarrera_balio).read()
                if Bide_izena.endswith('PKG-INFO'):
                    명세들.append(eduki_balio.decode())
                elif Bide_izena.endswith('.py') and Bide_izena not in ('setup.py',):
                    Erantsi_sarrera(Bide_izena, eduki_balio)
                elif '.egg-info/' not in Bide_izena and not Bide_izena.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Bide_izena)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 erro_balio 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* iturburu_zuhaitz 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if analizatu_eskaera(명세.get('Name', ''))[0] != Izena or 명세.get('Version') != bertsio_balio:
        raise ValueError('배포 메타데이터의 Izena·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(helbide, 한도):
    if not helbide.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(helbide, timeout=30) as erantzun:
        if not erantzun.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 helbide eraman_balio')
        datuak = erantzun.read(한도 + 1)
    if len(datuak) > 한도:
        raise ValueError('배포 Fitxategia Tamaina 제한 초과')
    return datuak


def transferitu_multzo(Izena, bertsio_balio, 파일들, 출처):
    명세 = {'name': Izena, 'version': bertsio_balio, 'source': 출처, 'files': [
        {'path': Bide_izena, 'size': len(datuak), 'sha256': hashlib.sha256(datuak).hexdigest()}
        for Bide_izena, datuak in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('multzo 명세 Tamaina 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[sarrera_balio['path']] for sarrera_balio in 명세['files'])


class multzo_biltegi:
    def __init__(자신, Bide_izena, informatika_lineaz_kanpo=False):
        자신.Bide_izena = Path(Bide_izena)
        자신.Bide_izena.mkdir(parents=True, exist_ok=True)
        자신.informatika_lineaz_kanpo = informatika_lineaz_kanpo

    def 준비(자신, eskaera):
        Izena, bertsio_balio = analizatu_eskaera(eskaera)
        열쇠 = Izena + ('==' + bertsio_balio if bertsio_balio else '')
        LOG_bide_izen = 자신.Bide_izena / (열쇠 + '.json')
        배포경로 = 자신.Bide_izena / (열쇠 + '.archive')
        if LOG_bide_izen.is_file() and 배포경로.is_file():
            LOG_marka = json.loads(LOG_bide_izen.read_text())
            datuak = 배포경로.read_bytes()
            if hashlib.sha256(datuak).hexdigest() != LOG_marka['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.informatika_lineaz_kanpo:
                raise ValueError('informatika_lineaz_kanpo 저장소에 없는 multzo: ' + eskaera)
            helbide = 'https://pypi.org/pypi/' + Izena + ('/' + bertsio_balio if bertsio_balio else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(helbide, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [sarrera_balio for sarrera_balio in msinfo32_exe['urls'] if not sarrera_balio.get('yanked') and sarrera_balio['filename'].endswith('-none-any.whl')]
            if not 후보 and Izena.startswith('micropython-'):
                후보 = [sarrera_balio for sarrera_balio in msinfo32_exe['urls'] if not sarrera_balio.get('yanked') and sarrera_balio['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            hautapen_balio = 후보[0]
            datuak = 웹읽기(hautapen_balio['url'], 4194304)
            if hashlib.sha256(datuak).hexdigest() != hautapen_balio['digests']['sha256']:
                raise ValueError('PyPI 배포 Fitxategia SHA-256 불일치')
            LOG_marka = {'name': Izena, 'version': msinfo32_exe['info']['version'], 'filename': hautapen_balio['filename'],
                    'url': hautapen_balio['url'], 'sha256': hautapen_balio['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_marka['filename'], datuak, Izena, LOG_marka['version'])
            배포경로.write_bytes(datuak)
            LOG_bide_izen.write_text(json.dumps(LOG_marka, ensure_ascii=False, indent=2) + '\n')
        if LOG_marka['name'] != Izena or bertsio_balio and LOG_marka['version'] != bertsio_balio:
            raise ValueError('biltegi_erro Izena·버전 불일치')
        파일들 = 압축풀기(LOG_marka['filename'], datuak, Izena, LOG_marka['version'])
        return transferitu_multzo(Izena, LOG_marka['version'], 파일들, LOG_marka['url'])


class multzo_eskaera(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            eskaera = bytearray()
            while b'\n' not in eskaera and len(eskaera) < 100:
                조각 = 자신.request.recv(100 - len(eskaera))
                if not 조각:
                    return
                eskaera.extend(조각)
            if not eskaera.endswith(b'\n') or eskaera.count(b'\n') != 1:
                raise ValueError('잘못된 multzo eskaera')
            erantzun = 자신.server.biltegi_erro.준비(eskaera[:-1].decode('ascii'))
        except Exception as errorea:
            머리 = json.dumps({'error': str(errorea)[:500]}, ensure_ascii=False).encode()
            erantzun = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(erantzun)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, ataka_zenbaki=8027, Bide_izena=None, informatika_lineaz_kanpo=False):
        자신.zerbitzari_balio = socketserver.TCPServer(('127.0.0.1', ataka_zenbaki), multzo_eskaera, bind_and_activate=False)
        자신.zerbitzari_balio.allow_reuse_address = True
        자신.zerbitzari_balio.server_bind()
        자신.zerbitzari_balio.server_activate()
        자신.zerbitzari_balio.biltegi_erro = multzo_biltegi(Bide_izena or Project_erro/'build/pip-cache', informatika_lineaz_kanpo)
        자신.ataka_zenbaki = 자신.zerbitzari_balio.server_address[1]
        자신.hari_balio = threading.Thread(target=자신.zerbitzari_balio.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.hari_balio.start()
        return 자신

    def __exit__(자신, *Argumentuak):
        자신.zerbitzari_balio.shutdown()
        자신.zerbitzari_balio.server_close()
        자신.hari_balio.join(timeout=2)


def Exekutatu_2():
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('--port', type=int, default=8027)
    analizatzaile_48ee4b1b.add_argument('--cache', type=Path, default=Project_erro/'build/pip-cache')
    analizatzaile_48ee4b1b.add_argument('--offline', action='store_true')
    analizatzaile_48ee4b1b.add_argument('--fetch', help='exekutatu_komando 없이 호환 배포 파일을 내려받아 검사·Store_balio')
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    if Argumentuak.fetch:
        datuak = multzo_biltegi(Argumentuak.cache, Argumentuak.offline).준비(Argumentuak.fetch)
        print('multzo 준비 완료:', Argumentuak.fetch, len(datuak), 'byte_balio')
        return
    with 꾸러미중계(Argumentuak.port, Argumentuak.cache, Argumentuak.offline) as 중계:
        print('multzo 중계: 127.0.0.1:' + str(중계.ataka_zenbaki), flush=True)
        try:
            중계.hari_balio.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Exekutatu_2()
