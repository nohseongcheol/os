#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 நிறுவு_மதிப்பு·실행한다."""
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

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]


def அலகிடு_HTTP_வேண்டுதல்(HTTP_வேண்டுதல்):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', HTTP_வேண்டுதல்)
    if not 맞음:
        raise ValueError('மூட்டை பெயர் 또는 பெயர்==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def சரிபார்_பாதை(பெயர், நிறுவல்_பாதை=True):
    பாதை_2 = PurePosixPath(பெயர்)
    if பாதை_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in பெயர்.split('/')):
        raise ValueError('허용하지 않는 மூட்டை பாதை_2: ' + பெயர்)
    if '\\' in பெயர் or any(ord(எழுத்துக்குறி_மதிப்பு) < 32 or ord(எழுத்துக்குறி_மதிப்பு) == 127 for எழுத்துக்குறி_மதிப்பு in பெயர்):
        raise ValueError('잘못된 மூட்டை பாதை_2 문자')
    if நிறுவல்_பாதை and (len(('/lib/' + பெயர்).encode()) > 63 or பெயர் in ('தமிழ்.py', 'மூட்டை.py')):
        raise ValueError('மூட்டை பாதை_2 제한 또는 இயல்புநிலை_மதிப்பு நூலகம் 충돌: ' + பெயர்)
    return பெயர்


def சுருக்க_நீக்கம்(கோப்பு_உள்ளீடு_பெயர், தரவு, பெயர், பதிப்பு_மதிப்பு):
    파일들 = {}
    명세들 = []
    def 추가(பாதை_2, உள்ளடக்கம்_மதிப்பு):
        சரிபார்_பாதை(பாதை_2)
        if பாதை_2 in 파일들:
            raise ValueError('중복 மூட்டை பாதை_2: ' + பாதை_2)
        if len(உள்ளடக்கம்_மதிப்பு) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + பாதை_2)
        உள்ளடக்கம்_மதிப்பு.decode('utf-8')
        파일들[பாதை_2] = உள்ளடக்கம்_மதிப்பு
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 மூலம்_மரம் 16개·합계 64 KiB 이하여야 합니다.')
    if கோப்பு_உள்ளீடு_பெயர்.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(தரவு)) as மூட்டை:
            항목들 = மூட்டை.infolist()
            if len(항목들) > 256 or sum(உள்ளீடு_மதிப்பு.file_size for உள்ளீடு_மதிப்பு in 항목들) > 1048576:
                raise ValueError('காப்பகம்_மதிப்பு அனுப்பு_சேமிப்பகம் அளவு 제한 초과')
            வேலை_பட்டியல் = [உள்ளீடு_மதிப்பு for உள்ளீடு_மதிப்பு in 항목들 if உள்ளீடு_மதிப்பு.filename.endswith('.dist-info/WHEEL')]
            if len(வேலை_பட்டியல்) != 1:
                raise ValueError('wheel வேலை_மதிப்பு_102996da 명세가 필요합니다.')
            வேலை_மதிப்பு_102996da = email.parser.Parser().parsestr(மூட்டை.read(வேலை_பட்டியல்[0]).decode())
            if வேலை_மதிப்பு_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not கோப்பு_உள்ளீடு_பெயர்.endswith('-none-any.whl'):
                raise ValueError('C நீட்டிப்பு_மதிப்பு·플랫폼 전용 wheel은 지원하지 않습니다.')
            for உள்ளீடு_மதிப்பு in 항목들:
                பாதை_2 = உள்ளீடு_மதிப்பு.filename.rstrip('/')
                சரிபார்_பாதை(பாதை_2, False)
                if (உள்ளீடு_மதிப்பு.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if உள்ளீடு_மதிப்பு.filename.endswith('/'):
                    continue
                if '.dist-info/' in பாதை_2:
                    if பாதை_2.endswith('/METADATA'):
                        명세들.append(மூட்டை.read(உள்ளீடு_மதிப்பு).decode())
                    continue
                if not பாதை_2.endswith('.py') or '.data/' in பாதை_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + பாதை_2)
                추가(பாதை_2, மூட்டை.read(உள்ளீடு_மதிப்பு))
    elif கோப்பு_உள்ளீடு_பெயர்.endswith('.tar.gz') and பெயர்.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py இயக்கு_கட்டளை 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(தரவு), mode='r|gz') as மூட்டை:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for உள்ளீடு_மதிப்பு in மூட்டை:
                항목수 += 1
                전체크기 += உள்ளீடு_மதிப்பு.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('காப்பகம்_மதிப்பு அனுப்பு_சேமிப்பகம் அளவு 제한 초과')
                சரிபார்_பாதை(உள்ளீடு_மதிப்பு.name, False)
                부분들 = உள்ளீடு_மதிப்பு.name.split('/')
                뿌리들.add(부분들[0])
                if உள்ளீடு_மதிப்பு.isdir():
                    continue
                if not உள்ளீடு_மதிப்பு.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython மூலம்_மரம் 배포형')
                பாதை_2 = '/'.join(부분들[1:])
                உள்ளடக்கம்_மதிப்பு = மூட்டை.extractfile(உள்ளீடு_மதிப்பு).read()
                if பாதை_2.endswith('PKG-INFO'):
                    명세들.append(உள்ளடக்கம்_மதிப்பு.decode())
                elif பாதை_2.endswith('.py') and பாதை_2 not in ('setup.py',):
                    추가(பாதை_2, உள்ளடக்கம்_மதிப்பு)
                elif '.egg-info/' not in பாதை_2 and not பாதை_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + பாதை_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 மூலம்_மதிப்பு 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* மூலம்_மரம் 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if அலகிடு_HTTP_வேண்டுதல்(명세.get('Name', ''))[0] != பெயர் or 명세.get('Version') != பதிப்பு_மதிப்பு:
        raise ValueError('배포 메타데이터의 பெயர்·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(முகவரி, 한도):
    if not முகவரி.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(முகவரி, timeout=30) as பதிலளி:
        if not பதிலளி.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 முகவரி நகர்த்து_மதிப்பு')
        தரவு = பதிலளி.read(한도 + 1)
    if len(தரவு) > 한도:
        raise ValueError('배포 கோப்பின்_பெயர் அளவு 제한 초과')
    return தரவு


def இடமாற்று_மூட்டை(பெயர், பதிப்பு_மதிப்பு, 파일들, 출처):
    명세 = {'name': பெயர், 'version': பதிப்பு_மதிப்பு, 'source': 출처, 'files': [
        {'path': பாதை_2, 'size': len(தரவு), 'sha256': hashlib.sha256(தரவு).hexdigest()}
        for பாதை_2, தரவு in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('மூட்டை 명세 அளவு 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[உள்ளீடு_மதிப்பு['path']] for உள்ளீடு_மதிப்பு in 명세['files'])


class மூட்டை_தொகுபதிவகம்:
    def __init__(자신, பாதை_2, தகவல்_தொழில்நுட்பம்_ஆஃப்லைன்=False):
        자신.பாதை_2 = Path(பாதை_2)
        자신.பாதை_2.mkdir(parents=True, exist_ok=True)
        자신.தகவல்_தொழில்நுட்பம்_ஆஃப்லைன் = தகவல்_தொழில்நுட்பம்_ஆஃப்லைன்

    def தயார்படுத்த(자신, HTTP_வேண்டுதல்):
        பெயர், பதிப்பு_மதிப்பு = அலகிடு_HTTP_வேண்டுதல்(HTTP_வேண்டுதல்)
        열쇠 = பெயர் + ('==' + பதிப்பு_மதிப்பு if பதிப்பு_மதிப்பு else '')
        பதிவு_பாதை = 자신.பாதை_2 / (열쇠 + '.json')
        배포경로 = 자신.பாதை_2 / (열쇠 + '.archive')
        if பதிவு_பாதை.is_file() and 배포경로.is_file():
            பதிவு_பதிவு = json.loads(பதிவு_பாதை.read_text())
            தரவு = 배포경로.read_bytes()
            if hashlib.sha256(தரவு).hexdigest() != பதிவு_பதிவு['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.தகவல்_தொழில்நுட்பம்_ஆஃப்லைன்:
                raise ValueError('தகவல்_தொழில்நுட்பம்_ஆஃப்லைன் 저장소에 없는 மூட்டை: ' + HTTP_வேண்டுதல்)
            முகவரி = 'https://pypi.org/pypi/' + பெயர் + ('/' + பதிப்பு_மதிப்பு if பதிப்பு_மதிப்பு else '') + '/json'
            கணினித்_தகவல் = json.loads(웹읽기(முகவரி, 4194304).decode())
            if கணினித்_தகவல்['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [உள்ளீடு_மதிப்பு for உள்ளீடு_மதிப்பு in கணினித்_தகவல்['urls'] if not உள்ளீடு_மதிப்பு.get('yanked') and உள்ளீடு_மதிப்பு['filename'].endswith('-none-any.whl')]
            if not 후보 and பெயர்.startswith('micropython-'):
                후보 = [உள்ளீடு_மதிப்பு for உள்ளீடு_மதிப்பு in கணினித்_தகவல்['urls'] if not உள்ளீடு_மதிப்பு.get('yanked') and உள்ளீடு_மதிப்பு['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            தேர்வு_மதிப்பு = 후보[0]
            தரவு = 웹읽기(தேர்வு_மதிப்பு['url'], 4194304)
            if hashlib.sha256(தரவு).hexdigest() != தேர்வு_மதிப்பு['digests']['sha256']:
                raise ValueError('PyPI 배포 கோப்பின்_பெயர் SHA-256 불일치')
            பதிவு_பதிவு = {'name': பெயர், 'version': கணினித்_தகவல்['info']['version'], 'filename': தேர்வு_மதிப்பு['filename'],
                    'url': தேர்வு_மதிப்பு['url'], 'sha256': தேர்வு_மதிப்பு['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            சுருக்க_நீக்கம்(பதிவு_பதிவு['filename'], தரவு, பெயர், பதிவு_பதிவு['version'])
            배포경로.write_bytes(தரவு)
            பதிவு_பாதை.write_text(json.dumps(பதிவு_பதிவு, ensure_ascii=False, indent=2) + '\n')
        if பதிவு_பதிவு['name'] != பெயர் or பதிப்பு_மதிப்பு and பதிவு_பதிவு['version'] != பதிப்பு_மதிப்பு:
            raise ValueError('தொகுபதிவகம்_மூலம் பெயர்·버전 불일치')
        파일들 = சுருக்க_நீக்கம்(பதிவு_பதிவு['filename'], தரவு, பெயர், பதிவு_பதிவு['version'])
        return இடமாற்று_மூட்டை(பெயர், பதிவு_பதிவு['version'], 파일들, பதிவு_பதிவு['url'])


class மூட்டை_HTTP_வேண்டுதல்(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            HTTP_வேண்டுதல் = bytearray()
            while b'\n' not in HTTP_வேண்டுதல் and len(HTTP_வேண்டுதல்) < 100:
                조각 = 자신.request.recv(100 - len(HTTP_வேண்டுதல்))
                if not 조각:
                    return
                HTTP_வேண்டுதல்.extend(조각)
            if not HTTP_வேண்டுதல்.endswith(b'\n') or HTTP_வேண்டுதல்.count(b'\n') != 1:
                raise ValueError('잘못된 மூட்டை HTTP_வேண்டுதல்')
            பதிலளி = 자신.server.தொகுபதிவகம்_மூலம்.தயார்படுத்த(HTTP_வேண்டுதல்[:-1].decode('ascii'))
        except Exception as பிழை:
            머리 = json.dumps({'error': str(பிழை)[:500]}, ensure_ascii=False).encode()
            பதிலளி = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(பதிலளி)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, முனைய_எண்=8027, பாதை_2=None, தகவல்_தொழில்நுட்பம்_ஆஃப்லைன்=False):
        자신.சேவையகம்_மதிப்பு = socketserver.TCPServer(('127.0.0.1', முனைய_எண்), மூட்டை_HTTP_வேண்டுதல், bind_and_activate=False)
        자신.சேவையகம்_மதிப்பு.allow_reuse_address = True
        자신.சேவையகம்_மதிப்பு.server_bind()
        자신.சேவையகம்_மதிப்பு.server_activate()
        자신.சேவையகம்_மதிப்பு.தொகுபதிவகம்_மூலம் = மூட்டை_தொகுபதிவகம்(பாதை_2 or திட்டப்பணி_மூலம்/'build/pip-cache', தகவல்_தொழில்நுட்பம்_ஆஃப்லைன்)
        자신.முனைய_எண் = 자신.சேவையகம்_மதிப்பு.server_address[1]
        자신.தொடரிழை_மதிப்பு = threading.Thread(target=자신.சேவையகம்_மதிப்பு.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.தொடரிழை_மதிப்பு.start()
        return 자신

    def __exit__(자신, *செயலுருபுகள்):
        자신.சேவையகம்_மதிப்பு.shutdown()
        자신.சேவையகம்_மதிப்பு.server_close()
        자신.தொடரிழை_மதிப்பு.join(timeout=2)


def செயல்படுத்துக():
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('--port', type=int, default=8027)
    பார்சர்_48ee4b1b.add_argument('--cache', type=Path, default=திட்டப்பணி_மூலம்/'build/pip-cache')
    பார்சர்_48ee4b1b.add_argument('--offline', action='store_true')
    பார்சர்_48ee4b1b.add_argument('--fetch', help='இயக்கு_கட்டளை 없이 호환 배포 파일을 내려받아 검사·சேகரி_மதிப்பு')
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    if செயலுருபுகள்.fetch:
        தரவு = மூட்டை_தொகுபதிவகம்(செயலுருபுகள்.cache, செயலுருபுகள்.offline).தயார்படுத்த(செயலுருபுகள்.fetch)
        print('மூட்டை தயார்படுத்த 완료:', செயலுருபுகள்.fetch, len(தரவு), 'பைட்_மதிப்பு')
        return
    with 꾸러미중계(செயலுருபுகள்.port, செயலுருபுகள்.cache, செயலுருபுகள்.offline) as 중계:
        print('மூட்டை 중계: 127.0.0.1:' + str(중계.முனைய_எண்), flush=True)
        try:
            중계.தொடரிழை_மதிப்பு.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    செயல்படுத்துக()
