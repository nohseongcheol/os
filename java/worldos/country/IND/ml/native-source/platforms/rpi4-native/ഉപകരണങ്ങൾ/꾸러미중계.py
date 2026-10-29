#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ഇന്_സ്റ്റാള്_ചെയ്യുക_മൂല്യം·실행한다."""
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

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]


def പാര്_സ്_ചെയ്യുക_HTTP_അപേക്ഷ(HTTP_അപേക്ഷ):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', HTTP_അപേക്ഷ)
    if not 맞음:
        raise ValueError('ബണ്ടിൽ പേരു് 또는 പേരു്==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def സാധൂകരിക്കുക_പാത(പേരു്, ഇന്_സ്റ്റാള്_ചെയ്യല്_പാത=True):
    വഴി = PurePosixPath(പേരു്)
    if വഴി.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in പേരു്.split('/')):
        raise ValueError('허용하지 않는 ബണ്ടിൽ വഴി: ' + പേരു്)
    if '\\' in പേരു് or any(ord(പ്രതീകം_മൂല്യം) < 32 or ord(പ്രതീകം_മൂല്യം) == 127 for പ്രതീകം_മൂല്യം in പേരു്):
        raise ValueError('잘못된 ബണ്ടിൽ വഴി 문자')
    if ഇന്_സ്റ്റാള്_ചെയ്യല്_പാത and (len(('/lib/' + പേരു്).encode()) > 63 or പേരു് in ('한국어.py', 'ബണ്ടിൽ.py')):
        raise ValueError('ബണ്ടിൽ വഴി 제한 또는 സ്ഥിരസ്ഥിതി_മൂല്യം లైబ్రరీ 충돌: ' + പേരു്)
    return പേരു്


def മര്_ദ്ദം_കുറയ്ക്കുക(ഫയല്_എന്_ട്രി_നാ_മം, ഡാറ്റാ, പേരു്, പതിപ്പ്_മൂല്യം):
    파일들 = {}
    명세들 = []
    def 추가(വഴി, ഉള്ളടക്കം_മൂല്യം):
        സാധൂകരിക്കുക_പാത(വഴി)
        if വഴി in 파일들:
            raise ValueError('중복 ബണ്ടിൽ വഴി: ' + വഴി)
        if len(ഉള്ളടക്കം_മൂല്യം) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + വഴി)
        ഉള്ളടക്കം_മൂല്യം.decode('utf-8')
        파일들[വഴി] = ഉള്ളടക്കം_മൂല്യം
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ഉറവിടം_ശാഖി 16개·합계 64 KiB 이하여야 합니다.')
    if ഫയല്_എന്_ട്രി_നാ_മം.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ഡാറ്റാ)) as ബണ്ടിൽ:
            항목들 = ബണ്ടിൽ.infolist()
            if len(항목들) > 256 or sum(എന്_ട്രി_മൂല്യം.file_size for എന്_ട്രി_മൂല്യം in 항목들) > 1048576:
                raise ValueError('ശേഖരം_മൂല്യം റിലീസ്_സംഭരണം വലിപ്പം 제한 초과')
            കേസ്_ലിസ്റ്റ് = [എന്_ട്രി_മൂല്യം for എന്_ട്രി_മൂല്യം in 항목들 if എന്_ട്രി_മൂല്യം.filename.endswith('.dist-info/WHEEL')]
            if len(കേസ്_ലിസ്റ്റ്) != 1:
                raise ValueError('wheel കേസ്_മൂല്യം 명세가 필요합니다.')
            കേസ്_മൂല്യം = email.parser.Parser().parsestr(ബണ്ടിൽ.read(കേസ്_ലിസ്റ്റ്[0]).decode())
            if കേസ്_മൂല്യം.get('Root-Is-Purelib', '').lower() != 'true' or not ഫയല്_എന്_ട്രി_നാ_മം.endswith('-none-any.whl'):
                raise ValueError('C വിപുലീകരണം_മൂല്യം·플랫폼 전용 wheel은 지원하지 않습니다.')
            for എന്_ട്രി_മൂല്യം in 항목들:
                വഴി = എന്_ട്രി_മൂല്യം.filename.rstrip('/')
                സാധൂകരിക്കുക_പാത(വഴി, False)
                if (എന്_ട്രി_മൂല്യം.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if എന്_ട്രി_മൂല്യം.filename.endswith('/'):
                    continue
                if '.dist-info/' in വഴി:
                    if വഴി.endswith('/METADATA'):
                        명세들.append(ബണ്ടിൽ.read(എന്_ട്രി_മൂല്യം).decode())
                    continue
                if not വഴി.endswith('.py') or '.data/' in വഴി:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + വഴി)
                추가(വഴി, ബണ്ടിൽ.read(എന്_ട്രി_മൂല്യം))
    elif ഫയല്_എന്_ട്രി_നാ_മം.endswith('.tar.gz') and പേരു്.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py നടപ്പാക്കുക_കമാന്_ഡ് 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ഡാറ്റാ), mode='r|gz') as ബണ്ടിൽ:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for എന്_ട്രി_മൂല്യം in ബണ്ടിൽ:
                항목수 += 1
                전체크기 += എന്_ട്രി_മൂല്യം.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ശേഖരം_മൂല്യം റിലീസ്_സംഭരണം വലിപ്പം 제한 초과')
                സാധൂകരിക്കുക_പാത(എന്_ട്രി_മൂല്യം.name, False)
                부분들 = എന്_ട്രി_മൂല്യം.name.split('/')
                뿌리들.add(부분들[0])
                if എന്_ട്രി_മൂല്യം.isdir():
                    continue
                if not എന്_ട്രി_മൂല്യം.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ഉറവിടം_ശാഖി 배포형')
                വഴി = '/'.join(부분들[1:])
                ഉള്ളടക്കം_മൂല്യം = ബണ്ടിൽ.extractfile(എന്_ട്രി_മൂല്യം).read()
                if വഴി.endswith('PKG-INFO'):
                    명세들.append(ഉള്ളടക്കം_മൂല്യം.decode())
                elif വഴി.endswith('.py') and വഴി not in ('setup.py',):
                    추가(വഴി, ഉള്ളടക്കം_മൂല്യം)
                elif '.egg-info/' not in വഴി and not വഴി.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + വഴി)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 വർഗ്ഗമൂലം_മൂല്യം 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ഉറവിടം_ശാഖി 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if പാര്_സ്_ചെയ്യുക_HTTP_അപേക്ഷ(명세.get('Name', ''))[0] != പേരു് or 명세.get('Version') != പതിപ്പ്_മൂല്യം:
        raise ValueError('배포 메타데이터의 പേരു്·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ഇമെയിൽ, 한도):
    if not ഇമെയിൽ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ഇമെയിൽ, timeout=30) as മറുപടി_നൽകുക:
        if not മറുപടി_നൽകുക.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ഇമെയിൽ നീക്കുക_മൂല്യം')
        ഡാറ്റാ = മറുപടി_നൽകുക.read(한도 + 1)
    if len(ഡാറ്റാ) > 한도:
        raise ValueError('배포 ഫയല് വലിപ്പം 제한 초과')
    return ഡാറ്റാ


def കൈമാറുക_ബണ്ടിൽ(പേരു്, പതിപ്പ്_മൂല്യം, 파일들, 출처):
    명세 = {'name': പേരു്, 'version': പതിപ്പ്_മൂല്യം, 'source': 출처, 'files': [
        {'path': വഴി, 'size': len(ഡാറ്റാ), 'sha256': hashlib.sha256(ഡാറ്റാ).hexdigest()}
        for വഴി, ഡാറ്റാ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ബണ്ടിൽ 명세 വലിപ്പം 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[എന്_ട്രി_മൂല്യം['path']] for എന്_ട്രി_മൂല്യം in 명세['files'])


class ബണ്ടിൽ_കലവറ:
    def __init__(자신, വഴി, വിവര_സാങ്കേതികവിദ്യ_ഓഫ്_ലൈന്=False):
        자신.വഴി = Path(വഴി)
        자신.വഴി.mkdir(parents=True, exist_ok=True)
        자신.വിവര_സാങ്കേതികവിദ്യ_ഓഫ്_ലൈന് = വിവര_സാങ്കേതികവിദ്യ_ഓഫ്_ലൈന്

    def തയ്യാറാക്കുക(자신, HTTP_അപേക്ഷ):
        പേരു്, പതിപ്പ്_മൂല്യം = പാര്_സ്_ചെയ്യുക_HTTP_അപേക്ഷ(HTTP_അപേക്ഷ)
        열쇠 = പേരു് + ('==' + പതിപ്പ്_മൂല്യം if പതിപ്പ്_മൂല്യം else '')
        ലോഗ്_പാത = 자신.വഴി / (열쇠 + '.json')
        배포경로 = 자신.വഴി / (열쇠 + '.archive')
        if ലോഗ്_പാത.is_file() and 배포경로.is_file():
            ലോഗ്_രേഖ = json.loads(ലോഗ്_പാത.read_text())
            ഡാറ്റാ = 배포경로.read_bytes()
            if hashlib.sha256(ഡാറ്റാ).hexdigest() != ലോഗ്_രേഖ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.വിവര_സാങ്കേതികവിദ്യ_ഓഫ്_ലൈന്:
                raise ValueError('വിവര_സാങ്കേതികവിദ്യ_ഓഫ്_ലൈന് 저장소에 없는 ബണ്ടിൽ: ' + HTTP_അപേക്ഷ)
            ഇമെയിൽ = 'https://pypi.org/pypi/' + പേരു് + ('/' + പതിപ്പ്_മൂല്യം if പതിപ്പ്_മൂല്യം else '') + '/json'
            സിസ്റ്റം_വിവരങ്ങള് = json.loads(웹읽기(ഇമെയിൽ, 4194304).decode())
            if സിസ്റ്റം_വിവരങ്ങള്['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [എന്_ട്രി_മൂല്യം for എന്_ട്രി_മൂല്യം in സിസ്റ്റം_വിവരങ്ങള്['urls'] if not എന്_ട്രി_മൂല്യം.get('yanked') and എന്_ട്രി_മൂല്യം['filename'].endswith('-none-any.whl')]
            if not 후보 and പേരു്.startswith('micropython-'):
                후보 = [എന്_ട്രി_മൂല്യം for എന്_ട്രി_മൂല്യം in സിസ്റ്റം_വിവരങ്ങള്['urls'] if not എന്_ട്രി_മൂല്യം.get('yanked') and എന്_ട്രി_മൂല്യം['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            തിരഞ്ഞെടുക്കല്_മൂല്യം = 후보[0]
            ഡാറ്റാ = 웹읽기(തിരഞ്ഞെടുക്കല്_മൂല്യം['url'], 4194304)
            if hashlib.sha256(ഡാറ്റാ).hexdigest() != തിരഞ്ഞെടുക്കല്_മൂല്യം['digests']['sha256']:
                raise ValueError('PyPI 배포 ഫയല് SHA-256 불일치')
            ലോഗ്_രേഖ = {'name': പേരു്, 'version': സിസ്റ്റം_വിവരങ്ങള്['info']['version'], 'filename': തിരഞ്ഞെടുക്കല്_മൂല്യം['filename'],
                    'url': തിരഞ്ഞെടുക്കല്_മൂല്യം['url'], 'sha256': തിരഞ്ഞെടുക്കല്_മൂല്യം['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            മര്_ദ്ദം_കുറയ്ക്കുക(ലോഗ്_രേഖ['filename'], ഡാറ്റാ, പേരു്, ലോഗ്_രേഖ['version'])
            배포경로.write_bytes(ഡാറ്റാ)
            ലോഗ്_പാത.write_text(json.dumps(ലോഗ്_രേഖ, ensure_ascii=False, indent=2) + '\n')
        if ലോഗ്_രേഖ['name'] != പേരു് or പതിപ്പ്_മൂല്യം and ലോഗ്_രേഖ['version'] != പതിപ്പ്_മൂല്യം:
            raise ValueError('കലവറ_വർഗ്ഗമൂലം പേരു്·버전 불일치')
        파일들 = മര്_ദ്ദം_കുറയ്ക്കുക(ലോഗ്_രേഖ['filename'], ഡാറ്റാ, പേരു്, ലോഗ്_രേഖ['version'])
        return കൈമാറുക_ബണ്ടിൽ(പേരു്, ലോഗ്_രേഖ['version'], 파일들, ലോഗ്_രേഖ['url'])


class ബണ്ടിൽ_HTTP_അപേക്ഷ(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            HTTP_അപേക്ഷ = bytearray()
            while b'\n' not in HTTP_അപേക്ഷ and len(HTTP_അപേക്ഷ) < 100:
                조각 = 자신.request.recv(100 - len(HTTP_അപേക്ഷ))
                if not 조각:
                    return
                HTTP_അപേക്ഷ.extend(조각)
            if not HTTP_അപേക്ഷ.endswith(b'\n') or HTTP_അപേക്ഷ.count(b'\n') != 1:
                raise ValueError('잘못된 ബണ്ടിൽ HTTP_അപേക്ഷ')
            മറുപടി_നൽകുക = 자신.server.കലവറ_വർഗ്ഗമൂലം.തയ്യാറാക്കുക(HTTP_അപേക്ഷ[:-1].decode('ascii'))
        except Exception as പിശക്:
            머리 = json.dumps({'error': str(പിശക്)[:500]}, ensure_ascii=False).encode()
            മറുപടി_നൽകുക = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(മറുപടി_നൽകുക)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, പോര്_ട്ട്_നമ്പര്=8027, വഴി=None, വിവര_സാങ്കേതികവിദ്യ_ഓഫ്_ലൈന്=False):
        자신.സെര്_വര്_മൂല്യം = socketserver.TCPServer(('127.0.0.1', പോര്_ട്ട്_നമ്പര്), ബണ്ടിൽ_HTTP_അപേക്ഷ, bind_and_activate=False)
        자신.സെര്_വര്_മൂല്യം.allow_reuse_address = True
        자신.സെര്_വര്_മൂല്യം.server_bind()
        자신.സെര്_വര്_മൂല്യം.server_activate()
        자신.സെര്_വര്_മൂല്യം.കലവറ_വർഗ്ഗമൂലം = ബണ്ടിൽ_കലവറ(വഴി or പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/pip-cache', വിവര_സാങ്കേതികവിദ്യ_ഓഫ്_ലൈന്)
        자신.പോര്_ട്ട്_നമ്പര് = 자신.സെര്_വര്_മൂല്യം.server_address[1]
        자신.ത്രെഡ്_മൂല്യം = threading.Thread(target=자신.സെര്_വര്_മൂല്യം.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ത്രെഡ്_മൂല്യം.start()
        return 자신

    def __exit__(자신, *인수):
        자신.സെര്_വര്_മൂല്യം.shutdown()
        자신.സെര്_വര്_മൂല്യം.server_close()
        자신.ത്രെഡ്_മൂല്യം.join(timeout=2)


def നടപ്പിലാക്കുക():
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('--port', type=int, default=8027)
    പാഴ്_സർ_48ee4b1b.add_argument('--cache', type=Path, default=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/pip-cache')
    പാഴ്_സർ_48ee4b1b.add_argument('--offline', action='store_true')
    പാഴ്_സർ_48ee4b1b.add_argument('--fetch', help='നടപ്പാക്കുക_കമാന്_ഡ് 없이 호환 배포 파일을 내려받아 검사·സ്_റ്റോർ_മൂല്യം')
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    if 인수.fetch:
        ഡാറ്റാ = ബണ്ടിൽ_കലവറ(인수.cache, 인수.offline).തയ്യാറാക്കുക(인수.fetch)
        print('ബണ്ടിൽ തയ്യാറാക്കുക 완료:', 인수.fetch, len(ഡാറ്റാ), 'బైట్_മൂല്യം')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ബണ്ടിൽ 중계: 127.0.0.1:' + str(중계.പോര്_ട്ട്_നമ്പര്), flush=True)
        try:
            중계.ത്രെഡ്_മൂല്യം.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
