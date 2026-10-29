#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 نصب_مقدار·실행한다."""
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

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('دسته_کردن نام 또는 نام==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ارزیابی_کردن_مسیر(نام, نصب_مسیر=True):
    مسیر = PurePosixPath(نام)
    if مسیر.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in نام.split('/')):
        raise ValueError('허용하지 않는 دسته_کردن مسیر: ' + نام)
    if '\\' in نام or any(ord(نویسه_مقدار) < 32 or ord(نویسه_مقدار) == 127 for نویسه_مقدار in نام):
        raise ValueError('잘못된 دسته_کردن مسیر 문자')
    if نصب_مسیر and (len(('/lib/' + نام).encode()) > 63 or نام in ('فارسی.py', 'دسته_کردن.py')):
        raise ValueError('دسته_کردن مسیر 제한 또는 مقدار_پیش_فرض کتابخانه 충돌: ' + نام)
    return نام


def 압축풀기(فایل_ورودی_نام, داده_ها, نام, نسخه_مقدار):
    파일들 = {}
    명세들 = []
    def 추가(مسیر, محتوا_مقدار):
        ارزیابی_کردن_مسیر(مسیر)
        if مسیر in 파일들:
            raise ValueError('중복 دسته_کردن مسیر: ' + مسیر)
        if len(محتوا_مقدار) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + مسیر)
        محتوا_مقدار.decode('utf-8')
        파일들[مسیر] = محتوا_مقدار
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 منبع_درخت 16개·합계 64 KiB 이하여야 합니다.')
    if فایل_ورودی_نام.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(داده_ها)) as دسته_کردن:
            항목들 = دسته_کردن.infolist()
            if len(항목들) > 256 or sum(ورودی_مقدار.file_size for ورودی_مقدار in 항목들) > 1048576:
                raise ValueError('آرشیو_مقدار انتشار_حافظه_تلفن اندازه 제한 초과')
            شغل_لیست = [ورودی_مقدار for ورودی_مقدار in 항목들 if ورودی_مقدار.filename.endswith('.dist-info/WHEEL')]
            if len(شغل_لیست) != 1:
                raise ValueError('wheel شغل_مقدار 명세가 필요합니다.')
            شغل_مقدار = email.parser.Parser().parsestr(دسته_کردن.read(شغل_لیست[0]).decode())
            if شغل_مقدار.get('Root-Is-Purelib', '').lower() != 'true' or not فایل_ورودی_نام.endswith('-none-any.whl'):
                raise ValueError('C تمدید_مقدار·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ورودی_مقدار in 항목들:
                مسیر = ورودی_مقدار.filename.rstrip('/')
                ارزیابی_کردن_مسیر(مسیر, False)
                if (ورودی_مقدار.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ورودی_مقدار.filename.endswith('/'):
                    continue
                if '.dist-info/' in مسیر:
                    if مسیر.endswith('/METADATA'):
                        명세들.append(دسته_کردن.read(ورودی_مقدار).decode())
                    continue
                if not مسیر.endswith('.py') or '.data/' in مسیر:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + مسیر)
                추가(مسیر, دسته_کردن.read(ورودی_مقدار))
    elif فایل_ورودی_نام.endswith('.tar.gz') and نام.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py اجرا_فرمان 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(داده_ها), mode='r|gz') as دسته_کردن:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ورودی_مقدار in دسته_کردن:
                항목수 += 1
                전체크기 += ورودی_مقدار.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('آرشیو_مقدار انتشار_حافظه_تلفن اندازه 제한 초과')
                ارزیابی_کردن_مسیر(ورودی_مقدار.name, False)
                부분들 = ورودی_مقدار.name.split('/')
                뿌리들.add(부분들[0])
                if ورودی_مقدار.isdir():
                    continue
                if not ورودی_مقدار.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython منبع_درخت 배포형')
                مسیر = '/'.join(부분들[1:])
                محتوا_مقدار = دسته_کردن.extractfile(ورودی_مقدار).read()
                if مسیر.endswith('PKG-INFO'):
                    명세들.append(محتوا_مقدار.decode())
                elif مسیر.endswith('.py') and مسیر not in ('setup.py',):
                    추가(مسیر, محتوا_مقدار)
                elif '.egg-info/' not in مسیر and not مسیر.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + مسیر)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 جذر_مقدار 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* منبع_درخت 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != نام or 명세.get('Version') != نسخه_مقدار:
        raise ValueError('배포 메타데이터의 نام·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(آدرس, 한도):
    if not آدرس.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(آدرس, timeout=30) as پاسخ_دادن:
        if not پاسخ_دادن.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 آدرس انتقال_مقدار')
        داده_ها = پاسخ_دادن.read(한도 + 1)
    if len(داده_ها) > 한도:
        raise ValueError('배포 پرونده اندازه 제한 초과')
    return داده_ها


def انتقال_دسته_کردن(نام, نسخه_مقدار, 파일들, 출처):
    명세 = {'name': نام, 'version': نسخه_مقدار, 'source': 출처, 'files': [
        {'path': مسیر, 'size': len(داده_ها), 'sha256': hashlib.sha256(داده_ها).hexdigest()}
        for مسیر, داده_ها in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('دسته_کردن 명세 اندازه 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ورودی_مقدار['path']] for ورودی_مقدار in 명세['files'])


class دسته_کردن_مخزن:
    def __init__(자신, مسیر, فناوری_اطلاعات_آفلاین=False):
        자신.مسیر = Path(مسیر)
        자신.مسیر.mkdir(parents=True, exist_ok=True)
        자신.فناوری_اطلاعات_آفلاین = فناوری_اطلاعات_آفلاین

    def آماده_کردن(자신, 요청):
        نام, نسخه_مقدار = 요청해석(요청)
        열쇠 = نام + ('==' + نسخه_مقدار if نسخه_مقدار else '')
        واقعه_نگار_مسیر = 자신.مسیر / (열쇠 + '.json')
        배포경로 = 자신.مسیر / (열쇠 + '.archive')
        if واقعه_نگار_مسیر.is_file() and 배포경로.is_file():
            واقعه_نگار_ردیف = json.loads(واقعه_نگار_مسیر.read_text())
            داده_ها = 배포경로.read_bytes()
            if hashlib.sha256(داده_ها).hexdigest() != واقعه_نگار_ردیف['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.فناوری_اطلاعات_آفلاین:
                raise ValueError('فناوری_اطلاعات_آفلاین 저장소에 없는 دسته_کردن: ' + 요청)
            آدرس = 'https://pypi.org/pypi/' + نام + ('/' + نسخه_مقدار if نسخه_مقدار else '') + '/json'
            اطلاعات_سیستم = json.loads(웹읽기(آدرس, 4194304).decode())
            if اطلاعات_سیستم['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ورودی_مقدار for ورودی_مقدار in اطلاعات_سیستم['urls'] if not ورودی_مقدار.get('yanked') and ورودی_مقدار['filename'].endswith('-none-any.whl')]
            if not 후보 and نام.startswith('micropython-'):
                후보 = [ورودی_مقدار for ورودی_مقدار in اطلاعات_سیستم['urls'] if not ورودی_مقدار.get('yanked') and ورودی_مقدار['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            مورد_انتخابی_مقدار = 후보[0]
            داده_ها = 웹읽기(مورد_انتخابی_مقدار['url'], 4194304)
            if hashlib.sha256(داده_ها).hexdigest() != مورد_انتخابی_مقدار['digests']['sha256']:
                raise ValueError('PyPI 배포 پرونده SHA-256 불일치')
            واقعه_نگار_ردیف = {'name': نام, 'version': اطلاعات_سیستم['info']['version'], 'filename': مورد_انتخابی_مقدار['filename'],
                    'url': مورد_انتخابی_مقدار['url'], 'sha256': مورد_انتخابی_مقدار['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(واقعه_نگار_ردیف['filename'], داده_ها, نام, واقعه_نگار_ردیف['version'])
            배포경로.write_bytes(داده_ها)
            واقعه_نگار_مسیر.write_text(json.dumps(واقعه_نگار_ردیف, ensure_ascii=False, indent=2) + '\n')
        if واقعه_نگار_ردیف['name'] != نام or نسخه_مقدار and واقعه_نگار_ردیف['version'] != نسخه_مقدار:
            raise ValueError('مخزن_جذر نام·버전 불일치')
        파일들 = 압축풀기(واقعه_نگار_ردیف['filename'], داده_ها, نام, واقعه_نگار_ردیف['version'])
        return انتقال_دسته_کردن(نام, واقعه_نگار_ردیف['version'], 파일들, واقعه_نگار_ردیف['url'])


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
                raise ValueError('잘못된 دسته_کردن 요청')
            پاسخ_دادن = 자신.server.مخزن_جذر.آماده_کردن(요청[:-1].decode('ascii'))
        except Exception as خطا:
            머리 = json.dumps({'error': str(خطا)[:500]}, ensure_ascii=False).encode()
            پاسخ_دادن = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(پاسخ_دادن)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, شماره_درگاه=8027, مسیر=None, فناوری_اطلاعات_آفلاین=False):
        자신.سرور_مقدار = socketserver.TCPServer(('127.0.0.1', شماره_درگاه), 꾸러미요청, bind_and_activate=False)
        자신.سرور_مقدار.allow_reuse_address = True
        자신.سرور_مقدار.server_bind()
        자신.سرور_مقدار.server_activate()
        자신.سرور_مقدار.مخزن_جذر = دسته_کردن_مخزن(مسیر or نمایش_دادن_جذر/'build/pip-cache', فناوری_اطلاعات_آفلاین)
        자신.شماره_درگاه = 자신.سرور_مقدار.server_address[1]
        자신.رشته_مقدار = threading.Thread(target=자신.سرور_مقدار.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.رشته_مقدار.start()
        return 자신

    def __exit__(자신, *نشانوندها):
        자신.سرور_مقدار.shutdown()
        자신.سرور_مقدار.server_close()
        자신.رشته_مقدار.join(timeout=2)


def اجرا_2():
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('--port', type=int, default=8027)
    مفسر_48ee4b1b.add_argument('--cache', type=Path, default=نمایش_دادن_جذر/'build/pip-cache')
    مفسر_48ee4b1b.add_argument('--offline', action='store_true')
    مفسر_48ee4b1b.add_argument('--fetch', help='اجرا_فرمان 없이 호환 배포 파일을 내려받아 검사·ذخیره_مقدار')
    نشانوندها = مفسر_48ee4b1b.parse_args()
    if نشانوندها.fetch:
        داده_ها = دسته_کردن_مخزن(نشانوندها.cache, نشانوندها.offline).آماده_کردن(نشانوندها.fetch)
        print('دسته_کردن آماده_کردن 완료:', نشانوندها.fetch, len(داده_ها), 'بایت_مقدار')
        return
    with 꾸러미중계(نشانوندها.port, نشانوندها.cache, نشانوندها.offline) as 중계:
        print('دسته_کردن 중계: 127.0.0.1:' + str(중계.شماره_درگاه), flush=True)
        try:
            중계.رشته_مقدار.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    اجرا_2()
