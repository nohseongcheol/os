#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ጸዓን_ዋጋ·실행한다."""
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
        raise ValueError('ጥማር ሽም 또는 ሽም==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def አረጋግፅ_መገዲ(ሽም, ምጽዓን_መገዲ=True):
    መገዲ = PurePosixPath(ሽም)
    if መገዲ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ሽም.split('/')):
        raise ValueError('허용하지 않는 ጥማር መገዲ: ' + ሽም)
    if '\\' in ሽም or any(ord(ፊደል_ዋጋ) < 32 or ord(ፊደል_ዋጋ) == 127 for ፊደል_ዋጋ in ሽም):
        raise ValueError('잘못된 ጥማር መገዲ 문자')
    if ምጽዓን_መገዲ and (len(('/lib/' + ሽም).encode()) > 63 or ሽም in ('ትግርኛ.py', 'ጥማር.py')):
        raise ValueError('ጥማር መገዲ 제한 또는 ንቡር_ዋጋ ቤት_ንባብ 충돌: ' + ሽም)
    return ሽም


def 압축풀기(ፋይል_ምእታው_ሽም, ሓበሬታ, ሽም, ሕታም_ዋጋ):
    파일들 = {}
    명세들 = []
    def 추가(መገዲ, ትሕዝቶ_ዋጋ):
        አረጋግፅ_መገዲ(መገዲ)
        if መገዲ in 파일들:
            raise ValueError('중복 ጥማር መገዲ: ' + መገዲ)
        if len(ትሕዝቶ_ዋጋ) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + መገዲ)
        ትሕዝቶ_ዋጋ.decode('utf-8')
        파일들[መገዲ] = ትሕዝቶ_ዋጋ
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ምንጪ_ገረብ 16개·합계 64 KiB 이하여야 합니다.')
    if ፋይል_ምእታው_ሽም.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ሓበሬታ)) as ጥማር:
            항목들 = ጥማር.infolist()
            if len(항목들) > 256 or sum(ምእታው_ዋጋ.file_size for ምእታው_ዋጋ in 항목들) > 1048576:
                raise ValueError('ሰንድ_ዋጋ ፍታሕ_መኽዘን መጠን 제한 초과')
            ዕዮ_ዝርዝር = [ምእታው_ዋጋ for ምእታው_ዋጋ in 항목들 if ምእታው_ዋጋ.filename.endswith('.dist-info/WHEEL')]
            if len(ዕዮ_ዝርዝር) != 1:
                raise ValueError('wheel ዕዮ_ዋጋ_102996da 명세가 필요합니다.')
            ዕዮ_ዋጋ_102996da = email.parser.Parser().parsestr(ጥማር.read(ዕዮ_ዝርዝር[0]).decode())
            if ዕዮ_ዋጋ_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not ፋይል_ምእታው_ሽም.endswith('-none-any.whl'):
                raise ValueError('C ቅጥያ_ዋጋ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ምእታው_ዋጋ in 항목들:
                መገዲ = ምእታው_ዋጋ.filename.rstrip('/')
                አረጋግፅ_መገዲ(መገዲ, False)
                if (ምእታው_ዋጋ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ምእታው_ዋጋ.filename.endswith('/'):
                    continue
                if '.dist-info/' in መገዲ:
                    if መገዲ.endswith('/METADATA'):
                        명세들.append(ጥማር.read(ምእታው_ዋጋ).decode())
                    continue
                if not መገዲ.endswith('.py') or '.data/' in መገዲ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + መገዲ)
                추가(መገዲ, ጥማር.read(ምእታው_ዋጋ))
    elif ፋይል_ምእታው_ሽም.endswith('.tar.gz') and ሽም.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ተግብር_ትእዛዝ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ሓበሬታ), mode='r|gz') as ጥማር:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ምእታው_ዋጋ in ጥማር:
                항목수 += 1
                전체크기 += ምእታው_ዋጋ.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ሰንድ_ዋጋ ፍታሕ_መኽዘን መጠን 제한 초과')
                አረጋግፅ_መገዲ(ምእታው_ዋጋ.name, False)
                부분들 = ምእታው_ዋጋ.name.split('/')
                뿌리들.add(부분들[0])
                if ምእታው_ዋጋ.isdir():
                    continue
                if not ምእታው_ዋጋ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ምንጪ_ገረብ 배포형')
                መገዲ = '/'.join(부분들[1:])
                ትሕዝቶ_ዋጋ = ጥማር.extractfile(ምእታው_ዋጋ).read()
                if መገዲ.endswith('PKG-INFO'):
                    명세들.append(ትሕዝቶ_ዋጋ.decode())
                elif መገዲ.endswith('.py') and መገዲ not in ('setup.py',):
                    추가(መገዲ, ትሕዝቶ_ዋጋ)
                elif '.egg-info/' not in መገዲ and not መገዲ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + መገዲ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ምንጪ_ገረብ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ሽም or 명세.get('Version') != ሕታም_ዋጋ:
        raise ValueError('배포 메타데이터의 ሽም·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ኣድራሻ, 한도):
    if not ኣድራሻ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ኣድራሻ, timeout=30) as መልስ:
        if not መልስ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ኣድራሻ ኣንቀሳቕስ_ዋጋ')
        ሓበሬታ = መልስ.read(한도 + 1)
    if len(ሓበሬታ) > 한도:
        raise ValueError('배포 ፋይል መጠን 제한 초과')
    return ሓበሬታ


def ምስጋር_ጥማር(ሽም, ሕታም_ዋጋ, 파일들, 출처):
    명세 = {'name': ሽም, 'version': ሕታም_ዋጋ, 'source': 출처, 'files': [
        {'path': መገዲ, 'size': len(ሓበሬታ), 'sha256': hashlib.sha256(ሓበሬታ).hexdigest()}
        for መገዲ, ሓበሬታ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ጥማር 명세 መጠን 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ምእታው_ዋጋ['path']] for ምእታው_ዋጋ in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, መገዲ, 오프라인=False):
        자신.መገዲ = Path(መገዲ)
        자신.መገዲ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def ኣዳልው(자신, 요청):
        ሽም, ሕታም_ዋጋ = 요청해석(요청)
        열쇠 = ሽም + ('==' + ሕታም_ዋጋ if ሕታም_ዋጋ else '')
        ምዝጉብ_መገዲ = 자신.መገዲ / (열쇠 + '.json')
        배포경로 = 자신.መገዲ / (열쇠 + '.archive')
        if ምዝጉብ_መገዲ.is_file() and 배포경로.is_file():
            ምዝጉብ_ሪጋ = json.loads(ምዝጉብ_መገዲ.read_text())
            ሓበሬታ = 배포경로.read_bytes()
            if hashlib.sha256(ሓበሬታ).hexdigest() != ምዝጉብ_ሪጋ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 ጥማር: ' + 요청)
            ኣድራሻ = 'https://pypi.org/pypi/' + ሽም + ('/' + ሕታም_ዋጋ if ሕታም_ዋጋ else '') + '/json'
            ናይ_ስርዓት_ሓበሬታ = json.loads(웹읽기(ኣድራሻ, 4194304).decode())
            if ናይ_ስርዓት_ሓበሬታ['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ምእታው_ዋጋ for ምእታው_ዋጋ in ናይ_ስርዓት_ሓበሬታ['urls'] if not ምእታው_ዋጋ.get('yanked') and ምእታው_ዋጋ['filename'].endswith('-none-any.whl')]
            if not 후보 and ሽም.startswith('micropython-'):
                후보 = [ምእታው_ዋጋ for ምእታው_ዋጋ in ናይ_ስርዓት_ሓበሬታ['urls'] if not ምእታው_ዋጋ.get('yanked') and ምእታው_ዋጋ['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ምሩጽ_ዋጋ = 후보[0]
            ሓበሬታ = 웹읽기(ምሩጽ_ዋጋ['url'], 4194304)
            if hashlib.sha256(ሓበሬታ).hexdigest() != ምሩጽ_ዋጋ['digests']['sha256']:
                raise ValueError('PyPI 배포 ፋይል SHA-256 불일치')
            ምዝጉብ_ሪጋ = {'name': ሽም, 'version': ናይ_ስርዓት_ሓበሬታ['info']['version'], 'filename': ምሩጽ_ዋጋ['filename'],
                    'url': ምሩጽ_ዋጋ['url'], 'sha256': ምሩጽ_ዋጋ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ምዝጉብ_ሪጋ['filename'], ሓበሬታ, ሽም, ምዝጉብ_ሪጋ['version'])
            배포경로.write_bytes(ሓበሬታ)
            ምዝጉብ_መገዲ.write_text(json.dumps(ምዝጉብ_ሪጋ, ensure_ascii=False, indent=2) + '\n')
        if ምዝጉብ_ሪጋ['name'] != ሽም or ሕታም_ዋጋ and ምዝጉብ_ሪጋ['version'] != ሕታም_ዋጋ:
            raise ValueError('저장소 ሽም·버전 불일치')
        파일들 = 압축풀기(ምዝጉብ_ሪጋ['filename'], ሓበሬታ, ሽም, ምዝጉብ_ሪጋ['version'])
        return ምስጋር_ጥማር(ሽም, ምዝጉብ_ሪጋ['version'], 파일들, ምዝጉብ_ሪጋ['url'])


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
                raise ValueError('잘못된 ጥማር 요청')
            መልስ = 자신.server.저장소.ኣዳልው(요청[:-1].decode('ascii'))
        except Exception as ጌጋ:
            머리 = json.dumps({'error': str(ጌጋ)[:500]}, ensure_ascii=False).encode()
            መልስ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(መልስ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, መገዲ=None, 오프라인=False):
        자신.ኣገልጋሊ_ዋጋ = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.ኣገልጋሊ_ዋጋ.allow_reuse_address = True
        자신.ኣገልጋሊ_ዋጋ.server_bind()
        자신.ኣገልጋሊ_ዋጋ.server_activate()
        자신.ኣገልጋሊ_ዋጋ.저장소 = 꾸러미저장소(መገዲ or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.ኣገልጋሊ_ዋጋ.server_address[1]
        자신.ፈትሊ_ዋጋ = threading.Thread(target=자신.ኣገልጋሊ_ዋጋ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ፈትሊ_ዋጋ.start()
        return 자신

    def __exit__(자신, *인수):
        자신.ኣገልጋሊ_ዋጋ.shutdown()
        자신.ኣገልጋሊ_ዋጋ.server_close()
        자신.ፈትሊ_ዋጋ.join(timeout=2)


def ኣኺድ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ተግብር_ትእዛዝ 없이 호환 배포 파일을 내려받아 검사·ከዝን_ዋጋ')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        ሓበሬታ = 꾸러미저장소(인수.cache, 인수.offline).ኣዳልው(인수.fetch)
        print('ጥማር ኣዳልው 완료:', 인수.fetch, len(ሓበሬታ), 'ባይት_ዋጋ')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ጥማር 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.ፈትሊ_ዋጋ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ኣኺድ()
