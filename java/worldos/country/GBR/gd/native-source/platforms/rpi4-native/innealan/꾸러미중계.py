#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 stàlaich_VALUE·실행한다."""
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

tilg_freumh = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('trusgan Ainm 또는 Ainm==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def dearbh_slighe(Ainm, stàladh_slighe=True):
    Slighe = PurePosixPath(Ainm)
    if Slighe.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Ainm.split('/')):
        raise ValueError('허용하지 않는 trusgan Slighe: ' + Ainm)
    if '\\' in Ainm or any(ord(caractar_VALUE) < 32 or ord(caractar_VALUE) == 127 for caractar_VALUE in Ainm):
        raise ValueError('잘못된 trusgan Slighe 문자')
    if stàladh_slighe and (len(('/lib/' + Ainm).encode()) > 63 or Ainm in ('한국어.py', 'trusgan.py')):
        raise ValueError('trusgan Slighe 제한 또는 luach_bunaiteach leabhar_lann 충돌: ' + Ainm)
    return Ainm


def 압축풀기(faidhle_cur_a_steach_ainm, dàta, Ainm, tionndadh_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(Slighe, susbaint_VALUE):
        dearbh_slighe(Slighe)
        if Slighe in 파일들:
            raise ValueError('중복 trusgan Slighe: ' + Slighe)
        if len(susbaint_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Slighe)
        susbaint_VALUE.decode('utf-8')
        파일들[Slighe] = susbaint_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 tùs_craobh 16개·합계 64 KiB 이하여야 합니다.')
    if faidhle_cur_a_steach_ainm.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(dàta)) as trusgan:
            항목들 = trusgan.infolist()
            if len(항목들) > 256 or sum(cur_a_steach_VALUE.file_size for cur_a_steach_VALUE in 항목들) > 1048576:
                raise ValueError('taisg_VALUE sgaoileadh_stòras atharraich_am_meud 제한 초과')
            cùis_Liosta = [cur_a_steach_VALUE for cur_a_steach_VALUE in 항목들 if cur_a_steach_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(cùis_Liosta) != 1:
                raise ValueError('wheel cùis_VALUE 명세가 필요합니다.')
            cùis_VALUE = email.parser.Parser().parsestr(trusgan.read(cùis_Liosta[0]).decode())
            if cùis_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not faidhle_cur_a_steach_ainm.endswith('-none-any.whl'):
                raise ValueError('C leudachan_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for cur_a_steach_VALUE in 항목들:
                Slighe = cur_a_steach_VALUE.filename.rstrip('/')
                dearbh_slighe(Slighe, False)
                if (cur_a_steach_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if cur_a_steach_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in Slighe:
                    if Slighe.endswith('/METADATA'):
                        명세들.append(trusgan.read(cur_a_steach_VALUE).decode())
                    continue
                if not Slighe.endswith('.py') or '.data/' in Slighe:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Slighe)
                추가(Slighe, trusgan.read(cur_a_steach_VALUE))
    elif faidhle_cur_a_steach_ainm.endswith('.tar.gz') and Ainm.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py gnìomhaich_àithne 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(dàta), mode='r|gz') as trusgan:
            뿌리들 = set()
            cur_a_steach_COUNT = 0
            전체크기 = 0
            for cur_a_steach_VALUE in trusgan:
                cur_a_steach_COUNT += 1
                전체크기 += cur_a_steach_VALUE.size
                if cur_a_steach_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('taisg_VALUE sgaoileadh_stòras atharraich_am_meud 제한 초과')
                dearbh_slighe(cur_a_steach_VALUE.name, False)
                부분들 = cur_a_steach_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if cur_a_steach_VALUE.isdir():
                    continue
                if not cur_a_steach_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython tùs_craobh 배포형')
                Slighe = '/'.join(부분들[1:])
                susbaint_VALUE = trusgan.extractfile(cur_a_steach_VALUE).read()
                if Slighe.endswith('PKG-INFO'):
                    명세들.append(susbaint_VALUE.decode())
                elif Slighe.endswith('.py') and Slighe not in ('setup.py',):
                    추가(Slighe, susbaint_VALUE)
                elif '.egg-info/' not in Slighe and not Slighe.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Slighe)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 freumh_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* tùs_craobh 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Ainm or 명세.get('Version') != tionndadh_VALUE:
        raise ValueError('배포 메타데이터의 Ainm·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADDRESS, 한도):
    if not ADDRESS.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ADDRESS, timeout=30) as freagair:
        if not freagair.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ADDRESS gluais_VALUE')
        dàta = freagair.read(한도 + 1)
    if len(dàta) > 한도:
        raise ValueError('배포 faidhle atharraich_am_meud 제한 초과')
    return dàta


def tar_chur_trusgan(Ainm, tionndadh_VALUE, 파일들, 출처):
    명세 = {'name': Ainm, 'version': tionndadh_VALUE, 'source': 출처, 'files': [
        {'path': Slighe, 'size': len(dàta), 'sha256': hashlib.sha256(dàta).hexdigest()}
        for Slighe, dàta in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('trusgan 명세 atharraich_am_meud 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[cur_a_steach_VALUE['path']] for cur_a_steach_VALUE in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Slighe, 오프라인=False):
        자신.Slighe = Path(Slighe)
        자신.Slighe.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Ullaich(자신, 요청):
        Ainm, tionndadh_VALUE = 요청해석(요청)
        열쇠 = Ainm + ('==' + tionndadh_VALUE if tionndadh_VALUE else '')
        LOG_slighe = 자신.Slighe / (열쇠 + '.json')
        배포경로 = 자신.Slighe / (열쇠 + '.archive')
        if LOG_slighe.is_file() and 배포경로.is_file():
            LOG_ràgh = json.loads(LOG_slighe.read_text())
            dàta = 배포경로.read_bytes()
            if hashlib.sha256(dàta).hexdigest() != LOG_ràgh['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 trusgan: ' + 요청)
            ADDRESS = 'https://pypi.org/pypi/' + Ainm + ('/' + tionndadh_VALUE if tionndadh_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADDRESS, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [cur_a_steach_VALUE for cur_a_steach_VALUE in msinfo32_exe['urls'] if not cur_a_steach_VALUE.get('yanked') and cur_a_steach_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Ainm.startswith('micropython-'):
                후보 = [cur_a_steach_VALUE for cur_a_steach_VALUE in msinfo32_exe['urls'] if not cur_a_steach_VALUE.get('yanked') and cur_a_steach_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            taghadh_VALUE = 후보[0]
            dàta = 웹읽기(taghadh_VALUE['url'], 4194304)
            if hashlib.sha256(dàta).hexdigest() != taghadh_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 faidhle SHA-256 불일치')
            LOG_ràgh = {'name': Ainm, 'version': msinfo32_exe['info']['version'], 'filename': taghadh_VALUE['filename'],
                    'url': taghadh_VALUE['url'], 'sha256': taghadh_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_ràgh['filename'], dàta, Ainm, LOG_ràgh['version'])
            배포경로.write_bytes(dàta)
            LOG_slighe.write_text(json.dumps(LOG_ràgh, ensure_ascii=False, indent=2) + '\n')
        if LOG_ràgh['name'] != Ainm or tionndadh_VALUE and LOG_ràgh['version'] != tionndadh_VALUE:
            raise ValueError('저장소 Ainm·버전 불일치')
        파일들 = 압축풀기(LOG_ràgh['filename'], dàta, Ainm, LOG_ràgh['version'])
        return tar_chur_trusgan(Ainm, LOG_ràgh['version'], 파일들, LOG_ràgh['url'])


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
                raise ValueError('잘못된 trusgan 요청')
            freagair = 자신.server.저장소.Ullaich(요청[:-1].decode('ascii'))
        except Exception as Mearachd:
            머리 = json.dumps({'error': str(Mearachd)[:500]}, ensure_ascii=False).encode()
            freagair = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(freagair)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Slighe=None, 오프라인=False):
        자신.frithealaiche_VALUE = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.frithealaiche_VALUE.allow_reuse_address = True
        자신.frithealaiche_VALUE.server_bind()
        자신.frithealaiche_VALUE.server_activate()
        자신.frithealaiche_VALUE.저장소 = 꾸러미저장소(Slighe or tilg_freumh/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.frithealaiche_VALUE.server_address[1]
        자신.snàithlean_VALUE = threading.Thread(target=자신.frithealaiche_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.snàithlean_VALUE.start()
        return 자신

    def __exit__(자신, *인수):
        자신.frithealaiche_VALUE.shutdown()
        자신.frithealaiche_VALUE.server_close()
        자신.snàithlean_VALUE.join(timeout=2)


def ruith():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=tilg_freumh/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='gnìomhaich_àithne 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        dàta = 꾸러미저장소(인수.cache, 인수.offline).Ullaich(인수.fetch)
        print('trusgan Ullaich 완료:', 인수.fetch, len(dàta), 'baidht_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('trusgan 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.snàithlean_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ruith()
