#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost संदेशमध्यस्थ_मूल्य. 게스트는 TCP로 받은 소스를 직접 स्थापित_करा_मूल्य·실행한다."""
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

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]


def विनंती_पार्स_करा(विनंती):
    आहे_जुळलेले = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', विनंती)
    if not आहे_जुळलेले:
        raise ValueError('बंडल नाव 또는 नाव==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', आहे_जुळलेले[1]).lower(), आहे_जुळलेले[2]


def प्रमाणित_पथ(नाव, स्थापना_पथ=True):
    मार्ग = PurePosixPath(नाव)
    if मार्ग.is_absolute() or any(उपभाग_मूल्य in ('', '.', '..') or उपभाग_मूल्य.startswith('.') for उपभाग_मूल्य in नाव.split('/')):
        raise ValueError('허용하지 않는 बंडल मार्ग: ' + नाव)
    if '\\' in नाव or any(ord(वर्ण_मूल्य) < 32 or ord(वर्ण_मूल्य) == 127 for वर्ण_मूल्य in नाव):
        raise ValueError('잘못된 बंडल मार्ग वर्ण')
    if स्थापना_पथ and (len(('/lib/' + नाव).encode()) > 63 or नाव in ('मराठी.py', 'बंडल.py')):
        raise ValueError('बंडल मार्ग मर्यादा_मूल्य 또는 डिफॉल्ट_मूल्य लायब्ररी 충돌: ' + नाव)
    return नाव


def विसंपीडनकरा(संचिका_प्रविष्टी_नाव, डेटा, नाव, आवृत्ती_मूल्य):
    संचिका_नोंदी = {}
    विनिर्देश_ce20b549 = []
    def शेवटीजोडा_प्रविष्टी(मार्ग, सामुग्री_मूल्य):
        प्रमाणित_पथ(मार्ग)
        if मार्ग in संचिका_नोंदी:
            raise ValueError('중복 बंडल मार्ग: ' + मार्ग)
        if len(सामुग्री_मूल्य) > 16384:
            raise ValueError('파일당 16 KiB मर्यादा_मूल्य 초과: ' + मार्ग)
        सामुग्री_मूल्य.decode('utf-8')
        संचिका_नोंदी[मार्ग] = सामुग्री_मूल्य
        if len(संचिका_नोंदी) > 16 or sum(map(len, संचिका_नोंदी.values())) > 65536:
            raise ValueError('꾸러미는 स्रोत_ट्री 16개·एकूण_मूल्य 64 KiB 이하여야 합니다.')
    if संचिका_प्रविष्टी_नाव.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(डेटा)) as बंडल:
            नोंदी_यादी = बंडल.infolist()
            if len(नोंदी_यादी) > 256 or sum(प्रविष्टी_मूल्य.file_size for प्रविष्टी_मूल्य in नोंदी_यादी) > 1048576:
                raise ValueError('संग्रह_मूल्य संग्रह_रिलीज आकार मर्यादा_मूल्य 초과')
            काम_यादी = [प्रविष्टी_मूल्य for प्रविष्टी_मूल्य in नोंदी_यादी if प्रविष्टी_मूल्य.filename.endswith('.dist-info/WHEEL')]
            if len(काम_यादी) != 1:
                raise ValueError('wheel काम_मूल्य 명세가 필요합니다.')
            काम_मूल्य = email.parser.Parser().parsestr(बंडल.read(काम_यादी[0]).decode())
            if काम_मूल्य.get('Root-Is-Purelib', '').lower() != 'true' or not संचिका_प्रविष्टी_नाव.endswith('-none-any.whl'):
                raise ValueError('C एक्सटेंशन_मूल्य·플랫폼 전용 wheel은 지원하지 않습니다.')
            for प्रविष्टी_मूल्य in नोंदी_यादी:
                मार्ग = प्रविष्टी_मूल्य.filename.rstrip('/')
                प्रमाणित_पथ(मार्ग, False)
                if (प्रविष्टी_मूल्य.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 संख्या 없습니다.')
                if प्रविष्टी_मूल्य.filename.endswith('/'):
                    continue
                if '.dist-info/' in मार्ग:
                    if मार्ग.endswith('/METADATA'):
                        विनिर्देश_ce20b549.append(बंडल.read(प्रविष्टी_मूल्य).decode())
                    continue
                if not मार्ग.endswith('.py') or '.data/' in मार्ग:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + मार्ग)
                शेवटीजोडा_प्रविष्टी(मार्ग, बंडल.read(प्रविष्टी_मूल्य))
    elif संचिका_प्रविष्टी_नाव.endswith('.tar.gz') and नाव.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py आज्ञा_कार्यवाही_करा 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(डेटा), mode='r|gz') as बंडल:
            मुळे_यादी = set()
            प्रविष्टी_संख्या = 0
            एकूण_आकारा = 0
            for प्रविष्टी_मूल्य in बंडल:
                प्रविष्टी_संख्या += 1
                एकूण_आकारा += प्रविष्टी_मूल्य.size
                if प्रविष्टी_संख्या > 256 or एकूण_आकारा > 1048576:
                    raise ValueError('संग्रह_मूल्य संग्रह_रिलीज आकार मर्यादा_मूल्य 초과')
                प्रमाणित_पथ(प्रविष्टी_मूल्य.name, False)
                भाग = प्रविष्टी_मूल्य.name.split('/')
                मुळे_यादी.add(भाग[0])
                if प्रविष्टी_मूल्य.isdir():
                    continue
                if not प्रविष्टी_मूल्य.isfile() or len(भाग) < 2:
                    raise ValueError('잘못된 MicroPython स्रोत_ट्री 배포형')
                मार्ग = '/'.join(भाग[1:])
                सामुग्री_मूल्य = बंडल.extractfile(प्रविष्टी_मूल्य).read()
                if मार्ग.endswith('PKG-INFO'):
                    विनिर्देश_ce20b549.append(सामुग्री_मूल्य.decode())
                elif मार्ग.endswith('.py') and मार्ग not in ('setup.py',):
                    शेवटीजोडा_प्रविष्टी(मार्ग, सामुग्री_मूल्य)
                elif '.egg-info/' not in मार्ग and not मार्ग.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + मार्ग)
            if len(मुळे_यादी) != 1:
                raise ValueError('MicroPython 소스의 मूळ_मूल्य 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* स्रोत_ट्री 배포형이 필요합니다.')
    if not संचिका_नोंदी or len(विनिर्देश_ce20b549) != 1:
        raise ValueError('소스와 वितरण_मूल्य 메타데이터가 필요합니다.')
    विनिर्देश = email.parser.Parser().parsestr(विनिर्देश_ce20b549[0])
    if विनंती_पार्स_करा(विनिर्देश.get('Name', ''))[0] != नाव or विनिर्देश.get('Version') != आवृत्ती_मूल्य:
        raise ValueError('वितरण_मूल्य 메타데이터의 नाव·버전 불일치')
    if विनिर्देश.get_all('Requires-Dist') or विनिर्देश.get_all('Requires'):
        raise ValueError('자동 अवलंबने 해결은 아직 지원하지 않습니다. अवलंबने 없는 호환 꾸러미를 사용하십시오.')
    return संचिका_नोंदी


def वेब_वाचा(पत्ता, धारणक्षमता_मर्यादा):
    if not पत्ता.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS वितरण_मूल्य 주소만 허용합니다.')
    with urllib.request.urlopen(पत्ता, timeout=30) as प्रत्युत्तर_द्या:
        if not प्रत्युत्तर_द्या.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 वितरण_मूल्य पत्ता हलवा_मूल्य')
        डेटा = प्रत्युत्तर_द्या.read(धारणक्षमता_मर्यादा + 1)
    if len(डेटा) > धारणक्षमता_मर्यादा:
        raise ValueError('वितरण_मूल्य फाइल आकार मर्यादा_मूल्य 초과')
    return डेटा


def स्थानांतर_बंडल(नाव, आवृत्ती_मूल्य, संचिका_नोंदी, उगम_मूल्य):
    विनिर्देश = {'name': नाव, 'version': आवृत्ती_मूल्य, 'source': उगम_मूल्य, 'files': [
        {'path': मार्ग, 'size': len(डेटा), 'sha256': hashlib.sha256(डेटा).hexdigest()}
        for मार्ग, डेटा in sorted(संचिका_नोंदी.items())]}
    शीर्ष_मूल्य = json.dumps(विनिर्देश, ensure_ascii=False).encode()
    if len(शीर्ष_मूल्य) > 8192:
        raise ValueError('बंडल विनिर्देश आकार 초과')
    return b'JKP1' + struct.pack('>I', len(शीर्ष_मूल्य)) + शीर्ष_मूल्य + b''.join(संचिका_नोंदी[प्रविष्टी_मूल्य['path']] for प्रविष्टी_मूल्य in विनिर्देश['files'])


class बंडल_भांडार:
    def __init__(स्वतः, मार्ग, आहे_ऑफलाइन=False):
        स्वतः.मार्ग = Path(मार्ग)
        स्वतः.मार्ग.mkdir(parents=True, exist_ok=True)
        स्वतः.आहे_ऑफलाइन = आहे_ऑफलाइन

    def तयार_करणे(स्वतः, विनंती):
        नाव, आवृत्ती_मूल्य = विनंती_पार्स_करा(विनंती)
        कळ_सामग्री = नाव + ('==' + आवृत्ती_मूल्य if आवृत्ती_मूल्य else '')
        लॉग_पथ = स्वतः.मार्ग / (कळ_सामग्री + '.json')
        वितरण_पथ = स्वतः.मार्ग / (कळ_सामग्री + '.archive')
        if लॉग_पथ.is_file() and वितरण_पथ.is_file():
            लॉग_नोंद = json.loads(लॉग_पथ.read_text())
            डेटा = वितरण_पथ.read_bytes()
            if hashlib.sha256(डेटा).hexdigest() != लॉग_नोंद['sha256']:
                raise ValueError('저장된 वितरण_मूल्य 파일의 SHA-256 불일치')
        else:
            if स्वतः.आहे_ऑफलाइन:
                raise ValueError('आहे_ऑफलाइन 저장소에 없는 बंडल: ' + विनंती)
            पत्ता = 'https://pypi.org/pypi/' + नाव + ('/' + आवृत्ती_मूल्य if आवृत्ती_मूल्य else '') + '/json'
            सिस्टम_माहिती = json.loads(वेब_वाचा(पत्ता, 4194304).decode())
            if सिस्टम_माहिती['info'].get('requires_dist'):
                raise ValueError('자동 अवलंबने 해결은 아직 지원하지 않습니다.')
            उमेदवार = [प्रविष्टी_मूल्य for प्रविष्टी_मूल्य in सिस्टम_माहिती['urls'] if not प्रविष्टी_मूल्य.get('yanked') and प्रविष्टी_मूल्य['filename'].endswith('-none-any.whl')]
            if not उमेदवार and नाव.startswith('micropython-'):
                उमेदवार = [प्रविष्टी_मूल्य for प्रविष्टी_मूल्य in सिस्टम_माहिती['urls'] if not प्रविष्टी_मूल्य.get('yanked') and प्रविष्टी_मूल्य['filename'].endswith('.tar.gz')]
            if not उमेदवार:
                raise ValueError('지원되는 순수 Python वितरण_मूल्य 파일이 없습니다.')
            निवड_मूल्य = उमेदवार[0]
            डेटा = वेब_वाचा(निवड_मूल्य['url'], 4194304)
            if hashlib.sha256(डेटा).hexdigest() != निवड_मूल्य['digests']['sha256']:
                raise ValueError('PyPI वितरण_मूल्य फाइल SHA-256 불일치')
            लॉग_नोंद = {'name': नाव, 'version': सिस्टम_माहिती['info']['version'], 'filename': निवड_मूल्य['filename'],
                    'url': निवड_मूल्य['url'], 'sha256': निवड_मूल्य['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            विसंपीडनकरा(लॉग_नोंद['filename'], डेटा, नाव, लॉग_नोंद['version'])
            वितरण_पथ.write_bytes(डेटा)
            लॉग_पथ.write_text(json.dumps(लॉग_नोंद, ensure_ascii=False, indent=2) + '\n')
        if लॉग_नोंद['name'] != नाव or आवृत्ती_मूल्य and लॉग_नोंद['version'] != आवृत्ती_मूल्य:
            raise ValueError('भांडार_मूळ नाव·버전 불일치')
        संचिका_नोंदी = विसंपीडनकरा(लॉग_नोंद['filename'], डेटा, नाव, लॉग_नोंद['version'])
        return स्थानांतर_बंडल(नाव, लॉग_नोंद['version'], संचिका_नोंदी, लॉग_नोंद['url'])


class बंडल_विनंती(socketserver.BaseRequestHandler):
    def handle(स्वतः):
        स्वतः.request.settimeout(10)
        try:
            विनंती = bytearray()
            while b'\n' not in विनंती and len(विनंती) < 100:
                तुकडा_मूल्य = स्वतः.request.recv(100 - len(विनंती))
                if not तुकडा_मूल्य:
                    return
                विनंती.extend(तुकडा_मूल्य)
            if not विनंती.endswith(b'\n') or विनंती.count(b'\n') != 1:
                raise ValueError('잘못된 बंडल विनंती')
            प्रत्युत्तर_द्या = स्वतः.server.भांडार_मूळ.तयार_करणे(विनंती[:-1].decode('ascii'))
        except Exception as त्रुटी:
            शीर्ष_मूल्य = json.dumps({'error': str(त्रुटी)[:500]}, ensure_ascii=False).encode()
            प्रत्युत्तर_द्या = b'JKP1' + struct.pack('>I', len(शीर्ष_मूल्य)) + शीर्ष_मूल्य
        try:
            स्वतः.request.sendall(प्रत्युत्तर_द्या)
        except OSError:
            pass


class बंडल_संदेशमध्यस्थ:
    def __init__(स्वतः, पोर्ट_नंबर=8027, मार्ग=None, आहे_ऑफलाइन=False):
        स्वतः.सर्व्हर_मूल्य = socketserver.TCPServer(('127.0.0.1', पोर्ट_नंबर), बंडल_विनंती, bind_and_activate=False)
        स्वतः.सर्व्हर_मूल्य.allow_reuse_address = True
        स्वतः.सर्व्हर_मूल्य.server_bind()
        स्वतः.सर्व्हर_मूल्य.server_activate()
        स्वतः.सर्व्हर_मूल्य.भांडार_मूळ = बंडल_भांडार(मार्ग or प्रोजेक्ट_मूळ/'build/pip-cache', आहे_ऑफलाइन)
        स्वतः.पोर्ट_नंबर = स्वतः.सर्व्हर_मूल्य.server_address[1]
        स्वतः.कार्यसूत्र_मूल्य_5b72a632 = threading.Thread(target=स्वतः.सर्व्हर_मूल्य.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(स्वतः):
        स्वतः.कार्यसूत्र_मूल्य_5b72a632.start()
        return स्वतः

    def __exit__(स्वतः, *बाबी):
        स्वतः.सर्व्हर_मूल्य.shutdown()
        स्वतः.सर्व्हर_मूल्य.server_close()
        स्वतः.कार्यसूत्र_मूल्य_5b72a632.join(timeout=2)


def सुरू_करा():
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--port', type=int, default=8027)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--cache', type=Path, default=प्रोजेक्ट_मूळ/'build/pip-cache')
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--offline', action='store_true')
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--fetch', help='आज्ञा_कार्यवाही_करा 없이 호환 वितरण_मूल्य 파일을 내려받아 पडताळण्या·साठवणे_मूल्य')
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    if बाबी.fetch:
        डेटा = बंडल_भांडार(बाबी.cache, बाबी.offline).तयार_करणे(बाबी.fetch)
        print('बंडल तयार_करणे आहे_पूर्ण:', बाबी.fetch, len(डेटा), 'बाइट_मूल्य')
        return
    with बंडल_संदेशमध्यस्थ(बाबी.port, बाबी.cache, बाबी.offline) as संदेशमध्यस्थ_मूल्य:
        print('बंडल संदेशमध्यस्थ_मूल्य: 127.0.0.1:' + str(संदेशमध्यस्थ_मूल्य.पोर्ट_नंबर), flush=True)
        try:
            संदेशमध्यस्थ_मूल्य.कार्यसूत्र_मूल्य_5b72a632.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    सुरू_करा()
