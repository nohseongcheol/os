#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 setja_upp_VALUE·실행한다."""
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

verk_rót = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('búnt Heiti 또는 Heiti==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def staðfesta_slóð(Heiti, uppsetning_slóð=True):
    SLÓÐ = PurePosixPath(Heiti)
    if SLÓÐ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Heiti.split('/')):
        raise ValueError('허용하지 않는 búnt SLÓÐ: ' + Heiti)
    if '\\' in Heiti or any(ord(stafur_VALUE) < 32 or ord(stafur_VALUE) == 127 for stafur_VALUE in Heiti):
        raise ValueError('잘못된 búnt SLÓÐ 문자')
    if uppsetning_slóð and (len(('/lib/' + Heiti).encode()) > 63 or Heiti in ('Íslenska.py', 'búnt.py')):
        raise ValueError('búnt SLÓÐ 제한 또는 sjálfgildi safn 충돌: ' + Heiti)
    return Heiti


def 압축풀기(skrá_færsla_heiti, gögn, Heiti, útgáfa_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(SLÓÐ, Efni_VALUE):
        staðfesta_slóð(SLÓÐ)
        if SLÓÐ in 파일들:
            raise ValueError('중복 búnt SLÓÐ: ' + SLÓÐ)
        if len(Efni_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + SLÓÐ)
        Efni_VALUE.decode('utf-8')
        파일들[SLÓÐ] = Efni_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 uppruni_tré 16개·samtala_VALUE 64 KiB 이하여야 합니다.')
    if skrá_færsla_heiti.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(gögn)) as búnt:
            항목들 = búnt.infolist()
            if len(항목들) > 256 or sum(færsla_VALUE.file_size for færsla_VALUE in 항목들) > 1048576:
                raise ValueError('Safn_VALUE losa_geymsla Stærð 제한 초과')
            mál_Listi = [færsla_VALUE for færsla_VALUE in 항목들 if færsla_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(mál_Listi) != 1:
                raise ValueError('wheel samningsvirði 명세가 필요합니다.')
            samningsvirði = email.parser.Parser().parsestr(búnt.read(mál_Listi[0]).decode())
            if samningsvirði.get('Root-Is-Purelib', '').lower() != 'true' or not skrá_færsla_heiti.endswith('-none-any.whl'):
                raise ValueError('C viðbót_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for færsla_VALUE in 항목들:
                SLÓÐ = færsla_VALUE.filename.rstrip('/')
                staðfesta_slóð(SLÓÐ, False)
                if (færsla_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 númer 없습니다.')
                if færsla_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in SLÓÐ:
                    if SLÓÐ.endswith('/METADATA'):
                        명세들.append(búnt.read(færsla_VALUE).decode())
                    continue
                if not SLÓÐ.endswith('.py') or '.data/' in SLÓÐ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + SLÓÐ)
                추가(SLÓÐ, búnt.read(færsla_VALUE))
    elif skrá_færsla_heiti.endswith('.tar.gz') and Heiti.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py keyra_skipun 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(gögn), mode='r|gz') as búnt:
            뿌리들 = set()
            færsla_COUNT = 0
            samtala_breyta_stærð = 0
            for færsla_VALUE in búnt:
                færsla_COUNT += 1
                samtala_breyta_stærð += færsla_VALUE.size
                if færsla_COUNT > 256 or samtala_breyta_stærð > 1048576:
                    raise ValueError('Safn_VALUE losa_geymsla Stærð 제한 초과')
                staðfesta_slóð(færsla_VALUE.name, False)
                부분들 = færsla_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if færsla_VALUE.isdir():
                    continue
                if not færsla_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython uppruni_tré 배포형')
                SLÓÐ = '/'.join(부분들[1:])
                Efni_VALUE = búnt.extractfile(færsla_VALUE).read()
                if SLÓÐ.endswith('PKG-INFO'):
                    명세들.append(Efni_VALUE.decode())
                elif SLÓÐ.endswith('.py') and SLÓÐ not in ('setup.py',):
                    추가(SLÓÐ, Efni_VALUE)
                elif '.egg-info/' not in SLÓÐ and not SLÓÐ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + SLÓÐ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 rót_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* uppruni_tré 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 dreifing_VALUE 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Heiti or 명세.get('Version') != útgáfa_VALUE:
        raise ValueError('dreifing_VALUE 메타데이터의 Heiti·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(slóð, 한도):
    if not slóð.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS dreifing_VALUE 주소만 허용합니다.')
    with urllib.request.urlopen(slóð, timeout=30) as svara:
        if not svara.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 dreifing_VALUE slóð færa_VALUE')
        gögn = svara.read(한도 + 1)
    if len(gögn) > 한도:
        raise ValueError('dreifing_VALUE Skrá Stærð 제한 초과')
    return gögn


def flytja_búnt(Heiti, útgáfa_VALUE, 파일들, 출처):
    명세 = {'name': Heiti, 'version': útgáfa_VALUE, 'source': 출처, 'files': [
        {'path': SLÓÐ, 'size': len(gögn), 'sha256': hashlib.sha256(gögn).hexdigest()}
        for SLÓÐ, gögn in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('búnt 명세 Stærð 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[færsla_VALUE['path']] for færsla_VALUE in 명세['files'])


class búnt_gagnageymsla:
    def __init__(자신, SLÓÐ, upplýsingatækni_ótengdur=False):
        자신.SLÓÐ = Path(SLÓÐ)
        자신.SLÓÐ.mkdir(parents=True, exist_ok=True)
        자신.upplýsingatækni_ótengdur = upplýsingatækni_ótengdur

    def Undirbúa(자신, 요청):
        Heiti, útgáfa_VALUE = 요청해석(요청)
        열쇠 = Heiti + ('==' + útgáfa_VALUE if útgáfa_VALUE else '')
        LOG_slóð = 자신.SLÓÐ / (열쇠 + '.json')
        dreifing_slóð = 자신.SLÓÐ / (열쇠 + '.archive')
        if LOG_slóð.is_file() and dreifing_slóð.is_file():
            LOG_lína = json.loads(LOG_slóð.read_text())
            gögn = dreifing_slóð.read_bytes()
            if hashlib.sha256(gögn).hexdigest() != LOG_lína['sha256']:
                raise ValueError('저장된 dreifing_VALUE 파일의 SHA-256 불일치')
        else:
            if 자신.upplýsingatækni_ótengdur:
                raise ValueError('upplýsingatækni_ótengdur 저장소에 없는 búnt: ' + 요청)
            slóð = 'https://pypi.org/pypi/' + Heiti + ('/' + útgáfa_VALUE if útgáfa_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(slóð, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [færsla_VALUE for færsla_VALUE in msinfo32_exe['urls'] if not færsla_VALUE.get('yanked') and færsla_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Heiti.startswith('micropython-'):
                후보 = [færsla_VALUE for færsla_VALUE in msinfo32_exe['urls'] if not færsla_VALUE.get('yanked') and færsla_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python dreifing_VALUE 파일이 없습니다.')
            val_VALUE = 후보[0]
            gögn = 웹읽기(val_VALUE['url'], 4194304)
            if hashlib.sha256(gögn).hexdigest() != val_VALUE['digests']['sha256']:
                raise ValueError('PyPI dreifing_VALUE Skrá SHA-256 불일치')
            LOG_lína = {'name': Heiti, 'version': msinfo32_exe['info']['version'], 'filename': val_VALUE['filename'],
                    'url': val_VALUE['url'], 'sha256': val_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_lína['filename'], gögn, Heiti, LOG_lína['version'])
            dreifing_slóð.write_bytes(gögn)
            LOG_slóð.write_text(json.dumps(LOG_lína, ensure_ascii=False, indent=2) + '\n')
        if LOG_lína['name'] != Heiti or útgáfa_VALUE and LOG_lína['version'] != útgáfa_VALUE:
            raise ValueError('gagnageymsla_rót Heiti·버전 불일치')
        파일들 = 압축풀기(LOG_lína['filename'], gögn, Heiti, LOG_lína['version'])
        return flytja_búnt(Heiti, LOG_lína['version'], 파일들, LOG_lína['url'])


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
                raise ValueError('잘못된 búnt 요청')
            svara = 자신.server.gagnageymsla_rót.Undirbúa(요청[:-1].decode('ascii'))
        except Exception as Villa:
            머리 = json.dumps({'error': str(Villa)[:500]}, ensure_ascii=False).encode()
            svara = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(svara)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, tengisnúmer=8027, SLÓÐ=None, upplýsingatækni_ótengdur=False):
        자신.þjónn_VALUE = socketserver.TCPServer(('127.0.0.1', tengisnúmer), 꾸러미요청, bind_and_activate=False)
        자신.þjónn_VALUE.allow_reuse_address = True
        자신.þjónn_VALUE.server_bind()
        자신.þjónn_VALUE.server_activate()
        자신.þjónn_VALUE.gagnageymsla_rót = búnt_gagnageymsla(SLÓÐ or verk_rót/'build/pip-cache', upplýsingatækni_ótengdur)
        자신.tengisnúmer = 자신.þjónn_VALUE.server_address[1]
        자신.þráður_VALUE = threading.Thread(target=자신.þjónn_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.þráður_VALUE.start()
        return 자신

    def __exit__(자신, *Viðföng):
        자신.þjónn_VALUE.shutdown()
        자신.þjónn_VALUE.server_close()
        자신.þráður_VALUE.join(timeout=2)


def Keyra_2():
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('--port', type=int, default=8027)
    þáttari_48ee4b1b.add_argument('--cache', type=Path, default=verk_rót/'build/pip-cache')
    þáttari_48ee4b1b.add_argument('--offline', action='store_true')
    þáttari_48ee4b1b.add_argument('--fetch', help='keyra_skipun 없이 호환 dreifing_VALUE 파일을 내려받아 검사·Store_VALUE')
    Viðföng = þáttari_48ee4b1b.parse_args()
    if Viðföng.fetch:
        gögn = búnt_gagnageymsla(Viðföng.cache, Viðföng.offline).Undirbúa(Viðföng.fetch)
        print('búnt Undirbúa 완료:', Viðföng.fetch, len(gögn), 'bæti_VALUE')
        return
    with 꾸러미중계(Viðföng.port, Viðföng.cache, Viðföng.offline) as 중계:
        print('búnt 중계: 127.0.0.1:' + str(중계.tengisnúmer), flush=True)
        try:
            중계.þráður_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Keyra_2()
