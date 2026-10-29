#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 इंस्टॉल_करें_मान·실행한다."""
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

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]


def पार्स_करें_अनुरोध(अनुरोध):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', अनुरोध)
    if not 맞음:
        raise ValueError('बंडल नाम 또는 नाम==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def मान्य_करें_पथ(नाम, स्थापना_पथ=True):
    पथ = PurePosixPath(नाम)
    if पथ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in नाम.split('/')):
        raise ValueError('허용하지 않는 बंडल पथ: ' + नाम)
    if '\\' in नाम or any(ord(कैरेक्टर_मान) < 32 or ord(कैरेक्टर_मान) == 127 for कैरेक्टर_मान in नाम):
        raise ValueError('잘못된 बंडल पथ 문자')
    if स्थापना_पथ and (len(('/lib/' + नाम).encode()) > 63 or नाम in ('हिंदी.py', 'बंडल.py')):
        raise ValueError('बंडल पथ 제한 또는 डिफ़ॉल्ट_मान लाइब्रेरी 충돌: ' + नाम)
    return नाम


def असंम्पिड्य(फ़ाइल_एन्ट्री_नाम, आँकड़े, नाम, संस्करण_मान):
    파일들 = {}
    명세들 = []
    def जोड़ें_एन्ट्री(पथ, सामग्री_मान):
        मान्य_करें_पथ(पथ)
        if पथ in 파일들:
            raise ValueError('중복 बंडल पथ: ' + पथ)
        if len(सामग्री_मान) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + पथ)
        सामग्री_मान.decode('utf-8')
        파일들[पथ] = सामग्री_मान
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 स्रोत_ट्री 16개·합계 64 KiB 이하여야 합니다.')
    if फ़ाइल_एन्ट्री_नाम.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(आँकड़े)) as बंडल:
            항목들 = बंडल.infolist()
            if len(항목들) > 256 or sum(एन्ट्री_मान.file_size for एन्ट्री_मान in 항목들) > 1048576:
                raise ValueError('संग्रह_मान रिलीज़_संग्रहण आकार 제한 초과')
            मामला_सूची = [एन्ट्री_मान for एन्ट्री_मान in 항목들 if एन्ट्री_मान.filename.endswith('.dist-info/WHEEL')]
            if len(मामला_सूची) != 1:
                raise ValueError('wheel मामला_मान 명세가 필요합니다.')
            मामला_मान = email.parser.Parser().parsestr(बंडल.read(मामला_सूची[0]).decode())
            if मामला_मान.get('Root-Is-Purelib', '').lower() != 'true' or not फ़ाइल_एन्ट्री_नाम.endswith('-none-any.whl'):
                raise ValueError('C एक्सटेंशन_मान·플랫폼 전용 wheel은 지원하지 않습니다.')
            for एन्ट्री_मान in 항목들:
                पथ = एन्ट्री_मान.filename.rstrip('/')
                मान्य_करें_पथ(पथ, False)
                if (एन्ट्री_मान.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if एन्ट्री_मान.filename.endswith('/'):
                    continue
                if '.dist-info/' in पथ:
                    if पथ.endswith('/METADATA'):
                        명세들.append(बंडल.read(एन्ट्री_मान).decode())
                    continue
                if not पथ.endswith('.py') or '.data/' in पथ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + पथ)
                जोड़ें_एन्ट्री(पथ, बंडल.read(एन्ट्री_मान))
    elif फ़ाइल_एन्ट्री_नाम.endswith('.tar.gz') and नाम.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py निष्पादित_करें_आदेश 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(आँकड़े), mode='r|gz') as बंडल:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for एन्ट्री_मान in बंडल:
                항목수 += 1
                전체크기 += एन्ट्री_मान.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('संग्रह_मान रिलीज़_संग्रहण आकार 제한 초과')
                मान्य_करें_पथ(एन्ट्री_मान.name, False)
                부분들 = एन्ट्री_मान.name.split('/')
                뿌리들.add(부분들[0])
                if एन्ट्री_मान.isdir():
                    continue
                if not एन्ट्री_मान.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython स्रोत_ट्री 배포형')
                पथ = '/'.join(부분들[1:])
                सामग्री_मान = बंडल.extractfile(एन्ट्री_मान).read()
                if पथ.endswith('PKG-INFO'):
                    명세들.append(सामग्री_मान.decode())
                elif पथ.endswith('.py') and पथ not in ('setup.py',):
                    जोड़ें_एन्ट्री(पथ, सामग्री_मान)
                elif '.egg-info/' not in पथ and not पथ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + पथ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 मूल_मान 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* स्रोत_ट्री 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if पार्स_करें_अनुरोध(명세.get('Name', ''))[0] != नाम or 명세.get('Version') != संस्करण_मान:
        raise ValueError('배포 메타데이터의 नाम·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def पढें_वेब(पता, 한도):
    if not पता.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(पता, timeout=30) as उत्तर:
        if not उत्तर.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 पता ले_जाएँ_मान')
        आँकड़े = उत्तर.read(한도 + 1)
    if len(आँकड़े) > 한도:
        raise ValueError('배포 संचिका आकार 제한 초과')
    return आँकड़े


def हस्तांतरण_बंडल(नाम, संस्करण_मान, 파일들, 출처):
    명세 = {'name': नाम, 'version': संस्करण_मान, 'source': 출처, 'files': [
        {'path': पथ, 'size': len(आँकड़े), 'sha256': hashlib.sha256(आँकड़े).hexdigest()}
        for पथ, आँकड़े in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('बंडल 명세 आकार 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[एन्ट्री_मान['path']] for एन्ट्री_मान in 명세['files'])


class बंडल_संग्रह:
    def __init__(자신, पथ, सूचना_प्रौद्योगिकी_ऑफलाइन=False):
        자신.पथ = Path(पथ)
        자신.पथ.mkdir(parents=True, exist_ok=True)
        자신.सूचना_प्रौद्योगिकी_ऑफलाइन = सूचना_प्रौद्योगिकी_ऑफलाइन

    def 준비(자신, अनुरोध):
        नाम, संस्करण_मान = पार्स_करें_अनुरोध(अनुरोध)
        열쇠 = नाम + ('==' + संस्करण_मान if संस्करण_मान else '')
        लॉग_पथ = 자신.पथ / (열쇠 + '.json')
        배포경로 = 자신.पथ / (열쇠 + '.archive')
        if लॉग_पथ.is_file() and 배포경로.is_file():
            लॉग_रिकॉर्ड = json.loads(लॉग_पथ.read_text())
            आँकड़े = 배포경로.read_bytes()
            if hashlib.sha256(आँकड़े).hexdigest() != लॉग_रिकॉर्ड['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.सूचना_प्रौद्योगिकी_ऑफलाइन:
                raise ValueError('सूचना_प्रौद्योगिकी_ऑफलाइन 저장소에 없는 बंडल: ' + अनुरोध)
            पता = 'https://pypi.org/pypi/' + नाम + ('/' + संस्करण_मान if संस्करण_मान else '') + '/json'
            सिस्टम_जानकारी = json.loads(पढें_वेब(पता, 4194304).decode())
            if सिस्टम_जानकारी['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [एन्ट्री_मान for एन्ट्री_मान in सिस्टम_जानकारी['urls'] if not एन्ट्री_मान.get('yanked') and एन्ट्री_मान['filename'].endswith('-none-any.whl')]
            if not 후보 and नाम.startswith('micropython-'):
                후보 = [एन्ट्री_मान for एन्ट्री_मान in सिस्टम_जानकारी['urls'] if not एन्ट्री_मान.get('yanked') and एन्ट्री_मान['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            चयन_मान = 후보[0]
            आँकड़े = पढें_वेब(चयन_मान['url'], 4194304)
            if hashlib.sha256(आँकड़े).hexdigest() != चयन_मान['digests']['sha256']:
                raise ValueError('PyPI 배포 संचिका SHA-256 불일치')
            लॉग_रिकॉर्ड = {'name': नाम, 'version': सिस्टम_जानकारी['info']['version'], 'filename': चयन_मान['filename'],
                    'url': चयन_मान['url'], 'sha256': चयन_मान['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            असंम्पिड्य(लॉग_रिकॉर्ड['filename'], आँकड़े, नाम, लॉग_रिकॉर्ड['version'])
            배포경로.write_bytes(आँकड़े)
            लॉग_पथ.write_text(json.dumps(लॉग_रिकॉर्ड, ensure_ascii=False, indent=2) + '\n')
        if लॉग_रिकॉर्ड['name'] != नाम or संस्करण_मान and लॉग_रिकॉर्ड['version'] != संस्करण_मान:
            raise ValueError('संग्रह_मूल नाम·버전 불일치')
        파일들 = असंम्पिड्य(लॉग_रिकॉर्ड['filename'], आँकड़े, नाम, लॉग_रिकॉर्ड['version'])
        return हस्तांतरण_बंडल(नाम, लॉग_रिकॉर्ड['version'], 파일들, लॉग_रिकॉर्ड['url'])


class बंडल_अनुरोध(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            अनुरोध = bytearray()
            while b'\n' not in अनुरोध and len(अनुरोध) < 100:
                조각 = 자신.request.recv(100 - len(अनुरोध))
                if not 조각:
                    return
                अनुरोध.extend(조각)
            if not अनुरोध.endswith(b'\n') or अनुरोध.count(b'\n') != 1:
                raise ValueError('잘못된 बंडल अनुरोध')
            उत्तर = 자신.server.संग्रह_मूल.준비(अनुरोध[:-1].decode('ascii'))
        except Exception as त्रुटि:
            머리 = json.dumps({'error': str(त्रुटि)[:500]}, ensure_ascii=False).encode()
            उत्तर = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(उत्तर)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, पोर्ट_संख्या=8027, पथ=None, सूचना_प्रौद्योगिकी_ऑफलाइन=False):
        자신.서버 = socketserver.TCPServer(('127.0.0.1', पोर्ट_संख्या), बंडल_अनुरोध, bind_and_activate=False)
        자신.서버.allow_reuse_address = True
        자신.서버.server_bind()
        자신.서버.server_activate()
        자신.서버.संग्रह_मूल = बंडल_संग्रह(पथ or प्रोजेक्ट_करें_मूल/'build/pip-cache', सूचना_प्रौद्योगिकी_ऑफलाइन)
        자신.पोर्ट_संख्या = 자신.서버.server_address[1]
        자신.थ्रेड_मान = threading.Thread(target=자신.서버.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.थ्रेड_मान.start()
        return 자신

    def __exit__(자신, *तर्क):
        자신.서버.shutdown()
        자신.서버.server_close()
        자신.थ्रेड_मान.join(timeout=2)


def चलाएँ():
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('--port', type=int, default=8027)
    पार्सर_48ee4b1b.add_argument('--cache', type=Path, default=प्रोजेक्ट_करें_मूल/'build/pip-cache')
    पार्सर_48ee4b1b.add_argument('--offline', action='store_true')
    पार्सर_48ee4b1b.add_argument('--fetch', help='निष्पादित_करें_आदेश 없이 호환 배포 파일을 내려받아 검사·स्टोर_मान')
    तर्क = पार्सर_48ee4b1b.parse_args()
    if तर्क.fetch:
        आँकड़े = बंडल_संग्रह(तर्क.cache, तर्क.offline).준비(तर्क.fetch)
        print('बंडल 준비 완료:', तर्क.fetch, len(आँकड़े), 'बाइट_मान')
        return
    with 꾸러미중계(तर्क.port, तर्क.cache, तर्क.offline) as 중계:
        print('बंडल 중계: 127.0.0.1:' + str(중계.पोर्ट_संख्या), flush=True)
        try:
            중계.थ्रेड_मान.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    चलाएँ()
