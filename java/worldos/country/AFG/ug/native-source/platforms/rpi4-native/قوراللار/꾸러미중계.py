#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 قاچىلاش_قىممىتى·실행한다."""
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

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('توپلام ئاتى 또는 ئاتى==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def دەلىللەش_يول_f98b46e1(ئاتى, قاچىلاش_يول=True):
    يول = PurePosixPath(ئاتى)
    if يول.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ئاتى.split('/')):
        raise ValueError('허용하지 않는 توپلام يول: ' + ئاتى)
    if '\\' in ئاتى or any(ord(ھەرپ_بەلگە_قىممىتى) < 32 or ord(ھەرپ_بەلگە_قىممىتى) == 127 for ھەرپ_بەلگە_قىممىتى in ئاتى):
        raise ValueError('잘못된 توپلام يول 문자')
    if قاچىلاش_يول and (len(('/lib/' + ئاتى).encode()) > 63 or ئاتى in ('한국어.py', 'توپلام.py')):
        raise ValueError('توپلام يول 제한 또는 سۈكۈتتىكى_قىممەت ئامبار 충돌: ' + ئاتى)
    return ئاتى


def 압축풀기(ھۆججەت_كىرگۈزۈش_نامى, مەلۇمات, ئاتى, نەشىر_نومۇرى_قىممىتى):
    파일들 = {}
    명세들 = []
    def 추가(يول, مەزمۇن_قىممىتى):
        دەلىللەش_يول_f98b46e1(يول)
        if يول in 파일들:
            raise ValueError('중복 توپلام يول: ' + يول)
        if len(مەزمۇن_قىممىتى) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + يول)
        مەزمۇن_قىممىتى.decode('utf-8')
        파일들[يول] = مەزمۇن_قىممىتى
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 مەنبە_دەرەخ 16개·합계 64 KiB 이하여야 합니다.')
    if ھۆججەت_كىرگۈزۈش_نامى.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(مەلۇمات)) as توپلام:
            항목들 = توپلام.infolist()
            if len(항목들) > 256 or sum(كىرگۈزۈش_قىممىتى.file_size for كىرگۈزۈش_قىممىتى in 항목들) > 1048576:
                raise ValueError('ئارخىپ_قىممىتى تارقىتىش_بوشلۇق چوڭلۇقى 제한 초과')
            خىزمەت_تىزىم = [كىرگۈزۈش_قىممىتى for كىرگۈزۈش_قىممىتى in 항목들 if كىرگۈزۈش_قىممىتى.filename.endswith('.dist-info/WHEEL')]
            if len(خىزمەت_تىزىم) != 1:
                raise ValueError('wheel خىزمەت_قىممىتى 명세가 필요합니다.')
            خىزمەت_قىممىتى = email.parser.Parser().parsestr(توپلام.read(خىزمەت_تىزىم[0]).decode())
            if خىزمەت_قىممىتى.get('Root-Is-Purelib', '').lower() != 'true' or not ھۆججەت_كىرگۈزۈش_نامى.endswith('-none-any.whl'):
                raise ValueError('C كېڭەيتمە_قىممىتى·플랫폼 전용 wheel은 지원하지 않습니다.')
            for كىرگۈزۈش_قىممىتى in 항목들:
                يول = كىرگۈزۈش_قىممىتى.filename.rstrip('/')
                دەلىللەش_يول_f98b46e1(يول, False)
                if (كىرگۈزۈش_قىممىتى.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if كىرگۈزۈش_قىممىتى.filename.endswith('/'):
                    continue
                if '.dist-info/' in يول:
                    if يول.endswith('/METADATA'):
                        명세들.append(توپلام.read(كىرگۈزۈش_قىممىتى).decode())
                    continue
                if not يول.endswith('.py') or '.data/' in يول:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + يول)
                추가(يول, توپلام.read(كىرگۈزۈش_قىممىتى))
    elif ھۆججەت_كىرگۈزۈش_نامى.endswith('.tar.gz') and ئاتى.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ئىجرا_قىلىش_بۇيرۇق 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(مەلۇمات), mode='r|gz') as توپلام:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for كىرگۈزۈش_قىممىتى in توپلام:
                항목수 += 1
                전체크기 += كىرگۈزۈش_قىممىتى.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ئارخىپ_قىممىتى تارقىتىش_بوشلۇق چوڭلۇقى 제한 초과')
                دەلىللەش_يول_f98b46e1(كىرگۈزۈش_قىممىتى.name, False)
                부분들 = كىرگۈزۈش_قىممىتى.name.split('/')
                뿌리들.add(부분들[0])
                if كىرگۈزۈش_قىممىتى.isdir():
                    continue
                if not كىرگۈزۈش_قىممىتى.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython مەنبە_دەرەخ 배포형')
                يول = '/'.join(부분들[1:])
                مەزمۇن_قىممىتى = توپلام.extractfile(كىرگۈزۈش_قىممىتى).read()
                if يول.endswith('PKG-INFO'):
                    명세들.append(مەزمۇن_قىممىتى.decode())
                elif يول.endswith('.py') and يول not in ('setup.py',):
                    추가(يول, مەزمۇن_قىممىتى)
                elif '.egg-info/' not in يول and not يول.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + يول)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 يىلتىز_قىممىتى 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* مەنبە_دەرەخ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ئاتى or 명세.get('Version') != نەشىر_نومۇرى_قىممىتى:
        raise ValueError('배포 메타데이터의 ئاتى·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ئادرېس, 한도):
    if not ئادرېس.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ئادرېس, timeout=30) as جاۋابلاش:
        if not جاۋابلاش.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ئادرېس يۆتكىمەك_قىممىتى')
        مەلۇمات = جاۋابلاش.read(한도 + 1)
    if len(مەلۇمات) > 한도:
        raise ValueError('배포 ھۆججەت چوڭلۇقى 제한 초과')
    return مەلۇمات


def يوللاش_توپلام(ئاتى, نەشىر_نومۇرى_قىممىتى, 파일들, 출처):
    명세 = {'name': ئاتى, 'version': نەشىر_نومۇرى_قىممىتى, 'source': 출처, 'files': [
        {'path': يول, 'size': len(مەلۇمات), 'sha256': hashlib.sha256(مەلۇمات).hexdigest()}
        for يول, مەلۇمات in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('توپلام 명세 چوڭلۇقى 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[كىرگۈزۈش_قىممىتى['path']] for كىرگۈزۈش_قىممىتى in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, يول, 오프라인=False):
        자신.يول = Path(يول)
        자신.يول.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def تەييارلىماق(자신, 요청):
        ئاتى, نەشىر_نومۇرى_قىممىتى = 요청해석(요청)
        열쇠 = ئاتى + ('==' + نەشىر_نومۇرى_قىممىتى if نەشىر_نومۇرى_قىممىتى else '')
        خاتىرە_يول = 자신.يول / (열쇠 + '.json')
        배포경로 = 자신.يول / (열쇠 + '.archive')
        if خاتىرە_يول.is_file() and 배포경로.is_file():
            خاتىرە_قۇر = json.loads(خاتىرە_يول.read_text())
            مەلۇمات = 배포경로.read_bytes()
            if hashlib.sha256(مەلۇمات).hexdigest() != خاتىرە_قۇر['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 توپلام: ' + 요청)
            ئادرېس = 'https://pypi.org/pypi/' + ئاتى + ('/' + نەشىر_نومۇرى_قىممىتى if نەشىر_نومۇرى_قىممىتى else '') + '/json'
            سىستېما_ئۇچۇرى = json.loads(웹읽기(ئادرېس, 4194304).decode())
            if سىستېما_ئۇچۇرى['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [كىرگۈزۈش_قىممىتى for كىرگۈزۈش_قىممىتى in سىستېما_ئۇچۇرى['urls'] if not كىرگۈزۈش_قىممىتى.get('yanked') and كىرگۈزۈش_قىممىتى['filename'].endswith('-none-any.whl')]
            if not 후보 and ئاتى.startswith('micropython-'):
                후보 = [كىرگۈزۈش_قىممىتى for كىرگۈزۈش_قىممىتى in سىستېما_ئۇچۇرى['urls'] if not كىرگۈزۈش_قىممىتى.get('yanked') and كىرگۈزۈش_قىممىتى['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            تاللاش_قىممىتى = 후보[0]
            مەلۇمات = 웹읽기(تاللاش_قىممىتى['url'], 4194304)
            if hashlib.sha256(مەلۇمات).hexdigest() != تاللاش_قىممىتى['digests']['sha256']:
                raise ValueError('PyPI 배포 ھۆججەت SHA-256 불일치')
            خاتىرە_قۇر = {'name': ئاتى, 'version': سىستېما_ئۇچۇرى['info']['version'], 'filename': تاللاش_قىممىتى['filename'],
                    'url': تاللاش_قىممىتى['url'], 'sha256': تاللاش_قىممىتى['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(خاتىرە_قۇر['filename'], مەلۇمات, ئاتى, خاتىرە_قۇر['version'])
            배포경로.write_bytes(مەلۇمات)
            خاتىرە_يول.write_text(json.dumps(خاتىرە_قۇر, ensure_ascii=False, indent=2) + '\n')
        if خاتىرە_قۇر['name'] != ئاتى or نەشىر_نومۇرى_قىممىتى and خاتىرە_قۇر['version'] != نەشىر_نومۇرى_قىممىتى:
            raise ValueError('저장소 ئاتى·버전 불일치')
        파일들 = 압축풀기(خاتىرە_قۇر['filename'], مەلۇمات, ئاتى, خاتىرە_قۇر['version'])
        return يوللاش_توپلام(ئاتى, خاتىرە_قۇر['version'], 파일들, خاتىرە_قۇر['url'])


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
                raise ValueError('잘못된 توپلام 요청')
            جاۋابلاش = 자신.server.저장소.تەييارلىماق(요청[:-1].decode('ascii'))
        except Exception as خاتالىق:
            머리 = json.dumps({'error': str(خاتالىق)[:500]}, ensure_ascii=False).encode()
            جاۋابلاش = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(جاۋابلاش)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, يول=None, 오프라인=False):
        자신.مۇلازىمىتېر_قىممىتى = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.مۇلازىمىتېر_قىممىتى.allow_reuse_address = True
        자신.مۇلازىمىتېر_قىممىتى.server_bind()
        자신.مۇلازىمىتېر_قىممىتى.server_activate()
        자신.مۇلازىمىتېر_قىممىتى.저장소 = 꾸러미저장소(يول or كۆرسىتىش_يىلتىز/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.مۇلازىمىتېر_قىممىتى.server_address[1]
        자신.ئېقىم_قىممىتى_5b72a632 = threading.Thread(target=자신.مۇلازىمىتېر_قىممىتى.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ئېقىم_قىممىتى_5b72a632.start()
        return 자신

    def __exit__(자신, *ئۆزگەرگۈچىلەر):
        자신.مۇلازىمىتېر_قىممىتى.shutdown()
        자신.مۇلازىمىتېر_قىممىتى.server_close()
        자신.ئېقىم_قىممىتى_5b72a632.join(timeout=2)


def ئىجرا_قىل_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=كۆرسىتىش_يىلتىز/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ئىجرا_قىلىش_بۇيرۇق 없이 호환 배포 파일을 내려받아 검사·ساقلىماق_قىممىتى')
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    if ئۆزگەرگۈچىلەر.fetch:
        مەلۇمات = 꾸러미저장소(ئۆزگەرگۈچىلەر.cache, ئۆزگەرگۈچىلەر.offline).تەييارلىماق(ئۆزگەرگۈچىلەر.fetch)
        print('توپلام تەييارلىماق 완료:', ئۆزگەرگۈچىلەر.fetch, len(مەلۇمات), 'بايت_قىممىتى')
        return
    with 꾸러미중계(ئۆزگەرگۈچىلەر.port, ئۆزگەرگۈچىلەر.cache, ئۆزگەرگۈچىلەر.offline) as 중계:
        print('توپلام 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.ئېقىم_قىممىتى_5b72a632.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ئىجرا_قىل_2()
