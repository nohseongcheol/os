#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ინსტალაცია_მნიშვნელობა·실행한다."""
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

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('შეკვრა სახელი 또는 სახელი==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def შემოწმება_მდებარეობა_f98b46e1(სახელი, ინსტალაცია_მდებარეობა=True):
    გეზი = PurePosixPath(სახელი)
    if გეზი.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in სახელი.split('/')):
        raise ValueError('허용하지 않는 შეკვრა გეზი: ' + სახელი)
    if '\\' in სახელი or any(ord(სიმბოლო_მნიშვნელობა_068c2631) < 32 or ord(სიმბოლო_მნიშვნელობა_068c2631) == 127 for სიმბოლო_მნიშვნელობა_068c2631 in სახელი):
        raise ValueError('잘못된 შეკვრა გეზი 문자')
    if ინსტალაცია_მდებარეობა and (len(('/lib/' + სახელი).encode()) > 63 or სახელი in ('한국어.py', 'შეკვრა.py')):
        raise ValueError('შეკვრა გეზი 제한 또는 ნაგულისხმევი_მნიშვნელობა ბიბლიოთეკა 충돌: ' + სახელი)
    return სახელი


def 압축풀기(ფაილი_შენატანი_სახელი, მონაცემები, სახელი, ვერსია_მნიშვნელობა):
    파일들 = {}
    명세들 = []
    def 추가(გეზი, შიგთავსი_მნიშვნელობა):
        შემოწმება_მდებარეობა_f98b46e1(გეზი)
        if გეზი in 파일들:
            raise ValueError('중복 შეკვრა გეზი: ' + გეზი)
        if len(შიგთავსი_მნიშვნელობა) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + გეზი)
        შიგთავსი_მნიშვნელობა.decode('utf-8')
        파일들[გეზი] = შიგთავსი_მნიშვნელობა
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 წყარო_ხე 16개·합계 64 KiB 이하여야 합니다.')
    if ფაილი_შენატანი_სახელი.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(მონაცემები)) as შეკვრა:
            항목들 = შეკვრა.infolist()
            if len(항목들) > 256 or sum(შენატანი_მნიშვნელობა.file_size for შენატანი_მნიშვნელობა in 항목들) > 1048576:
                raise ValueError('არქივი_მნიშვნელობა რელიზი_საცავი ზომა 제한 초과')
            დავალება_სია = [შენატანი_მნიშვნელობა for შენატანი_მნიშვნელობა in 항목들 if შენატანი_მნიშვნელობა.filename.endswith('.dist-info/WHEEL')]
            if len(დავალება_სია) != 1:
                raise ValueError('wheel დავალება_მნიშვნელობა 명세가 필요합니다.')
            დავალება_მნიშვნელობა = email.parser.Parser().parsestr(შეკვრა.read(დავალება_სია[0]).decode())
            if დავალება_მნიშვნელობა.get('Root-Is-Purelib', '').lower() != 'true' or not ფაილი_შენატანი_სახელი.endswith('-none-any.whl'):
                raise ValueError('C გაფართოება_მნიშვნელობა·플랫폼 전용 wheel은 지원하지 않습니다.')
            for შენატანი_მნიშვნელობა in 항목들:
                გეზი = შენატანი_მნიშვნელობა.filename.rstrip('/')
                შემოწმება_მდებარეობა_f98b46e1(გეზი, False)
                if (შენატანი_მნიშვნელობა.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if შენატანი_მნიშვნელობა.filename.endswith('/'):
                    continue
                if '.dist-info/' in გეზი:
                    if გეზი.endswith('/METADATA'):
                        명세들.append(შეკვრა.read(შენატანი_მნიშვნელობა).decode())
                    continue
                if not გეზი.endswith('.py') or '.data/' in გეზი:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + გეზი)
                추가(გეზი, შეკვრა.read(შენატანი_მნიშვნელობა))
    elif ფაილი_შენატანი_სახელი.endswith('.tar.gz') and სახელი.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py შესრულება_ბრძანება 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(მონაცემები), mode='r|gz') as შეკვრა:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for შენატანი_მნიშვნელობა in შეკვრა:
                항목수 += 1
                전체크기 += შენატანი_მნიშვნელობა.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('არქივი_მნიშვნელობა რელიზი_საცავი ზომა 제한 초과')
                შემოწმება_მდებარეობა_f98b46e1(შენატანი_მნიშვნელობა.name, False)
                부분들 = შენატანი_მნიშვნელობა.name.split('/')
                뿌리들.add(부분들[0])
                if შენატანი_მნიშვნელობა.isdir():
                    continue
                if not შენატანი_მნიშვნელობა.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython წყარო_ხე 배포형')
                გეზი = '/'.join(부분들[1:])
                შიგთავსი_მნიშვნელობა = შეკვრა.extractfile(შენატანი_მნიშვნელობა).read()
                if გეზი.endswith('PKG-INFO'):
                    명세들.append(შიგთავსი_მნიშვნელობა.decode())
                elif გეზი.endswith('.py') and გეზი not in ('setup.py',):
                    추가(გეზი, შიგთავსი_მნიშვნელობა)
                elif '.egg-info/' not in გეზი and not გეზი.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + გეზი)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ფესვი_მნიშვნელობა 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* წყარო_ხე 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != სახელი or 명세.get('Version') != ვერსია_მნიშვნელობა:
        raise ValueError('배포 메타데이터의 სახელი·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(მისამართი, 한도):
    if not მისამართი.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(მისამართი, timeout=30) as პასუხი:
        if not პასუხი.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 მისამართი გადატანა_მნიშვნელობა')
        მონაცემები = პასუხი.read(한도 + 1)
    if len(მონაცემები) > 한도:
        raise ValueError('배포 ფაილი ზომა 제한 초과')
    return მონაცემები


def გადატანა_შეკვრა(სახელი, ვერსია_მნიშვნელობა, 파일들, 출처):
    명세 = {'name': სახელი, 'version': ვერსია_მნიშვნელობა, 'source': 출처, 'files': [
        {'path': გეზი, 'size': len(მონაცემები), 'sha256': hashlib.sha256(მონაცემები).hexdigest()}
        for გეზი, მონაცემები in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('შეკვრა 명세 ზომა 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[შენატანი_მნიშვნელობა['path']] for შენატანი_მნიშვნელობა in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, გეზი, 오프라인=False):
        자신.გეზი = Path(გეზი)
        자신.გეზი.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def მომზადება(자신, 요청):
        სახელი, ვერსია_მნიშვნელობა = 요청해석(요청)
        열쇠 = სახელი + ('==' + ვერსია_მნიშვნელობა if ვერსია_მნიშვნელობა else '')
        ჟურნალი_მდებარეობა = 자신.გეზი / (열쇠 + '.json')
        배포경로 = 자신.გეზი / (열쇠 + '.archive')
        if ჟურნალი_მდებარეობა.is_file() and 배포경로.is_file():
            ჟურნალი_ჩაწერა = json.loads(ჟურნალი_მდებარეობა.read_text())
            მონაცემები = 배포경로.read_bytes()
            if hashlib.sha256(მონაცემები).hexdigest() != ჟურნალი_ჩაწერა['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 შეკვრა: ' + 요청)
            მისამართი = 'https://pypi.org/pypi/' + სახელი + ('/' + ვერსია_მნიშვნელობა if ვერსია_მნიშვნელობა else '') + '/json'
            სისტემის_ინფორმაცია = json.loads(웹읽기(მისამართი, 4194304).decode())
            if სისტემის_ინფორმაცია['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [შენატანი_მნიშვნელობა for შენატანი_მნიშვნელობა in სისტემის_ინფორმაცია['urls'] if not შენატანი_მნიშვნელობა.get('yanked') and შენატანი_მნიშვნელობა['filename'].endswith('-none-any.whl')]
            if not 후보 and სახელი.startswith('micropython-'):
                후보 = [შენატანი_მნიშვნელობა for შენატანი_მნიშვნელობა in სისტემის_ინფორმაცია['urls'] if not შენატანი_მნიშვნელობა.get('yanked') and შენატანი_მნიშვნელობა['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            მონიშნული_ობიექტი_მნიშვნელობა = 후보[0]
            მონაცემები = 웹읽기(მონიშნული_ობიექტი_მნიშვნელობა['url'], 4194304)
            if hashlib.sha256(მონაცემები).hexdigest() != მონიშნული_ობიექტი_მნიშვნელობა['digests']['sha256']:
                raise ValueError('PyPI 배포 ფაილი SHA-256 불일치')
            ჟურნალი_ჩაწერა = {'name': სახელი, 'version': სისტემის_ინფორმაცია['info']['version'], 'filename': მონიშნული_ობიექტი_მნიშვნელობა['filename'],
                    'url': მონიშნული_ობიექტი_მნიშვნელობა['url'], 'sha256': მონიშნული_ობიექტი_მნიშვნელობა['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ჟურნალი_ჩაწერა['filename'], მონაცემები, სახელი, ჟურნალი_ჩაწერა['version'])
            배포경로.write_bytes(მონაცემები)
            ჟურნალი_მდებარეობა.write_text(json.dumps(ჟურნალი_ჩაწერა, ensure_ascii=False, indent=2) + '\n')
        if ჟურნალი_ჩაწერა['name'] != სახელი or ვერსია_მნიშვნელობა and ჟურნალი_ჩაწერა['version'] != ვერსია_მნიშვნელობა:
            raise ValueError('저장소 სახელი·버전 불일치')
        파일들 = 압축풀기(ჟურნალი_ჩაწერა['filename'], მონაცემები, სახელი, ჟურნალი_ჩაწერა['version'])
        return გადატანა_შეკვრა(სახელი, ჟურნალი_ჩაწერა['version'], 파일들, ჟურნალი_ჩაწერა['url'])


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
                raise ValueError('잘못된 შეკვრა 요청')
            პასუხი = 자신.server.저장소.მომზადება(요청[:-1].decode('ascii'))
        except Exception as შეცდომა:
            머리 = json.dumps({'error': str(შეცდომა)[:500]}, ensure_ascii=False).encode()
            პასუხი = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(პასუხი)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, გეზი=None, 오프라인=False):
        자신.სერვერი_მნიშვნელობა = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.სერვერი_მნიშვნელობა.allow_reuse_address = True
        자신.სერვერი_მნიშვნელობა.server_bind()
        자신.სერვერი_მნიშვნელობა.server_activate()
        자신.სერვერი_მნიშვნელობა.저장소 = 꾸러미저장소(გეზი or პროეცირება_ფესვი/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.სერვერი_მნიშვნელობა.server_address[1]
        자신.თემა_მნიშვნელობა = threading.Thread(target=자신.სერვერი_მნიშვნელობა.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.თემა_მნიშვნელობა.start()
        return 자신

    def __exit__(자신, *인수):
        자신.სერვერი_მნიშვნელობა.shutdown()
        자신.სერვერი_მნიშვნელობა.server_close()
        자신.თემა_მნიშვნელობა.join(timeout=2)


def გაშვება():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=პროეცირება_ფესვი/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='შესრულება_ბრძანება 없이 호환 배포 파일을 내려받아 검사·შენახვა_მნიშვნელობა')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        მონაცემები = 꾸러미저장소(인수.cache, 인수.offline).მომზადება(인수.fetch)
        print('შეკვრა მომზადება 완료:', 인수.fetch, len(მონაცემები), 'ბაიტი_მნიშვნელობა')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('შეკვრა 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.თემა_მნიშვნელობა.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    გაშვება()
