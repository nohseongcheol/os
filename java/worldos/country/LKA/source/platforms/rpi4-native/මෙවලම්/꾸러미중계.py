#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ස්ථාපනය_කරන්න_අගය·실행한다."""
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

기준 = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('පොදිය නම 또는 නම==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def වලංගු_කරන්න_පෙත(නම, ස්ථාපනය_පෙත=True):
    මාර්_ගය = PurePosixPath(නම)
    if මාර්_ගය.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in නම.split('/')):
        raise ValueError('허용하지 않는 පොදිය මාර්_ගය: ' + නම)
    if '\\' in නම or any(ord(අනුලකුණ_අගය) < 32 or ord(අනුලකුණ_අගය) == 127 for අනුලකුණ_අගය in නම):
        raise ValueError('잘못된 පොදිය මාර්_ගය 문자')
    if ස්ථාපනය_පෙත and (len(('/lib/' + නම).encode()) > 63 or නම in ('한국어.py', 'පොදිය.py')):
        raise ValueError('පොදිය මාර්_ගය 제한 또는 පෙරනිමි_අගය ලේඛාගාරය 충돌: ' + නම)
    return නම


def 압축풀기(ගොනුව_පිවිසුම_නම, දත්ත, නම, අනුවාදය_අගය):
    파일들 = {}
    명세들 = []
    def 추가(මාර්_ගය, අන්තර්ගතය_අගය):
        වලංගු_කරන්න_පෙත(මාර්_ගය)
        if මාර්_ගය in 파일들:
            raise ValueError('중복 පොදිය මාර්_ගය: ' + මාර්_ගය)
        if len(අන්තර්ගතය_අගය) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + මාර්_ගය)
        අන්තර්ගතය_අගය.decode('utf-8')
        파일들[මාර්_ගය] = අන්තර්ගතය_අගය
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 මූලය_රුක 16개·합계 64 KiB 이하여야 합니다.')
    if ගොනුව_පිවිසුම_නම.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(දත්ත)) as පොදිය:
            항목들 = පොදිය.infolist()
            if len(항목들) > 256 or sum(පිවිසුම_අගය.file_size for පිවිසුම_අගය in 항목들) > 1048576:
                raise ValueError('සංරක්ෂිතය_අගය මුදාහැරීම_ගබඩාව ප්_රමාණය 제한 초과')
            කාරණය_ලැයිස්තුව = [පිවිසුම_අගය for පිවිසුම_අගය in 항목들 if පිවිසුම_අගය.filename.endswith('.dist-info/WHEEL')]
            if len(කාරණය_ලැයිස්තුව) != 1:
                raise ValueError('wheel කාරණය_අගය 명세가 필요합니다.')
            කාරණය_අගය = email.parser.Parser().parsestr(පොදිය.read(කාරණය_ලැයිස්තුව[0]).decode())
            if කාරණය_අගය.get('Root-Is-Purelib', '').lower() != 'true' or not ගොනුව_පිවිසුම_නම.endswith('-none-any.whl'):
                raise ValueError('C දිගුව_අගය·플랫폼 전용 wheel은 지원하지 않습니다.')
            for පිවිසුම_අගය in 항목들:
                මාර්_ගය = පිවිසුම_අගය.filename.rstrip('/')
                වලංගු_කරන්න_පෙත(මාර්_ගය, False)
                if (පිවිසුම_අගය.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if පිවිසුම_අගය.filename.endswith('/'):
                    continue
                if '.dist-info/' in මාර්_ගය:
                    if මාර්_ගය.endswith('/METADATA'):
                        명세들.append(පොදිය.read(පිවිසුම_අගය).decode())
                    continue
                if not මාර්_ගය.endswith('.py') or '.data/' in මාර්_ගය:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + මාර්_ගය)
                추가(මාර්_ගය, පොදිය.read(පිවිසුම_අගය))
    elif ගොනුව_පිවිසුම_නම.endswith('.tar.gz') and නම.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ක්_රියාත්මක_කරන්න_විධානය 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(දත්ත), mode='r|gz') as පොදිය:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for පිවිසුම_අගය in පොදිය:
                항목수 += 1
                전체크기 += පිවිසුම_අගය.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('සංරක්ෂිතය_අගය මුදාහැරීම_ගබඩාව ප්_රමාණය 제한 초과')
                වලංගු_කරන්න_පෙත(පිවිසුම_අගය.name, False)
                부분들 = පිවිසුම_අගය.name.split('/')
                뿌리들.add(부분들[0])
                if පිවිසුම_අගය.isdir():
                    continue
                if not පිවිසුම_අගය.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython මූලය_රුක 배포형')
                මාර්_ගය = '/'.join(부분들[1:])
                අන්තර්ගතය_අගය = පොදිය.extractfile(පිවිසුම_අගය).read()
                if මාර්_ගය.endswith('PKG-INFO'):
                    명세들.append(අන්තර්ගතය_අගය.decode())
                elif මාර්_ගය.endswith('.py') and මාර්_ගය not in ('setup.py',):
                    추가(මාර්_ගය, අන්තර්ගතය_අගය)
                elif '.egg-info/' not in මාර්_ගය and not මාර්_ගය.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + මාර්_ගය)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* මූලය_රුක 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != නම or 명세.get('Version') != අනුවාදය_අගය:
        raise ValueError('배포 메타데이터의 නම·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(යොමුව, 한도):
    if not යොමුව.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(යොමුව, timeout=30) as පිළිතුරු_දෙන්න:
        if not පිළිතුරු_දෙන්න.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 යොමුව ගෙනයන්න_අගය')
        දත්ත = පිළිතුරු_දෙන්න.read(한도 + 1)
    if len(දත්ත) > 한도:
        raise ValueError('배포 ගොනු ප්_රමාණය 제한 초과')
    return දත්ත


def මාරුව_පොදිය(නම, අනුවාදය_අගය, 파일들, 출처):
    명세 = {'name': නම, 'version': අනුවාදය_අගය, 'source': 출처, 'files': [
        {'path': මාර්_ගය, 'size': len(දත්ත), 'sha256': hashlib.sha256(දත්ත).hexdigest()}
        for මාර්_ගය, දත්ත in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('පොදිය 명세 ප්_රමාණය 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[පිවිසුම_අගය['path']] for පිවිසුම_අගය in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, මාර්_ගය, 오프라인=False):
        자신.මාර්_ගය = Path(මාර්_ගය)
        자신.මාර්_ගය.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def පිළියෙල_කරන්න(자신, 요청):
        නම, අනුවාදය_අගය = 요청해석(요청)
        열쇠 = නම + ('==' + අනුවාදය_අගය if අනුවාදය_අගය else '')
        ලොගය_පෙත = 자신.මාර්_ගය / (열쇠 + '.json')
        배포경로 = 자신.මාර්_ගය / (열쇠 + '.archive')
        if ලොගය_පෙත.is_file() and 배포경로.is_file():
            ලොගය_පේළිය = json.loads(ලොගය_පෙත.read_text())
            දත්ත = 배포경로.read_bytes()
            if hashlib.sha256(දත්ත).hexdigest() != ලොගය_පේළිය['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 පොදිය: ' + 요청)
            යොමුව = 'https://pypi.org/pypi/' + නම + ('/' + අනුවාදය_අගය if අනුවාදය_අගය else '') + '/json'
            පද්ධති_තොරතුරු = json.loads(웹읽기(යොමුව, 4194304).decode())
            if පද්ධති_තොරතුරු['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [පිවිසුම_අගය for පිවිසුම_අගය in පද්ධති_තොරතුරු['urls'] if not පිවිසුම_අගය.get('yanked') and පිවිසුම_අගය['filename'].endswith('-none-any.whl')]
            if not 후보 and නම.startswith('micropython-'):
                후보 = [පිවිසුම_අගය for පිවිසුම_අගය in පද්ධති_තොරතුරු['urls'] if not පිවිසුම_අගය.get('yanked') and පිවිසුම_අගය['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            තේරීම_අගය = 후보[0]
            දත්ත = 웹읽기(තේරීම_අගය['url'], 4194304)
            if hashlib.sha256(දත්ත).hexdigest() != තේරීම_අගය['digests']['sha256']:
                raise ValueError('PyPI 배포 ගොනු SHA-256 불일치')
            ලොගය_පේළිය = {'name': නම, 'version': පද්ධති_තොරතුරු['info']['version'], 'filename': තේරීම_අගය['filename'],
                    'url': තේරීම_අගය['url'], 'sha256': තේරීම_අගය['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ලොගය_පේළිය['filename'], දත්ත, නම, ලොගය_පේළිය['version'])
            배포경로.write_bytes(දත්ත)
            ලොගය_පෙත.write_text(json.dumps(ලොගය_පේළිය, ensure_ascii=False, indent=2) + '\n')
        if ලොගය_පේළිය['name'] != නම or අනුවාදය_අගය and ලොගය_පේළිය['version'] != අනුවාදය_අගය:
            raise ValueError('저장소 නම·버전 불일치')
        파일들 = 압축풀기(ලොගය_පේළිය['filename'], දත්ත, නම, ලොගය_පේළිය['version'])
        return මාරුව_පොදිය(නම, ලොගය_පේළිය['version'], 파일들, ලොගය_පේළිය['url'])


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
                raise ValueError('잘못된 පොදිය 요청')
            පිළිතුරු_දෙන්න = 자신.server.저장소.පිළියෙල_කරන්න(요청[:-1].decode('ascii'))
        except Exception as දෝෂය:
            머리 = json.dumps({'error': str(දෝෂය)[:500]}, ensure_ascii=False).encode()
            පිළිතුරු_දෙන්න = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(පිළිතුරු_දෙන්න)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, මාර්_ගය=None, 오프라인=False):
        자신.සේවාදායකය_අගය = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.සේවාදායකය_අගය.allow_reuse_address = True
        자신.සේවාදායකය_අගය.server_bind()
        자신.සේවාදායකය_අගය.server_activate()
        자신.සේවාදායකය_අගය.저장소 = 꾸러미저장소(මාර්_ගය or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.සේවාදායකය_අගය.server_address[1]
        자신.පොට_අගය = threading.Thread(target=자신.සේවාදායකය_අගය.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.පොට_අගය.start()
        return 자신

    def __exit__(자신, *විස්තාරක):
        자신.සේවාදායකය_අගය.shutdown()
        자신.සේවාදායකය_අගය.server_close()
        자신.පොට_අගය.join(timeout=2)


def ක්_රියාත්මක_කරන්න_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ක්_රියාත්මක_කරන්න_විධානය 없이 호환 배포 파일을 내려받아 검사·ගබඩා_කරන්න_අගය')
    විස්තාරක = 해석기.parse_args()
    if විස්තාරක.fetch:
        දත්ත = 꾸러미저장소(විස්තාරක.cache, විස්තාරක.offline).පිළියෙල_කරන්න(විස්තාරක.fetch)
        print('පොදිය පිළියෙල_කරන්න 완료:', විස්තාරක.fetch, len(දත්ත), 'බයිටය_අගය')
        return
    with 꾸러미중계(විස්තාරක.port, විස්තාරක.cache, විස්තාරක.offline) as 중계:
        print('පොදිය 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.පොට_අගය.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
