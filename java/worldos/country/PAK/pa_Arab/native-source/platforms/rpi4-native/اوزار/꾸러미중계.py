#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 تنصیب_کرو_قدر·실행한다."""
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
        raise ValueError('گٹھ ناں 또는 ناں==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def تریخ_دے_مطابق_کرو_راہ(ناں, تنصیب_کاری_راہ=True):
    راہ = PurePosixPath(ناں)
    if راہ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ناں.split('/')):
        raise ValueError('허용하지 않는 گٹھ راہ: ' + ناں)
    if '\\' in ناں or any(ord(کریکٹر_قدر) < 32 or ord(کریکٹر_قدر) == 127 for کریکٹر_قدر in ناں):
        raise ValueError('잘못된 گٹھ راہ 문자')
    if تنصیب_کاری_راہ and (len(('/lib/' + ناں).encode()) > 63 or ناں in ('한국어.py', 'گٹھ.py')):
        raise ValueError('گٹھ راہ 제한 또는 طےشدہ_قدر لائبریری 충돌: ' + ناں)
    return ناں


def 압축풀기(فائل_داخلہ_ناں, کوائف, ناں, ورژن_قدر):
    파일들 = {}
    명세들 = []
    def 추가(راہ, اجزاء_قدر):
        تریخ_دے_مطابق_کرو_راہ(راہ)
        if راہ in 파일들:
            raise ValueError('중복 گٹھ راہ: ' + راہ)
        if len(اجزاء_قدر) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + راہ)
        اجزاء_قدر.decode('utf-8')
        파일들[راہ] = اجزاء_قدر
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ماخذ_شجرہ 16개·합계 64 KiB 이하여야 합니다.')
    if فائل_داخلہ_ناں.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(کوائف)) as گٹھ:
            항목들 = گٹھ.infolist()
            if len(항목들) > 256 or sum(داخلہ_قدر.file_size for داخلہ_قدر in 항목들) > 1048576:
                raise ValueError('محفوظہ_قدر اجراء_ذخیرہ سائز 제한 초과')
            حالت_فرست = [داخلہ_قدر for داخلہ_قدر in 항목들 if داخلہ_قدر.filename.endswith('.dist-info/WHEEL')]
            if len(حالت_فرست) != 1:
                raise ValueError('wheel حالت_قدر_102996da 명세가 필요합니다.')
            حالت_قدر_102996da = email.parser.Parser().parsestr(گٹھ.read(حالت_فرست[0]).decode())
            if حالت_قدر_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not فائل_داخلہ_ناں.endswith('-none-any.whl'):
                raise ValueError('C توسیع_قدر·플랫폼 전용 wheel은 지원하지 않습니다.')
            for داخلہ_قدر in 항목들:
                راہ = داخلہ_قدر.filename.rstrip('/')
                تریخ_دے_مطابق_کرو_راہ(راہ, False)
                if (داخلہ_قدر.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if داخلہ_قدر.filename.endswith('/'):
                    continue
                if '.dist-info/' in راہ:
                    if راہ.endswith('/METADATA'):
                        명세들.append(گٹھ.read(داخلہ_قدر).decode())
                    continue
                if not راہ.endswith('.py') or '.data/' in راہ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + راہ)
                추가(راہ, گٹھ.read(داخلہ_قدر))
    elif فائل_داخلہ_ناں.endswith('.tar.gz') and ناں.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py نفاذ_کرو_حکم 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(کوائف), mode='r|gz') as گٹھ:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for داخلہ_قدر in گٹھ:
                항목수 += 1
                전체크기 += داخلہ_قدر.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('محفوظہ_قدر اجراء_ذخیرہ سائز 제한 초과')
                تریخ_دے_مطابق_کرو_راہ(داخلہ_قدر.name, False)
                부분들 = داخلہ_قدر.name.split('/')
                뿌리들.add(부분들[0])
                if داخلہ_قدر.isdir():
                    continue
                if not داخلہ_قدر.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ماخذ_شجرہ 배포형')
                راہ = '/'.join(부분들[1:])
                اجزاء_قدر = گٹھ.extractfile(داخلہ_قدر).read()
                if راہ.endswith('PKG-INFO'):
                    명세들.append(اجزاء_قدر.decode())
                elif راہ.endswith('.py') and راہ not in ('setup.py',):
                    추가(راہ, اجزاء_قدر)
                elif '.egg-info/' not in راہ and not راہ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + راہ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ماخذ_شجرہ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ناں or 명세.get('Version') != ورژن_قدر:
        raise ValueError('배포 메타데이터의 ناں·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(پتا, 한도):
    if not پتا.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(پتا, timeout=30) as جواب_دیوؤ:
        if not جواب_دیوؤ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 پتا بڑھاؤ_قدر')
        کوائف = جواب_دیوؤ.read(한도 + 1)
    if len(کوائف) > 한도:
        raise ValueError('배포 فائل سائز 제한 초과')
    return کوائف


def منتقلی_گٹھ(ناں, ورژن_قدر, 파일들, 출처):
    명세 = {'name': ناں, 'version': ورژن_قدر, 'source': 출처, 'files': [
        {'path': راہ, 'size': len(کوائف), 'sha256': hashlib.sha256(کوائف).hexdigest()}
        for راہ, کوائف in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('گٹھ 명세 سائز 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[داخلہ_قدر['path']] for داخلہ_قدر in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, راہ, 오프라인=False):
        자신.راہ = Path(راہ)
        자신.راہ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def تیاری_کرو(자신, 요청):
        ناں, ورژن_قدر = 요청해석(요청)
        열쇠 = ناں + ('==' + ورژن_قدر if ورژن_قدر else '')
        لاگ_راہ = 자신.راہ / (열쇠 + '.json')
        배포경로 = 자신.راہ / (열쇠 + '.archive')
        if لاگ_راہ.is_file() and 배포경로.is_file():
            لاگ_صف = json.loads(لاگ_راہ.read_text())
            کوائف = 배포경로.read_bytes()
            if hashlib.sha256(کوائف).hexdigest() != لاگ_صف['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 گٹھ: ' + 요청)
            پتا = 'https://pypi.org/pypi/' + ناں + ('/' + ورژن_قدر if ورژن_قدر else '') + '/json'
            سسٹم_دی_معلومات = json.loads(웹읽기(پتا, 4194304).decode())
            if سسٹم_دی_معلومات['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [داخلہ_قدر for داخلہ_قدر in سسٹم_دی_معلومات['urls'] if not داخلہ_قدر.get('yanked') and داخلہ_قدر['filename'].endswith('-none-any.whl')]
            if not 후보 and ناں.startswith('micropython-'):
                후보 = [داخلہ_قدر for داخلہ_قدر in سسٹم_دی_معلومات['urls'] if not داخلہ_قدر.get('yanked') and داخلہ_قدر['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            انتخاب_قدر = 후보[0]
            کوائف = 웹읽기(انتخاب_قدر['url'], 4194304)
            if hashlib.sha256(کوائف).hexdigest() != انتخاب_قدر['digests']['sha256']:
                raise ValueError('PyPI 배포 فائل SHA-256 불일치')
            لاگ_صف = {'name': ناں, 'version': سسٹم_دی_معلومات['info']['version'], 'filename': انتخاب_قدر['filename'],
                    'url': انتخاب_قدر['url'], 'sha256': انتخاب_قدر['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(لاگ_صف['filename'], کوائف, ناں, لاگ_صف['version'])
            배포경로.write_bytes(کوائف)
            لاگ_راہ.write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2) + '\n')
        if لاگ_صف['name'] != ناں or ورژن_قدر and لاگ_صف['version'] != ورژن_قدر:
            raise ValueError('저장소 ناں·버전 불일치')
        파일들 = 압축풀기(لاگ_صف['filename'], کوائف, ناں, لاگ_صف['version'])
        return منتقلی_گٹھ(ناں, لاگ_صف['version'], 파일들, لاگ_صف['url'])


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
                raise ValueError('잘못된 گٹھ 요청')
            جواب_دیوؤ = 자신.server.저장소.تیاری_کرو(요청[:-1].decode('ascii'))
        except Exception as نقص:
            머리 = json.dumps({'error': str(نقص)[:500]}, ensure_ascii=False).encode()
            جواب_دیوؤ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(جواب_دیوؤ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, راہ=None, 오프라인=False):
        자신.سرور_قدر = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.سرور_قدر.allow_reuse_address = True
        자신.سرور_قدر.server_bind()
        자신.سرور_قدر.server_activate()
        자신.سرور_قدر.저장소 = 꾸러미저장소(راہ or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.سرور_قدر.server_address[1]
        자신.لڑی_قدر = threading.Thread(target=자신.سرور_قدر.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.لڑی_قدر.start()
        return 자신

    def __exit__(자신, *인수):
        자신.سرور_قدر.shutdown()
        자신.سرور_قدر.server_close()
        자신.لڑی_قدر.join(timeout=2)


def چلاؤ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='نفاذ_کرو_حکم 없이 호환 배포 파일을 내려받아 검사·ذخیرہ_کرو_قدر')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        کوائف = 꾸러미저장소(인수.cache, 인수.offline).تیاری_کرو(인수.fetch)
        print('گٹھ تیاری_کرو 완료:', 인수.fetch, len(کوائف), 'بائٹ_قدر')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('گٹھ 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.لڑی_قدر.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    چلاؤ()
