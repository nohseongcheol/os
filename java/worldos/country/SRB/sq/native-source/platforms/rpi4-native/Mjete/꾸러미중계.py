#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instaloj_VALUE·실행한다."""
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

Project_rrënjë = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('grupoj Emër 또는 Emër==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def vlerësoj_shteg(Emër, instalim_shteg=True):
    POZICIONI = PurePosixPath(Emër)
    if POZICIONI.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Emër.split('/')):
        raise ValueError('허용하지 않는 grupoj POZICIONI: ' + Emër)
    if '\\' in Emër or any(ord(karakter_VALUE) < 32 or ord(karakter_VALUE) == 127 for karakter_VALUE in Emër):
        raise ValueError('잘못된 grupoj POZICIONI 문자')
    if instalim_shteg and (len(('/lib/' + Emër).encode()) > 63 or Emër in ('한국어.py', 'grupoj.py')):
        raise ValueError('grupoj POZICIONI 제한 또는 vlerë_e_parazgjedhur bibliotekë 충돌: ' + Emër)
    return Emër


def 압축풀기(skedar_futje_emër, të_dhëna, Emër, version_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(POZICIONI, Përmbajtje_VALUE):
        vlerësoj_shteg(POZICIONI)
        if POZICIONI in 파일들:
            raise ValueError('중복 grupoj POZICIONI: ' + POZICIONI)
        if len(Përmbajtje_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + POZICIONI)
        Përmbajtje_VALUE.decode('utf-8')
        파일들[POZICIONI] = Përmbajtje_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 burim_degëzim 16개·합계 64 KiB 이하여야 합니다.')
    if skedar_futje_emër.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(të_dhëna)) as grupoj:
            항목들 = grupoj.infolist()
            if len(항목들) > 256 or sum(futje_VALUE.file_size for futje_VALUE in 항목들) > 1048576:
                raise ValueError('arkiv_VALUE liroj_hapësira_ruajtëse Madhësi 제한 초과')
            punë_Listë = [futje_VALUE for futje_VALUE in 항목들 if futje_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(punë_Listë) != 1:
                raise ValueError('wheel punë_VALUE 명세가 필요합니다.')
            punë_VALUE = email.parser.Parser().parsestr(grupoj.read(punë_Listë[0]).decode())
            if punë_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not skedar_futje_emër.endswith('-none-any.whl'):
                raise ValueError('C shtesë_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for futje_VALUE in 항목들:
                POZICIONI = futje_VALUE.filename.rstrip('/')
                vlerësoj_shteg(POZICIONI, False)
                if (futje_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if futje_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in POZICIONI:
                    if POZICIONI.endswith('/METADATA'):
                        명세들.append(grupoj.read(futje_VALUE).decode())
                    continue
                if not POZICIONI.endswith('.py') or '.data/' in POZICIONI:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + POZICIONI)
                추가(POZICIONI, grupoj.read(futje_VALUE))
    elif skedar_futje_emër.endswith('.tar.gz') and Emër.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py zbatoj_komandë 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(të_dhëna), mode='r|gz') as grupoj:
            뿌리들 = set()
            futje_COUNT = 0
            전체크기 = 0
            for futje_VALUE in grupoj:
                futje_COUNT += 1
                전체크기 += futje_VALUE.size
                if futje_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('arkiv_VALUE liroj_hapësira_ruajtëse Madhësi 제한 초과')
                vlerësoj_shteg(futje_VALUE.name, False)
                부분들 = futje_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if futje_VALUE.isdir():
                    continue
                if not futje_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython burim_degëzim 배포형')
                POZICIONI = '/'.join(부분들[1:])
                Përmbajtje_VALUE = grupoj.extractfile(futje_VALUE).read()
                if POZICIONI.endswith('PKG-INFO'):
                    명세들.append(Përmbajtje_VALUE.decode())
                elif POZICIONI.endswith('.py') and POZICIONI not in ('setup.py',):
                    추가(POZICIONI, Përmbajtje_VALUE)
                elif '.egg-info/' not in POZICIONI and not POZICIONI.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + POZICIONI)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 rrënjë_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* burim_degëzim 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Emër or 명세.get('Version') != version_VALUE:
        raise ValueError('배포 메타데이터의 Emër·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(email, 한도):
    if not email.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(email, timeout=30) as replikë:
        if not replikë.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 email lëviz_VALUE')
        të_dhëna = replikë.read(한도 + 1)
    if len(të_dhëna) > 한도:
        raise ValueError('배포 Kartelë Madhësi 제한 초과')
    return të_dhëna


def transferim_grupoj(Emër, version_VALUE, 파일들, 출처):
    명세 = {'name': Emër, 'version': version_VALUE, 'source': 출처, 'files': [
        {'path': POZICIONI, 'size': len(të_dhëna), 'sha256': hashlib.sha256(të_dhëna).hexdigest()}
        for POZICIONI, të_dhëna in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('grupoj 명세 Madhësi 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[futje_VALUE['path']] for futje_VALUE in 명세['files'])


class grupoj_depo:
    def __init__(자신, POZICIONI, teknologjia_e_informacionit_Jashtë_linje=False):
        자신.POZICIONI = Path(POZICIONI)
        자신.POZICIONI.mkdir(parents=True, exist_ok=True)
        자신.teknologjia_e_informacionit_Jashtë_linje = teknologjia_e_informacionit_Jashtë_linje

    def Përgatit(자신, 요청):
        Emër, version_VALUE = 요청해석(요청)
        열쇠 = Emër + ('==' + version_VALUE if version_VALUE else '')
        LOG_shteg = 자신.POZICIONI / (열쇠 + '.json')
        배포경로 = 자신.POZICIONI / (열쇠 + '.archive')
        if LOG_shteg.is_file() and 배포경로.is_file():
            LOG_RECORD = json.loads(LOG_shteg.read_text())
            të_dhëna = 배포경로.read_bytes()
            if hashlib.sha256(të_dhëna).hexdigest() != LOG_RECORD['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.teknologjia_e_informacionit_Jashtë_linje:
                raise ValueError('teknologjia_e_informacionit_Jashtë_linje 저장소에 없는 grupoj: ' + 요청)
            email = 'https://pypi.org/pypi/' + Emër + ('/' + version_VALUE if version_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(email, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [futje_VALUE for futje_VALUE in msinfo32_exe['urls'] if not futje_VALUE.get('yanked') and futje_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Emër.startswith('micropython-'):
                후보 = [futje_VALUE for futje_VALUE in msinfo32_exe['urls'] if not futje_VALUE.get('yanked') and futje_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            përzgjedhje_VALUE = 후보[0]
            të_dhëna = 웹읽기(përzgjedhje_VALUE['url'], 4194304)
            if hashlib.sha256(të_dhëna).hexdigest() != përzgjedhje_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Kartelë SHA-256 불일치')
            LOG_RECORD = {'name': Emër, 'version': msinfo32_exe['info']['version'], 'filename': përzgjedhje_VALUE['filename'],
                    'url': përzgjedhje_VALUE['url'], 'sha256': përzgjedhje_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_RECORD['filename'], të_dhëna, Emër, LOG_RECORD['version'])
            배포경로.write_bytes(të_dhëna)
            LOG_shteg.write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_RECORD['name'] != Emër or version_VALUE and LOG_RECORD['version'] != version_VALUE:
            raise ValueError('depo_rrënjë Emër·버전 불일치')
        파일들 = 압축풀기(LOG_RECORD['filename'], të_dhëna, Emër, LOG_RECORD['version'])
        return transferim_grupoj(Emër, LOG_RECORD['version'], 파일들, LOG_RECORD['url'])


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
                raise ValueError('잘못된 grupoj 요청')
            replikë = 자신.server.depo_rrënjë.Përgatit(요청[:-1].decode('ascii'))
        except Exception as GABIM:
            머리 = json.dumps({'error': str(GABIM)[:500]}, ensure_ascii=False).encode()
            replikë = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(replikë)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, numri_i_portës=8027, POZICIONI=None, teknologjia_e_informacionit_Jashtë_linje=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', numri_i_portës), 꾸러미요청, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.depo_rrënjë = grupoj_depo(POZICIONI or Project_rrënjë/'build/pip-cache', teknologjia_e_informacionit_Jashtë_linje)
        자신.numri_i_portës = 자신.server_VALUE.server_address[1]
        자신.thread_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.thread_VALUE.start()
        return 자신

    def __exit__(자신, *Argumente):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.thread_VALUE.join(timeout=2)


def Ekzekuto():
    analizues_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizues_48ee4b1b.add_argument('--port', type=int, default=8027)
    analizues_48ee4b1b.add_argument('--cache', type=Path, default=Project_rrënjë/'build/pip-cache')
    analizues_48ee4b1b.add_argument('--offline', action='store_true')
    analizues_48ee4b1b.add_argument('--fetch', help='zbatoj_komandë 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Argumente = analizues_48ee4b1b.parse_args()
    if Argumente.fetch:
        të_dhëna = grupoj_depo(Argumente.cache, Argumente.offline).Përgatit(Argumente.fetch)
        print('grupoj Përgatit 완료:', Argumente.fetch, len(të_dhëna), 'bajt_VALUE')
        return
    with 꾸러미중계(Argumente.port, Argumente.cache, Argumente.offline) as 중계:
        print('grupoj 중계: 127.0.0.1:' + str(중계.numri_i_portës), flush=True)
        try:
            중계.thread_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Ekzekuto()
