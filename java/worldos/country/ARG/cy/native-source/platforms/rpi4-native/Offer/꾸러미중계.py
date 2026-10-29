#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 gosod_VALUE·실행한다."""
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

prosiect_gwraidd = Path(__file__).resolve().parents[1]


def dosrannu_cais_HTTP(cais_HTTP):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', cais_HTTP)
    if not 맞음:
        raise ValueError('bwndel Enw 또는 Enw==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def dilysu_llwybr_f98b46e1(Enw, gosodiad_llwybr=True):
    LLWYBR = PurePosixPath(Enw)
    if LLWYBR.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Enw.split('/')):
        raise ValueError('허용하지 않는 bwndel LLWYBR: ' + Enw)
    if '\\' in Enw or any(ord(nod_VALUE) < 32 or ord(nod_VALUE) == 127 for nod_VALUE in Enw):
        raise ValueError('잘못된 bwndel LLWYBR 문자')
    if gosodiad_llwybr and (len(('/lib/' + Enw).encode()) > 63 or Enw in ('Cymraeg.py', 'bwndel.py')):
        raise ValueError('bwndel LLWYBR 제한 또는 gwerth_diofyn llyfrgell 충돌: ' + Enw)
    return Enw


def 압축풀기(ffeil_cofnod_enw, data, Enw, fersiwn_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(LLWYBR, Cynnwys_VALUE):
        dilysu_llwybr_f98b46e1(LLWYBR)
        if LLWYBR in 파일들:
            raise ValueError('중복 bwndel LLWYBR: ' + LLWYBR)
        if len(Cynnwys_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + LLWYBR)
        Cynnwys_VALUE.decode('utf-8')
        파일들[LLWYBR] = Cynnwys_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ffynhonnell_coeden 16개·합계 64 KiB 이하여야 합니다.')
    if ffeil_cofnod_enw.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as bwndel:
            항목들 = bwndel.infolist()
            if len(항목들) > 256 or sum(cofnod_VALUE.file_size for cofnod_VALUE in 항목들) > 1048576:
                raise ValueError('Archif_VALUE rhyddhau_Storio Maint 제한 초과')
            tasg_Rhestr = [cofnod_VALUE for cofnod_VALUE in 항목들 if cofnod_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(tasg_Rhestr) != 1:
                raise ValueError('wheel tasg_VALUE 명세가 필요합니다.')
            tasg_VALUE = email.parser.Parser().parsestr(bwndel.read(tasg_Rhestr[0]).decode())
            if tasg_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not ffeil_cofnod_enw.endswith('-none-any.whl'):
                raise ValueError('C estyniad_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for cofnod_VALUE in 항목들:
                LLWYBR = cofnod_VALUE.filename.rstrip('/')
                dilysu_llwybr_f98b46e1(LLWYBR, False)
                if (cofnod_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if cofnod_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in LLWYBR:
                    if LLWYBR.endswith('/METADATA'):
                        명세들.append(bwndel.read(cofnod_VALUE).decode())
                    continue
                if not LLWYBR.endswith('.py') or '.data/' in LLWYBR:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + LLWYBR)
                추가(LLWYBR, bwndel.read(cofnod_VALUE))
    elif ffeil_cofnod_enw.endswith('.tar.gz') and Enw.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Gweithredu_gorchymyn 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as bwndel:
            뿌리들 = set()
            cofnod_COUNT = 0
            전체크기 = 0
            for cofnod_VALUE in bwndel:
                cofnod_COUNT += 1
                전체크기 += cofnod_VALUE.size
                if cofnod_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Archif_VALUE rhyddhau_Storio Maint 제한 초과')
                dilysu_llwybr_f98b46e1(cofnod_VALUE.name, False)
                부분들 = cofnod_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if cofnod_VALUE.isdir():
                    continue
                if not cofnod_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ffynhonnell_coeden 배포형')
                LLWYBR = '/'.join(부분들[1:])
                Cynnwys_VALUE = bwndel.extractfile(cofnod_VALUE).read()
                if LLWYBR.endswith('PKG-INFO'):
                    명세들.append(Cynnwys_VALUE.decode())
                elif LLWYBR.endswith('.py') and LLWYBR not in ('setup.py',):
                    추가(LLWYBR, Cynnwys_VALUE)
                elif '.egg-info/' not in LLWYBR and not LLWYBR.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + LLWYBR)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 gwraidd_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ffynhonnell_coeden 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if dosrannu_cais_HTTP(명세.get('Name', ''))[0] != Enw or 명세.get('Version') != fersiwn_VALUE:
        raise ValueError('배포 메타데이터의 Enw·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADDRESS, 한도):
    if not ADDRESS.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ADDRESS, timeout=30) as ateb:
        if not ateb.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ADDRESS symud_VALUE')
        data = ateb.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 Ffeil Maint 제한 초과')
    return data


def trosglwyddo_bwndel(Enw, fersiwn_VALUE, 파일들, 출처):
    명세 = {'name': Enw, 'version': fersiwn_VALUE, 'source': 출처, 'files': [
        {'path': LLWYBR, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for LLWYBR, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('bwndel 명세 Maint 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[cofnod_VALUE['path']] for cofnod_VALUE in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, LLWYBR, technoleg_gwybodaeth_All_lein=False):
        자신.LLWYBR = Path(LLWYBR)
        자신.LLWYBR.mkdir(parents=True, exist_ok=True)
        자신.technoleg_gwybodaeth_All_lein = technoleg_gwybodaeth_All_lein

    def Paratoi(자신, cais_HTTP):
        Enw, fersiwn_VALUE = dosrannu_cais_HTTP(cais_HTTP)
        열쇠 = Enw + ('==' + fersiwn_VALUE if fersiwn_VALUE else '')
        LOG_llwybr = 자신.LLWYBR / (열쇠 + '.json')
        배포경로 = 자신.LLWYBR / (열쇠 + '.archive')
        if LOG_llwybr.is_file() and 배포경로.is_file():
            LOG_rhes = json.loads(LOG_llwybr.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_rhes['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.technoleg_gwybodaeth_All_lein:
                raise ValueError('technoleg_gwybodaeth_All_lein 저장소에 없는 bwndel: ' + cais_HTTP)
            ADDRESS = 'https://pypi.org/pypi/' + Enw + ('/' + fersiwn_VALUE if fersiwn_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADDRESS, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [cofnod_VALUE for cofnod_VALUE in msinfo32_exe['urls'] if not cofnod_VALUE.get('yanked') and cofnod_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Enw.startswith('micropython-'):
                후보 = [cofnod_VALUE for cofnod_VALUE in msinfo32_exe['urls'] if not cofnod_VALUE.get('yanked') and cofnod_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            dewisiad_VALUE = 후보[0]
            data = 웹읽기(dewisiad_VALUE['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != dewisiad_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Ffeil SHA-256 불일치')
            LOG_rhes = {'name': Enw, 'version': msinfo32_exe['info']['version'], 'filename': dewisiad_VALUE['filename'],
                    'url': dewisiad_VALUE['url'], 'sha256': dewisiad_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_rhes['filename'], data, Enw, LOG_rhes['version'])
            배포경로.write_bytes(data)
            LOG_llwybr.write_text(json.dumps(LOG_rhes, ensure_ascii=False, indent=2) + '\n')
        if LOG_rhes['name'] != Enw or fersiwn_VALUE and LOG_rhes['version'] != fersiwn_VALUE:
            raise ValueError('저장소 Enw·버전 불일치')
        파일들 = 압축풀기(LOG_rhes['filename'], data, Enw, LOG_rhes['version'])
        return trosglwyddo_bwndel(Enw, LOG_rhes['version'], 파일들, LOG_rhes['url'])


class bwndel_cais_HTTP(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            cais_HTTP = bytearray()
            while b'\n' not in cais_HTTP and len(cais_HTTP) < 100:
                조각 = 자신.request.recv(100 - len(cais_HTTP))
                if not 조각:
                    return
                cais_HTTP.extend(조각)
            if not cais_HTTP.endswith(b'\n') or cais_HTTP.count(b'\n') != 1:
                raise ValueError('잘못된 bwndel cais_HTTP')
            ateb = 자신.server.저장소.Paratoi(cais_HTTP[:-1].decode('ascii'))
        except Exception as Gwall:
            머리 = json.dumps({'error': str(Gwall)[:500]}, ensure_ascii=False).encode()
            ateb = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ateb)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, rhif_porth=8027, LLWYBR=None, technoleg_gwybodaeth_All_lein=False):
        자신.gweinydd_VALUE = socketserver.TCPServer(('127.0.0.1', rhif_porth), bwndel_cais_HTTP, bind_and_activate=False)
        자신.gweinydd_VALUE.allow_reuse_address = True
        자신.gweinydd_VALUE.server_bind()
        자신.gweinydd_VALUE.server_activate()
        자신.gweinydd_VALUE.저장소 = 꾸러미저장소(LLWYBR or prosiect_gwraidd/'build/pip-cache', technoleg_gwybodaeth_All_lein)
        자신.rhif_porth = 자신.gweinydd_VALUE.server_address[1]
        자신.edefyn_VALUE = threading.Thread(target=자신.gweinydd_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.edefyn_VALUE.start()
        return 자신

    def __exit__(자신, *인수):
        자신.gweinydd_VALUE.shutdown()
        자신.gweinydd_VALUE.server_close()
        자신.edefyn_VALUE.join(timeout=2)


def Gweithredu_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=prosiect_gwraidd/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='Gweithredu_gorchymyn 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        data = 꾸러미저장소(인수.cache, 인수.offline).Paratoi(인수.fetch)
        print('bwndel Paratoi 완료:', 인수.fetch, len(data), 'beit_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('bwndel 중계: 127.0.0.1:' + str(중계.rhif_porth), flush=True)
        try:
            중계.edefyn_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Gweithredu_2()
