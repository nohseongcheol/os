#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 نصب_کریں_قدر·실행한다."""
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

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('بنڈل نام 또는 نام==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def جواز_دہی_کریں_راہ(نام, تنصیب_راہ=True):
    راستہ_2 = PurePosixPath(نام)
    if راستہ_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in نام.split('/')):
        raise ValueError('허용하지 않는 بنڈل راستہ_2: ' + نام)
    if '\\' in نام or any(ord(کریکٹر_قدر) < 32 or ord(کریکٹر_قدر) == 127 for کریکٹر_قدر in نام):
        raise ValueError('잘못된 بنڈل راستہ_2 문자')
    if تنصیب_راہ and (len(('/lib/' + نام).encode()) > 63 or نام in ('اردو.py', 'بنڈل.py')):
        raise ValueError('بنڈل راستہ_2 제한 또는 طے_شدہ_قدر لائبریری 충돌: ' + نام)
    return نام


def 압축풀기(فائل_اندراج_نام, کوائف, نام, ورژن_قدر):
    파일들 = {}
    명세들 = []
    def 추가(راستہ_2, مشمول_قدر):
        جواز_دہی_کریں_راہ(راستہ_2)
        if راستہ_2 in 파일들:
            raise ValueError('중복 بنڈل راستہ_2: ' + راستہ_2)
        if len(مشمول_قدر) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + راستہ_2)
        مشمول_قدر.decode('utf-8')
        파일들[راستہ_2] = مشمول_قدر
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ماخذ_شجر 16개·합계 64 KiB 이하여야 합니다.')
    if فائل_اندراج_نام.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(کوائف)) as بنڈل:
            항목들 = بنڈل.infolist()
            if len(항목들) > 256 or sum(اندراج_قدر.file_size for اندراج_قدر in 항목들) > 1048576:
                raise ValueError('محفوظ_قدر ریلیز_ذخیرہ حجم 제한 초과')
            جاب_فہرست = [اندراج_قدر for اندراج_قدر in 항목들 if اندراج_قدر.filename.endswith('.dist-info/WHEEL')]
            if len(جاب_فہرست) != 1:
                raise ValueError('wheel جاب_قدر 명세가 필요합니다.')
            جاب_قدر = email.parser.Parser().parsestr(بنڈل.read(جاب_فہرست[0]).decode())
            if جاب_قدر.get('Root-Is-Purelib', '').lower() != 'true' or not فائل_اندراج_نام.endswith('-none-any.whl'):
                raise ValueError('C توسیع_قدر·플랫폼 전용 wheel은 지원하지 않습니다.')
            for اندراج_قدر in 항목들:
                راستہ_2 = اندراج_قدر.filename.rstrip('/')
                جواز_دہی_کریں_راہ(راستہ_2, False)
                if (اندراج_قدر.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if اندراج_قدر.filename.endswith('/'):
                    continue
                if '.dist-info/' in راستہ_2:
                    if راستہ_2.endswith('/METADATA'):
                        명세들.append(بنڈل.read(اندراج_قدر).decode())
                    continue
                if not راستہ_2.endswith('.py') or '.data/' in راستہ_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + راستہ_2)
                추가(راستہ_2, بنڈل.read(اندراج_قدر))
    elif فائل_اندراج_نام.endswith('.tar.gz') and نام.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py نفاذ_کریں_حکم 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(کوائف), mode='r|gz') as بنڈل:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for اندراج_قدر in بنڈل:
                항목수 += 1
                전체크기 += اندراج_قدر.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('محفوظ_قدر ریلیز_ذخیرہ حجم 제한 초과')
                جواز_دہی_کریں_راہ(اندراج_قدر.name, False)
                부분들 = اندراج_قدر.name.split('/')
                뿌리들.add(부분들[0])
                if اندراج_قدر.isdir():
                    continue
                if not اندراج_قدر.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ماخذ_شجر 배포형')
                راستہ_2 = '/'.join(부분들[1:])
                مشمول_قدر = بنڈل.extractfile(اندراج_قدر).read()
                if راستہ_2.endswith('PKG-INFO'):
                    명세들.append(مشمول_قدر.decode())
                elif راستہ_2.endswith('.py') and راستہ_2 not in ('setup.py',):
                    추가(راستہ_2, مشمول_قدر)
                elif '.egg-info/' not in راستہ_2 and not راستہ_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + راستہ_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 روٹ_قدر 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ماخذ_شجر 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != نام or 명세.get('Version') != ورژن_قدر:
        raise ValueError('배포 메타데이터의 نام·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(پتہ, 한도):
    if not پتہ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(پتہ, timeout=30) as جواب_دیں:
        if not جواب_دیں.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 پتہ منتقل_کریں_قدر')
        کوائف = جواب_دیں.read(한도 + 1)
    if len(کوائف) > 한도:
        raise ValueError('배포 فائل_کا_نام حجم 제한 초과')
    return کوائف


def منتقلی_بنڈل(نام, ورژن_قدر, 파일들, 출처):
    명세 = {'name': نام, 'version': ورژن_قدر, 'source': 출처, 'files': [
        {'path': راستہ_2, 'size': len(کوائف), 'sha256': hashlib.sha256(کوائف).hexdigest()}
        for راستہ_2, کوائف in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('بنڈل 명세 حجم 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[اندراج_قدر['path']] for اندراج_قدر in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, راستہ_2, معلومات_ٹیکنالوجی_آف_لائن=False):
        자신.راستہ_2 = Path(راستہ_2)
        자신.راستہ_2.mkdir(parents=True, exist_ok=True)
        자신.معلومات_ٹیکنالوجی_آف_لائن = معلومات_ٹیکنالوجی_آف_لائن

    def تیار_کریں(자신, 요청):
        نام, ورژن_قدر = 요청해석(요청)
        열쇠 = نام + ('==' + ورژن_قدر if ورژن_قدر else '')
        لاگ_راہ = 자신.راستہ_2 / (열쇠 + '.json')
        배포경로 = 자신.راستہ_2 / (열쇠 + '.archive')
        if لاگ_راہ.is_file() and 배포경로.is_file():
            لاگ_صف = json.loads(لاگ_راہ.read_text())
            کوائف = 배포경로.read_bytes()
            if hashlib.sha256(کوائف).hexdigest() != لاگ_صف['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.معلومات_ٹیکنالوجی_آف_لائن:
                raise ValueError('معلومات_ٹیکنالوجی_آف_لائن 저장소에 없는 بنڈل: ' + 요청)
            پتہ = 'https://pypi.org/pypi/' + نام + ('/' + ورژن_قدر if ورژن_قدر else '') + '/json'
            نظام_کی_معلومات = json.loads(웹읽기(پتہ, 4194304).decode())
            if نظام_کی_معلومات['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [اندراج_قدر for اندراج_قدر in نظام_کی_معلومات['urls'] if not اندراج_قدر.get('yanked') and اندراج_قدر['filename'].endswith('-none-any.whl')]
            if not 후보 and نام.startswith('micropython-'):
                후보 = [اندراج_قدر for اندراج_قدر in نظام_کی_معلومات['urls'] if not اندراج_قدر.get('yanked') and اندراج_قدر['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            انتخاب_قدر = 후보[0]
            کوائف = 웹읽기(انتخاب_قدر['url'], 4194304)
            if hashlib.sha256(کوائف).hexdigest() != انتخاب_قدر['digests']['sha256']:
                raise ValueError('PyPI 배포 فائل_کا_نام SHA-256 불일치')
            لاگ_صف = {'name': نام, 'version': نظام_کی_معلومات['info']['version'], 'filename': انتخاب_قدر['filename'],
                    'url': انتخاب_قدر['url'], 'sha256': انتخاب_قدر['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(لاگ_صف['filename'], کوائف, نام, لاگ_صف['version'])
            배포경로.write_bytes(کوائف)
            لاگ_راہ.write_text(json.dumps(لاگ_صف, ensure_ascii=False, indent=2) + '\n')
        if لاگ_صف['name'] != نام or ورژن_قدر and لاگ_صف['version'] != ورژن_قدر:
            raise ValueError('저장소 نام·버전 불일치')
        파일들 = 압축풀기(لاگ_صف['filename'], کوائف, نام, لاگ_صف['version'])
        return منتقلی_بنڈل(نام, لاگ_صف['version'], 파일들, لاگ_صف['url'])


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
                raise ValueError('잘못된 بنڈل 요청')
            جواب_دیں = 자신.server.저장소.تیار_کریں(요청[:-1].decode('ascii'))
        except Exception as غلطی:
            머리 = json.dumps({'error': str(غلطی)[:500]}, ensure_ascii=False).encode()
            جواب_دیں = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(جواب_دیں)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, دہانہ_نمبر=8027, راستہ_2=None, معلومات_ٹیکنالوجی_آف_لائن=False):
        자신.سرور_قدر = socketserver.TCPServer(('127.0.0.1', دہانہ_نمبر), 꾸러미요청, bind_and_activate=False)
        자신.سرور_قدر.allow_reuse_address = True
        자신.سرور_قدر.server_bind()
        자신.سرور_قدر.server_activate()
        자신.سرور_قدر.저장소 = 꾸러미저장소(راستہ_2 or عکس_ڈالنا_روٹ/'build/pip-cache', معلومات_ٹیکنالوجی_آف_لائن)
        자신.دہانہ_نمبر = 자신.سرور_قدر.server_address[1]
        자신.تھریڈ_قدر = threading.Thread(target=자신.سرور_قدر.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.تھریڈ_قدر.start()
        return 자신

    def __exit__(자신, *دلائل):
        자신.سرور_قدر.shutdown()
        자신.سرور_قدر.server_close()
        자신.تھریڈ_قدر.join(timeout=2)


def چلائیں():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=عکس_ڈالنا_روٹ/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='نفاذ_کریں_حکم 없이 호환 배포 파일을 내려받아 검사·ذخیرہ_کریں_قدر')
    دلائل = 해석기.parse_args()
    if دلائل.fetch:
        کوائف = 꾸러미저장소(دلائل.cache, دلائل.offline).تیار_کریں(دلائل.fetch)
        print('بنڈل تیار_کریں 완료:', دلائل.fetch, len(کوائف), 'بائٹ_قدر')
        return
    with 꾸러미중계(دلائل.port, دلائل.cache, دلائل.offline) as 중계:
        print('بنڈل 중계: 127.0.0.1:' + str(중계.دہانہ_نمبر), flush=True)
        try:
            중계.تھریڈ_قدر.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    چلائیں()
