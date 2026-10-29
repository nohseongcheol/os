#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 نصب_ڪريو_قدر·실행한다."""
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
        raise ValueError('بنڊل نالو 또는 نالو==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ڪارگر_ڪريو_راههه(نالو, تنصيب_راههه=True):
    راههه = PurePosixPath(نالو)
    if راههه.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in نالو.split('/')):
        raise ValueError('허용하지 않는 بنڊل راههه: ' + نالو)
    if '\\' in نالو or any(ord(ڪريڪٽر_قدر) < 32 or ord(ڪريڪٽر_قدر) == 127 for ڪريڪٽر_قدر in نالو):
        raise ValueError('잘못된 بنڊل راههه 문자')
    if تنصيب_راههه and (len(('/lib/' + نالو).encode()) > 63 or نالو in ('한국어.py', 'بنڊل.py')):
        raise ValueError('بنڊل راههه 제한 또는 طئي_ٿيل_ملهه لائبريري 충돌: ' + نالو)
    return نالو


def 압축풀기(فائل_داخلا_نالو, ڪوائف, نالو, ورزين_قدر):
    파일들 = {}
    명세들 = []
    def 추가(راههه, مواد_قدر):
        ڪارگر_ڪريو_راههه(راههه)
        if راههه in 파일들:
            raise ValueError('중복 بنڊل راههه: ' + راههه)
        if len(مواد_قدر) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + راههه)
        مواد_قدر.decode('utf-8')
        파일들[راههه] = مواد_قدر
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ماخذ_شجرو 16개·합계 64 KiB 이하여야 합니다.')
    if فائل_داخلا_نالو.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ڪوائف)) as بنڊل:
            항목들 = بنڊل.infolist()
            if len(항목들) > 256 or sum(داخلا_قدر.file_size for داخلا_قدر in 항목들) > 1048576:
                raise ValueError('محفوظ_قدر جاري_ڪريو_ذخيرو سائيز 제한 초과')
            حالت_فهرست = [داخلا_قدر for داخلا_قدر in 항목들 if داخلا_قدر.filename.endswith('.dist-info/WHEEL')]
            if len(حالت_فهرست) != 1:
                raise ValueError('wheel حالت_قدر_102996da 명세가 필요합니다.')
            حالت_قدر_102996da = email.parser.Parser().parsestr(بنڊل.read(حالت_فهرست[0]).decode())
            if حالت_قدر_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not فائل_داخلا_نالو.endswith('-none-any.whl'):
                raise ValueError('C واڌ_قدر·플랫폼 전용 wheel은 지원하지 않습니다.')
            for داخلا_قدر in 항목들:
                راههه = داخلا_قدر.filename.rstrip('/')
                ڪارگر_ڪريو_راههه(راههه, False)
                if (داخلا_قدر.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if داخلا_قدر.filename.endswith('/'):
                    continue
                if '.dist-info/' in راههه:
                    if راههه.endswith('/METADATA'):
                        명세들.append(بنڊل.read(داخلا_قدر).decode())
                    continue
                if not راههه.endswith('.py') or '.data/' in راههه:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + راههه)
                추가(راههه, بنڊل.read(داخلا_قدر))
    elif فائل_داخلا_نالو.endswith('.tar.gz') and نالو.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py تعميل_ڪرڻ_حڪم 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ڪوائف), mode='r|gz') as بنڊل:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for داخلا_قدر in بنڊل:
                항목수 += 1
                전체크기 += داخلا_قدر.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('محفوظ_قدر جاري_ڪريو_ذخيرو سائيز 제한 초과')
                ڪارگر_ڪريو_راههه(داخلا_قدر.name, False)
                부분들 = داخلا_قدر.name.split('/')
                뿌리들.add(부분들[0])
                if داخلا_قدر.isdir():
                    continue
                if not داخلا_قدر.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ماخذ_شجرو 배포형')
                راههه = '/'.join(부분들[1:])
                مواد_قدر = بنڊل.extractfile(داخلا_قدر).read()
                if راههه.endswith('PKG-INFO'):
                    명세들.append(مواد_قدر.decode())
                elif راههه.endswith('.py') and راههه not in ('setup.py',):
                    추가(راههه, مواد_قدر)
                elif '.egg-info/' not in راههه and not راههه.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + راههه)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ماخذ_شجرو 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != نالو or 명세.get('Version') != ورزين_قدر:
        raise ValueError('배포 메타데이터의 نالو·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(پتو, 한도):
    if not پتو.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(پتو, timeout=30) as جواب_ڏيو:
        if not جواب_ڏيو.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 پتو وڌايو_قدر')
        ڪوائف = جواب_ڏيو.read(한도 + 1)
    if len(ڪوائف) > 한도:
        raise ValueError('배포 فائل سائيز 제한 초과')
    return ڪوائف


def منتقلي_بنڊل(نالو, ورزين_قدر, 파일들, 출처):
    명세 = {'name': نالو, 'version': ورزين_قدر, 'source': 출처, 'files': [
        {'path': راههه, 'size': len(ڪوائف), 'sha256': hashlib.sha256(ڪوائف).hexdigest()}
        for راههه, ڪوائف in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('بنڊل 명세 سائيز 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[داخلا_قدر['path']] for داخلا_قدر in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, راههه, 오프라인=False):
        자신.راههه = Path(راههه)
        자신.راههه.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def تياري_ڪريو(자신, 요청):
        نالو, ورزين_قدر = 요청해석(요청)
        열쇠 = نالو + ('==' + ورزين_قدر if ورزين_قدر else '')
        لاگ_راههه = 자신.راههه / (열쇠 + '.json')
        배포경로 = 자신.راههه / (열쇠 + '.archive')
        if لاگ_راههه.is_file() and 배포경로.is_file():
            لاگ_صف = json.loads(لاگ_راههه.read_text())
            ڪوائف = 배포경로.read_bytes()
            if hashlib.sha256(ڪوائف).hexdigest() != لاگ_صف['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 بنڊل: ' + 요청)
            پتو = 'https://pypi.org/pypi/' + نالو + ('/' + ورزين_قدر if ورزين_قدر else '') + '/json'
            سسٽم_معلومات = json.loads(웹읽기(پتو, 4194304).decode())
            if سسٽم_معلومات['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [داخلا_قدر for داخلا_قدر in سسٽم_معلومات['urls'] if not داخلا_قدر.get('yanked') and داخلا_قدر['filename'].endswith('-none-any.whl')]
            if not 후보 and نالو.startswith('micropython-'):
                후보 = [داخلا_قدر for داخلا_قدر in سسٽم_معلومات['urls'] if not داخلا_قدر.get('yanked') and داخلا_قدر['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            چونڊ_قدر = 후보[0]
            ڪوائف = 웹읽기(چونڊ_قدر['url'], 4194304)
            if hashlib.sha256(ڪوائف).hexdigest() != چونڊ_قدر['digests']['sha256']:
                raise ValueError('PyPI 배포 فائل SHA-256 불일치')
            لاگ_صف = {'name': نالو, 'version': سسٽم_معلومات['info']['version'], 'filename': چونڊ_قدر['filename'],
                    'url': چونڊ_قدر['url'], 'sha256': چونڊ_قدر['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(لاگ_صف['filename'], ڪوائف, نالو, لاگ_صف['version'])
            배포경로.write_bytes(ڪوائف)
            لاگ_راههه.write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2) + '\n')
        if لاگ_صف['name'] != نالو or ورزين_قدر and لاگ_صف['version'] != ورزين_قدر:
            raise ValueError('저장소 نالو·버전 불일치')
        파일들 = 압축풀기(لاگ_صف['filename'], ڪوائف, نالو, لاگ_صف['version'])
        return منتقلي_بنڊل(نالو, لاگ_صف['version'], 파일들, لاگ_صف['url'])


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
                raise ValueError('잘못된 بنڊل 요청')
            جواب_ڏيو = 자신.server.저장소.تياري_ڪريو(요청[:-1].decode('ascii'))
        except Exception as نقص:
            머리 = json.dumps({'error': str(نقص)[:500]}, ensure_ascii=False).encode()
            جواب_ڏيو = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(جواب_ڏيو)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, راههه=None, 오프라인=False):
        자신.سرور_قدر = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.سرور_قدر.allow_reuse_address = True
        자신.سرور_قدر.server_bind()
        자신.سرور_قدر.server_activate()
        자신.سرور_قدر.저장소 = 꾸러미저장소(راههه or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.سرور_قدر.server_address[1]
        자신.لڙي_قدر = threading.Thread(target=자신.سرور_قدر.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.لڙي_قدر.start()
        return 자신

    def __exit__(자신, *인수):
        자신.سرور_قدر.shutdown()
        자신.سرور_قدر.server_close()
        자신.لڙي_قدر.join(timeout=2)


def هلائڻ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='تعميل_ڪرڻ_حڪم 없이 호환 배포 파일을 내려받아 검사·روڪيو_قدر')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        ڪوائف = 꾸러미저장소(인수.cache, 인수.offline).تياري_ڪريو(인수.fetch)
        print('بنڊل تياري_ڪريو 완료:', 인수.fetch, len(ڪوائف), 'بائٽ_قدر')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('بنڊل 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.لڙي_قدر.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    هلائڻ()
