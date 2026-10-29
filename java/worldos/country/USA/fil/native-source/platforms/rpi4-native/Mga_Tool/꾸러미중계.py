#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 i_install_VALUE·실행한다."""
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

Project_root = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('bundle pangalan 또는 pangalan==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def patunayan_path(pangalan, pag_install_path=True):
    path = PurePosixPath(pangalan)
    if path.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in pangalan.split('/')):
        raise ValueError('허용하지 않는 bundle path: ' + pangalan)
    if '\\' in pangalan or any(ord(karakter_VALUE) < 32 or ord(karakter_VALUE) == 127 for karakter_VALUE in pangalan):
        raise ValueError('잘못된 bundle path 문자')
    if pag_install_path and (len(('/lib/' + pangalan).encode()) > 63 or pangalan in ('한국어.py', 'bundle.py')):
        raise ValueError('bundle path 제한 또는 value_ng_default library 충돌: ' + pangalan)
    return pangalan


def 압축풀기(file_pagpasok_pangalan, data, pangalan, bersyon_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(path, Nilalaman_VALUE):
        patunayan_path(path)
        if path in 파일들:
            raise ValueError('중복 bundle path: ' + path)
        if len(Nilalaman_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + path)
        Nilalaman_VALUE.decode('utf-8')
        파일들[path] = Nilalaman_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 pinagmulan_balangkas 16개·합계 64 KiB 이하여야 합니다.')
    if file_pagpasok_pangalan.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as bundle:
            항목들 = bundle.infolist()
            if len(항목들) > 256 or sum(pagpasok_VALUE.file_size for pagpasok_VALUE in 항목들) > 1048576:
                raise ValueError('Archive_VALUE release_Storage sukat_82232621 제한 초과')
            kaso_list = [pagpasok_VALUE for pagpasok_VALUE in 항목들 if pagpasok_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(kaso_list) != 1:
                raise ValueError('wheel kaso_VALUE 명세가 필요합니다.')
            kaso_VALUE = email.parser.Parser().parsestr(bundle.read(kaso_list[0]).decode())
            if kaso_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not file_pagpasok_pangalan.endswith('-none-any.whl'):
                raise ValueError('C extension_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for pagpasok_VALUE in 항목들:
                path = pagpasok_VALUE.filename.rstrip('/')
                patunayan_path(path, False)
                if (pagpasok_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if pagpasok_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in path:
                    if path.endswith('/METADATA'):
                        명세들.append(bundle.read(pagpasok_VALUE).decode())
                    continue
                if not path.endswith('.py') or '.data/' in path:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + path)
                추가(path, bundle.read(pagpasok_VALUE))
    elif file_pagpasok_pangalan.endswith('.tar.gz') and pangalan.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Mag_execute_utos 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as bundle:
            뿌리들 = set()
            pagpasok_COUNT = 0
            전체크기 = 0
            for pagpasok_VALUE in bundle:
                pagpasok_COUNT += 1
                전체크기 += pagpasok_VALUE.size
                if pagpasok_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Archive_VALUE release_Storage sukat_82232621 제한 초과')
                patunayan_path(pagpasok_VALUE.name, False)
                부분들 = pagpasok_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if pagpasok_VALUE.isdir():
                    continue
                if not pagpasok_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython pinagmulan_balangkas 배포형')
                path = '/'.join(부분들[1:])
                Nilalaman_VALUE = bundle.extractfile(pagpasok_VALUE).read()
                if path.endswith('PKG-INFO'):
                    명세들.append(Nilalaman_VALUE.decode())
                elif path.endswith('.py') and path not in ('setup.py',):
                    추가(path, Nilalaman_VALUE)
                elif '.egg-info/' not in path and not path.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + path)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 root_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* pinagmulan_balangkas 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != pangalan or 명세.get('Version') != bersyon_VALUE:
        raise ValueError('배포 메타데이터의 pangalan·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(email, 한도):
    if not email.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(email, timeout=30) as tumugon:
        if not tumugon.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 email ilipat_VALUE')
        data = tumugon.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 file sukat_82232621 제한 초과')
    return data


def lipat_bundle(pangalan, bersyon_VALUE, 파일들, 출처):
    명세 = {'name': pangalan, 'version': bersyon_VALUE, 'source': 출처, 'files': [
        {'path': path, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for path, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('bundle 명세 sukat_82232621 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[pagpasok_VALUE['path']] for pagpasok_VALUE in 명세['files'])


class bundle_repository:
    def __init__(자신, path, information_technology_Offline=False):
        자신.path = Path(path)
        자신.path.mkdir(parents=True, exist_ok=True)
        자신.information_technology_Offline = information_technology_Offline

    def Ihanda(자신, 요청):
        pangalan, bersyon_VALUE = 요청해석(요청)
        열쇠 = pangalan + ('==' + bersyon_VALUE if bersyon_VALUE else '')
        LOG_path = 자신.path / (열쇠 + '.json')
        배포경로 = 자신.path / (열쇠 + '.archive')
        if LOG_path.is_file() and 배포경로.is_file():
            LOG_hanay = json.loads(LOG_path.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_hanay['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.information_technology_Offline:
                raise ValueError('information_technology_Offline 저장소에 없는 bundle: ' + 요청)
            email = 'https://pypi.org/pypi/' + pangalan + ('/' + bersyon_VALUE if bersyon_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(email, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [pagpasok_VALUE for pagpasok_VALUE in msinfo32_exe['urls'] if not pagpasok_VALUE.get('yanked') and pagpasok_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and pangalan.startswith('micropython-'):
                후보 = [pagpasok_VALUE for pagpasok_VALUE in msinfo32_exe['urls'] if not pagpasok_VALUE.get('yanked') and pagpasok_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            seleksyon_VALUE = 후보[0]
            data = 웹읽기(seleksyon_VALUE['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != seleksyon_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 file SHA-256 불일치')
            LOG_hanay = {'name': pangalan, 'version': msinfo32_exe['info']['version'], 'filename': seleksyon_VALUE['filename'],
                    'url': seleksyon_VALUE['url'], 'sha256': seleksyon_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_hanay['filename'], data, pangalan, LOG_hanay['version'])
            배포경로.write_bytes(data)
            LOG_path.write_text(json.dumps(LOG_hanay, ensure_ascii=False, indent=2) + '\n')
        if LOG_hanay['name'] != pangalan or bersyon_VALUE and LOG_hanay['version'] != bersyon_VALUE:
            raise ValueError('repository_root pangalan·버전 불일치')
        파일들 = 압축풀기(LOG_hanay['filename'], data, pangalan, LOG_hanay['version'])
        return lipat_bundle(pangalan, LOG_hanay['version'], 파일들, LOG_hanay['url'])


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
                raise ValueError('잘못된 bundle 요청')
            tumugon = 자신.server.repository_root.Ihanda(요청[:-1].decode('ascii'))
        except Exception as error:
            머리 = json.dumps({'error': str(error)[:500]}, ensure_ascii=False).encode()
            tumugon = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(tumugon)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, numero_ng_port=8027, path=None, information_technology_Offline=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', numero_ng_port), 꾸러미요청, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.repository_root = bundle_repository(path or Project_root/'build/pip-cache', information_technology_Offline)
        자신.numero_ng_port = 자신.server_VALUE.server_address[1]
        자신.thread_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.thread_VALUE.start()
        return 자신

    def __exit__(자신, *인수):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.thread_VALUE.join(timeout=2)


def run():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=Project_root/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='Mag_execute_utos 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = parser_48ee4b1b.parse_args()
    if 인수.fetch:
        data = bundle_repository(인수.cache, 인수.offline).Ihanda(인수.fetch)
        print('bundle Ihanda 완료:', 인수.fetch, len(data), 'byte_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('bundle 중계: 127.0.0.1:' + str(중계.numero_ng_port), flush=True)
        try:
            중계.thread_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    run()
