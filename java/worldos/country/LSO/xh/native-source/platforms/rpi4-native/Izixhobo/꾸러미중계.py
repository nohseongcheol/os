#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 fakela_ixabiso·실행한다."""
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
        raise ValueError('umqulu Igama 또는 Igama==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def qinisekisa_indlela(Igama, ufakelo_indlela=True):
    INDLELA = PurePosixPath(Igama)
    if INDLELA.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Igama.split('/')):
        raise ValueError('허용하지 않는 umqulu INDLELA: ' + Igama)
    if '\\' in Igama or any(ord(ikharakhtha_ixabiso) < 32 or ord(ikharakhtha_ixabiso) == 127 for ikharakhtha_ixabiso in Igama):
        raise ValueError('잘못된 umqulu INDLELA 문자')
    if ufakelo_indlela and (len(('/lib/' + Igama).encode()) > 63 or Igama in ('isiXhosa.py', 'umqulu.py')):
        raise ValueError('umqulu INDLELA 제한 또는 ixabiso_elisisiseko ilayibhrari 충돌: ' + Igama)
    return Igama


def 압축풀기(ifayile_ufako_nkcukacha_igama, iingcombolo, Igama, inguqulelo_ixabiso):
    파일들 = {}
    명세들 = []
    def 추가(INDLELA, Isiqulatho_ixabiso):
        qinisekisa_indlela(INDLELA)
        if INDLELA in 파일들:
            raise ValueError('중복 umqulu INDLELA: ' + INDLELA)
        if len(Isiqulatho_ixabiso) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + INDLELA)
        Isiqulatho_ixabiso.decode('utf-8')
        파일들[INDLELA] = Isiqulatho_ixabiso
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 umthombo_umthi 16개·합계 64 KiB 이하여야 합니다.')
    if ifayile_ufako_nkcukacha_igama.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(iingcombolo)) as umqulu:
            항목들 = umqulu.infolist()
            if len(항목들) > 256 or sum(ufako_nkcukacha_ixabiso.file_size for ufako_nkcukacha_ixabiso in 항목들) > 1048576:
                raise ValueError('Uvimba_ixabiso vulela_Ugcino Ubukhulu 제한 초과')
            isiganeko_uludwe = [ufako_nkcukacha_ixabiso for ufako_nkcukacha_ixabiso in 항목들 if ufako_nkcukacha_ixabiso.filename.endswith('.dist-info/WHEEL')]
            if len(isiganeko_uludwe) != 1:
                raise ValueError('wheel isiganeko_ixabiso 명세가 필요합니다.')
            isiganeko_ixabiso = email.parser.Parser().parsestr(umqulu.read(isiganeko_uludwe[0]).decode())
            if isiganeko_ixabiso.get('Root-Is-Purelib', '').lower() != 'true' or not ifayile_ufako_nkcukacha_igama.endswith('-none-any.whl'):
                raise ValueError('C isongezelelo_ixabiso·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ufako_nkcukacha_ixabiso in 항목들:
                INDLELA = ufako_nkcukacha_ixabiso.filename.rstrip('/')
                qinisekisa_indlela(INDLELA, False)
                if (ufako_nkcukacha_ixabiso.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ufako_nkcukacha_ixabiso.filename.endswith('/'):
                    continue
                if '.dist-info/' in INDLELA:
                    if INDLELA.endswith('/METADATA'):
                        명세들.append(umqulu.read(ufako_nkcukacha_ixabiso).decode())
                    continue
                if not INDLELA.endswith('.py') or '.data/' in INDLELA:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + INDLELA)
                추가(INDLELA, umqulu.read(ufako_nkcukacha_ixabiso))
    elif ifayile_ufako_nkcukacha_igama.endswith('.tar.gz') and Igama.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ukwenza_umyalelo 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(iingcombolo), mode='r|gz') as umqulu:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ufako_nkcukacha_ixabiso in umqulu:
                항목수 += 1
                전체크기 += ufako_nkcukacha_ixabiso.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Uvimba_ixabiso vulela_Ugcino Ubukhulu 제한 초과')
                qinisekisa_indlela(ufako_nkcukacha_ixabiso.name, False)
                부분들 = ufako_nkcukacha_ixabiso.name.split('/')
                뿌리들.add(부분들[0])
                if ufako_nkcukacha_ixabiso.isdir():
                    continue
                if not ufako_nkcukacha_ixabiso.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython umthombo_umthi 배포형')
                INDLELA = '/'.join(부분들[1:])
                Isiqulatho_ixabiso = umqulu.extractfile(ufako_nkcukacha_ixabiso).read()
                if INDLELA.endswith('PKG-INFO'):
                    명세들.append(Isiqulatho_ixabiso.decode())
                elif INDLELA.endswith('.py') and INDLELA not in ('setup.py',):
                    추가(INDLELA, Isiqulatho_ixabiso)
                elif '.egg-info/' not in INDLELA and not INDLELA.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + INDLELA)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* umthombo_umthi 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Igama or 명세.get('Version') != inguqulelo_ixabiso:
        raise ValueError('배포 메타데이터의 Igama·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(idilesi, 한도):
    if not idilesi.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(idilesi, timeout=30) as phendula:
        if not phendula.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 idilesi fudusa_ixabiso')
        iingcombolo = phendula.read(한도 + 1)
    if len(iingcombolo) > 한도:
        raise ValueError('배포 iFayili Ubukhulu 제한 초과')
    return iingcombolo


def gqithisela_umqulu(Igama, inguqulelo_ixabiso, 파일들, 출처):
    명세 = {'name': Igama, 'version': inguqulelo_ixabiso, 'source': 출처, 'files': [
        {'path': INDLELA, 'size': len(iingcombolo), 'sha256': hashlib.sha256(iingcombolo).hexdigest()}
        for INDLELA, iingcombolo in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('umqulu 명세 Ubukhulu 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ufako_nkcukacha_ixabiso['path']] for ufako_nkcukacha_ixabiso in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, INDLELA, 오프라인=False):
        자신.INDLELA = Path(INDLELA)
        자신.INDLELA.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def lungisa(자신, 요청):
        Igama, inguqulelo_ixabiso = 요청해석(요청)
        열쇠 = Igama + ('==' + inguqulelo_ixabiso if inguqulelo_ixabiso else '')
        ilog_indlela = 자신.INDLELA / (열쇠 + '.json')
        배포경로 = 자신.INDLELA / (열쇠 + '.archive')
        if ilog_indlela.is_file() and 배포경로.is_file():
            ilog_umqolo = json.loads(ilog_indlela.read_text())
            iingcombolo = 배포경로.read_bytes()
            if hashlib.sha256(iingcombolo).hexdigest() != ilog_umqolo['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 umqulu: ' + 요청)
            idilesi = 'https://pypi.org/pypi/' + Igama + ('/' + inguqulelo_ixabiso if inguqulelo_ixabiso else '') + '/json'
            i_msinfo32_exe = json.loads(웹읽기(idilesi, 4194304).decode())
            if i_msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ufako_nkcukacha_ixabiso for ufako_nkcukacha_ixabiso in i_msinfo32_exe['urls'] if not ufako_nkcukacha_ixabiso.get('yanked') and ufako_nkcukacha_ixabiso['filename'].endswith('-none-any.whl')]
            if not 후보 and Igama.startswith('micropython-'):
                후보 = [ufako_nkcukacha_ixabiso for ufako_nkcukacha_ixabiso in i_msinfo32_exe['urls'] if not ufako_nkcukacha_ixabiso.get('yanked') and ufako_nkcukacha_ixabiso['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ukukhetha_ixabiso = 후보[0]
            iingcombolo = 웹읽기(ukukhetha_ixabiso['url'], 4194304)
            if hashlib.sha256(iingcombolo).hexdigest() != ukukhetha_ixabiso['digests']['sha256']:
                raise ValueError('PyPI 배포 iFayili SHA-256 불일치')
            ilog_umqolo = {'name': Igama, 'version': i_msinfo32_exe['info']['version'], 'filename': ukukhetha_ixabiso['filename'],
                    'url': ukukhetha_ixabiso['url'], 'sha256': ukukhetha_ixabiso['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ilog_umqolo['filename'], iingcombolo, Igama, ilog_umqolo['version'])
            배포경로.write_bytes(iingcombolo)
            ilog_indlela.write_text(json.dumps(ilog_umqolo, ensure_ascii=False, indent=2) + '\n')
        if ilog_umqolo['name'] != Igama or inguqulelo_ixabiso and ilog_umqolo['version'] != inguqulelo_ixabiso:
            raise ValueError('저장소 Igama·버전 불일치')
        파일들 = 압축풀기(ilog_umqolo['filename'], iingcombolo, Igama, ilog_umqolo['version'])
        return gqithisela_umqulu(Igama, ilog_umqolo['version'], 파일들, ilog_umqolo['url'])


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
                raise ValueError('잘못된 umqulu 요청')
            phendula = 자신.server.저장소.lungisa(요청[:-1].decode('ascii'))
        except Exception as Impazamo:
            머리 = json.dumps({'error': str(Impazamo)[:500]}, ensure_ascii=False).encode()
            phendula = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(phendula)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, INDLELA=None, 오프라인=False):
        자신.iseva_ixabiso = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.iseva_ixabiso.allow_reuse_address = True
        자신.iseva_ixabiso.server_bind()
        자신.iseva_ixabiso.server_activate()
        자신.iseva_ixabiso.저장소 = 꾸러미저장소(INDLELA or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.iseva_ixabiso.server_address[1]
        자신.ithredi_ixabiso = threading.Thread(target=자신.iseva_ixabiso.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ithredi_ixabiso.start()
        return 자신

    def __exit__(자신, *인수):
        자신.iseva_ixabiso.shutdown()
        자신.iseva_ixabiso.server_close()
        자신.ithredi_ixabiso.join(timeout=2)


def Phumeza():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ukwenza_umyalelo 없이 호환 배포 파일을 내려받아 검사·Store_ixabiso')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        iingcombolo = 꾸러미저장소(인수.cache, 인수.offline).lungisa(인수.fetch)
        print('umqulu lungisa 완료:', 인수.fetch, len(iingcombolo), 'ibhayithi_ixabiso')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('umqulu 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.ithredi_ixabiso.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Phumeza()
