#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installéieren_VALUE·실행한다."""
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

projezéieren_Racinn = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('Bëndel Numm 또는 Numm==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def validéieren_Wee(Numm, Installatioun_Wee=True):
    Wee = PurePosixPath(Numm)
    if Wee.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Numm.split('/')):
        raise ValueError('허용하지 않는 Bëndel Wee: ' + Numm)
    if '\\' in Numm or any(ord(Zeechen_VALUE) < 32 or ord(Zeechen_VALUE) == 127 for Zeechen_VALUE in Numm):
        raise ValueError('잘못된 Bëndel Wee 문자')
    if Installatioun_Wee and (len(('/lib/' + Numm).encode()) > 63 or Numm in ('한국어.py', 'Bëndel.py')):
        raise ValueError('Bëndel Wee 제한 또는 Standardwäert Bibliothéik 충돌: ' + Numm)
    return Numm


def 압축풀기(Fichier_Agab_Numm, Daten, Numm, Versioun_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(Wee, Inhalt_VALUE):
        validéieren_Wee(Wee)
        if Wee in 파일들:
            raise ValueError('중복 Bëndel Wee: ' + Wee)
        if len(Inhalt_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Wee)
        Inhalt_VALUE.decode('utf-8')
        파일들[Wee] = Inhalt_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 Quell_Bamstruktur 16개·합계 64 KiB 이하여야 합니다.')
    if Fichier_Agab_Numm.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(Daten)) as Bëndel:
            항목들 = Bëndel.infolist()
            if len(항목들) > 256 or sum(Agab_VALUE.file_size for Agab_VALUE in 항목들) > 1048576:
                raise ValueError('Archiv_VALUE Versioun_Späicher d_Gréisst_veränneren 제한 초과')
            Job_Lëscht = [Agab_VALUE for Agab_VALUE in 항목들 if Agab_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(Job_Lëscht) != 1:
                raise ValueError('wheel Job_VALUE 명세가 필요합니다.')
            Job_VALUE = email.parser.Parser().parsestr(Bëndel.read(Job_Lëscht[0]).decode())
            if Job_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not Fichier_Agab_Numm.endswith('-none-any.whl'):
                raise ValueError('C Extensioun_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for Agab_VALUE in 항목들:
                Wee = Agab_VALUE.filename.rstrip('/')
                validéieren_Wee(Wee, False)
                if (Agab_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if Agab_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in Wee:
                    if Wee.endswith('/METADATA'):
                        명세들.append(Bëndel.read(Agab_VALUE).decode())
                    continue
                if not Wee.endswith('.py') or '.data/' in Wee:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Wee)
                추가(Wee, Bëndel.read(Agab_VALUE))
    elif Fichier_Agab_Numm.endswith('.tar.gz') and Numm.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ausféieren_Befeel 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(Daten), mode='r|gz') as Bëndel:
            뿌리들 = set()
            Agab_COUNT = 0
            전체크기 = 0
            for Agab_VALUE in Bëndel:
                Agab_COUNT += 1
                전체크기 += Agab_VALUE.size
                if Agab_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Archiv_VALUE Versioun_Späicher d_Gréisst_veränneren 제한 초과')
                validéieren_Wee(Agab_VALUE.name, False)
                부분들 = Agab_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if Agab_VALUE.isdir():
                    continue
                if not Agab_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython Quell_Bamstruktur 배포형')
                Wee = '/'.join(부분들[1:])
                Inhalt_VALUE = Bëndel.extractfile(Agab_VALUE).read()
                if Wee.endswith('PKG-INFO'):
                    명세들.append(Inhalt_VALUE.decode())
                elif Wee.endswith('.py') and Wee not in ('setup.py',):
                    추가(Wee, Inhalt_VALUE)
                elif '.egg-info/' not in Wee and not Wee.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Wee)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 Racinn_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* Quell_Bamstruktur 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Numm or 명세.get('Version') != Versioun_VALUE:
        raise ValueError('배포 메타데이터의 Numm·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(Adress, 한도):
    if not Adress.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(Adress, timeout=30) as äntweren:
        if not äntweren.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 Adress verréckelen_VALUE')
        Daten = äntweren.read(한도 + 1)
    if len(Daten) > 한도:
        raise ValueError('배포 Fichier d_Gréisst_veränneren 제한 초과')
    return Daten


def Transfer_Bëndel(Numm, Versioun_VALUE, 파일들, 출처):
    명세 = {'name': Numm, 'version': Versioun_VALUE, 'source': 출처, 'files': [
        {'path': Wee, 'size': len(Daten), 'sha256': hashlib.sha256(Daten).hexdigest()}
        for Wee, Daten in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('Bëndel 명세 d_Gréisst_veränneren 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[Agab_VALUE['path']] for Agab_VALUE in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Wee, 오프라인=False):
        자신.Wee = Path(Wee)
        자신.Wee.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Préparéieren(자신, 요청):
        Numm, Versioun_VALUE = 요청해석(요청)
        열쇠 = Numm + ('==' + Versioun_VALUE if Versioun_VALUE else '')
        LOG_Wee = 자신.Wee / (열쇠 + '.json')
        배포경로 = 자신.Wee / (열쇠 + '.archive')
        if LOG_Wee.is_file() and 배포경로.is_file():
            LOG_Rei = json.loads(LOG_Wee.read_text())
            Daten = 배포경로.read_bytes()
            if hashlib.sha256(Daten).hexdigest() != LOG_Rei['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 Bëndel: ' + 요청)
            Adress = 'https://pypi.org/pypi/' + Numm + ('/' + Versioun_VALUE if Versioun_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(Adress, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [Agab_VALUE for Agab_VALUE in msinfo32_exe['urls'] if not Agab_VALUE.get('yanked') and Agab_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Numm.startswith('micropython-'):
                후보 = [Agab_VALUE for Agab_VALUE in msinfo32_exe['urls'] if not Agab_VALUE.get('yanked') and Agab_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            Auswiel_VALUE = 후보[0]
            Daten = 웹읽기(Auswiel_VALUE['url'], 4194304)
            if hashlib.sha256(Daten).hexdigest() != Auswiel_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Fichier SHA-256 불일치')
            LOG_Rei = {'name': Numm, 'version': msinfo32_exe['info']['version'], 'filename': Auswiel_VALUE['filename'],
                    'url': Auswiel_VALUE['url'], 'sha256': Auswiel_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_Rei['filename'], Daten, Numm, LOG_Rei['version'])
            배포경로.write_bytes(Daten)
            LOG_Wee.write_text(json.dumps(LOG_Rei, ensure_ascii=False, indent=2) + '\n')
        if LOG_Rei['name'] != Numm or Versioun_VALUE and LOG_Rei['version'] != Versioun_VALUE:
            raise ValueError('저장소 Numm·버전 불일치')
        파일들 = 압축풀기(LOG_Rei['filename'], Daten, Numm, LOG_Rei['version'])
        return Transfer_Bëndel(Numm, LOG_Rei['version'], 파일들, LOG_Rei['url'])


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
                raise ValueError('잘못된 Bëndel 요청')
            äntweren = 자신.server.저장소.Préparéieren(요청[:-1].decode('ascii'))
        except Exception as Feeler:
            머리 = json.dumps({'error': str(Feeler)[:500]}, ensure_ascii=False).encode()
            äntweren = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(äntweren)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Wee=None, 오프라인=False):
        자신.Server_VALUE = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.Server_VALUE.allow_reuse_address = True
        자신.Server_VALUE.server_bind()
        자신.Server_VALUE.server_activate()
        자신.Server_VALUE.저장소 = 꾸러미저장소(Wee or projezéieren_Racinn/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.Server_VALUE.server_address[1]
        자신.Thread_VALUE = threading.Thread(target=자신.Server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.Thread_VALUE.start()
        return 자신

    def __exit__(자신, *인수):
        자신.Server_VALUE.shutdown()
        자신.Server_VALUE.server_close()
        자신.Thread_VALUE.join(timeout=2)


def Laf():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=projezéieren_Racinn/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ausféieren_Befeel 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        Daten = 꾸러미저장소(인수.cache, 인수.offline).Préparéieren(인수.fetch)
        print('Bëndel Préparéieren 완료:', 인수.fetch, len(Daten), 'Byte_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('Bëndel 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.Thread_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Laf()
