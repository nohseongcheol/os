#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ସଂସ୍ଥାପନ_ମୂଲ୍ୟ·실행한다."""
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

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('ବଣ୍ଡଲ୍ ନାମ 또는 ନାମ==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ବୈଧକରଣ_ପଥ_f98b46e1(ନାମ, ସଂସ୍ଥାପନୀକରଣ_ପଥ=True):
    ପଥ = PurePosixPath(ନାମ)
    if ପଥ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ନାମ.split('/')):
        raise ValueError('허용하지 않는 ବଣ୍ଡଲ୍ ପଥ: ' + ନାମ)
    if '\\' in ନାମ or any(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) < 32 or ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ) == 127 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in ନାମ):
        raise ValueError('잘못된 ବଣ୍ଡଲ୍ ପଥ 문자')
    if ସଂସ୍ଥାପନୀକରଣ_ପଥ and (len(('/lib/' + ନାମ).encode()) > 63 or ନାମ in ('한국어.py', 'ବଣ୍ଡଲ୍.py')):
        raise ValueError('ବଣ୍ଡଲ୍ ପଥ 제한 또는 ଡିଫଲ୍ଟ_ମାନ ଲାଇବ୍ରେରୀ 충돌: ' + ନାମ)
    return ନାମ


def 압축풀기(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ, ଡାଟା, ନାମ, ସଂସ୍କରଣ_ମୂଲ୍ୟ):
    파일들 = {}
    명세들 = []
    def 추가(ପଥ, ବିଷୟ_ମୂଲ୍ୟ):
        ବୈଧକରଣ_ପଥ_f98b46e1(ପଥ)
        if ପଥ in 파일들:
            raise ValueError('중복 ବଣ୍ଡଲ୍ ପଥ: ' + ପଥ)
        if len(ବିଷୟ_ମୂଲ୍ୟ) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ପଥ)
        ବିଷୟ_ମୂଲ୍ୟ.decode('utf-8')
        파일들[ପଥ] = ବିଷୟ_ମୂଲ୍ୟ
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ଉତ୍ସ_ବୃକ୍ଷ 16개·합계 64 KiB 이하여야 합니다.')
    if ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ଡାଟା)) as ବଣ୍ଡଲ୍:
            항목들 = ବଣ୍ଡଲ୍.infolist()
            if len(항목들) > 256 or sum(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.file_size for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 항목들) > 1048576:
                raise ValueError('ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ ରିଲିଜ୍_ଷ୍ଟୋରେଜ୍ ଆକାର 제한 초과')
            କର୍ମ_ତାଲିକା = [ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 항목들 if ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.filename.endswith('.dist-info/WHEEL')]
            if len(କର୍ମ_ତାଲିକା) != 1:
                raise ValueError('wheel କର୍ମ_ମୂଲ୍ୟ 명세가 필요합니다.')
            କର୍ମ_ମୂଲ୍ୟ = email.parser.Parser().parsestr(ବଣ୍ଡଲ୍.read(କର୍ମ_ତାଲିକା[0]).decode())
            if କର୍ମ_ମୂଲ୍ୟ.get('Root-Is-Purelib', '').lower() != 'true' or not ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ.endswith('-none-any.whl'):
                raise ValueError('C ଏକ୍ସଟେନସନ୍_ମୂଲ୍ୟ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 항목들:
                ପଥ = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.filename.rstrip('/')
                ବୈଧକରଣ_ପଥ_f98b46e1(ପଥ, False)
                if (ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.filename.endswith('/'):
                    continue
                if '.dist-info/' in ପଥ:
                    if ପଥ.endswith('/METADATA'):
                        명세들.append(ବଣ୍ଡଲ୍.read(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ).decode())
                    continue
                if not ପଥ.endswith('.py') or '.data/' in ପଥ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ପଥ)
                추가(ପଥ, ବଣ୍ଡଲ୍.read(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ))
    elif ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ.endswith('.tar.gz') and ନାମ.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ଡାଟା), mode='r|gz') as ବଣ୍ଡଲ୍:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ବଣ୍ଡଲ୍:
                항목수 += 1
                전체크기 += ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ଅଭିଲେଖାଗାର_ମୂଲ୍ୟ ରିଲିଜ୍_ଷ୍ଟୋରେଜ୍ ଆକାର 제한 초과')
                ବୈଧକରଣ_ପଥ_f98b46e1(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.name, False)
                부분들 = ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.name.split('/')
                뿌리들.add(부분들[0])
                if ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.isdir():
                    continue
                if not ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ଉତ୍ସ_ବୃକ୍ଷ 배포형')
                ପଥ = '/'.join(부분들[1:])
                ବିଷୟ_ମୂଲ୍ୟ = ବଣ୍ଡଲ୍.extractfile(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ).read()
                if ପଥ.endswith('PKG-INFO'):
                    명세들.append(ବିଷୟ_ମୂଲ୍ୟ.decode())
                elif ପଥ.endswith('.py') and ପଥ not in ('setup.py',):
                    추가(ପଥ, ବିଷୟ_ମୂଲ୍ୟ)
                elif '.egg-info/' not in ପଥ and not ପଥ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ପଥ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ରୁଟ୍_ମୂଲ୍ୟ 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ଉତ୍ସ_ବୃକ୍ଷ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ନାମ or 명세.get('Version') != ସଂସ୍କରଣ_ମୂଲ୍ୟ:
        raise ValueError('배포 메타데이터의 ନାମ·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ଠିକଣା, 한도):
    if not ଠିକଣା.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ଠିକଣା, timeout=30) as ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ:
        if not ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ଠିକଣା ଘୁଞ୍ଚାଇବା_ମୂଲ୍ୟ')
        ଡାଟା = ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ.read(한도 + 1)
    if len(ଡାଟା) > 한도:
        raise ValueError('배포 ଫାଇଲ ଆକାର 제한 초과')
    return ଡାଟା


def ସ୍ଥାନାନ୍ତର_ବଣ୍ଡଲ୍(ନାମ, ସଂସ୍କରଣ_ମୂଲ୍ୟ, 파일들, 출처):
    명세 = {'name': ନାମ, 'version': ସଂସ୍କରଣ_ମୂଲ୍ୟ, 'source': 출처, 'files': [
        {'path': ପଥ, 'size': len(ଡାଟା), 'sha256': hashlib.sha256(ଡାଟା).hexdigest()}
        for ପଥ, ଡାଟା in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ବଣ୍ଡଲ୍ 명세 ଆକାର 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['path']] for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, ପଥ, ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅଫଲାଇନ୍=False):
        자신.ପଥ = Path(ପଥ)
        자신.ପଥ.mkdir(parents=True, exist_ok=True)
        자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅଫଲାଇନ୍ = ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅଫଲାଇନ୍

    def ପ୍ରସ୍ତୁତ(자신, 요청):
        ନାମ, ସଂସ୍କରଣ_ମୂଲ୍ୟ = 요청해석(요청)
        열쇠 = ନାମ + ('==' + ସଂସ୍କରଣ_ମୂଲ୍ୟ if ସଂସ୍କରଣ_ମୂଲ୍ୟ else '')
        ଲଗ୍_ପଥ = 자신.ପଥ / (열쇠 + '.json')
        배포경로 = 자신.ପଥ / (열쇠 + '.archive')
        if ଲଗ୍_ପଥ.is_file() and 배포경로.is_file():
            ଲଗ୍_ଧାଡ଼ି = json.loads(ଲଗ୍_ପଥ.read_text())
            ଡାଟା = 배포경로.read_bytes()
            if hashlib.sha256(ଡାଟା).hexdigest() != ଲଗ୍_ଧାଡ଼ି['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅଫଲାଇନ୍:
                raise ValueError('ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅଫଲାଇନ୍ 저장소에 없는 ବଣ୍ଡଲ୍: ' + 요청)
            ଠିକଣା = 'https://pypi.org/pypi/' + ନାମ + ('/' + ସଂସ୍କରଣ_ମୂଲ୍ୟ if ସଂସ୍କରଣ_ମୂଲ୍ୟ else '') + '/json'
            ସିଷ୍ଟମ୍_ସୂଚନା = json.loads(웹읽기(ଠିକଣା, 4194304).decode())
            if ସିଷ୍ଟମ୍_ସୂଚନା['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ସିଷ୍ଟମ୍_ସୂଚନା['urls'] if not ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.get('yanked') and ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['filename'].endswith('-none-any.whl')]
            if not 후보 and ନାମ.startswith('micropython-'):
                후보 = [ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in ସିଷ୍ଟମ୍_ସୂଚନା['urls'] if not ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.get('yanked') and ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ଚୟନ_ମୂଲ୍ୟ = 후보[0]
            ଡାଟା = 웹읽기(ଚୟନ_ମୂଲ୍ୟ['url'], 4194304)
            if hashlib.sha256(ଡାଟା).hexdigest() != ଚୟନ_ମୂଲ୍ୟ['digests']['sha256']:
                raise ValueError('PyPI 배포 ଫାଇଲ SHA-256 불일치')
            ଲଗ୍_ଧାଡ଼ି = {'name': ନାମ, 'version': ସିଷ୍ଟମ୍_ସୂଚନା['info']['version'], 'filename': ଚୟନ_ମୂଲ୍ୟ['filename'],
                    'url': ଚୟନ_ମୂଲ୍ୟ['url'], 'sha256': ଚୟନ_ମୂଲ୍ୟ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ଲଗ୍_ଧାଡ଼ି['filename'], ଡାଟା, ନାମ, ଲଗ୍_ଧାଡ଼ି['version'])
            배포경로.write_bytes(ଡାଟା)
            ଲଗ୍_ପଥ.write_text(json.dumps(ଲଗ୍_ଧାଡ଼ି, ensure_ascii=False, indent=2) + '\n')
        if ଲଗ୍_ଧାଡ଼ି['name'] != ନାମ or ସଂସ୍କରଣ_ମୂଲ୍ୟ and ଲଗ୍_ଧାଡ଼ି['version'] != ସଂସ୍କରଣ_ମୂଲ୍ୟ:
            raise ValueError('저장소 ନାମ·버전 불일치')
        파일들 = 압축풀기(ଲଗ୍_ଧାଡ଼ି['filename'], ଡାଟା, ନାମ, ଲଗ୍_ଧାଡ଼ି['version'])
        return ସ୍ଥାନାନ୍ତର_ବଣ୍ଡଲ୍(ନାମ, ଲଗ୍_ଧାଡ଼ି['version'], 파일들, ଲଗ୍_ଧାଡ଼ି['url'])


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
                raise ValueError('잘못된 ବଣ୍ଡଲ୍ 요청')
            ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ = 자신.server.저장소.ପ୍ରସ୍ତୁତ(요청[:-1].decode('ascii'))
        except Exception as ତ୍ରୁଟି:
            머리 = json.dumps({'error': str(ତ୍ରୁଟି)[:500]}, ensure_ascii=False).encode()
            ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, ପୋର୍ଟ୍_ନମ୍ଵର୍=8027, ପଥ=None, ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅଫଲାଇନ୍=False):
        자신.ସର୍ଭର୍_ମୂଲ୍ୟ = socketserver.TCPServer(('127.0.0.1', ପୋର୍ଟ୍_ନମ୍ଵର୍), 꾸러미요청, bind_and_activate=False)
        자신.ସର୍ଭର୍_ମୂଲ୍ୟ.allow_reuse_address = True
        자신.ସର୍ଭର୍_ମୂଲ୍ୟ.server_bind()
        자신.ସର୍ଭର୍_ମୂଲ୍ୟ.server_activate()
        자신.ସର୍ଭର୍_ମୂଲ୍ୟ.저장소 = 꾸러미저장소(ପଥ or ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/pip-cache', ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅଫଲାଇନ୍)
        자신.ପୋର୍ଟ୍_ନମ୍ଵର୍ = 자신.ସର୍ଭର୍_ମୂଲ୍ୟ.server_address[1]
        자신.ଧାରା_ମୂଲ୍ୟ = threading.Thread(target=자신.ସର୍ଭର୍_ମୂଲ୍ୟ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ଧାରା_ମୂଲ୍ୟ.start()
        return 자신

    def __exit__(자신, *인수):
        자신.ସର୍ଭର୍_ମୂଲ୍ୟ.shutdown()
        자신.ସର୍ଭର୍_ମୂଲ୍ୟ.server_close()
        자신.ଧାରା_ମୂଲ୍ୟ.join(timeout=2)


def ଚଳାନ୍ତୁ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 없이 호환 배포 파일을 내려받아 검사·ସଞ୍ଚୟ_କରିବା_ମୂଲ୍ୟ')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        ଡାଟା = 꾸러미저장소(인수.cache, 인수.offline).ପ୍ରସ୍ତୁତ(인수.fetch)
        print('ବଣ୍ଡଲ୍ ପ୍ରସ୍ତୁତ 완료:', 인수.fetch, len(ଡାଟା), 'ବାଇଟ୍_ମୂଲ୍ୟ')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ବଣ୍ଡଲ୍ 중계: 127.0.0.1:' + str(중계.ପୋର୍ଟ୍_ନମ୍ଵର୍), flush=True)
        try:
            중계.ଧାରା_ମୂଲ୍ୟ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
