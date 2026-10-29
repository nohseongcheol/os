#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 स्थापणूक_मोल·실행한다."""
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

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('रास नांव 또는 नांव==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def पुनर्तपासणी_करची_पाथ(नांव, स्थापणूक_पाथ=True):
    पाथ = PurePosixPath(नांव)
    if पाथ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in नांव.split('/')):
        raise ValueError('허용하지 않는 रास पाथ: ' + नांव)
    if '\\' in नांव or any(ord(वर्ण_मोल) < 32 or ord(वर्ण_मोल) == 127 for वर्ण_मोल in नांव):
        raise ValueError('잘못된 रास पाथ 문자')
    if स्थापणूक_पाथ and (len(('/lib/' + नांव).encode()) > 63 or नांव in ('한국어.py', 'रास.py')):
        raise ValueError('रास पाथ 제한 또는 डिफॉल्ट_मोल लायब्ररी 충돌: ' + नांव)
    return नांव


def 압축풀기(फायल_प्रवेश_नांव, डेटा, नांव, वर्जन_मोल):
    파일들 = {}
    명세들 = []
    def 추가(पाथ, अनुक्रमणिका_मोल):
        पुनर्तपासणी_करची_पाथ(पाथ)
        if पाथ in 파일들:
            raise ValueError('중복 रास पाथ: ' + पाथ)
        if len(अनुक्रमणिका_मोल) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + पाथ)
        अनुक्रमणिका_मोल.decode('utf-8')
        파일들[पाथ] = अनुक्रमणिका_मोल
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 स्त्रोत_ट्री 16개·합계 64 KiB 이하여야 합니다.')
    if फायल_प्रवेश_नांव.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(डेटा)) as रास:
            항목들 = रास.infolist()
            if len(항목들) > 256 or sum(प्रवेश_मोल.file_size for प्रवेश_मोल in 항목들) > 1048576:
                raise ValueError('संग्रह_मोल रिलीज_सांठवण आवाठ 제한 초과')
            काम_सुची = [प्रवेश_मोल for प्रवेश_मोल in 항목들 if प्रवेश_मोल.filename.endswith('.dist-info/WHEEL')]
            if len(काम_सुची) != 1:
                raise ValueError('wheel काम_मोल 명세가 필요합니다.')
            काम_मोल = email.parser.Parser().parsestr(रास.read(काम_सुची[0]).decode())
            if काम_मोल.get('Root-Is-Purelib', '').lower() != 'true' or not फायल_प्रवेश_नांव.endswith('-none-any.whl'):
                raise ValueError('C विस्तार_मोल·플랫폼 전용 wheel은 지원하지 않습니다.')
            for प्रवेश_मोल in 항목들:
                पाथ = प्रवेश_मोल.filename.rstrip('/')
                पुनर्तपासणी_करची_पाथ(पाथ, False)
                if (प्रवेश_मोल.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if प्रवेश_मोल.filename.endswith('/'):
                    continue
                if '.dist-info/' in पाथ:
                    if पाथ.endswith('/METADATA'):
                        명세들.append(रास.read(प्रवेश_मोल).decode())
                    continue
                if not पाथ.endswith('.py') or '.data/' in पाथ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + पाथ)
                추가(पाथ, रास.read(प्रवेश_मोल))
    elif फायल_प्रवेश_नांव.endswith('.tar.gz') and नांव.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py पाळो_दिवचो_आदेश 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(डेटा), mode='r|gz') as रास:
            뿌리들 = set()
            प्रवेश_COUNT = 0
            전체크기 = 0
            for प्रवेश_मोल in रास:
                प्रवेश_COUNT += 1
                전체크기 += प्रवेश_मोल.size
                if प्रवेश_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('संग्रह_मोल रिलीज_सांठवण आवाठ 제한 초과')
                पुनर्तपासणी_करची_पाथ(प्रवेश_मोल.name, False)
                부분들 = प्रवेश_मोल.name.split('/')
                뿌리들.add(부분들[0])
                if प्रवेश_मोल.isdir():
                    continue
                if not प्रवेश_मोल.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython स्त्रोत_ट्री 배포형')
                पाथ = '/'.join(부분들[1:])
                अनुक्रमणिका_मोल = रास.extractfile(प्रवेश_मोल).read()
                if पाथ.endswith('PKG-INFO'):
                    명세들.append(अनुक्रमणिका_मोल.decode())
                elif पाथ.endswith('.py') and पाथ not in ('setup.py',):
                    추가(पाथ, अनुक्रमणिका_मोल)
                elif '.egg-info/' not in पाथ and not पाथ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + पाथ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 रूट_मोल 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* स्त्रोत_ट्री 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != नांव or 명세.get('Version') != वर्जन_मोल:
        raise ValueError('배포 메타데이터의 नांव·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(नामो, 한도):
    if not नामो.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(नामो, timeout=30) as जाप_दिवप:
        if not जाप_दिवप.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 नामो हालोवचें_मोल')
        डेटा = जाप_दिवप.read(한도 + 1)
    if len(डेटा) > 한도:
        raise ValueError('배포 फायल आवाठ 제한 초과')
    return डेटा


def ट्रान्सफर_रास(नांव, वर्जन_मोल, 파일들, 출처):
    명세 = {'name': नांव, 'version': वर्जन_मोल, 'source': 출처, 'files': [
        {'path': पाथ, 'size': len(डेटा), 'sha256': hashlib.sha256(डेटा).hexdigest()}
        for पाथ, डेटा in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('रास 명세 आवाठ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[प्रवेश_मोल['path']] for प्रवेश_मोल in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, पाथ, 오프라인=False):
        자신.पाथ = Path(पाथ)
        자신.पाथ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def तयार_करचें_9ce364fc(자신, 요청):
        नांव, वर्जन_मोल = 요청해석(요청)
        열쇠 = नांव + ('==' + वर्जन_मोल if वर्जन_मोल else '')
        LOG_पाथ = 자신.पाथ / (열쇠 + '.json')
        배포경로 = 자신.पाथ / (열쇠 + '.archive')
        if LOG_पाथ.is_file() and 배포경로.is_file():
            LOG_नोंद = json.loads(LOG_पाथ.read_text())
            डेटा = 배포경로.read_bytes()
            if hashlib.sha256(डेटा).hexdigest() != LOG_नोंद['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 रास: ' + 요청)
            नामो = 'https://pypi.org/pypi/' + नांव + ('/' + वर्जन_मोल if वर्जन_मोल else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(नामो, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [प्रवेश_मोल for प्रवेश_मोल in msinfo32_exe['urls'] if not प्रवेश_मोल.get('yanked') and प्रवेश_मोल['filename'].endswith('-none-any.whl')]
            if not 후보 and नांव.startswith('micropython-'):
                후보 = [प्रवेश_मोल for प्रवेश_मोल in msinfo32_exe['urls'] if not प्रवेश_मोल.get('yanked') and प्रवेश_मोल['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            निवड_मोल = 후보[0]
            डेटा = 웹읽기(निवड_मोल['url'], 4194304)
            if hashlib.sha256(डेटा).hexdigest() != निवड_मोल['digests']['sha256']:
                raise ValueError('PyPI 배포 फायल SHA-256 불일치')
            LOG_नोंद = {'name': नांव, 'version': msinfo32_exe['info']['version'], 'filename': निवड_मोल['filename'],
                    'url': निवड_मोल['url'], 'sha256': निवड_मोल['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_नोंद['filename'], डेटा, नांव, LOG_नोंद['version'])
            배포경로.write_bytes(डेटा)
            LOG_पाथ.write_text(json.dumps(LOG_नोंद, ensure_ascii=False, indent=2) + '\n')
        if LOG_नोंद['name'] != नांव or वर्जन_मोल and LOG_नोंद['version'] != वर्जन_मोल:
            raise ValueError('저장소 नांव·버전 불일치')
        파일들 = 압축풀기(LOG_नोंद['filename'], डेटा, नांव, LOG_नोंद['version'])
        return ट्रान्सफर_रास(नांव, LOG_नोंद['version'], 파일들, LOG_नोंद['url'])


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
                raise ValueError('잘못된 रास 요청')
            जाप_दिवप = 자신.server.저장소.तयार_करचें_9ce364fc(요청[:-1].decode('ascii'))
        except Exception as चूक:
            머리 = json.dumps({'error': str(चूक)[:500]}, ensure_ascii=False).encode()
            जाप_दिवप = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(जाप_दिवप)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, पाथ=None, 오프라인=False):
        자신.सर्वर_मोल = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.सर्वर_मोल.allow_reuse_address = True
        자신.सर्वर_मोल.server_bind()
        자신.सर्वर_मोल.server_activate()
        자신.सर्वर_मोल.저장소 = 꾸러미저장소(पाथ or प्रॉजॅक्ट_रूट/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.सर्वर_मोल.server_address[1]
        자신.थ्रॅड_मोल = threading.Thread(target=자신.सर्वर_मोल.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.थ्रॅड_मोल.start()
        return 자신

    def __exit__(자신, *인수):
        자신.सर्वर_मोल.shutdown()
        자신.सर्वर_मोल.server_close()
        자신.थ्रॅड_मोल.join(timeout=2)


def चलोवप():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=प्रॉजॅक्ट_रूट/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='पाळो_दिवचो_आदेश 없이 호환 배포 파일을 내려받아 검사·Store_मोल')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        डेटा = 꾸러미저장소(인수.cache, 인수.offline).तयार_करचें_9ce364fc(인수.fetch)
        print('रास तयार_करचें_9ce364fc 완료:', 인수.fetch, len(डेटा), 'बायट_मोल')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('रास 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.थ्रॅड_मोल.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    चलोवप()
