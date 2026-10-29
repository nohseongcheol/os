#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ಸ್ಥಾಪಿಸು_ಮೌಲ್ಯ·실행한다."""
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

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('ಬಂಡಲ್ ಹೆಸರು 또는 ಹೆಸರು==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ಸಕ್ರಮೀಕರಿಸು_ಹಾದಿ(ಹೆಸರು, 설치경로=True):
    ಮಾರ್ಗ = PurePosixPath(ಹೆಸರು)
    if ಮಾರ್ಗ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ಹೆಸರು.split('/')):
        raise ValueError('허용하지 않는 ಬಂಡಲ್ ಮಾರ್ಗ: ' + ಹೆಸರು)
    if '\\' in ಹೆಸರು or any(ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) < 32 or ord(ಅಕ್ಷರ_ಮೌಲ್ಯ) == 127 for ಅಕ್ಷರ_ಮೌಲ್ಯ in ಹೆಸರು):
        raise ValueError('잘못된 ಬಂಡಲ್ ಮಾರ್ಗ 문자')
    if 설치경로 and (len(('/lib/' + ಹೆಸರು).encode()) > 63 or ಹೆಸರು in ('ಕನ್ನಡ.py', 'ಬಂಡಲ್.py')):
        raise ValueError('ಬಂಡಲ್ ಮಾರ್ಗ 제한 또는 ಅಕ್ಷಮ_ಬೆಲೆ ಲೈಬ್ರರಿ 충돌: ' + ಹೆಸರು)
    return ಹೆಸರು


def 압축풀기(ಫೈಲ್_ನಮೂದು_ಹೆಸರು, ಡೇಟಾ, ಹೆಸರು, ಆವೃತ್ತಿ_ಮೌಲ್ಯ):
    파일들 = {}
    명세들 = []
    def 추가(ಮಾರ್ಗ, ವಿಷಯ_ಮೌಲ್ಯ):
        ಸಕ್ರಮೀಕರಿಸು_ಹಾದಿ(ಮಾರ್ಗ)
        if ಮಾರ್ಗ in 파일들:
            raise ValueError('중복 ಬಂಡಲ್ ಮಾರ್ಗ: ' + ಮಾರ್ಗ)
        if len(ವಿಷಯ_ಮೌಲ್ಯ) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ಮಾರ್ಗ)
        ವಿಷಯ_ಮೌಲ್ಯ.decode('utf-8')
        파일들[ಮಾರ್ಗ] = ವಿಷಯ_ಮೌಲ್ಯ
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ಮೂಲ_ವೃಕ್ಷ 16개·합계 64 KiB 이하여야 합니다.')
    if ಫೈಲ್_ನಮೂದು_ಹೆಸರು.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ಡೇಟಾ)) as ಬಂಡಲ್:
            항목들 = ಬಂಡಲ್.infolist()
            if len(항목들) > 256 or sum(ನಮೂದು_ಮೌಲ್ಯ.file_size for ನಮೂದು_ಮೌಲ್ಯ in 항목들) > 1048576:
                raise ValueError('ಅರ್ಖೀವ್_ಮೌಲ್ಯ ಬಿಡುಗಡೆ_ಸಂಗ್ರಹ ಗಾತ್ರ 제한 초과')
            ಕೆಲಸ_ಪಟ್ಟಿ = [ನಮೂದು_ಮೌಲ್ಯ for ನಮೂದು_ಮೌಲ್ಯ in 항목들 if ನಮೂದು_ಮೌಲ್ಯ.filename.endswith('.dist-info/WHEEL')]
            if len(ಕೆಲಸ_ಪಟ್ಟಿ) != 1:
                raise ValueError('wheel ಕೆಲಸ_ಮೌಲ್ಯ 명세가 필요합니다.')
            ಕೆಲಸ_ಮೌಲ್ಯ = email.parser.Parser().parsestr(ಬಂಡಲ್.read(ಕೆಲಸ_ಪಟ್ಟಿ[0]).decode())
            if ಕೆಲಸ_ಮೌಲ್ಯ.get('Root-Is-Purelib', '').lower() != 'true' or not ಫೈಲ್_ನಮೂದು_ಹೆಸರು.endswith('-none-any.whl'):
                raise ValueError('C ವಿಸ್ತರಣೆ_ಮೌಲ್ಯ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ನಮೂದು_ಮೌಲ್ಯ in 항목들:
                ಮಾರ್ಗ = ನಮೂದು_ಮೌಲ್ಯ.filename.rstrip('/')
                ಸಕ್ರಮೀಕರಿಸು_ಹಾದಿ(ಮಾರ್ಗ, False)
                if (ನಮೂದು_ಮೌಲ್ಯ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ನಮೂದು_ಮೌಲ್ಯ.filename.endswith('/'):
                    continue
                if '.dist-info/' in ಮಾರ್ಗ:
                    if ಮಾರ್ಗ.endswith('/METADATA'):
                        명세들.append(ಬಂಡಲ್.read(ನಮೂದು_ಮೌಲ್ಯ).decode())
                    continue
                if not ಮಾರ್ಗ.endswith('.py') or '.data/' in ಮಾರ್ಗ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ಮಾರ್ಗ)
                추가(ಮಾರ್ಗ, ಬಂಡಲ್.read(ನಮೂದು_ಮೌಲ್ಯ))
    elif ಫೈಲ್_ನಮೂದು_ಹೆಸರು.endswith('.tar.gz') and ಹೆಸರು.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ಪೂರೈಸು_ಆದೇಶ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ಡೇಟಾ), mode='r|gz') as ಬಂಡಲ್:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ನಮೂದು_ಮೌಲ್ಯ in ಬಂಡಲ್:
                항목수 += 1
                전체크기 += ನಮೂದು_ಮೌಲ್ಯ.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ಅರ್ಖೀವ್_ಮೌಲ್ಯ ಬಿಡುಗಡೆ_ಸಂಗ್ರಹ ಗಾತ್ರ 제한 초과')
                ಸಕ್ರಮೀಕರಿಸು_ಹಾದಿ(ನಮೂದು_ಮೌಲ್ಯ.name, False)
                부분들 = ನಮೂದು_ಮೌಲ್ಯ.name.split('/')
                뿌리들.add(부분들[0])
                if ನಮೂದು_ಮೌಲ್ಯ.isdir():
                    continue
                if not ನಮೂದು_ಮೌಲ್ಯ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ಮೂಲ_ವೃಕ್ಷ 배포형')
                ಮಾರ್ಗ = '/'.join(부분들[1:])
                ವಿಷಯ_ಮೌಲ್ಯ = ಬಂಡಲ್.extractfile(ನಮೂದು_ಮೌಲ್ಯ).read()
                if ಮಾರ್ಗ.endswith('PKG-INFO'):
                    명세들.append(ವಿಷಯ_ಮೌಲ್ಯ.decode())
                elif ಮಾರ್ಗ.endswith('.py') and ಮಾರ್ಗ not in ('setup.py',):
                    추가(ಮಾರ್ಗ, ವಿಷಯ_ಮೌಲ್ಯ)
                elif '.egg-info/' not in ಮಾರ್ಗ and not ಮಾರ್ಗ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ಮಾರ್ಗ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ಮೂಲ_ಮೌಲ್ಯ 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ಮೂಲ_ವೃಕ್ಷ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ಹೆಸರು or 명세.get('Version') != ಆವೃತ್ತಿ_ಮೌಲ್ಯ:
        raise ValueError('배포 메타데이터의 ಹೆಸರು·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ಇಮೇಲ್, 한도):
    if not ಇಮೇಲ್.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ಇಮೇಲ್, timeout=30) as ಪ್ರತ್ಯುತ್ತರ:
        if not ಪ್ರತ್ಯುತ್ತರ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ಇಮೇಲ್ ಸರಿಸು_ಮೌಲ್ಯ')
        ಡೇಟಾ = ಪ್ರತ್ಯುತ್ತರ.read(한도 + 1)
    if len(ಡೇಟಾ) > 한도:
        raise ValueError('배포 ಕಡತ ಗಾತ್ರ 제한 초과')
    return ಡೇಟಾ


def ವರ್ಗಾವಣೆ_ಬಂಡಲ್(ಹೆಸರು, ಆವೃತ್ತಿ_ಮೌಲ್ಯ, 파일들, 출처):
    명세 = {'name': ಹೆಸರು, 'version': ಆವೃತ್ತಿ_ಮೌಲ್ಯ, 'source': 출처, 'files': [
        {'path': ಮಾರ್ಗ, 'size': len(ಡೇಟಾ), 'sha256': hashlib.sha256(ಡೇಟಾ).hexdigest()}
        for ಮಾರ್ಗ, ಡೇಟಾ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ಬಂಡಲ್ 명세 ಗಾತ್ರ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ನಮೂದು_ಮೌಲ್ಯ['path']] for ನಮೂದು_ಮೌಲ್ಯ in 명세['files'])


class ಬಂಡಲ್_ಸಂಗ್ರಹಣೆ:
    def __init__(자신, ಮಾರ್ಗ, ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಆಫ್_ಲೈನ್=False):
        자신.ಮಾರ್ಗ = Path(ಮಾರ್ಗ)
        자신.ಮಾರ್ಗ.mkdir(parents=True, exist_ok=True)
        자신.ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಆಫ್_ಲೈನ್ = ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಆಫ್_ಲೈನ್

    def ಸಿದ್ಧಪಡಿಸು(자신, 요청):
        ಹೆಸರು, ಆವೃತ್ತಿ_ಮೌಲ್ಯ = 요청해석(요청)
        열쇠 = ಹೆಸರು + ('==' + ಆವೃತ್ತಿ_ಮೌಲ್ಯ if ಆವೃತ್ತಿ_ಮೌಲ್ಯ else '')
        ಲಾಗ್_ಹಾದಿ = 자신.ಮಾರ್ಗ / (열쇠 + '.json')
        배포경로 = 자신.ಮಾರ್ಗ / (열쇠 + '.archive')
        if ಲಾಗ್_ಹಾದಿ.is_file() and 배포경로.is_file():
            ಲಾಗ್_ದಾಖಲೆ = json.loads(ಲಾಗ್_ಹಾದಿ.read_text())
            ಡೇಟಾ = 배포경로.read_bytes()
            if hashlib.sha256(ಡೇಟಾ).hexdigest() != ಲಾಗ್_ದಾಖಲೆ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಆಫ್_ಲೈನ್:
                raise ValueError('ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಆಫ್_ಲೈನ್ 저장소에 없는 ಬಂಡಲ್: ' + 요청)
            ಇಮೇಲ್ = 'https://pypi.org/pypi/' + ಹೆಸರು + ('/' + ಆವೃತ್ತಿ_ಮೌಲ್ಯ if ಆವೃತ್ತಿ_ಮೌಲ್ಯ else '') + '/json'
            ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ = json.loads(웹읽기(ಇಮೇಲ್, 4194304).decode())
            if ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ನಮೂದು_ಮೌಲ್ಯ for ನಮೂದು_ಮೌಲ್ಯ in ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ['urls'] if not ನಮೂದು_ಮೌಲ್ಯ.get('yanked') and ನಮೂದು_ಮೌಲ್ಯ['filename'].endswith('-none-any.whl')]
            if not 후보 and ಹೆಸರು.startswith('micropython-'):
                후보 = [ನಮೂದು_ಮೌಲ್ಯ for ನಮೂದು_ಮೌಲ್ಯ in ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ['urls'] if not ನಮೂದು_ಮೌಲ್ಯ.get('yanked') and ನಮೂದು_ಮೌಲ್ಯ['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ಆಯ್ಕೆ_ಮೌಲ್ಯ = 후보[0]
            ಡೇಟಾ = 웹읽기(ಆಯ್ಕೆ_ಮೌಲ್ಯ['url'], 4194304)
            if hashlib.sha256(ಡೇಟಾ).hexdigest() != ಆಯ್ಕೆ_ಮೌಲ್ಯ['digests']['sha256']:
                raise ValueError('PyPI 배포 ಕಡತ SHA-256 불일치')
            ಲಾಗ್_ದಾಖಲೆ = {'name': ಹೆಸರು, 'version': ಸಿಸ್ಟಮ್_ಮಾಹಿತಿ['info']['version'], 'filename': ಆಯ್ಕೆ_ಮೌಲ್ಯ['filename'],
                    'url': ಆಯ್ಕೆ_ಮೌಲ್ಯ['url'], 'sha256': ಆಯ್ಕೆ_ಮೌಲ್ಯ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ಲಾಗ್_ದಾಖಲೆ['filename'], ಡೇಟಾ, ಹೆಸರು, ಲಾಗ್_ದಾಖಲೆ['version'])
            배포경로.write_bytes(ಡೇಟಾ)
            ಲಾಗ್_ಹಾದಿ.write_text(json.dumps(ಲಾಗ್_ದಾಖಲೆ, ensure_ascii=False, indent=2) + '\n')
        if ಲಾಗ್_ದಾಖಲೆ['name'] != ಹೆಸರು or ಆವೃತ್ತಿ_ಮೌಲ್ಯ and ಲಾಗ್_ದಾಖಲೆ['version'] != ಆವೃತ್ತಿ_ಮೌಲ್ಯ:
            raise ValueError('ಸಂಗ್ರಹಣೆ_ಮೂಲ ಹೆಸರು·버전 불일치')
        파일들 = 압축풀기(ಲಾಗ್_ದಾಖಲೆ['filename'], ಡೇಟಾ, ಹೆಸರು, ಲಾಗ್_ದಾಖಲೆ['version'])
        return ವರ್ಗಾವಣೆ_ಬಂಡಲ್(ಹೆಸರು, ಲಾಗ್_ದಾಖಲೆ['version'], 파일들, ಲಾಗ್_ದಾಖಲೆ['url'])


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
                raise ValueError('잘못된 ಬಂಡಲ್ 요청')
            ಪ್ರತ್ಯುತ್ತರ = 자신.server.ಸಂಗ್ರಹಣೆ_ಮೂಲ.ಸಿದ್ಧಪಡಿಸು(요청[:-1].decode('ascii'))
        except Exception as ದೋಷ:
            머리 = json.dumps({'error': str(ದೋಷ)[:500]}, ensure_ascii=False).encode()
            ಪ್ರತ್ಯುತ್ತರ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ಪ್ರತ್ಯುತ್ತರ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=8027, ಮಾರ್ಗ=None, ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಆಫ್_ಲೈನ್=False):
        자신.ಸರ್ವರ್_ಮೌಲ್ಯ = socketserver.TCPServer(('127.0.0.1', ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), 꾸러미요청, bind_and_activate=False)
        자신.ಸರ್ವರ್_ಮೌಲ್ಯ.allow_reuse_address = True
        자신.ಸರ್ವರ್_ಮೌಲ್ಯ.server_bind()
        자신.ಸರ್ವರ್_ಮೌಲ್ಯ.server_activate()
        자신.ಸರ್ವರ್_ಮೌಲ್ಯ.ಸಂಗ್ರಹಣೆ_ಮೂಲ = ಬಂಡಲ್_ಸಂಗ್ರಹಣೆ(ಮಾರ್ಗ or ಬಿಂಬಿಸು_ಮೂಲ/'build/pip-cache', ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಆಫ್_ಲೈನ್)
        자신.ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = 자신.ಸರ್ವರ್_ಮೌಲ್ಯ.server_address[1]
        자신.ಎಳೆ_ಮೌಲ್ಯ = threading.Thread(target=자신.ಸರ್ವರ್_ಮೌಲ್ಯ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ಎಳೆ_ಮೌಲ್ಯ.start()
        return 자신

    def __exit__(자신, *인수):
        자신.ಸರ್ವರ್_ಮೌಲ್ಯ.shutdown()
        자신.ಸರ್ವರ್_ಮೌಲ್ಯ.server_close()
        자신.ಎಳೆ_ಮೌಲ್ಯ.join(timeout=2)


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--port', type=int, default=8027)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--cache', type=Path, default=ಬಿಂಬಿಸು_ಮೂಲ/'build/pip-cache')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--offline', action='store_true')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--fetch', help='ಪೂರೈಸು_ಆದೇಶ 없이 호환 배포 파일을 내려받아 검사·ಸ್ಟೋರ್_ಮೌಲ್ಯ')
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    if 인수.fetch:
        ಡೇಟಾ = ಬಂಡಲ್_ಸಂಗ್ರಹಣೆ(인수.cache, 인수.offline).ಸಿದ್ಧಪಡಿಸು(인수.fetch)
        print('ಬಂಡಲ್ ಸಿದ್ಧಪಡಿಸು 완료:', 인수.fetch, len(ಡೇಟಾ), 'ಬೈಟ್_ಮೌಲ್ಯ')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ಬಂಡಲ್ 중계: 127.0.0.1:' + str(중계.ಪೋರ್ಟ್_ಸಂಖ್ಯೆ), flush=True)
        try:
            중계.ಎಳೆ_ಮೌಲ್ಯ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
