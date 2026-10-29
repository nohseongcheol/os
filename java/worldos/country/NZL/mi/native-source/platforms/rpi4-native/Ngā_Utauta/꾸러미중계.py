#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 tāuta_uara·실행한다."""
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

whakaatu_pūtake = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('pūpū Ingoa 또는 Ingoa==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def whakamana_ara_f98b46e1(Ingoa, tāutanga_ara=True):
    ara = PurePosixPath(Ingoa)
    if ara.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Ingoa.split('/')):
        raise ValueError('허용하지 않는 pūpū ara: ' + Ingoa)
    if '\\' in Ingoa or any(ord(pūāhua_uara) < 32 or ord(pūāhua_uara) == 127 for pūāhua_uara in Ingoa):
        raise ValueError('잘못된 pūpū ara 문자')
    if tāutanga_ara and (len(('/lib/' + Ingoa).encode()) > 63 or Ingoa in ('Reo_Māori.py', 'pūpū.py')):
        raise ValueError('pūpū ara 제한 또는 uara_taunoa puna 충돌: ' + Ingoa)
    return Ingoa


def 압축풀기(kōnae_tāurunga_ingoa, raraunga, Ingoa, putanga_uara):
    파일들 = {}
    명세들 = []
    def 추가(ara, Ihirangi_uara):
        whakamana_ara_f98b46e1(ara)
        if ara in 파일들:
            raise ValueError('중복 pūpū ara: ' + ara)
        if len(Ihirangi_uara) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ara)
        Ihirangi_uara.decode('utf-8')
        파일들[ara] = Ihirangi_uara
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 pūtake_rākau 16개·합계 64 KiB 이하여야 합니다.')
    if kōnae_tāurunga_ingoa.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(raraunga)) as pūpū:
            항목들 = pūpū.infolist()
            if len(항목들) > 256 or sum(tāurunga_uara.file_size for tāurunga_uara in 항목들) > 1048576:
                raise ValueError('Pūranga_uara tuku_Rokiroki rahi 제한 초과')
            kēhi_Rārangi = [tāurunga_uara for tāurunga_uara in 항목들 if tāurunga_uara.filename.endswith('.dist-info/WHEEL')]
            if len(kēhi_Rārangi) != 1:
                raise ValueError('wheel kēhi_uara 명세가 필요합니다.')
            kēhi_uara = email.parser.Parser().parsestr(pūpū.read(kēhi_Rārangi[0]).decode())
            if kēhi_uara.get('Root-Is-Purelib', '').lower() != 'true' or not kōnae_tāurunga_ingoa.endswith('-none-any.whl'):
                raise ValueError('C toronga_uara·플랫폼 전용 wheel은 지원하지 않습니다.')
            for tāurunga_uara in 항목들:
                ara = tāurunga_uara.filename.rstrip('/')
                whakamana_ara_f98b46e1(ara, False)
                if (tāurunga_uara.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if tāurunga_uara.filename.endswith('/'):
                    continue
                if '.dist-info/' in ara:
                    if ara.endswith('/METADATA'):
                        명세들.append(pūpū.read(tāurunga_uara).decode())
                    continue
                if not ara.endswith('.py') or '.data/' in ara:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ara)
                추가(ara, pūpū.read(tāurunga_uara))
    elif kōnae_tāurunga_ingoa.endswith('.tar.gz') and Ingoa.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py kawe_tono 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(raraunga), mode='r|gz') as pūpū:
            뿌리들 = set()
            tāurunga_COUNT = 0
            전체크기 = 0
            for tāurunga_uara in pūpū:
                tāurunga_COUNT += 1
                전체크기 += tāurunga_uara.size
                if tāurunga_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Pūranga_uara tuku_Rokiroki rahi 제한 초과')
                whakamana_ara_f98b46e1(tāurunga_uara.name, False)
                부분들 = tāurunga_uara.name.split('/')
                뿌리들.add(부분들[0])
                if tāurunga_uara.isdir():
                    continue
                if not tāurunga_uara.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython pūtake_rākau 배포형')
                ara = '/'.join(부분들[1:])
                Ihirangi_uara = pūpū.extractfile(tāurunga_uara).read()
                if ara.endswith('PKG-INFO'):
                    명세들.append(Ihirangi_uara.decode())
                elif ara.endswith('.py') and ara not in ('setup.py',):
                    추가(ara, Ihirangi_uara)
                elif '.egg-info/' not in ara and not ara.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ara)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 pūtake_uara 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* pūtake_rākau 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Ingoa or 명세.get('Version') != putanga_uara:
        raise ValueError('배포 메타데이터의 Ingoa·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADDRESS, 한도):
    if not ADDRESS.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ADDRESS, timeout=30) as whakautu:
        if not whakautu.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ADDRESS nuku_uara')
        raraunga = whakautu.read(한도 + 1)
    if len(raraunga) > 한도:
        raise ValueError('배포 Kōnae rahi 제한 초과')
    return raraunga


def whakawhiti_pūpū(Ingoa, putanga_uara, 파일들, 출처):
    명세 = {'name': Ingoa, 'version': putanga_uara, 'source': 출처, 'files': [
        {'path': ara, 'size': len(raraunga), 'sha256': hashlib.sha256(raraunga).hexdigest()}
        for ara, raraunga in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('pūpū 명세 rahi 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[tāurunga_uara['path']] for tāurunga_uara in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, ara, 오프라인=False):
        자신.ara = Path(ara)
        자신.ara.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Whakarite(자신, 요청):
        Ingoa, putanga_uara = 요청해석(요청)
        열쇠 = Ingoa + ('==' + putanga_uara if putanga_uara else '')
        LOG_ara = 자신.ara / (열쇠 + '.json')
        배포경로 = 자신.ara / (열쇠 + '.archive')
        if LOG_ara.is_file() and 배포경로.is_file():
            LOG_RECORD = json.loads(LOG_ara.read_text())
            raraunga = 배포경로.read_bytes()
            if hashlib.sha256(raraunga).hexdigest() != LOG_RECORD['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 pūpū: ' + 요청)
            ADDRESS = 'https://pypi.org/pypi/' + Ingoa + ('/' + putanga_uara if putanga_uara else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADDRESS, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [tāurunga_uara for tāurunga_uara in msinfo32_exe['urls'] if not tāurunga_uara.get('yanked') and tāurunga_uara['filename'].endswith('-none-any.whl')]
            if not 후보 and Ingoa.startswith('micropython-'):
                후보 = [tāurunga_uara for tāurunga_uara in msinfo32_exe['urls'] if not tāurunga_uara.get('yanked') and tāurunga_uara['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            tīpakonga_uara = 후보[0]
            raraunga = 웹읽기(tīpakonga_uara['url'], 4194304)
            if hashlib.sha256(raraunga).hexdigest() != tīpakonga_uara['digests']['sha256']:
                raise ValueError('PyPI 배포 Kōnae SHA-256 불일치')
            LOG_RECORD = {'name': Ingoa, 'version': msinfo32_exe['info']['version'], 'filename': tīpakonga_uara['filename'],
                    'url': tīpakonga_uara['url'], 'sha256': tīpakonga_uara['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_RECORD['filename'], raraunga, Ingoa, LOG_RECORD['version'])
            배포경로.write_bytes(raraunga)
            LOG_ara.write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_RECORD['name'] != Ingoa or putanga_uara and LOG_RECORD['version'] != putanga_uara:
            raise ValueError('저장소 Ingoa·버전 불일치')
        파일들 = 압축풀기(LOG_RECORD['filename'], raraunga, Ingoa, LOG_RECORD['version'])
        return whakawhiti_pūpū(Ingoa, LOG_RECORD['version'], 파일들, LOG_RECORD['url'])


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
                raise ValueError('잘못된 pūpū 요청')
            whakautu = 자신.server.저장소.Whakarite(요청[:-1].decode('ascii'))
        except Exception as Pōhēhē:
            머리 = json.dumps({'error': str(Pōhēhē)[:500]}, ensure_ascii=False).encode()
            whakautu = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(whakautu)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, ara=None, 오프라인=False):
        자신.tūmau_uara = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.tūmau_uara.allow_reuse_address = True
        자신.tūmau_uara.server_bind()
        자신.tūmau_uara.server_activate()
        자신.tūmau_uara.저장소 = 꾸러미저장소(ara or whakaatu_pūtake/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.tūmau_uara.server_address[1]
        자신.miro_uara = threading.Thread(target=자신.tūmau_uara.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.miro_uara.start()
        return 자신

    def __exit__(자신, *인수):
        자신.tūmau_uara.shutdown()
        자신.tūmau_uara.server_close()
        자신.miro_uara.join(timeout=2)


def whakahaere():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=whakaatu_pūtake/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='kawe_tono 없이 호환 배포 파일을 내려받아 검사·Store_uara')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        raraunga = 꾸러미저장소(인수.cache, 인수.offline).Whakarite(인수.fetch)
        print('pūpū Whakarite 완료:', 인수.fetch, len(raraunga), 'paita_uara')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('pūpū 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.miro_uara.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    whakahaere()
