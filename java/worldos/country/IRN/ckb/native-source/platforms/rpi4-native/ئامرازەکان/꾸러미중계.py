#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 دامەزرێنە_نرخ·실행한다."""
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
        raise ValueError('گورزە ناو 또는 ناو==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ڕەوایی_گوزەر(ناو, دامەزراندن_گوزەر=True):
    گوزەر = PurePosixPath(ناو)
    if گوزەر.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ناو.split('/')):
        raise ValueError('허용하지 않는 گورزە گوزەر: ' + ناو)
    if '\\' in ناو or any(ord(نووسە_نرخ) < 32 or ord(نووسە_نرخ) == 127 for نووسە_نرخ in ناو):
        raise ValueError('잘못된 گورزە گوزەر 문자')
    if دامەزراندن_گوزەر and (len(('/lib/' + ناو).encode()) > 63 or ناو in ('한국어.py', 'گورزە.py')):
        raise ValueError('گورزە گوزەر 제한 또는 بەهای_گریمانە کتێبخانە 충돌: ' + ناو)
    return ناو


def 압축풀기(فایل_تێنووسین_ناو, دەیتا, ناو, وەشان_نرخ):
    파일들 = {}
    명세들 = []
    def 추가(گوزەر, ناوەرۆک_نرخ):
        ڕەوایی_گوزەر(گوزەر)
        if گوزەر in 파일들:
            raise ValueError('중복 گورزە گوزەر: ' + گوزەر)
        if len(ناوەرۆک_نرخ) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + گوزەر)
        ناوەرۆک_نرخ.decode('utf-8')
        파일들[گوزەر] = ناوەرۆک_نرخ
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ژێدەر_دار 16개·합계 64 KiB 이하여야 합니다.')
    if فایل_تێنووسین_ناو.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(دەیتا)) as گورزە:
            항목들 = گورزە.infolist()
            if len(항목들) > 256 or sum(تێنووسین_نرخ.file_size for تێنووسین_نرخ in 항목들) > 1048576:
                raise ValueError('ئەرشیف_نرخ وەشان_هەمارگە گۆڕینی_ئەندازە 제한 초과')
            ئەرک_لیست = [تێنووسین_نرخ for تێنووسین_نرخ in 항목들 if تێنووسین_نرخ.filename.endswith('.dist-info/WHEEL')]
            if len(ئەرک_لیست) != 1:
                raise ValueError('wheel ئەرک_نرخ 명세가 필요합니다.')
            ئەرک_نرخ = email.parser.Parser().parsestr(گورزە.read(ئەرک_لیست[0]).decode())
            if ئەرک_نرخ.get('Root-Is-Purelib', '').lower() != 'true' or not فایل_تێنووسین_ناو.endswith('-none-any.whl'):
                raise ValueError('C پاشبەند_نرخ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for تێنووسین_نرخ in 항목들:
                گوزەر = تێنووسین_نرخ.filename.rstrip('/')
                ڕەوایی_گوزەر(گوزەر, False)
                if (تێنووسین_نرخ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if تێنووسین_نرخ.filename.endswith('/'):
                    continue
                if '.dist-info/' in گوزەر:
                    if گوزەر.endswith('/METADATA'):
                        명세들.append(گورزە.read(تێنووسین_نرخ).decode())
                    continue
                if not گوزەر.endswith('.py') or '.data/' in گوزەر:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + گوزەر)
                추가(گوزەر, گورزە.read(تێنووسین_نرخ))
    elif فایل_تێنووسین_ناو.endswith('.tar.gz') and ناو.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py جێبەجێکردن_فەرمان 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(دەیتا), mode='r|gz') as گورزە:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for تێنووسین_نرخ in گورزە:
                항목수 += 1
                전체크기 += تێنووسین_نرخ.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ئەرشیف_نرخ وەشان_هەمارگە گۆڕینی_ئەندازە 제한 초과')
                ڕەوایی_گوزەر(تێنووسین_نرخ.name, False)
                부분들 = تێنووسین_نرخ.name.split('/')
                뿌리들.add(부분들[0])
                if تێنووسین_نرخ.isdir():
                    continue
                if not تێنووسین_نرخ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ژێدەر_دار 배포형')
                گوزەر = '/'.join(부분들[1:])
                ناوەرۆک_نرخ = گورزە.extractfile(تێنووسین_نرخ).read()
                if گوزەر.endswith('PKG-INFO'):
                    명세들.append(ناوەرۆک_نرخ.decode())
                elif گوزەر.endswith('.py') and گوزەر not in ('setup.py',):
                    추가(گوزەر, ناوەرۆک_نرخ)
                elif '.egg-info/' not in گوزەر and not گوزەر.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + گوزەر)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ژێدەر_دار 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ناو or 명세.get('Version') != وەشان_نرخ:
        raise ValueError('배포 메타데이터의 ناو·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ناونیشان, 한도):
    if not ناونیشان.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ناونیشان, timeout=30) as وەڵامدانەوه:
        if not وەڵامدانەوه.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ناونیشان گواستنەوە_نرخ')
        دەیتا = وەڵامدانەوه.read(한도 + 1)
    if len(دەیتا) > 한도:
        raise ValueError('배포 فایل گۆڕینی_ئەندازە 제한 초과')
    return دەیتا


def گواستنەوە_گورزە(ناو, وەشان_نرخ, 파일들, 출처):
    명세 = {'name': ناو, 'version': وەشان_نرخ, 'source': 출처, 'files': [
        {'path': گوزەر, 'size': len(دەیتا), 'sha256': hashlib.sha256(دەیتا).hexdigest()}
        for گوزەر, دەیتا in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('گورزە 명세 گۆڕینی_ئەندازە 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[تێنووسین_نرخ['path']] for تێنووسین_نرخ in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, گوزەر, 오프라인=False):
        자신.گوزەر = Path(گوزەر)
        자신.گوزەر.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def ئامادە_کردن_9ce364fc(자신, 요청):
        ناو, وەشان_نرخ = 요청해석(요청)
        열쇠 = ناو + ('==' + وەشان_نرخ if وەشان_نرخ else '')
        تۆمار_گوزەر = 자신.گوزەر / (열쇠 + '.json')
        배포경로 = 자신.گوزەر / (열쇠 + '.archive')
        if تۆمار_گوزەر.is_file() and 배포경로.is_file():
            تۆمار_ڕزن = json.loads(تۆمار_گوزەر.read_text())
            دەیتا = 배포경로.read_bytes()
            if hashlib.sha256(دەیتا).hexdigest() != تۆمار_ڕزن['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 گورزە: ' + 요청)
            ناونیشان = 'https://pypi.org/pypi/' + ناو + ('/' + وەشان_نرخ if وەشان_نرخ else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ناونیشان, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [تێنووسین_نرخ for تێنووسین_نرخ in msinfo32_exe['urls'] if not تێنووسین_نرخ.get('yanked') and تێنووسین_نرخ['filename'].endswith('-none-any.whl')]
            if not 후보 and ناو.startswith('micropython-'):
                후보 = [تێنووسین_نرخ for تێنووسین_نرخ in msinfo32_exe['urls'] if not تێنووسین_نرخ.get('yanked') and تێنووسین_نرخ['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            بژاردە_نرخ = 후보[0]
            دەیتا = 웹읽기(بژاردە_نرخ['url'], 4194304)
            if hashlib.sha256(دەیتا).hexdigest() != بژاردە_نرخ['digests']['sha256']:
                raise ValueError('PyPI 배포 فایل SHA-256 불일치')
            تۆمار_ڕزن = {'name': ناو, 'version': msinfo32_exe['info']['version'], 'filename': بژاردە_نرخ['filename'],
                    'url': بژاردە_نرخ['url'], 'sha256': بژاردە_نرخ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(تۆمار_ڕزن['filename'], دەیتا, ناو, تۆمار_ڕزن['version'])
            배포경로.write_bytes(دەیتا)
            تۆمار_گوزەر.write_text(json.dumps(تۆمار_ڕزن, ensure_ascii=False, indent=2) + '\n')
        if تۆمار_ڕزن['name'] != ناو or وەشان_نرخ and تۆمار_ڕزن['version'] != وەشان_نرخ:
            raise ValueError('저장소 ناو·버전 불일치')
        파일들 = 압축풀기(تۆمار_ڕزن['filename'], دەیتا, ناو, تۆمار_ڕزن['version'])
        return گواستنەوە_گورزە(ناو, تۆمار_ڕزن['version'], 파일들, تۆمار_ڕزن['url'])


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
                raise ValueError('잘못된 گورزە 요청')
            وەڵامدانەوه = 자신.server.저장소.ئامادە_کردن_9ce364fc(요청[:-1].decode('ascii'))
        except Exception as هەڵە:
            머리 = json.dumps({'error': str(هەڵە)[:500]}, ensure_ascii=False).encode()
            وەڵامدانەوه = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(وەڵامدانەوه)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, گوزەر=None, 오프라인=False):
        자신.ڕاژەکار_نرخ = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.ڕاژەکار_نرخ.allow_reuse_address = True
        자신.ڕاژەکار_نرخ.server_bind()
        자신.ڕاژەکار_نرخ.server_activate()
        자신.ڕاژەکار_نرخ.저장소 = 꾸러미저장소(گوزەر or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.ڕاژەکار_نرخ.server_address[1]
        자신.ڕستە_نرخ = threading.Thread(target=자신.ڕاژەکار_نرخ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ڕستە_نرخ.start()
        return 자신

    def __exit__(자신, *인수):
        자신.ڕاژەکار_نرخ.shutdown()
        자신.ڕاژەکار_نرخ.server_close()
        자신.ڕستە_نرخ.join(timeout=2)


def ڕادان():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='جێبەجێکردن_فەرمان 없이 호환 배포 파일을 내려받아 검사·Store_نرخ')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        دەیتا = 꾸러미저장소(인수.cache, 인수.offline).ئامادە_کردن_9ce364fc(인수.fetch)
        print('گورزە ئامادە_کردن_9ce364fc 완료:', 인수.fetch, len(دەیتا), 'بایت_نرخ')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('گورزە 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.ڕستە_نرخ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ڕادان()
