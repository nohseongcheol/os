#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 સ્થાપિત_કરો_મૂલ્ય·실행한다."""
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

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('બન્ડલ નામ 또는 નામ==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def માન્ય_કરો_પાથ(નામ, સ્થાપના_પાથ=True):
    પથ = PurePosixPath(નામ)
    if પથ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in નામ.split('/')):
        raise ValueError('허용하지 않는 બન્ડલ પથ: ' + નામ)
    if '\\' in નામ or any(ord(વર્ણ_મૂલ્ય) < 32 or ord(વર્ણ_મૂલ્ય) == 127 for વર્ણ_મૂલ્ય in નામ):
        raise ValueError('잘못된 બન્ડલ પથ 문자')
    if સ્થાપના_પાથ and (len(('/lib/' + નામ).encode()) > 63 or નામ in ('ગુજરાતી.py', 'બન્ડલ.py')):
        raise ValueError('બન્ડલ પથ 제한 또는 ડિફૉલ્ટ_મૂલ્ય લાઇબ્રેરી 충돌: ' + નામ)
    return નામ


def 압축풀기(ફાઇલ_પ્રવેશ_નામ, ડેટા, નામ, વર્ઝન_મૂલ્ય):
    파일들 = {}
    명세들 = []
    def 추가(પથ, સામગ્રી_મૂલ્ય):
        માન્ય_કરો_પાથ(પથ)
        if પથ in 파일들:
            raise ValueError('중복 બન્ડલ પથ: ' + પથ)
        if len(સામગ્રી_મૂલ્ય) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + પથ)
        સામગ્રી_મૂલ્ય.decode('utf-8')
        파일들[પથ] = સામગ્રી_મૂલ્ય
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 સ્રોત_ટ્રી 16개·합계 64 KiB 이하여야 합니다.')
    if ફાઇલ_પ્રવેશ_નામ.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ડેટા)) as બન્ડલ:
            항목들 = બન્ડલ.infolist()
            if len(항목들) > 256 or sum(પ્રવેશ_મૂલ્ય.file_size for પ્રવેશ_મૂલ્ય in 항목들) > 1048576:
                raise ValueError('સંગ્રહ_મૂલ્ય રિલીઝ_સંગ્રહ માપ 제한 초과')
            કામ_સૂચી = [પ્રવેશ_મૂલ્ય for પ્રવેશ_મૂલ્ય in 항목들 if પ્રવેશ_મૂલ્ય.filename.endswith('.dist-info/WHEEL')]
            if len(કામ_સૂચી) != 1:
                raise ValueError('wheel કામ_મૂલ્ય 명세가 필요합니다.')
            કામ_મૂલ્ય = email.parser.Parser().parsestr(બન્ડલ.read(કામ_સૂચી[0]).decode())
            if કામ_મૂલ્ય.get('Root-Is-Purelib', '').lower() != 'true' or not ફાઇલ_પ્રવેશ_નામ.endswith('-none-any.whl'):
                raise ValueError('C એક્સ્ટેંશન_મૂલ્ય·플랫폼 전용 wheel은 지원하지 않습니다.')
            for પ્રવેશ_મૂલ્ય in 항목들:
                પથ = પ્રવેશ_મૂલ્ય.filename.rstrip('/')
                માન્ય_કરો_પાથ(પથ, False)
                if (પ્રવેશ_મૂલ્ય.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if પ્રવેશ_મૂલ્ય.filename.endswith('/'):
                    continue
                if '.dist-info/' in પથ:
                    if પથ.endswith('/METADATA'):
                        명세들.append(બન્ડલ.read(પ્રવેશ_મૂલ્ય).decode())
                    continue
                if not પથ.endswith('.py') or '.data/' in પથ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + પથ)
                추가(પથ, બન્ડલ.read(પ્રવેશ_મૂલ્ય))
    elif ફાઇલ_પ્રવેશ_નામ.endswith('.tar.gz') and નામ.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py અમલ_કરો_આદેશ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ડેટા), mode='r|gz') as બન્ડલ:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for પ્રવેશ_મૂલ્ય in બન્ડલ:
                항목수 += 1
                전체크기 += પ્રવેશ_મૂલ્ય.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('સંગ્રહ_મૂલ્ય રિલીઝ_સંગ્રહ માપ 제한 초과')
                માન્ય_કરો_પાથ(પ્રવેશ_મૂલ્ય.name, False)
                부분들 = પ્રવેશ_મૂલ્ય.name.split('/')
                뿌리들.add(부분들[0])
                if પ્રવેશ_મૂલ્ય.isdir():
                    continue
                if not પ્રવેશ_મૂલ્ય.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython સ્રોત_ટ્રી 배포형')
                પથ = '/'.join(부분들[1:])
                સામગ્રી_મૂલ્ય = બન્ડલ.extractfile(પ્રવેશ_મૂલ્ય).read()
                if પથ.endswith('PKG-INFO'):
                    명세들.append(સામગ્રી_મૂલ્ય.decode())
                elif પથ.endswith('.py') and પથ not in ('setup.py',):
                    추가(પથ, સામગ્રી_મૂલ્ય)
                elif '.egg-info/' not in પથ and not પથ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + પથ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 રૂટ_મૂલ્ય 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* સ્રોત_ટ્રી 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != નામ or 명세.get('Version') != વર્ઝન_મૂલ્ય:
        raise ValueError('배포 메타데이터의 નામ·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(સરનામું, 한도):
    if not સરનામું.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(સરનામું, timeout=30) as જવાબ:
        if not જવાબ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 સરનામું ખસેડવું_મૂલ્ય')
        ડેટા = જવાબ.read(한도 + 1)
    if len(ડેટા) > 한도:
        raise ValueError('배포 ફાઈલ માપ 제한 초과')
    return ડેટા


def સ્થાનાંતર_બન્ડલ(નામ, વર્ઝન_મૂલ્ય, 파일들, 출처):
    명세 = {'name': નામ, 'version': વર્ઝન_મૂલ્ય, 'source': 출처, 'files': [
        {'path': પથ, 'size': len(ડેટા), 'sha256': hashlib.sha256(ડેટા).hexdigest()}
        for પથ, ડેટા in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('બન્ડલ 명세 માપ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[પ્રવેશ_મૂલ્ય['path']] for પ્રવેશ_મૂલ્ય in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, પથ, ઇન્ટરમિટેંટ_ઑફલાઇન=False):
        자신.પથ = Path(પથ)
        자신.પથ.mkdir(parents=True, exist_ok=True)
        자신.ઇન્ટરમિટેંટ_ઑફલાઇન = ઇન્ટરમિટેંટ_ઑફલાઇન

    def તૈયાર_કરો(자신, 요청):
        નામ, વર્ઝન_મૂલ્ય = 요청해석(요청)
        열쇠 = નામ + ('==' + વર્ઝન_મૂલ્ય if વર્ઝન_મૂલ્ય else '')
        લૉગ_પાથ = 자신.પથ / (열쇠 + '.json')
        배포경로 = 자신.પથ / (열쇠 + '.archive')
        if લૉગ_પાથ.is_file() and 배포경로.is_file():
            લૉગ_પંક્તિ = json.loads(લૉગ_પાથ.read_text())
            ડેટા = 배포경로.read_bytes()
            if hashlib.sha256(ડેટા).hexdigest() != લૉગ_પંક્તિ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.ઇન્ટરમિટેંટ_ઑફલાઇન:
                raise ValueError('ઇન્ટરમિટેંટ_ઑફલાઇન 저장소에 없는 બન્ડલ: ' + 요청)
            સરનામું = 'https://pypi.org/pypi/' + નામ + ('/' + વર્ઝન_મૂલ્ય if વર્ઝન_મૂલ્ય else '') + '/json'
            સિસ્ટમ_માહિતી = json.loads(웹읽기(સરનામું, 4194304).decode())
            if સિસ્ટમ_માહિતી['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [પ્રવેશ_મૂલ્ય for પ્રવેશ_મૂલ્ય in સિસ્ટમ_માહિતી['urls'] if not પ્રવેશ_મૂલ્ય.get('yanked') and પ્રવેશ_મૂલ્ય['filename'].endswith('-none-any.whl')]
            if not 후보 and નામ.startswith('micropython-'):
                후보 = [પ્રવેશ_મૂલ્ય for પ્રવેશ_મૂલ્ય in સિસ્ટમ_માહિતી['urls'] if not પ્રવેશ_મૂલ્ય.get('yanked') and પ્રવેશ_મૂલ્ય['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ચયન_મૂલ્ય = 후보[0]
            ડેટા = 웹읽기(ચયન_મૂલ્ય['url'], 4194304)
            if hashlib.sha256(ડેટા).hexdigest() != ચયન_મૂલ્ય['digests']['sha256']:
                raise ValueError('PyPI 배포 ફાઈલ SHA-256 불일치')
            લૉગ_પંક્તિ = {'name': નામ, 'version': સિસ્ટમ_માહિતી['info']['version'], 'filename': ચયન_મૂલ્ય['filename'],
                    'url': ચયન_મૂલ્ય['url'], 'sha256': ચયન_મૂલ્ય['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(લૉગ_પંક્તિ['filename'], ડેટા, નામ, લૉગ_પંક્તિ['version'])
            배포경로.write_bytes(ડેટા)
            લૉગ_પાથ.write_text(json.dumps(લૉગ_પંક્તિ, ensure_ascii=False, indent=2) + '\n')
        if લૉગ_પંક્તિ['name'] != નામ or વર્ઝન_મૂલ્ય and લૉગ_પંક્તિ['version'] != વર્ઝન_મૂલ્ય:
            raise ValueError('저장소 નામ·버전 불일치')
        파일들 = 압축풀기(લૉગ_પંક્તિ['filename'], ડેટા, નામ, લૉગ_પંક્તિ['version'])
        return સ્થાનાંતર_બન્ડલ(નામ, લૉગ_પંક્તિ['version'], 파일들, લૉગ_પંક્તિ['url'])


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
                raise ValueError('잘못된 બન્ડલ 요청')
            જવાબ = 자신.server.저장소.તૈયાર_કરો(요청[:-1].decode('ascii'))
        except Exception as ભૂલ:
            머리 = json.dumps({'error': str(ભૂલ)[:500]}, ensure_ascii=False).encode()
            જવાબ = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(જવાબ)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, પોર્ટ_નંબર=8027, પથ=None, ઇન્ટરમિટેંટ_ઑફલાઇન=False):
        자신.સર્વર_મૂલ્ય = socketserver.TCPServer(('127.0.0.1', પોર્ટ_નંબર), 꾸러미요청, bind_and_activate=False)
        자신.સર્વર_મૂલ્ય.allow_reuse_address = True
        자신.સર્વર_મૂલ્ય.server_bind()
        자신.સર્વર_મૂલ્ય.server_activate()
        자신.સર્વર_મૂલ્ય.저장소 = 꾸러미저장소(પથ or પ્રોજેક્ટ_રૂટ/'build/pip-cache', ઇન્ટરમિટેંટ_ઑફલાઇન)
        자신.પોર્ટ_નંબર = 자신.સર્વર_મૂલ્ય.server_address[1]
        자신.થ્રેડ_મૂલ્ય = threading.Thread(target=자신.સર્વર_મૂલ્ય.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.થ્રેડ_મૂલ્ય.start()
        return 자신

    def __exit__(자신, *દલીલો):
        자신.સર્વર_મૂલ્ય.shutdown()
        자신.સર્વર_મૂલ્ય.server_close()
        자신.થ્રેડ_મૂલ્ય.join(timeout=2)


def ચલાવો_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=પ્રોજેક્ટ_રૂટ/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='અમલ_કરો_આદેશ 없이 호환 배포 파일을 내려받아 검사·સંગ્રહ_કરવો_મૂલ્ય')
    દલીલો = 해석기.parse_args()
    if દલીલો.fetch:
        ડેટા = 꾸러미저장소(દલીલો.cache, દલીલો.offline).તૈયાર_કરો(દલીલો.fetch)
        print('બન્ડલ તૈયાર_કરો 완료:', દલીલો.fetch, len(ડેટા), 'બાઇટ_મૂલ્ય')
        return
    with 꾸러미중계(દલીલો.port, દલીલો.cache, દલીલો.offline) as 중계:
        print('બન્ડલ 중계: 127.0.0.1:' + str(중계.પોર્ટ_નંબર), flush=True)
        try:
            중계.થ્રેડ_મૂલ્ય.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ચલાવો_2()
