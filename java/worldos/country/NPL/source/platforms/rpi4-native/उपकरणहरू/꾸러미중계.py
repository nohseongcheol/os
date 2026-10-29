#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 स्थापना_गर्नुहोस्_मान·실행한다."""
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

परियोजना_रूट = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('पोको नाम 또는 नाम==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def वैध_गर्नुहोस्_बाटो(नाम, स्थापना_बाटो=True):
    मार्ग = PurePosixPath(नाम)
    if मार्ग.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in नाम.split('/')):
        raise ValueError('허용하지 않는 पोको मार्ग: ' + नाम)
    if '\\' in नाम or any(ord(वर्ण_मान) < 32 or ord(वर्ण_मान) == 127 for वर्ण_मान in नाम):
        raise ValueError('잘못된 पोको मार्ग 문자')
    if स्थापना_बाटो and (len(('/lib/' + नाम).encode()) > 63 or नाम in ('नेपाली.py', 'पोको.py')):
        raise ValueError('पोको मार्ग 제한 또는 पूर्वनिर्धारित_मान पुस्तकालय 충돌: ' + नाम)
    return नाम


def 압축풀기(फाइल_प्रविष्टि_नाम, लगत, नाम, संस्करण_मान):
    파일들 = {}
    명세들 = []
    def 추가(मार्ग, सामग्री_मान):
        वैध_गर्नुहोस्_बाटो(मार्ग)
        if मार्ग in 파일들:
            raise ValueError('중복 पोको मार्ग: ' + मार्ग)
        if len(सामग्री_मान) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + मार्ग)
        सामग्री_मान.decode('utf-8')
        파일들[मार्ग] = सामग्री_मान
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 स्रोत_वृक्ष 16개·합계 64 KiB 이하여야 합니다.')
    if फाइल_प्रविष्टि_नाम.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(लगत)) as पोको:
            항목들 = पोको.infolist()
            if len(항목들) > 256 or sum(प्रविष्टि_मान.file_size for प्रविष्टि_मान in 항목들) > 1048576:
                raise ValueError('सङ्ग्रह_मान जारी_भण्डारण आकार 제한 초과')
            केस_सूची = [प्रविष्टि_मान for प्रविष्टि_मान in 항목들 if प्रविष्टि_मान.filename.endswith('.dist-info/WHEEL')]
            if len(केस_सूची) != 1:
                raise ValueError('wheel केस_मान 명세가 필요합니다.')
            केस_मान = email.parser.Parser().parsestr(पोको.read(केस_सूची[0]).decode())
            if केस_मान.get('Root-Is-Purelib', '').lower() != 'true' or not फाइल_प्रविष्टि_नाम.endswith('-none-any.whl'):
                raise ValueError('C विस्तार_मान·플랫폼 전용 wheel은 지원하지 않습니다.')
            for प्रविष्टि_मान in 항목들:
                मार्ग = प्रविष्टि_मान.filename.rstrip('/')
                वैध_गर्नुहोस्_बाटो(मार्ग, False)
                if (प्रविष्टि_मान.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if प्रविष्टि_मान.filename.endswith('/'):
                    continue
                if '.dist-info/' in मार्ग:
                    if मार्ग.endswith('/METADATA'):
                        명세들.append(पोको.read(प्रविष्टि_मान).decode())
                    continue
                if not मार्ग.endswith('.py') or '.data/' in मार्ग:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + मार्ग)
                추가(मार्ग, पोको.read(प्रविष्टि_मान))
    elif फाइल_प्रविष्टि_नाम.endswith('.tar.gz') and नाम.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py कार्यान्वयन_गर्नुहोस्_आदेश 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(लगत), mode='r|gz') as पोको:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for प्रविष्टि_मान in पोको:
                항목수 += 1
                전체크기 += प्रविष्टि_मान.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('सङ्ग्रह_मान जारी_भण्डारण आकार 제한 초과')
                वैध_गर्नुहोस्_बाटो(प्रविष्टि_मान.name, False)
                부분들 = प्रविष्टि_मान.name.split('/')
                뿌리들.add(부분들[0])
                if प्रविष्टि_मान.isdir():
                    continue
                if not प्रविष्टि_मान.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython स्रोत_वृक्ष 배포형')
                मार्ग = '/'.join(부분들[1:])
                सामग्री_मान = पोको.extractfile(प्रविष्टि_मान).read()
                if मार्ग.endswith('PKG-INFO'):
                    명세들.append(सामग्री_मान.decode())
                elif मार्ग.endswith('.py') and मार्ग not in ('setup.py',):
                    추가(मार्ग, सामग्री_मान)
                elif '.egg-info/' not in मार्ग and not मार्ग.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + मार्ग)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 रूट_मान 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* स्रोत_वृक्ष 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != नाम or 명세.get('Version') != संस्करण_मान:
        raise ValueError('배포 메타데이터의 नाम·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ठेगाना, 한도):
    if not ठेगाना.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ठेगाना, timeout=30) as जवाफ_दिनुहोस्:
        if not जवाफ_दिनुहोस्.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ठेगाना लैजानुहोस्_मान')
        लगत = जवाफ_दिनुहोस्.read(한도 + 1)
    if len(लगत) > 한도:
        raise ValueError('배포 फाइल आकार 제한 초과')
    return लगत


def ट्रान्सफर_पोको(नाम, संस्करण_मान, 파일들, 출처):
    명세 = {'name': नाम, 'version': संस्करण_मान, 'source': 출처, 'files': [
        {'path': मार्ग, 'size': len(लगत), 'sha256': hashlib.sha256(लगत).hexdigest()}
        for मार्ग, लगत in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('पोको 명세 आकार 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[प्रविष्टि_मान['path']] for प्रविष्टि_मान in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, मार्ग, 오프라인=False):
        자신.मार्ग = Path(मार्ग)
        자신.मार्ग.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def तयार_गर्नुहोस्(자신, 요청):
        नाम, संस्करण_मान = 요청해석(요청)
        열쇠 = नाम + ('==' + संस्करण_मान if संस्करण_मान else '')
        लग_बाटो = 자신.मार्ग / (열쇠 + '.json')
        배포경로 = 자신.मार्ग / (열쇠 + '.archive')
        if लग_बाटो.is_file() and 배포경로.is_file():
            लग_रेकर्ड = json.loads(लग_बाटो.read_text())
            लगत = 배포경로.read_bytes()
            if hashlib.sha256(लगत).hexdigest() != लग_रेकर्ड['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 पोको: ' + 요청)
            ठेगाना = 'https://pypi.org/pypi/' + नाम + ('/' + संस्करण_मान if संस्करण_मान else '') + '/json'
            प्रणाली_जानकारी = json.loads(웹읽기(ठेगाना, 4194304).decode())
            if प्रणाली_जानकारी['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [प्रविष्टि_मान for प्रविष्टि_मान in प्रणाली_जानकारी['urls'] if not प्रविष्टि_मान.get('yanked') and प्रविष्टि_मान['filename'].endswith('-none-any.whl')]
            if not 후보 and नाम.startswith('micropython-'):
                후보 = [प्रविष्टि_मान for प्रविष्टि_मान in प्रणाली_जानकारी['urls'] if not प्रविष्टि_मान.get('yanked') and प्रविष्टि_मान['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            चयन_मान = 후보[0]
            लगत = 웹읽기(चयन_मान['url'], 4194304)
            if hashlib.sha256(लगत).hexdigest() != चयन_मान['digests']['sha256']:
                raise ValueError('PyPI 배포 फाइल SHA-256 불일치')
            लग_रेकर्ड = {'name': नाम, 'version': प्रणाली_जानकारी['info']['version'], 'filename': चयन_मान['filename'],
                    'url': चयन_मान['url'], 'sha256': चयन_मान['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(लग_रेकर्ड['filename'], लगत, नाम, लग_रेकर्ड['version'])
            배포경로.write_bytes(लगत)
            लग_बाटो.write_text(json.dumps(लग_रेकर्ड, ensure_ascii=False, indent=2) + '\n')
        if लग_रेकर्ड['name'] != नाम or संस्करण_मान and लग_रेकर्ड['version'] != संस्करण_मान:
            raise ValueError('저장소 नाम·버전 불일치')
        파일들 = 압축풀기(लग_रेकर्ड['filename'], लगत, नाम, लग_रेकर्ड['version'])
        return ट्रान्सफर_पोको(नाम, लग_रेकर्ड['version'], 파일들, लग_रेकर्ड['url'])


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
                raise ValueError('잘못된 पोको 요청')
            जवाफ_दिनुहोस् = 자신.server.저장소.तयार_गर्नुहोस्(요청[:-1].decode('ascii'))
        except Exception as त्रुटि:
            머리 = json.dumps({'error': str(त्रुटि)[:500]}, ensure_ascii=False).encode()
            जवाफ_दिनुहोस् = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(जवाफ_दिनुहोस्)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, मार्ग=None, 오프라인=False):
        자신.सर्भर_मान = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.सर्भर_मान.allow_reuse_address = True
        자신.सर्भर_मान.server_bind()
        자신.सर्भर_मान.server_activate()
        자신.सर्भर_मान.저장소 = 꾸러미저장소(मार्ग or परियोजना_रूट/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.सर्भर_मान.server_address[1]
        자신.धागो_मान = threading.Thread(target=자신.सर्भर_मान.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.धागो_मान.start()
        return 자신

    def __exit__(자신, *तर्क):
        자신.सर्भर_मान.shutdown()
        자신.सर्भर_मान.server_close()
        자신.धागो_मान.join(timeout=2)


def चलाउनुहोस्():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=परियोजना_रूट/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='कार्यान्वयन_गर्नुहोस्_आदेश 없이 호환 배포 파일을 내려받아 검사·भण्डार_गर्नुहोस्_मान')
    तर्क = 해석기.parse_args()
    if तर्क.fetch:
        लगत = 꾸러미저장소(तर्क.cache, तर्क.offline).तयार_गर्नुहोस्(तर्क.fetch)
        print('पोको तयार_गर्नुहोस् 완료:', तर्क.fetch, len(लगत), 'बाइट_मान')
        return
    with 꾸러미중계(तर्क.port, तर्क.cache, तर्क.offline) as 중계:
        print('पोको 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.धागो_मान.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    चलाउनुहोस्()
