#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installere_VALUE·실행한다."""
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

spegle_rot = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('bunt Namn 또는 Namn==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def bekrefte_bane(Namn, installasjon_bane=True):
    STIGE = PurePosixPath(Namn)
    if STIGE.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Namn.split('/')):
        raise ValueError('허용하지 않는 bunt STIGE: ' + Namn)
    if '\\' in Namn or any(ord(teikn_VALUE) < 32 or ord(teikn_VALUE) == 127 for teikn_VALUE in Namn):
        raise ValueError('잘못된 bunt STIGE 문자')
    if installasjon_bane and (len(('/lib/' + Namn).encode()) > 63 or Namn in ('한국어.py', 'bunt.py')):
        raise ValueError('bunt STIGE 제한 또는 standardverdi bibliotek 충돌: ' + Namn)
    return Namn


def 압축풀기(fil_oppføring_namn, data, Namn, versjon_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(STIGE, Innhald_VALUE):
        bekrefte_bane(STIGE)
        if STIGE in 파일들:
            raise ValueError('중복 bunt STIGE: ' + STIGE)
        if len(Innhald_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + STIGE)
        Innhald_VALUE.decode('utf-8')
        파일들[STIGE] = Innhald_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 kjelde_tre 16개·합계 64 KiB 이하여야 합니다.')
    if fil_oppføring_namn.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as bunt:
            항목들 = bunt.infolist()
            if len(항목들) > 256 or sum(oppføring_VALUE.file_size for oppføring_VALUE in 항목들) > 1048576:
                raise ValueError('Arkiv_VALUE frigi_Lagring Storleik 제한 초과')
            sak_Liste = [oppføring_VALUE for oppføring_VALUE in 항목들 if oppføring_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(sak_Liste) != 1:
                raise ValueError('wheel sak_VALUE 명세가 필요합니다.')
            sak_VALUE = email.parser.Parser().parsestr(bunt.read(sak_Liste[0]).decode())
            if sak_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not fil_oppføring_namn.endswith('-none-any.whl'):
                raise ValueError('C filtype_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for oppføring_VALUE in 항목들:
                STIGE = oppføring_VALUE.filename.rstrip('/')
                bekrefte_bane(STIGE, False)
                if (oppføring_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if oppføring_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in STIGE:
                    if STIGE.endswith('/METADATA'):
                        명세들.append(bunt.read(oppføring_VALUE).decode())
                    continue
                if not STIGE.endswith('.py') or '.data/' in STIGE:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + STIGE)
                추가(STIGE, bunt.read(oppføring_VALUE))
    elif fil_oppføring_namn.endswith('.tar.gz') and Namn.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Utfør_kommando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as bunt:
            뿌리들 = set()
            oppføring_COUNT = 0
            전체크기 = 0
            for oppføring_VALUE in bunt:
                oppføring_COUNT += 1
                전체크기 += oppføring_VALUE.size
                if oppføring_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Arkiv_VALUE frigi_Lagring Storleik 제한 초과')
                bekrefte_bane(oppføring_VALUE.name, False)
                부분들 = oppføring_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if oppføring_VALUE.isdir():
                    continue
                if not oppføring_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython kjelde_tre 배포형')
                STIGE = '/'.join(부분들[1:])
                Innhald_VALUE = bunt.extractfile(oppføring_VALUE).read()
                if STIGE.endswith('PKG-INFO'):
                    명세들.append(Innhald_VALUE.decode())
                elif STIGE.endswith('.py') and STIGE not in ('setup.py',):
                    추가(STIGE, Innhald_VALUE)
                elif '.egg-info/' not in STIGE and not STIGE.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + STIGE)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 rot_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* kjelde_tre 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Namn or 명세.get('Version') != versjon_VALUE:
        raise ValueError('배포 메타데이터의 Namn·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADDRESS, 한도):
    if not ADDRESS.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ADDRESS, timeout=30) as svare:
        if not svare.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ADDRESS flytte_VALUE')
        data = svare.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 Fil Storleik 제한 초과')
    return data


def Overfør_bunt(Namn, versjon_VALUE, 파일들, nullpunkt_VALUE):
    명세 = {'name': Namn, 'version': versjon_VALUE, 'source': nullpunkt_VALUE, 'files': [
        {'path': STIGE, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for STIGE, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('bunt 명세 Storleik 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[oppføring_VALUE['path']] for oppføring_VALUE in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, STIGE, informasjonsteknologi_Fråkopla=False):
        자신.STIGE = Path(STIGE)
        자신.STIGE.mkdir(parents=True, exist_ok=True)
        자신.informasjonsteknologi_Fråkopla = informasjonsteknologi_Fråkopla

    def Klargjer(자신, 요청):
        Namn, versjon_VALUE = 요청해석(요청)
        열쇠 = Namn + ('==' + versjon_VALUE if versjon_VALUE else '')
        LOG_bane = 자신.STIGE / (열쇠 + '.json')
        배포경로 = 자신.STIGE / (열쇠 + '.archive')
        if LOG_bane.is_file() and 배포경로.is_file():
            LOG_rad = json.loads(LOG_bane.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_rad['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.informasjonsteknologi_Fråkopla:
                raise ValueError('informasjonsteknologi_Fråkopla 저장소에 없는 bunt: ' + 요청)
            ADDRESS = 'https://pypi.org/pypi/' + Namn + ('/' + versjon_VALUE if versjon_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADDRESS, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [oppføring_VALUE for oppføring_VALUE in msinfo32_exe['urls'] if not oppføring_VALUE.get('yanked') and oppføring_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Namn.startswith('micropython-'):
                후보 = [oppføring_VALUE for oppføring_VALUE in msinfo32_exe['urls'] if not oppføring_VALUE.get('yanked') and oppføring_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            merkt_område_VALUE = 후보[0]
            data = 웹읽기(merkt_område_VALUE['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != merkt_område_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Fil SHA-256 불일치')
            LOG_rad = {'name': Namn, 'version': msinfo32_exe['info']['version'], 'filename': merkt_område_VALUE['filename'],
                    'url': merkt_område_VALUE['url'], 'sha256': merkt_område_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_rad['filename'], data, Namn, LOG_rad['version'])
            배포경로.write_bytes(data)
            LOG_bane.write_text(json.dumps(LOG_rad, ensure_ascii=False, indent=2) + '\n')
        if LOG_rad['name'] != Namn or versjon_VALUE and LOG_rad['version'] != versjon_VALUE:
            raise ValueError('저장소 Namn·버전 불일치')
        파일들 = 압축풀기(LOG_rad['filename'], data, Namn, LOG_rad['version'])
        return Overfør_bunt(Namn, LOG_rad['version'], 파일들, LOG_rad['url'])


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
                raise ValueError('잘못된 bunt 요청')
            svare = 자신.server.저장소.Klargjer(요청[:-1].decode('ascii'))
        except Exception as FEIL:
            머리 = json.dumps({'error': str(FEIL)[:500]}, ensure_ascii=False).encode()
            svare = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(svare)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, portnummer=8027, STIGE=None, informasjonsteknologi_Fråkopla=False):
        자신.tenar_VALUE = socketserver.TCPServer(('127.0.0.1', portnummer), 꾸러미요청, bind_and_activate=False)
        자신.tenar_VALUE.allow_reuse_address = True
        자신.tenar_VALUE.server_bind()
        자신.tenar_VALUE.server_activate()
        자신.tenar_VALUE.저장소 = 꾸러미저장소(STIGE or spegle_rot/'build/pip-cache', informasjonsteknologi_Fråkopla)
        자신.portnummer = 자신.tenar_VALUE.server_address[1]
        자신.tråd_VALUE = threading.Thread(target=자신.tenar_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.tråd_VALUE.start()
        return 자신

    def __exit__(자신, *Argument):
        자신.tenar_VALUE.shutdown()
        자신.tenar_VALUE.server_close()
        자신.tråd_VALUE.join(timeout=2)


def Køyr_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=spegle_rot/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='Utfør_kommando 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Argument = 해석기.parse_args()
    if Argument.fetch:
        data = 꾸러미저장소(Argument.cache, Argument.offline).Klargjer(Argument.fetch)
        print('bunt Klargjer 완료:', Argument.fetch, len(data), 'byte_VALUE')
        return
    with 꾸러미중계(Argument.port, Argument.cache, Argument.offline) as 중계:
        print('bunt 중계: 127.0.0.1:' + str(중계.portnummer), flush=True)
        try:
            중계.tråd_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Køyr_2()
