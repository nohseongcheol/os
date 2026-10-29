#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 faka_inani·실행한다."""
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
        raise ValueError('isigaxa Igama 또는 Igama==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def qinisekisa_umzila(Igama, ukufaka_umzila=True):
    Indlela_2 = PurePosixPath(Igama)
    if Indlela_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Igama.split('/')):
        raise ValueError('허용하지 않는 isigaxa Indlela_2: ' + Igama)
    if '\\' in Igama or any(ord(uhlamvusimo_inani) < 32 or ord(uhlamvusimo_inani) == 127 for uhlamvusimo_inani in Igama):
        raise ValueError('잘못된 isigaxa Indlela_2 문자')
    if ukufaka_umzila and (len(('/lib/' + Igama).encode()) > 63 or Igama in ('Isi_Zulu.py', 'isigaxa.py')):
        raise ValueError('isigaxa Indlela_2 제한 또는 inani_elimisiwe umtapo 충돌: ' + Igama)
    return Igama


def 압축풀기(ifayela_okufakwayo_igama, imininingwane, Igama, isibuyekezo_inani):
    파일들 = {}
    명세들 = []
    def 추가(Indlela_2, Okuqukethwe_inani):
        qinisekisa_umzila(Indlela_2)
        if Indlela_2 in 파일들:
            raise ValueError('중복 isigaxa Indlela_2: ' + Indlela_2)
        if len(Okuqukethwe_inani) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Indlela_2)
        Okuqukethwe_inani.decode('utf-8')
        파일들[Indlela_2] = Okuqukethwe_inani
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 umthombo_isihlahla 16개·합계 64 KiB 이하여야 합니다.')
    if ifayela_okufakwayo_igama.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(imininingwane)) as isigaxa:
            항목들 = isigaxa.infolist()
            if len(항목들) > 256 or sum(okufakwayo_inani.file_size for okufakwayo_inani in 항목들) > 1048576:
                raise ValueError('londoloza_inani khulula_Indawo_yokugcina Ubungako 제한 초과')
            udaba_Uhlu = [okufakwayo_inani for okufakwayo_inani in 항목들 if okufakwayo_inani.filename.endswith('.dist-info/WHEEL')]
            if len(udaba_Uhlu) != 1:
                raise ValueError('wheel udaba_inani 명세가 필요합니다.')
            udaba_inani = email.parser.Parser().parsestr(isigaxa.read(udaba_Uhlu[0]).decode())
            if udaba_inani.get('Root-Is-Purelib', '').lower() != 'true' or not ifayela_okufakwayo_igama.endswith('-none-any.whl'):
                raise ValueError('C iselulo_inani·플랫폼 전용 wheel은 지원하지 않습니다.')
            for okufakwayo_inani in 항목들:
                Indlela_2 = okufakwayo_inani.filename.rstrip('/')
                qinisekisa_umzila(Indlela_2, False)
                if (okufakwayo_inani.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if okufakwayo_inani.filename.endswith('/'):
                    continue
                if '.dist-info/' in Indlela_2:
                    if Indlela_2.endswith('/METADATA'):
                        명세들.append(isigaxa.read(okufakwayo_inani).decode())
                    continue
                if not Indlela_2.endswith('.py') or '.data/' in Indlela_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Indlela_2)
                추가(Indlela_2, isigaxa.read(okufakwayo_inani))
    elif ifayela_okufakwayo_igama.endswith('.tar.gz') and Igama.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py yenza_umyalo 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(imininingwane), mode='r|gz') as isigaxa:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for okufakwayo_inani in isigaxa:
                항목수 += 1
                전체크기 += okufakwayo_inani.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('londoloza_inani khulula_Indawo_yokugcina Ubungako 제한 초과')
                qinisekisa_umzila(okufakwayo_inani.name, False)
                부분들 = okufakwayo_inani.name.split('/')
                뿌리들.add(부분들[0])
                if okufakwayo_inani.isdir():
                    continue
                if not okufakwayo_inani.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython umthombo_isihlahla 배포형')
                Indlela_2 = '/'.join(부분들[1:])
                Okuqukethwe_inani = isigaxa.extractfile(okufakwayo_inani).read()
                if Indlela_2.endswith('PKG-INFO'):
                    명세들.append(Okuqukethwe_inani.decode())
                elif Indlela_2.endswith('.py') and Indlela_2 not in ('setup.py',):
                    추가(Indlela_2, Okuqukethwe_inani)
                elif '.egg-info/' not in Indlela_2 and not Indlela_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Indlela_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* umthombo_isihlahla 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Igama or 명세.get('Version') != isibuyekezo_inani:
        raise ValueError('배포 메타데이터의 Igama·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ikheli, 한도):
    if not ikheli.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ikheli, timeout=30) as phendula:
        if not phendula.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ikheli susa_inani')
        imininingwane = phendula.read(한도 + 1)
    if len(imininingwane) > 한도:
        raise ValueError('배포 Ihele Ubungako 제한 초과')
    return imininingwane


def dlulisa_isigaxa(Igama, isibuyekezo_inani, 파일들, 출처):
    명세 = {'name': Igama, 'version': isibuyekezo_inani, 'source': 출처, 'files': [
        {'path': Indlela_2, 'size': len(imininingwane), 'sha256': hashlib.sha256(imininingwane).hexdigest()}
        for Indlela_2, imininingwane in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('isigaxa 명세 Ubungako 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[okufakwayo_inani['path']] for okufakwayo_inani in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Indlela_2, 오프라인=False):
        자신.Indlela_2 = Path(Indlela_2)
        자신.Indlela_2.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Hlela(자신, 요청):
        Igama, isibuyekezo_inani = 요청해석(요청)
        열쇠 = Igama + ('==' + isibuyekezo_inani if isibuyekezo_inani else '')
        loga_umzila = 자신.Indlela_2 / (열쇠 + '.json')
        배포경로 = 자신.Indlela_2 / (열쇠 + '.archive')
        if loga_umzila.is_file() and 배포경로.is_file():
            loga_umugqa = json.loads(loga_umzila.read_text())
            imininingwane = 배포경로.read_bytes()
            if hashlib.sha256(imininingwane).hexdigest() != loga_umugqa['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 isigaxa: ' + 요청)
            ikheli = 'https://pypi.org/pypi/' + Igama + ('/' + isibuyekezo_inani if isibuyekezo_inani else '') + '/json'
            I_msinfo32_exe = json.loads(웹읽기(ikheli, 4194304).decode())
            if I_msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [okufakwayo_inani for okufakwayo_inani in I_msinfo32_exe['urls'] if not okufakwayo_inani.get('yanked') and okufakwayo_inani['filename'].endswith('-none-any.whl')]
            if not 후보 and Igama.startswith('micropython-'):
                후보 = [okufakwayo_inani for okufakwayo_inani in I_msinfo32_exe['urls'] if not okufakwayo_inani.get('yanked') and okufakwayo_inani['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            okukhethiwe_inani = 후보[0]
            imininingwane = 웹읽기(okukhethiwe_inani['url'], 4194304)
            if hashlib.sha256(imininingwane).hexdigest() != okukhethiwe_inani['digests']['sha256']:
                raise ValueError('PyPI 배포 Ihele SHA-256 불일치')
            loga_umugqa = {'name': Igama, 'version': I_msinfo32_exe['info']['version'], 'filename': okukhethiwe_inani['filename'],
                    'url': okukhethiwe_inani['url'], 'sha256': okukhethiwe_inani['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(loga_umugqa['filename'], imininingwane, Igama, loga_umugqa['version'])
            배포경로.write_bytes(imininingwane)
            loga_umzila.write_text(json.dumps(loga_umugqa, ensure_ascii=False, indent=2) + '\n')
        if loga_umugqa['name'] != Igama or isibuyekezo_inani and loga_umugqa['version'] != isibuyekezo_inani:
            raise ValueError('저장소 Igama·버전 불일치')
        파일들 = 압축풀기(loga_umugqa['filename'], imininingwane, Igama, loga_umugqa['version'])
        return dlulisa_isigaxa(Igama, loga_umugqa['version'], 파일들, loga_umugqa['url'])


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
                raise ValueError('잘못된 isigaxa 요청')
            phendula = 자신.server.저장소.Hlela(요청[:-1].decode('ascii'))
        except Exception as Iphutha:
            머리 = json.dumps({'error': str(Iphutha)[:500]}, ensure_ascii=False).encode()
            phendula = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(phendula)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Indlela_2=None, 오프라인=False):
        자신.Iseva_inani = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.Iseva_inani.allow_reuse_address = True
        자신.Iseva_inani.server_bind()
        자신.Iseva_inani.server_activate()
        자신.Iseva_inani.저장소 = 꾸러미저장소(Indlela_2 or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.Iseva_inani.server_address[1]
        자신.uhlu_lwemilayezo_inani = threading.Thread(target=자신.Iseva_inani.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.uhlu_lwemilayezo_inani.start()
        return 자신

    def __exit__(자신, *인수):
        자신.Iseva_inani.shutdown()
        자신.Iseva_inani.server_close()
        자신.uhlu_lwemilayezo_inani.join(timeout=2)


def Sebenzisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='yenza_umyalo 없이 호환 배포 파일을 내려받아 검사·Store_inani')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        imininingwane = 꾸러미저장소(인수.cache, 인수.offline).Hlela(인수.fetch)
        print('isigaxa Hlela 완료:', 인수.fetch, len(imininingwane), 'ibhayithi_inani')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('isigaxa 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.uhlu_lwemilayezo_inani.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Sebenzisa()
