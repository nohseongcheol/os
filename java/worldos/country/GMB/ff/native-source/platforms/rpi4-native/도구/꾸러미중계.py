#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 diiñde_njaru·실행한다."""
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
        raise ValueError('꾸러미 innde 또는 innde==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def 경로확인(innde, aafgol_laawol=True):
    laawol = PurePosixPath(innde)
    if laawol.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in innde.split('/')):
        raise ValueError('허용하지 않는 꾸러미 laawol: ' + innde)
    if '\\' in innde or any(ord(alkulal_njaru) < 32 or ord(alkulal_njaru) == 127 for alkulal_njaru in innde):
        raise ValueError('잘못된 꾸러미 laawol 문자')
    if aafgol_laawol and (len(('/lib/' + innde).encode()) > 63 or innde in ('한국어.py', '꾸러미.py')):
        raise ValueError('꾸러미 laawol 제한 또는 lasli_njaru defterdu 충돌: ' + innde)
    return innde


def 압축풀기(fiilde_naatnugol_innde, keɓe, innde, yamre_njaru):
    파일들 = {}
    명세들 = []
    def 추가(laawol, loowdi_njaru):
        경로확인(laawol)
        if laawol in 파일들:
            raise ValueError('중복 꾸러미 laawol: ' + laawol)
        if len(loowdi_njaru) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + laawol)
        loowdi_njaru.decode('utf-8')
        파일들[laawol] = loowdi_njaru
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 sewnde_lekki 16개·합계 64 KiB 이하여야 합니다.')
    if fiilde_naatnugol_innde.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(keɓe)) as 꾸러미:
            항목들 = 꾸러미.infolist()
            if len(항목들) > 256 or sum(naatnugol_njaru.file_size for naatnugol_njaru in 항목들) > 1048576:
                raise ValueError('ƴeewtirde_njaru 해제 waylude_etannde 제한 초과')
            haaju_Doggol = [naatnugol_njaru for naatnugol_njaru in 항목들 if naatnugol_njaru.filename.endswith('.dist-info/WHEEL')]
            if len(haaju_Doggol) != 1:
                raise ValueError('wheel haaju_njaru 명세가 필요합니다.')
            haaju_njaru = email.parser.Parser().parsestr(꾸러미.read(haaju_Doggol[0]).decode())
            if haaju_njaru.get('Root-Is-Purelib', '').lower() != 'true' or not fiilde_naatnugol_innde.endswith('-none-any.whl'):
                raise ValueError('C timmital_njaru·플랫폼 전용 wheel은 지원하지 않습니다.')
            for naatnugol_njaru in 항목들:
                laawol = naatnugol_njaru.filename.rstrip('/')
                경로확인(laawol, False)
                if (naatnugol_njaru.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if naatnugol_njaru.filename.endswith('/'):
                    continue
                if '.dist-info/' in laawol:
                    if laawol.endswith('/METADATA'):
                        명세들.append(꾸러미.read(naatnugol_njaru).decode())
                    continue
                if not laawol.endswith('.py') or '.data/' in laawol:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + laawol)
                추가(laawol, 꾸러미.read(naatnugol_njaru))
    elif fiilde_naatnugol_innde.endswith('.tar.gz') and innde.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py 실행 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(keɓe), mode='r|gz') as 꾸러미:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for naatnugol_njaru in 꾸러미:
                항목수 += 1
                전체크기 += naatnugol_njaru.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ƴeewtirde_njaru 해제 waylude_etannde 제한 초과')
                경로확인(naatnugol_njaru.name, False)
                부분들 = naatnugol_njaru.name.split('/')
                뿌리들.add(부분들[0])
                if naatnugol_njaru.isdir():
                    continue
                if not naatnugol_njaru.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython sewnde_lekki 배포형')
                laawol = '/'.join(부분들[1:])
                loowdi_njaru = 꾸러미.extractfile(naatnugol_njaru).read()
                if laawol.endswith('PKG-INFO'):
                    명세들.append(loowdi_njaru.decode())
                elif laawol.endswith('.py') and laawol not in ('setup.py',):
                    추가(laawol, loowdi_njaru)
                elif '.egg-info/' not in laawol and not laawol.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + laawol)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* sewnde_lekki 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != innde or 명세.get('Version') != yamre_njaru:
        raise ValueError('배포 메타데이터의 innde·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ñiiɓirde, 한도):
    if not ñiiɓirde.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ñiiɓirde, timeout=30) as 응답:
        if not 응답.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ñiiɓirde dirtinde_njaru')
        keɓe = 응답.read(한도 + 1)
    if len(keɓe) > 한도:
        raise ValueError('배포 fiilde waylude_etannde 제한 초과')
    return keɓe


def 전송묶음(innde, yamre_njaru, 파일들, 출처):
    명세 = {'name': innde, 'version': yamre_njaru, 'source': 출처, 'files': [
        {'path': laawol, 'size': len(keɓe), 'sha256': hashlib.sha256(keɓe).hexdigest()}
        for laawol, keɓe in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('꾸러미 명세 waylude_etannde 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[naatnugol_njaru['path']] for naatnugol_njaru in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, laawol, 오프라인=False):
        자신.laawol = Path(laawol)
        자신.laawol.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Heblu(자신, 요청):
        innde, yamre_njaru = 요청해석(요청)
        열쇠 = innde + ('==' + yamre_njaru if yamre_njaru else '')
        suurnal_laawol = 자신.laawol / (열쇠 + '.json')
        배포경로 = 자신.laawol / (열쇠 + '.archive')
        if suurnal_laawol.is_file() and 배포경로.is_file():
            suurnal_winndande = json.loads(suurnal_laawol.read_text())
            keɓe = 배포경로.read_bytes()
            if hashlib.sha256(keɓe).hexdigest() != suurnal_winndande['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 꾸러미: ' + 요청)
            ñiiɓirde = 'https://pypi.org/pypi/' + innde + ('/' + yamre_njaru if yamre_njaru else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ñiiɓirde, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [naatnugol_njaru for naatnugol_njaru in msinfo32_exe['urls'] if not naatnugol_njaru.get('yanked') and naatnugol_njaru['filename'].endswith('-none-any.whl')]
            if not 후보 and innde.startswith('micropython-'):
                후보 = [naatnugol_njaru for naatnugol_njaru in msinfo32_exe['urls'] if not naatnugol_njaru.get('yanked') and naatnugol_njaru['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            cuɓal_njaru = 후보[0]
            keɓe = 웹읽기(cuɓal_njaru['url'], 4194304)
            if hashlib.sha256(keɓe).hexdigest() != cuɓal_njaru['digests']['sha256']:
                raise ValueError('PyPI 배포 fiilde SHA-256 불일치')
            suurnal_winndande = {'name': innde, 'version': msinfo32_exe['info']['version'], 'filename': cuɓal_njaru['filename'],
                    'url': cuɓal_njaru['url'], 'sha256': cuɓal_njaru['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(suurnal_winndande['filename'], keɓe, innde, suurnal_winndande['version'])
            배포경로.write_bytes(keɓe)
            suurnal_laawol.write_text(json.dumps(suurnal_winndande, ensure_ascii=False, indent=2) + '\n')
        if suurnal_winndande['name'] != innde or yamre_njaru and suurnal_winndande['version'] != yamre_njaru:
            raise ValueError('저장소 innde·버전 불일치')
        파일들 = 압축풀기(suurnal_winndande['filename'], keɓe, innde, suurnal_winndande['version'])
        return 전송묶음(innde, suurnal_winndande['version'], 파일들, suurnal_winndande['url'])


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
                raise ValueError('잘못된 꾸러미 요청')
            응답 = 자신.server.저장소.Heblu(요청[:-1].decode('ascii'))
        except Exception as juumre:
            머리 = json.dumps({'error': str(juumre)[:500]}, ensure_ascii=False).encode()
            응답 = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(응답)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, laawol=None, 오프라인=False):
        자신.sarworde_njaru = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.sarworde_njaru.allow_reuse_address = True
        자신.sarworde_njaru.server_bind()
        자신.sarworde_njaru.server_activate()
        자신.sarworde_njaru.저장소 = 꾸러미저장소(laawol or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.sarworde_njaru.server_address[1]
        자신.piilol_njaru = threading.Thread(target=자신.sarworde_njaru.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.piilol_njaru.start()
        return 자신

    def __exit__(자신, *인수):
        자신.sarworde_njaru.shutdown()
        자신.sarworde_njaru.server_close()
        자신.piilol_njaru.join(timeout=2)


def huutoraade():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='실행 없이 호환 배포 파일을 내려받아 검사·resde_njaru')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        keɓe = 꾸러미저장소(인수.cache, 인수.offline).Heblu(인수.fetch)
        print('꾸러미 Heblu 완료:', 인수.fetch, len(keɓe), 'oktee_njaru')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('꾸러미 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.piilol_njaru.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    huutoraade()
