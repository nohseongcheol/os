#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ਸਥਾਪਿਤ_ਕਰੋ_ਕੀਮਤ·실행한다."""
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

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('ਬੰਡਲ ਨਾਂ 또는 ਨਾਂ==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ਪ੍ਰਮਾਣਿਤ_ਰਸਤਾ(ਨਾਂ, ਸਥਾਪਨਾ_ਰਸਤਾ=True):
    ਮਾਰਗ = PurePosixPath(ਨਾਂ)
    if ਮਾਰਗ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ਨਾਂ.split('/')):
        raise ValueError('허용하지 않는 ਬੰਡਲ ਮਾਰਗ: ' + ਨਾਂ)
    if '\\' in ਨਾਂ or any(ord(ਵਰਣ_ਕੀਮਤ) < 32 or ord(ਵਰਣ_ਕੀਮਤ) == 127 for ਵਰਣ_ਕੀਮਤ in ਨਾਂ):
        raise ValueError('잘못된 ਬੰਡਲ ਮਾਰਗ 문자')
    if ਸਥਾਪਨਾ_ਰਸਤਾ and (len(('/lib/' + ਨਾਂ).encode()) > 63 or ਨਾਂ in ('ਪੰਜਾਬੀ.py', 'ਬੰਡਲ.py')):
        raise ValueError('ਬੰਡਲ ਮਾਰਗ 제한 또는 ਡਿਫੌਲਟ_ਵੈਲਯੂ ਪੁਸਤਕਾਲਾ 충돌: ' + ਨਾਂ)
    return ਨਾਂ


def 압축풀기(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ, ਸਮੱਗਰੀ, ਨਾਂ, ਵਰਜ਼ਨ_ਕੀਮਤ):
    파일들 = {}
    명세들 = []
    def 추가(ਮਾਰਗ, ਤਤਕਰਾ_ਕੀਮਤ):
        ਪ੍ਰਮਾਣਿਤ_ਰਸਤਾ(ਮਾਰਗ)
        if ਮਾਰਗ in 파일들:
            raise ValueError('중복 ਬੰਡਲ ਮਾਰਗ: ' + ਮਾਰਗ)
        if len(ਤਤਕਰਾ_ਕੀਮਤ) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ਮਾਰਗ)
        ਤਤਕਰਾ_ਕੀਮਤ.decode('utf-8')
        파일들[ਮਾਰਗ] = ਤਤਕਰਾ_ਕੀਮਤ
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ਸਰੋਤ_ਟ੍ਰੀ 16개·합계 64 KiB 이하여야 합니다.')
    if ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ਸਮੱਗਰੀ)) as ਬੰਡਲ:
            항목들 = ਬੰਡਲ.infolist()
            if len(항목들) > 256 or sum(ਦਾਖਲਾ_ਕੀਮਤ.file_size for ਦਾਖਲਾ_ਕੀਮਤ in 항목들) > 1048576:
                raise ValueError('ਸੰਗ੍ਰਹਿ_ਕੀਮਤ ਰਿਲੀਜ_ਸਟੋਰੇਜ ਆਕਾਰ 제한 초과')
            ਕੰਮ_ਸੂਚੀ = [ਦਾਖਲਾ_ਕੀਮਤ for ਦਾਖਲਾ_ਕੀਮਤ in 항목들 if ਦਾਖਲਾ_ਕੀਮਤ.filename.endswith('.dist-info/WHEEL')]
            if len(ਕੰਮ_ਸੂਚੀ) != 1:
                raise ValueError('wheel ਕੰਮ_ਕੀਮਤ 명세가 필요합니다.')
            ਕੰਮ_ਕੀਮਤ = email.parser.Parser().parsestr(ਬੰਡਲ.read(ਕੰਮ_ਸੂਚੀ[0]).decode())
            if ਕੰਮ_ਕੀਮਤ.get('Root-Is-Purelib', '').lower() != 'true' or not ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ.endswith('-none-any.whl'):
                raise ValueError('C ਪ੍ਰਸਾਰ_ਕੀਮਤ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ਦਾਖਲਾ_ਕੀਮਤ in 항목들:
                ਮਾਰਗ = ਦਾਖਲਾ_ਕੀਮਤ.filename.rstrip('/')
                ਪ੍ਰਮਾਣਿਤ_ਰਸਤਾ(ਮਾਰਗ, False)
                if (ਦਾਖਲਾ_ਕੀਮਤ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ਦਾਖਲਾ_ਕੀਮਤ.filename.endswith('/'):
                    continue
                if '.dist-info/' in ਮਾਰਗ:
                    if ਮਾਰਗ.endswith('/METADATA'):
                        명세들.append(ਬੰਡਲ.read(ਦਾਖਲਾ_ਕੀਮਤ).decode())
                    continue
                if not ਮਾਰਗ.endswith('.py') or '.data/' in ਮਾਰਗ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ਮਾਰਗ)
                추가(ਮਾਰਗ, ਬੰਡਲ.read(ਦਾਖਲਾ_ਕੀਮਤ))
    elif ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ.endswith('.tar.gz') and ਨਾਂ.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ਸਮੱਗਰੀ), mode='r|gz') as ਬੰਡਲ:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ਦਾਖਲਾ_ਕੀਮਤ in ਬੰਡਲ:
                항목수 += 1
                전체크기 += ਦਾਖਲਾ_ਕੀਮਤ.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ਸੰਗ੍ਰਹਿ_ਕੀਮਤ ਰਿਲੀਜ_ਸਟੋਰੇਜ ਆਕਾਰ 제한 초과')
                ਪ੍ਰਮਾਣਿਤ_ਰਸਤਾ(ਦਾਖਲਾ_ਕੀਮਤ.name, False)
                부분들 = ਦਾਖਲਾ_ਕੀਮਤ.name.split('/')
                뿌리들.add(부분들[0])
                if ਦਾਖਲਾ_ਕੀਮਤ.isdir():
                    continue
                if not ਦਾਖਲਾ_ਕੀਮਤ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ਸਰੋਤ_ਟ੍ਰੀ 배포형')
                ਮਾਰਗ = '/'.join(부분들[1:])
                ਤਤਕਰਾ_ਕੀਮਤ = ਬੰਡਲ.extractfile(ਦਾਖਲਾ_ਕੀਮਤ).read()
                if ਮਾਰਗ.endswith('PKG-INFO'):
                    명세들.append(ਤਤਕਰਾ_ਕੀਮਤ.decode())
                elif ਮਾਰਗ.endswith('.py') and ਮਾਰਗ not in ('setup.py',):
                    추가(ਮਾਰਗ, ਤਤਕਰਾ_ਕੀਮਤ)
                elif '.egg-info/' not in ਮਾਰਗ and not ਮਾਰਗ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ਮਾਰਗ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ਰੂਟ_ਕੀਮਤ 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ਸਰੋਤ_ਟ੍ਰੀ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ਨਾਂ or 명세.get('Version') != ਵਰਜ਼ਨ_ਕੀਮਤ:
        raise ValueError('배포 메타데이터의 ਨਾਂ·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ਪਤਾ, 한도):
    if not ਪਤਾ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ਪਤਾ, timeout=30) as ਜਵਾਬ_ਦਿਓ:
        if not ਜਵਾਬ_ਦਿਓ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ਪਤਾ ਖਿਸਕਾਉਣਾ_ਕੀਮਤ')
        ਸਮੱਗਰੀ = ਜਵਾਬ_ਦਿਓ.read(한도 + 1)
    if len(ਸਮੱਗਰੀ) > 한도:
        raise ValueError('배포 ਫਾਇਲ ਆਕਾਰ 제한 초과')
    return ਸਮੱਗਰੀ


def ਸਥਾਂਨਤਰ_ਬੰਡਲ(ਨਾਂ, ਵਰਜ਼ਨ_ਕੀਮਤ, 파일들, 출처):
    명세 = {'name': ਨਾਂ, 'version': ਵਰਜ਼ਨ_ਕੀਮਤ, 'source': 출처, 'files': [
        {'path': ਮਾਰਗ, 'size': len(ਸਮੱਗਰੀ), 'sha256': hashlib.sha256(ਸਮੱਗਰੀ).hexdigest()}
        for ਮਾਰਗ, ਸਮੱਗਰੀ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ਬੰਡਲ 명세 ਆਕਾਰ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ਦਾਖਲਾ_ਕੀਮਤ['path']] for ਦਾਖਲਾ_ਕੀਮਤ in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, ਮਾਰਗ, 오프라인=False):
        자신.ਮਾਰਗ = Path(ਮਾਰਗ)
        자신.ਮਾਰਗ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def ਤਿਆਰ_ਕਰੋ(자신, 요청):
        ਨਾਂ, ਵਰਜ਼ਨ_ਕੀਮਤ = 요청해석(요청)
        열쇠 = ਨਾਂ + ('==' + ਵਰਜ਼ਨ_ਕੀਮਤ if ਵਰਜ਼ਨ_ਕੀਮਤ else '')
        ਲੌਗ_ਰਸਤਾ = 자신.ਮਾਰਗ / (열쇠 + '.json')
        배포경로 = 자신.ਮਾਰਗ / (열쇠 + '.archive')
        if ਲੌਗ_ਰਸਤਾ.is_file() and 배포경로.is_file():
            ਲੌਗ_ਕਤਾਰ = json.loads(ਲੌਗ_ਰਸਤਾ.read_text())
            ਸਮੱਗਰੀ = 배포경로.read_bytes()
            if hashlib.sha256(ਸਮੱਗਰੀ).hexdigest() != ਲੌਗ_ਕਤਾਰ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 ਬੰਡਲ: ' + 요청)
            ਪਤਾ = 'https://pypi.org/pypi/' + ਨਾਂ + ('/' + ਵਰਜ਼ਨ_ਕੀਮਤ if ਵਰਜ਼ਨ_ਕੀਮਤ else '') + '/json'
            ਸਿਸਟਮ_ਜਾਣਕਾਰੀ = json.loads(웹읽기(ਪਤਾ, 4194304).decode())
            if ਸਿਸਟਮ_ਜਾਣਕਾਰੀ['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ਦਾਖਲਾ_ਕੀਮਤ for ਦਾਖਲਾ_ਕੀਮਤ in ਸਿਸਟਮ_ਜਾਣਕਾਰੀ['urls'] if not ਦਾਖਲਾ_ਕੀਮਤ.get('yanked') and ਦਾਖਲਾ_ਕੀਮਤ['filename'].endswith('-none-any.whl')]
            if not 후보 and ਨਾਂ.startswith('micropython-'):
                후보 = [ਦਾਖਲਾ_ਕੀਮਤ for ਦਾਖਲਾ_ਕੀਮਤ in ਸਿਸਟਮ_ਜਾਣਕਾਰੀ['urls'] if not ਦਾਖਲਾ_ਕੀਮਤ.get('yanked') and ਦਾਖਲਾ_ਕੀਮਤ['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ਚੋਣ_ਕੀਮਤ = 후보[0]
            ਸਮੱਗਰੀ = 웹읽기(ਚੋਣ_ਕੀਮਤ['url'], 4194304)
            if hashlib.sha256(ਸਮੱਗਰੀ).hexdigest() != ਚੋਣ_ਕੀਮਤ['digests']['sha256']:
                raise ValueError('PyPI 배포 ਫਾਇਲ SHA-256 불일치')
            ਲੌਗ_ਕਤਾਰ = {'name': ਨਾਂ, 'version': ਸਿਸਟਮ_ਜਾਣਕਾਰੀ['info']['version'], 'filename': ਚੋਣ_ਕੀਮਤ['filename'],
                    'url': ਚੋਣ_ਕੀਮਤ['url'], 'sha256': ਚੋਣ_ਕੀਮਤ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ਲੌਗ_ਕਤਾਰ['filename'], ਸਮੱਗਰੀ, ਨਾਂ, ਲੌਗ_ਕਤਾਰ['version'])
            배포경로.write_bytes(ਸਮੱਗਰੀ)
            ਲੌਗ_ਰਸਤਾ.write_text(json.dumps(ਲੌਗ_ਕਤਾਰ, ensure_ascii=False, indent=2) + '\n')
        if ਲੌਗ_ਕਤਾਰ['name'] != ਨਾਂ or ਵਰਜ਼ਨ_ਕੀਮਤ and ਲੌਗ_ਕਤਾਰ['version'] != ਵਰਜ਼ਨ_ਕੀਮਤ:
            raise ValueError('저장소 ਨਾਂ·버전 불일치')
        파일들 = 압축풀기(ਲੌਗ_ਕਤਾਰ['filename'], ਸਮੱਗਰੀ, ਨਾਂ, ਲੌਗ_ਕਤਾਰ['version'])
        return ਸਥਾਂਨਤਰ_ਬੰਡਲ(ਨਾਂ, ਲੌਗ_ਕਤਾਰ['version'], 파일들, ਲੌਗ_ਕਤਾਰ['url'])


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
                raise ValueError('잘못된 ਬੰਡਲ 요청')
            ਜਵਾਬ_ਦਿਓ = 자신.server.저장소.ਤਿਆਰ_ਕਰੋ(요청[:-1].decode('ascii'))
        except Exception as ਗਲਤੀ:
            머리 = json.dumps({'error': str(ਗਲਤੀ)[:500]}, ensure_ascii=False).encode()
            ਜਵਾਬ_ਦਿਓ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ਜਵਾਬ_ਦਿਓ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, ਮਾਰਗ=None, 오프라인=False):
        자신.ਸਰਵਰ_ਕੀਮਤ = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.ਸਰਵਰ_ਕੀਮਤ.allow_reuse_address = True
        자신.ਸਰਵਰ_ਕੀਮਤ.server_bind()
        자신.ਸਰਵਰ_ਕੀਮਤ.server_activate()
        자신.ਸਰਵਰ_ਕੀਮਤ.저장소 = 꾸러미저장소(ਮਾਰਗ or ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.ਸਰਵਰ_ਕੀਮਤ.server_address[1]
        자신.ਥ੍ਰੈਡ_ਕੀਮਤ = threading.Thread(target=자신.ਸਰਵਰ_ਕੀਮਤ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ਥ੍ਰੈਡ_ਕੀਮਤ.start()
        return 자신

    def __exit__(자신, *ਆਰਗੂਮੈਂਟ):
        자신.ਸਰਵਰ_ਕੀਮਤ.shutdown()
        자신.ਸਰਵਰ_ਕੀਮਤ.server_close()
        자신.ਥ੍ਰੈਡ_ਕੀਮਤ.join(timeout=2)


def ਚਲਾਓ_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 없이 호환 배포 파일을 내려받아 검사·ਸੰਭਾਲੋ_ਕੀਮਤ')
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    if ਆਰਗੂਮੈਂਟ.fetch:
        ਸਮੱਗਰੀ = 꾸러미저장소(ਆਰਗੂਮੈਂਟ.cache, ਆਰਗੂਮੈਂਟ.offline).ਤਿਆਰ_ਕਰੋ(ਆਰਗੂਮੈਂਟ.fetch)
        print('ਬੰਡਲ ਤਿਆਰ_ਕਰੋ 완료:', ਆਰਗੂਮੈਂਟ.fetch, len(ਸਮੱਗਰੀ), 'ਬਾਈਟ_ਕੀਮਤ')
        return
    with 꾸러미중계(ਆਰਗੂਮੈਂਟ.port, ਆਰਗੂਮੈਂਟ.cache, ਆਰਗੂਮੈਂਟ.offline) as 중계:
        print('ਬੰਡਲ 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.ਥ੍ਰੈਡ_ਕੀਮਤ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ਚਲਾਓ_2()
