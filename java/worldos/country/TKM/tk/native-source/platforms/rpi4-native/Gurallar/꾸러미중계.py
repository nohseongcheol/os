#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 gurna_baha·실행한다."""
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
        raise ValueError('toplum Ad 또는 Ad==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def tassykla_ýol(Ad, gurnama_ýol=True):
    Ýol = PurePosixPath(Ad)
    if Ýol.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Ad.split('/')):
        raise ValueError('허용하지 않는 toplum Ýol: ' + Ad)
    if '\\' in Ad or any(ord(nyşan_baha_068c2631) < 32 or ord(nyşan_baha_068c2631) == 127 for nyşan_baha_068c2631 in Ad):
        raise ValueError('잘못된 toplum Ýol 문자')
    if gurnama_ýol and (len(('/lib/' + Ad).encode()) > 63 or Ad in ('한국어.py', 'toplum.py')):
        raise ValueError('toplum Ýol 제한 또는 öňünden_kabul_edilen_baha Kitaphana 충돌: ' + Ad)
    return Ad


def 압축풀기(faýl_girizmeklik_at, maglumat, Ad, wersiýa_baha):
    파일들 = {}
    명세들 = []
    def 추가(Ýol, Mazmun_baha):
        tassykla_ýol(Ýol)
        if Ýol in 파일들:
            raise ValueError('중복 toplum Ýol: ' + Ýol)
        if len(Mazmun_baha) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Ýol)
        Mazmun_baha.decode('utf-8')
        파일들[Ýol] = Mazmun_baha
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 gor_agaç 16개·합계 64 KiB 이하여야 합니다.')
    if faýl_girizmeklik_at.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(maglumat)) as toplum:
            항목들 = toplum.infolist()
            if len(항목들) > 256 or sum(girizmeklik_baha.file_size for girizmeklik_baha in 항목들) > 1048576:
                raise ValueError('Arhiw_baha goýbermek_Ammar Ululyk 제한 초과')
            ýumuş_Sanaw = [girizmeklik_baha for girizmeklik_baha in 항목들 if girizmeklik_baha.filename.endswith('.dist-info/WHEEL')]
            if len(ýumuş_Sanaw) != 1:
                raise ValueError('wheel ýumuş_baha_102996da 명세가 필요합니다.')
            ýumuş_baha_102996da = email.parser.Parser().parsestr(toplum.read(ýumuş_Sanaw[0]).decode())
            if ýumuş_baha_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not faýl_girizmeklik_at.endswith('-none-any.whl'):
                raise ValueError('C giňelme_baha·플랫폼 전용 wheel은 지원하지 않습니다.')
            for girizmeklik_baha in 항목들:
                Ýol = girizmeklik_baha.filename.rstrip('/')
                tassykla_ýol(Ýol, False)
                if (girizmeklik_baha.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if girizmeklik_baha.filename.endswith('/'):
                    continue
                if '.dist-info/' in Ýol:
                    if Ýol.endswith('/METADATA'):
                        명세들.append(toplum.read(girizmeklik_baha).decode())
                    continue
                if not Ýol.endswith('.py') or '.data/' in Ýol:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Ýol)
                추가(Ýol, toplum.read(girizmeklik_baha))
    elif faýl_girizmeklik_at.endswith('.tar.gz') and Ad.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ýerine_ýetir_buýruk 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(maglumat), mode='r|gz') as toplum:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for girizmeklik_baha in toplum:
                항목수 += 1
                전체크기 += girizmeklik_baha.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Arhiw_baha goýbermek_Ammar Ululyk 제한 초과')
                tassykla_ýol(girizmeklik_baha.name, False)
                부분들 = girizmeklik_baha.name.split('/')
                뿌리들.add(부분들[0])
                if girizmeklik_baha.isdir():
                    continue
                if not girizmeklik_baha.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython gor_agaç 배포형')
                Ýol = '/'.join(부분들[1:])
                Mazmun_baha = toplum.extractfile(girizmeklik_baha).read()
                if Ýol.endswith('PKG-INFO'):
                    명세들.append(Mazmun_baha.decode())
                elif Ýol.endswith('.py') and Ýol not in ('setup.py',):
                    추가(Ýol, Mazmun_baha)
                elif '.egg-info/' not in Ýol and not Ýol.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Ýol)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* gor_agaç 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Ad or 명세.get('Version') != wersiýa_baha:
        raise ValueError('배포 메타데이터의 Ad·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(salgy, 한도):
    if not salgy.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(salgy, timeout=30) as jogap_bermek:
        if not jogap_bermek.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 salgy ýerini_üýtget_baha')
        maglumat = jogap_bermek.read(한도 + 1)
    if len(maglumat) > 한도:
        raise ValueError('배포 Faýl Ululyk 제한 초과')
    return maglumat


def geçir_toplum(Ad, wersiýa_baha, 파일들, 출처):
    명세 = {'name': Ad, 'version': wersiýa_baha, 'source': 출처, 'files': [
        {'path': Ýol, 'size': len(maglumat), 'sha256': hashlib.sha256(maglumat).hexdigest()}
        for Ýol, maglumat in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('toplum 명세 Ululyk 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[girizmeklik_baha['path']] for girizmeklik_baha in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Ýol, 오프라인=False):
        자신.Ýol = Path(Ýol)
        자신.Ýol.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Taýýarla(자신, 요청):
        Ad, wersiýa_baha = 요청해석(요청)
        열쇠 = Ad + ('==' + wersiýa_baha if wersiýa_baha else '')
        hasaba_alyş_ýol = 자신.Ýol / (열쇠 + '.json')
        배포경로 = 자신.Ýol / (열쇠 + '.archive')
        if hasaba_alyş_ýol.is_file() and 배포경로.is_file():
            hasaba_alyş_setir = json.loads(hasaba_alyş_ýol.read_text())
            maglumat = 배포경로.read_bytes()
            if hashlib.sha256(maglumat).hexdigest() != hasaba_alyş_setir['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 toplum: ' + 요청)
            salgy = 'https://pypi.org/pypi/' + Ad + ('/' + wersiýa_baha if wersiýa_baha else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(salgy, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [girizmeklik_baha for girizmeklik_baha in msinfo32_exe['urls'] if not girizmeklik_baha.get('yanked') and girizmeklik_baha['filename'].endswith('-none-any.whl')]
            if not 후보 and Ad.startswith('micropython-'):
                후보 = [girizmeklik_baha for girizmeklik_baha in msinfo32_exe['urls'] if not girizmeklik_baha.get('yanked') and girizmeklik_baha['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            saýlama_baha = 후보[0]
            maglumat = 웹읽기(saýlama_baha['url'], 4194304)
            if hashlib.sha256(maglumat).hexdigest() != saýlama_baha['digests']['sha256']:
                raise ValueError('PyPI 배포 Faýl SHA-256 불일치')
            hasaba_alyş_setir = {'name': Ad, 'version': msinfo32_exe['info']['version'], 'filename': saýlama_baha['filename'],
                    'url': saýlama_baha['url'], 'sha256': saýlama_baha['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(hasaba_alyş_setir['filename'], maglumat, Ad, hasaba_alyş_setir['version'])
            배포경로.write_bytes(maglumat)
            hasaba_alyş_ýol.write_text(json.dumps(hasaba_alyş_setir, ensure_ascii=False, indent=2) + '\n')
        if hasaba_alyş_setir['name'] != Ad or wersiýa_baha and hasaba_alyş_setir['version'] != wersiýa_baha:
            raise ValueError('저장소 Ad·버전 불일치')
        파일들 = 압축풀기(hasaba_alyş_setir['filename'], maglumat, Ad, hasaba_alyş_setir['version'])
        return geçir_toplum(Ad, hasaba_alyş_setir['version'], 파일들, hasaba_alyş_setir['url'])


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
                raise ValueError('잘못된 toplum 요청')
            jogap_bermek = 자신.server.저장소.Taýýarla(요청[:-1].decode('ascii'))
        except Exception as Hata:
            머리 = json.dumps({'error': str(Hata)[:500]}, ensure_ascii=False).encode()
            jogap_bermek = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(jogap_bermek)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Ýol=None, 오프라인=False):
        자신.serwer_baha = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.serwer_baha.allow_reuse_address = True
        자신.serwer_baha.server_bind()
        자신.serwer_baha.server_activate()
        자신.serwer_baha.저장소 = 꾸러미저장소(Ýol or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.serwer_baha.server_address[1]
        자신.akym_baha = threading.Thread(target=자신.serwer_baha.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.akym_baha.start()
        return 자신

    def __exit__(자신, *인수):
        자신.serwer_baha.shutdown()
        자신.serwer_baha.server_close()
        자신.akym_baha.join(timeout=2)


def Bitir():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ýerine_ýetir_buýruk 없이 호환 배포 파일을 내려받아 검사·Store_baha')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        maglumat = 꾸러미저장소(인수.cache, 인수.offline).Taýýarla(인수.fetch)
        print('toplum Taýýarla 완료:', 인수.fetch, len(maglumat), 'baýt_baha')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('toplum 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.akym_baha.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Bitir()
