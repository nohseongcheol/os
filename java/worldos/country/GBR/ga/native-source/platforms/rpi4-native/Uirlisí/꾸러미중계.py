#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 suiteáil_VALUE·실행한다."""
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

teilgean_fréamh = Path(__file__).resolve().parents[1]


def parsáil_iarratas_HTTP(iarratas_HTTP):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', iarratas_HTTP)
    if not 맞음:
        raise ValueError('beart Ainm 또는 Ainm==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def bailíochtaigh_cosán(Ainm, suiteáil_cosán=True):
    CONAIR = PurePosixPath(Ainm)
    if CONAIR.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Ainm.split('/')):
        raise ValueError('허용하지 않는 beart CONAIR: ' + Ainm)
    if '\\' in Ainm or any(ord(carachtar_VALUE) < 32 or ord(carachtar_VALUE) == 127 for carachtar_VALUE in Ainm):
        raise ValueError('잘못된 beart CONAIR 문자')
    if suiteáil_cosán and (len(('/lib/' + Ainm).encode()) > 63 or Ainm in ('Gaeilge.py', 'beart.py')):
        raise ValueError('beart CONAIR 제한 또는 luach_réamhshocraithe leabharlann 충돌: ' + Ainm)
    return Ainm


def 압축풀기(comhad_iontráil_ainm, sonraí, Ainm, leagan_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(CONAIR, Inneachar_VALUE):
        bailíochtaigh_cosán(CONAIR)
        if CONAIR in 파일들:
            raise ValueError('중복 beart CONAIR: ' + CONAIR)
        if len(Inneachar_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + CONAIR)
        Inneachar_VALUE.decode('utf-8')
        파일들[CONAIR] = Inneachar_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 foinse_crann 16개·합계 64 KiB 이하여야 합니다.')
    if comhad_iontráil_ainm.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(sonraí)) as beart:
            항목들 = beart.infolist()
            if len(항목들) > 256 or sum(iontráil_VALUE.file_size for iontráil_VALUE in 항목들) > 1048576:
                raise ValueError('Cartlann_VALUE leagan_Stóras Méid 제한 초과')
            cás_Liosta = [iontráil_VALUE for iontráil_VALUE in 항목들 if iontráil_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(cás_Liosta) != 1:
                raise ValueError('wheel cás_VALUE 명세가 필요합니다.')
            cás_VALUE = email.parser.Parser().parsestr(beart.read(cás_Liosta[0]).decode())
            if cás_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not comhad_iontráil_ainm.endswith('-none-any.whl'):
                raise ValueError('C breisiú_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for iontráil_VALUE in 항목들:
                CONAIR = iontráil_VALUE.filename.rstrip('/')
                bailíochtaigh_cosán(CONAIR, False)
                if (iontráil_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if iontráil_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in CONAIR:
                    if CONAIR.endswith('/METADATA'):
                        명세들.append(beart.read(iontráil_VALUE).decode())
                    continue
                if not CONAIR.endswith('.py') or '.data/' in CONAIR:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + CONAIR)
                추가(CONAIR, beart.read(iontráil_VALUE))
    elif comhad_iontráil_ainm.endswith('.tar.gz') and Ainm.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Rith_ordú 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(sonraí), mode='r|gz') as beart:
            뿌리들 = set()
            iontráil_COUNT = 0
            전체크기 = 0
            for iontráil_VALUE in beart:
                iontráil_COUNT += 1
                전체크기 += iontráil_VALUE.size
                if iontráil_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Cartlann_VALUE leagan_Stóras Méid 제한 초과')
                bailíochtaigh_cosán(iontráil_VALUE.name, False)
                부분들 = iontráil_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if iontráil_VALUE.isdir():
                    continue
                if not iontráil_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython foinse_crann 배포형')
                CONAIR = '/'.join(부분들[1:])
                Inneachar_VALUE = beart.extractfile(iontráil_VALUE).read()
                if CONAIR.endswith('PKG-INFO'):
                    명세들.append(Inneachar_VALUE.decode())
                elif CONAIR.endswith('.py') and CONAIR not in ('setup.py',):
                    추가(CONAIR, Inneachar_VALUE)
                elif '.egg-info/' not in CONAIR and not CONAIR.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + CONAIR)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 fréamh_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* foinse_crann 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if parsáil_iarratas_HTTP(명세.get('Name', ''))[0] != Ainm or 명세.get('Version') != leagan_VALUE:
        raise ValueError('배포 메타데이터의 Ainm·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADDRESS, 한도):
    if not ADDRESS.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ADDRESS, timeout=30) as freagair:
        if not freagair.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ADDRESS bog_VALUE')
        sonraí = freagair.read(한도 + 1)
    if len(sonraí) > 한도:
        raise ValueError('배포 Comhad Méid 제한 초과')
    return sonraí


def traschur_beart(Ainm, leagan_VALUE, 파일들, 출처):
    명세 = {'name': Ainm, 'version': leagan_VALUE, 'source': 출처, 'files': [
        {'path': CONAIR, 'size': len(sonraí), 'sha256': hashlib.sha256(sonraí).hexdigest()}
        for CONAIR, sonraí in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('beart 명세 Méid 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[iontráil_VALUE['path']] for iontráil_VALUE in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, CONAIR, teicneolaíocht_faisnéise_As_Líne=False):
        자신.CONAIR = Path(CONAIR)
        자신.CONAIR.mkdir(parents=True, exist_ok=True)
        자신.teicneolaíocht_faisnéise_As_Líne = teicneolaíocht_faisnéise_As_Líne

    def Ullmhaigh(자신, iarratas_HTTP):
        Ainm, leagan_VALUE = parsáil_iarratas_HTTP(iarratas_HTTP)
        열쇠 = Ainm + ('==' + leagan_VALUE if leagan_VALUE else '')
        LOG_cosán = 자신.CONAIR / (열쇠 + '.json')
        배포경로 = 자신.CONAIR / (열쇠 + '.archive')
        if LOG_cosán.is_file() and 배포경로.is_file():
            LOG_ró = json.loads(LOG_cosán.read_text())
            sonraí = 배포경로.read_bytes()
            if hashlib.sha256(sonraí).hexdigest() != LOG_ró['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.teicneolaíocht_faisnéise_As_Líne:
                raise ValueError('teicneolaíocht_faisnéise_As_Líne 저장소에 없는 beart: ' + iarratas_HTTP)
            ADDRESS = 'https://pypi.org/pypi/' + Ainm + ('/' + leagan_VALUE if leagan_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADDRESS, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [iontráil_VALUE for iontráil_VALUE in msinfo32_exe['urls'] if not iontráil_VALUE.get('yanked') and iontráil_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Ainm.startswith('micropython-'):
                후보 = [iontráil_VALUE for iontráil_VALUE in msinfo32_exe['urls'] if not iontráil_VALUE.get('yanked') and iontráil_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            roghnú_VALUE = 후보[0]
            sonraí = 웹읽기(roghnú_VALUE['url'], 4194304)
            if hashlib.sha256(sonraí).hexdigest() != roghnú_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Comhad SHA-256 불일치')
            LOG_ró = {'name': Ainm, 'version': msinfo32_exe['info']['version'], 'filename': roghnú_VALUE['filename'],
                    'url': roghnú_VALUE['url'], 'sha256': roghnú_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_ró['filename'], sonraí, Ainm, LOG_ró['version'])
            배포경로.write_bytes(sonraí)
            LOG_cosán.write_text(json.dumps(LOG_ró, ensure_ascii=False, indent=2) + '\n')
        if LOG_ró['name'] != Ainm or leagan_VALUE and LOG_ró['version'] != leagan_VALUE:
            raise ValueError('저장소 Ainm·버전 불일치')
        파일들 = 압축풀기(LOG_ró['filename'], sonraí, Ainm, LOG_ró['version'])
        return traschur_beart(Ainm, LOG_ró['version'], 파일들, LOG_ró['url'])


class beart_iarratas_HTTP(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            iarratas_HTTP = bytearray()
            while b'\n' not in iarratas_HTTP and len(iarratas_HTTP) < 100:
                조각 = 자신.request.recv(100 - len(iarratas_HTTP))
                if not 조각:
                    return
                iarratas_HTTP.extend(조각)
            if not iarratas_HTTP.endswith(b'\n') or iarratas_HTTP.count(b'\n') != 1:
                raise ValueError('잘못된 beart iarratas_HTTP')
            freagair = 자신.server.저장소.Ullmhaigh(iarratas_HTTP[:-1].decode('ascii'))
        except Exception as ERREÁID:
            머리 = json.dumps({'error': str(ERREÁID)[:500]}, ensure_ascii=False).encode()
            freagair = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(freagair)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, uimhir_phoirt=8027, CONAIR=None, teicneolaíocht_faisnéise_As_Líne=False):
        자신.freastalaí_VALUE = socketserver.TCPServer(('127.0.0.1', uimhir_phoirt), beart_iarratas_HTTP, bind_and_activate=False)
        자신.freastalaí_VALUE.allow_reuse_address = True
        자신.freastalaí_VALUE.server_bind()
        자신.freastalaí_VALUE.server_activate()
        자신.freastalaí_VALUE.저장소 = 꾸러미저장소(CONAIR or teilgean_fréamh/'build/pip-cache', teicneolaíocht_faisnéise_As_Líne)
        자신.uimhir_phoirt = 자신.freastalaí_VALUE.server_address[1]
        자신.snáithe_VALUE = threading.Thread(target=자신.freastalaí_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.snáithe_VALUE.start()
        return 자신

    def __exit__(자신, *Argóintí):
        자신.freastalaí_VALUE.shutdown()
        자신.freastalaí_VALUE.server_close()
        자신.snáithe_VALUE.join(timeout=2)


def Rith_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=teilgean_fréamh/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='Rith_ordú 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Argóintí = 해석기.parse_args()
    if Argóintí.fetch:
        sonraí = 꾸러미저장소(Argóintí.cache, Argóintí.offline).Ullmhaigh(Argóintí.fetch)
        print('beart Ullmhaigh 완료:', Argóintí.fetch, len(sonraí), 'beart_VALUE')
        return
    with 꾸러미중계(Argóintí.port, Argóintí.cache, Argóintí.offline) as 중계:
        print('beart 중계: 127.0.0.1:' + str(중계.uimhir_phoirt), flush=True)
        try:
            중계.snáithe_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Rith_2()
