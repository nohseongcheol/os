#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 tsenya_Boleng·실행한다."""
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
        raise ValueError('ngatanngwe leina 또는 leina==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def netefatsa_tsela(leina, tsenyo_tsela=True):
    tsela = PurePosixPath(leina)
    if tsela.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in leina.split('/')):
        raise ValueError('허용하지 않는 ngatanngwe tsela: ' + leina)
    if '\\' in leina or any(ord(Letshwao_Boleng) < 32 or ord(Letshwao_Boleng) == 127 for Letshwao_Boleng in leina):
        raise ValueError('잘못된 ngatanngwe tsela 문자')
    if tsenyo_tsela and (len(('/lib/' + leina).encode()) > 63 or leina in ('한국어.py', 'ngatanngwe.py')):
        raise ValueError('ngatanngwe tsela 제한 또는 boleng_jo_bo_rulaganyeditsweng_ruri laeborari 충돌: ' + leina)
    return leina


def 압축풀기(faele_tsenyo_leina, tshedimosetso, leina, kgaolo_Boleng):
    파일들 = {}
    명세들 = []
    def 추가(tsela, Diteng_Boleng):
        netefatsa_tsela(tsela)
        if tsela in 파일들:
            raise ValueError('중복 ngatanngwe tsela: ' + tsela)
        if len(Diteng_Boleng) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + tsela)
        Diteng_Boleng.decode('utf-8')
        파일들[tsela] = Diteng_Boleng
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 Motswedi_sebopego_sa_tshedimosetso 16개·합계 64 KiB 이하여야 합니다.')
    if faele_tsenyo_leina.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(tshedimosetso)) as ngatanngwe:
            항목들 = ngatanngwe.infolist()
            if len(항목들) > 256 or sum(tsenyo_Boleng.file_size for tsenyo_Boleng in 항목들) > 1048576:
                raise ValueError('boloka_Boleng ntsha_Polokelo lekanya 제한 초과')
            konteraka_lenaane = [tsenyo_Boleng for tsenyo_Boleng in 항목들 if tsenyo_Boleng.filename.endswith('.dist-info/WHEEL')]
            if len(konteraka_lenaane) != 1:
                raise ValueError('wheel konteraka_Boleng 명세가 필요합니다.')
            konteraka_Boleng = email.parser.Parser().parsestr(ngatanngwe.read(konteraka_lenaane[0]).decode())
            if konteraka_Boleng.get('Root-Is-Purelib', '').lower() != 'true' or not faele_tsenyo_leina.endswith('-none-any.whl'):
                raise ValueError('C katoloso_Boleng·플랫폼 전용 wheel은 지원하지 않습니다.')
            for tsenyo_Boleng in 항목들:
                tsela = tsenyo_Boleng.filename.rstrip('/')
                netefatsa_tsela(tsela, False)
                if (tsenyo_Boleng.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if tsenyo_Boleng.filename.endswith('/'):
                    continue
                if '.dist-info/' in tsela:
                    if tsela.endswith('/METADATA'):
                        명세들.append(ngatanngwe.read(tsenyo_Boleng).decode())
                    continue
                if not tsela.endswith('.py') or '.data/' in tsela:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + tsela)
                추가(tsela, ngatanngwe.read(tsenyo_Boleng))
    elif faele_tsenyo_leina.endswith('.tar.gz') and leina.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py diragatsa_Taelo 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(tshedimosetso), mode='r|gz') as ngatanngwe:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for tsenyo_Boleng in ngatanngwe:
                항목수 += 1
                전체크기 += tsenyo_Boleng.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('boloka_Boleng ntsha_Polokelo lekanya 제한 초과')
                netefatsa_tsela(tsenyo_Boleng.name, False)
                부분들 = tsenyo_Boleng.name.split('/')
                뿌리들.add(부분들[0])
                if tsenyo_Boleng.isdir():
                    continue
                if not tsenyo_Boleng.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython Motswedi_sebopego_sa_tshedimosetso 배포형')
                tsela = '/'.join(부분들[1:])
                Diteng_Boleng = ngatanngwe.extractfile(tsenyo_Boleng).read()
                if tsela.endswith('PKG-INFO'):
                    명세들.append(Diteng_Boleng.decode())
                elif tsela.endswith('.py') and tsela not in ('setup.py',):
                    추가(tsela, Diteng_Boleng)
                elif '.egg-info/' not in tsela and not tsela.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + tsela)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* Motswedi_sebopego_sa_tshedimosetso 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != leina or 명세.get('Version') != kgaolo_Boleng:
        raise ValueError('배포 메타데이터의 leina·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(aterese, 한도):
    if not aterese.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(aterese, timeout=30) as araba:
        if not araba.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 aterese sutisa_Boleng')
        tshedimosetso = araba.read(한도 + 1)
    if len(tshedimosetso) > 한도:
        raise ValueError('배포 faele lekanya 제한 초과')
    return tshedimosetso


def fudusa_ngatanngwe(leina, kgaolo_Boleng, 파일들, 출처):
    명세 = {'name': leina, 'version': kgaolo_Boleng, 'source': 출처, 'files': [
        {'path': tsela, 'size': len(tshedimosetso), 'sha256': hashlib.sha256(tshedimosetso).hexdigest()}
        for tsela, tshedimosetso in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ngatanngwe 명세 lekanya 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[tsenyo_Boleng['path']] for tsenyo_Boleng in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, tsela, 오프라인=False):
        자신.tsela = Path(tsela)
        자신.tsela.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Baakanya(자신, 요청):
        leina, kgaolo_Boleng = 요청해석(요청)
        열쇠 = leina + ('==' + kgaolo_Boleng if kgaolo_Boleng else '')
        rekota_tsela = 자신.tsela / (열쇠 + '.json')
        배포경로 = 자신.tsela / (열쇠 + '.archive')
        if rekota_tsela.is_file() and 배포경로.is_file():
            rekota_mola = json.loads(rekota_tsela.read_text())
            tshedimosetso = 배포경로.read_bytes()
            if hashlib.sha256(tshedimosetso).hexdigest() != rekota_mola['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 ngatanngwe: ' + 요청)
            aterese = 'https://pypi.org/pypi/' + leina + ('/' + kgaolo_Boleng if kgaolo_Boleng else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(aterese, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [tsenyo_Boleng for tsenyo_Boleng in msinfo32_exe['urls'] if not tsenyo_Boleng.get('yanked') and tsenyo_Boleng['filename'].endswith('-none-any.whl')]
            if not 후보 and leina.startswith('micropython-'):
                후보 = [tsenyo_Boleng for tsenyo_Boleng in msinfo32_exe['urls'] if not tsenyo_Boleng.get('yanked') and tsenyo_Boleng['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            tlhopho_Boleng = 후보[0]
            tshedimosetso = 웹읽기(tlhopho_Boleng['url'], 4194304)
            if hashlib.sha256(tshedimosetso).hexdigest() != tlhopho_Boleng['digests']['sha256']:
                raise ValueError('PyPI 배포 faele SHA-256 불일치')
            rekota_mola = {'name': leina, 'version': msinfo32_exe['info']['version'], 'filename': tlhopho_Boleng['filename'],
                    'url': tlhopho_Boleng['url'], 'sha256': tlhopho_Boleng['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(rekota_mola['filename'], tshedimosetso, leina, rekota_mola['version'])
            배포경로.write_bytes(tshedimosetso)
            rekota_tsela.write_text(json.dumps(rekota_mola, ensure_ascii=False, indent=2) + '\n')
        if rekota_mola['name'] != leina or kgaolo_Boleng and rekota_mola['version'] != kgaolo_Boleng:
            raise ValueError('저장소 leina·버전 불일치')
        파일들 = 압축풀기(rekota_mola['filename'], tshedimosetso, leina, rekota_mola['version'])
        return fudusa_ngatanngwe(leina, rekota_mola['version'], 파일들, rekota_mola['url'])


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
                raise ValueError('잘못된 ngatanngwe 요청')
            araba = 자신.server.저장소.Baakanya(요청[:-1].decode('ascii'))
        except Exception as phoso:
            머리 = json.dumps({'error': str(phoso)[:500]}, ensure_ascii=False).encode()
            araba = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(araba)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, tsela=None, 오프라인=False):
        자신.sefara_Boleng = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.sefara_Boleng.allow_reuse_address = True
        자신.sefara_Boleng.server_bind()
        자신.sefara_Boleng.server_activate()
        자신.sefara_Boleng.저장소 = 꾸러미저장소(tsela or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.sefara_Boleng.server_address[1]
        자신.tlhale_Boleng = threading.Thread(target=자신.sefara_Boleng.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.tlhale_Boleng.start()
        return 자신

    def __exit__(자신, *인수):
        자신.sefara_Boleng.shutdown()
        자신.sefara_Boleng.server_close()
        자신.tlhale_Boleng.join(timeout=2)


def dirisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='diragatsa_Taelo 없이 호환 배포 파일을 내려받아 검사·Store_Boleng')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        tshedimosetso = 꾸러미저장소(인수.cache, 인수.offline).Baakanya(인수.fetch)
        print('ngatanngwe Baakanya 완료:', 인수.fetch, len(tshedimosetso), 'baete_Boleng')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ngatanngwe 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.tlhale_Boleng.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    dirisa()
