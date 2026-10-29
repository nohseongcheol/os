#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installa_VALUE·실행한다."""
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

pprojetta_għerq = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('lott isem 또는 isem==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def vvalida_mogħdija(isem, installazzjoni_mogħdija=True):
    mogħdija = PurePosixPath(isem)
    if mogħdija.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in isem.split('/')):
        raise ValueError('허용하지 않는 lott mogħdija: ' + isem)
    if '\\' in isem or any(ord(karattru_VALUE) < 32 or ord(karattru_VALUE) == 127 for karattru_VALUE in isem):
        raise ValueError('잘못된 lott mogħdija 문자')
    if installazzjoni_mogħdija and (len(('/lib/' + isem).encode()) > 63 or isem in ('Malti.py', 'lott.py')):
        raise ValueError('lott mogħdija 제한 또는 valur_default librerija 충돌: ' + isem)
    return isem


def 압축풀기(fajl_entrata_isem, data, isem, verżjoni_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(mogħdija, Kontenut_VALUE):
        vvalida_mogħdija(mogħdija)
        if mogħdija in 파일들:
            raise ValueError('중복 lott mogħdija: ' + mogħdija)
        if len(Kontenut_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + mogħdija)
        Kontenut_VALUE.decode('utf-8')
        파일들[mogħdija] = Kontenut_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 sors_siġra 16개·합계 64 KiB 이하여야 합니다.')
    if fajl_entrata_isem.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as lott:
            항목들 = lott.infolist()
            if len(항목들) > 256 or sum(entrata_VALUE.file_size for entrata_VALUE in 항목들) > 1048576:
                raise ValueError('Arkivju_VALUE mexxi_Ħażna daqqas 제한 초과')
            każ_Lista = [entrata_VALUE for entrata_VALUE in 항목들 if entrata_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(każ_Lista) != 1:
                raise ValueError('wheel każ_VALUE 명세가 필요합니다.')
            każ_VALUE = email.parser.Parser().parsestr(lott.read(każ_Lista[0]).decode())
            if każ_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not fajl_entrata_isem.endswith('-none-any.whl'):
                raise ValueError('C estensjoni_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for entrata_VALUE in 항목들:
                mogħdija = entrata_VALUE.filename.rstrip('/')
                vvalida_mogħdija(mogħdija, False)
                if (entrata_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if entrata_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in mogħdija:
                    if mogħdija.endswith('/METADATA'):
                        명세들.append(lott.read(entrata_VALUE).decode())
                    continue
                if not mogħdija.endswith('.py') or '.data/' in mogħdija:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + mogħdija)
                추가(mogħdija, lott.read(entrata_VALUE))
    elif fajl_entrata_isem.endswith('.tar.gz') and isem.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py eżegwixxa_kmand 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as lott:
            뿌리들 = set()
            entrata_COUNT = 0
            전체크기 = 0
            for entrata_VALUE in lott:
                entrata_COUNT += 1
                전체크기 += entrata_VALUE.size
                if entrata_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Arkivju_VALUE mexxi_Ħażna daqqas 제한 초과')
                vvalida_mogħdija(entrata_VALUE.name, False)
                부분들 = entrata_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if entrata_VALUE.isdir():
                    continue
                if not entrata_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython sors_siġra 배포형')
                mogħdija = '/'.join(부분들[1:])
                Kontenut_VALUE = lott.extractfile(entrata_VALUE).read()
                if mogħdija.endswith('PKG-INFO'):
                    명세들.append(Kontenut_VALUE.decode())
                elif mogħdija.endswith('.py') and mogħdija not in ('setup.py',):
                    추가(mogħdija, Kontenut_VALUE)
                elif '.egg-info/' not in mogħdija and not mogħdija.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + mogħdija)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 għerq_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* sors_siġra 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != isem or 명세.get('Version') != verżjoni_VALUE:
        raise ValueError('배포 메타데이터의 isem·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADDRESS, 한도):
    if not ADDRESS.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ADDRESS, timeout=30) as wieġeb:
        if not wieġeb.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ADDRESS mexxi_VALUE')
        data = wieġeb.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 fajl daqqas 제한 초과')
    return data


def trasferiment_lott(isem, verżjoni_VALUE, 파일들, 출처):
    명세 = {'name': isem, 'version': verżjoni_VALUE, 'source': 출처, 'files': [
        {'path': mogħdija, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for mogħdija, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('lott 명세 daqqas 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[entrata_VALUE['path']] for entrata_VALUE in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, mogħdija, 오프라인=False):
        자신.mogħdija = Path(mogħdija)
        자신.mogħdija.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Ħejji(자신, 요청):
        isem, verżjoni_VALUE = 요청해석(요청)
        열쇠 = isem + ('==' + verżjoni_VALUE if verżjoni_VALUE else '')
        LOG_mogħdija = 자신.mogħdija / (열쇠 + '.json')
        배포경로 = 자신.mogħdija / (열쇠 + '.archive')
        if LOG_mogħdija.is_file() and 배포경로.is_file():
            LOG_RECORD = json.loads(LOG_mogħdija.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_RECORD['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 lott: ' + 요청)
            ADDRESS = 'https://pypi.org/pypi/' + isem + ('/' + verżjoni_VALUE if verżjoni_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADDRESS, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [entrata_VALUE for entrata_VALUE in msinfo32_exe['urls'] if not entrata_VALUE.get('yanked') and entrata_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and isem.startswith('micropython-'):
                후보 = [entrata_VALUE for entrata_VALUE in msinfo32_exe['urls'] if not entrata_VALUE.get('yanked') and entrata_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            għażla_VALUE = 후보[0]
            data = 웹읽기(għażla_VALUE['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != għażla_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 fajl SHA-256 불일치')
            LOG_RECORD = {'name': isem, 'version': msinfo32_exe['info']['version'], 'filename': għażla_VALUE['filename'],
                    'url': għażla_VALUE['url'], 'sha256': għażla_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_RECORD['filename'], data, isem, LOG_RECORD['version'])
            배포경로.write_bytes(data)
            LOG_mogħdija.write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_RECORD['name'] != isem or verżjoni_VALUE and LOG_RECORD['version'] != verżjoni_VALUE:
            raise ValueError('저장소 isem·버전 불일치')
        파일들 = 압축풀기(LOG_RECORD['filename'], data, isem, LOG_RECORD['version'])
        return trasferiment_lott(isem, LOG_RECORD['version'], 파일들, LOG_RECORD['url'])


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
                raise ValueError('잘못된 lott 요청')
            wieġeb = 자신.server.저장소.Ħejji(요청[:-1].decode('ascii'))
        except Exception as żball:
            머리 = json.dumps({'error': str(żball)[:500]}, ensure_ascii=False).encode()
            wieġeb = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(wieġeb)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, mogħdija=None, 오프라인=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.저장소 = 꾸러미저장소(mogħdija or pprojetta_għerq/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.server_VALUE.server_address[1]
        자신.fil_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.fil_VALUE.start()
        return 자신

    def __exit__(자신, *인수):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.fil_VALUE.join(timeout=2)


def serje():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=pprojetta_għerq/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='eżegwixxa_kmand 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        data = 꾸러미저장소(인수.cache, 인수.offline).Ħejji(인수.fetch)
        print('lott Ħejji 완료:', 인수.fetch, len(data), 'byte_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('lott 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.fil_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    serje()
