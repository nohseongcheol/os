#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 wùbe_valuu·실행한다."""
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
        raise ValueError('ngwungwu Aha 또는 Aha==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def mee_ịbanihe_ụzọ_ozi(Aha, nkwakọnye_ụzọ_ozi=True):
    ụzọ_ozi = PurePosixPath(Aha)
    if ụzọ_ozi.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Aha.split('/')):
        raise ValueError('허용하지 않는 ngwungwu ụzọ_ozi: ' + Aha)
    if '\\' in Aha or any(ord(mkpụrụedemede_valuu) < 32 or ord(mkpụrụedemede_valuu) == 127 for mkpụrụedemede_valuu in Aha):
        raise ValueError('잘못된 ngwungwu ụzọ_ozi 문자')
    if nkwakọnye_ụzọ_ozi and (len(('/lib/' + Aha).encode()) > 63 or Aha in ('한국어.py', 'ngwungwu.py')):
        raise ValueError('ngwungwu ụzọ_ozi 제한 또는 Ngwa_ihe_dịadị ọbaakwụkwọ 충돌: ' + Aha)
    return Aha


def 압축풀기(ọbọakwụkwọ_ndebà_akara_ahà, datà, Aha, ụdị_valuu):
    파일들 = {}
    명세들 = []
    def 추가(ụzọ_ozi, ndịnà_valuu):
        mee_ịbanihe_ụzọ_ozi(ụzọ_ozi)
        if ụzọ_ozi in 파일들:
            raise ValueError('중복 ngwungwu ụzọ_ozi: ' + ụzọ_ozi)
        if len(ndịnà_valuu) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ụzọ_ozi)
        ndịnà_valuu.decode('utf-8')
        파일들[ụzọ_ozi] = ndịnà_valuu
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ebensìbịa_èsèrèsè_osisi 16개·합계 64 KiB 이하여야 합니다.')
    if ọbọakwụkwọ_ndebà_akara_ahà.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(datà)) as ngwungwu:
            항목들 = ngwungwu.infolist()
            if len(항목들) > 256 or sum(ndebà_valuu.file_size for ndebà_valuu in 항목들) > 1048576:
                raise ValueError('ọkpụ_valuu bupute_Nchekwa Ụhara 제한 초과')
            ngō_ndepụta = [ndebà_valuu for ndebà_valuu in 항목들 if ndebà_valuu.filename.endswith('.dist-info/WHEEL')]
            if len(ngō_ndepụta) != 1:
                raise ValueError('wheel ngō_valuu 명세가 필요합니다.')
            ngō_valuu = email.parser.Parser().parsestr(ngwungwu.read(ngō_ndepụta[0]).decode())
            if ngō_valuu.get('Root-Is-Purelib', '').lower() != 'true' or not ọbọakwụkwọ_ndebà_akara_ahà.endswith('-none-any.whl'):
                raise ValueError('C mgbatị_valuu·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ndebà_valuu in 항목들:
                ụzọ_ozi = ndebà_valuu.filename.rstrip('/')
                mee_ịbanihe_ụzọ_ozi(ụzọ_ozi, False)
                if (ndebà_valuu.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ndebà_valuu.filename.endswith('/'):
                    continue
                if '.dist-info/' in ụzọ_ozi:
                    if ụzọ_ozi.endswith('/METADATA'):
                        명세들.append(ngwungwu.read(ndebà_valuu).decode())
                    continue
                if not ụzọ_ozi.endswith('.py') or '.data/' in ụzọ_ozi:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ụzọ_ozi)
                추가(ụzọ_ozi, ngwungwu.read(ndebà_valuu))
    elif ọbọakwụkwọ_ndebà_akara_ahà.endswith('.tar.gz') and Aha.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py mee_nnyemiwu 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(datà), mode='r|gz') as ngwungwu:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ndebà_valuu in ngwungwu:
                항목수 += 1
                전체크기 += ndebà_valuu.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ọkpụ_valuu bupute_Nchekwa Ụhara 제한 초과')
                mee_ịbanihe_ụzọ_ozi(ndebà_valuu.name, False)
                부분들 = ndebà_valuu.name.split('/')
                뿌리들.add(부분들[0])
                if ndebà_valuu.isdir():
                    continue
                if not ndebà_valuu.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ebensìbịa_èsèrèsè_osisi 배포형')
                ụzọ_ozi = '/'.join(부분들[1:])
                ndịnà_valuu = ngwungwu.extractfile(ndebà_valuu).read()
                if ụzọ_ozi.endswith('PKG-INFO'):
                    명세들.append(ndịnà_valuu.decode())
                elif ụzọ_ozi.endswith('.py') and ụzọ_ozi not in ('setup.py',):
                    추가(ụzọ_ozi, ndịnà_valuu)
                elif '.egg-info/' not in ụzọ_ozi and not ụzọ_ozi.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ụzọ_ozi)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ebensìbịa_èsèrèsè_osisi 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Aha or 명세.get('Version') != ụdị_valuu:
        raise ValueError('배포 메타데이터의 Aha·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(àdreèsì, 한도):
    if not àdreèsì.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(àdreèsì, timeout=30) as nzaghachi:
        if not nzaghachi.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 àdreèsì gàa_valuu')
        datà = nzaghachi.read(한도 + 1)
    if len(datà) > 한도:
        raise ValueError('배포 Faịlụ Ụhara 제한 초과')
    return datà


def dògharịa_ngwungwu(Aha, ụdị_valuu, 파일들, 출처):
    명세 = {'name': Aha, 'version': ụdị_valuu, 'source': 출처, 'files': [
        {'path': ụzọ_ozi, 'size': len(datà), 'sha256': hashlib.sha256(datà).hexdigest()}
        for ụzọ_ozi, datà in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ngwungwu 명세 Ụhara 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ndebà_valuu['path']] for ndebà_valuu in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, ụzọ_ozi, 오프라인=False):
        자신.ụzọ_ozi = Path(ụzọ_ozi)
        자신.ụzọ_ozi.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Kwado(자신, 요청):
        Aha, ụdị_valuu = 요청해석(요청)
        열쇠 = Aha + ('==' + ụdị_valuu if ụdị_valuu else '')
        ndekọ_ụzọ_ozi = 자신.ụzọ_ozi / (열쇠 + '.json')
        배포경로 = 자신.ụzọ_ozi / (열쇠 + '.archive')
        if ndekọ_ụzọ_ozi.is_file() and 배포경로.is_file():
            ndekọ_NDEKỌ = json.loads(ndekọ_ụzọ_ozi.read_text())
            datà = 배포경로.read_bytes()
            if hashlib.sha256(datà).hexdigest() != ndekọ_NDEKỌ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 ngwungwu: ' + 요청)
            àdreèsì = 'https://pypi.org/pypi/' + Aha + ('/' + ụdị_valuu if ụdị_valuu else '') + '/json'
            Ozi_Sistèm = json.loads(웹읽기(àdreèsì, 4194304).decode())
            if Ozi_Sistèm['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ndebà_valuu for ndebà_valuu in Ozi_Sistèm['urls'] if not ndebà_valuu.get('yanked') and ndebà_valuu['filename'].endswith('-none-any.whl')]
            if not 후보 and Aha.startswith('micropython-'):
                후보 = [ndebà_valuu for ndebà_valuu in Ozi_Sistèm['urls'] if not ndebà_valuu.get('yanked') and ndebà_valuu['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ebenhọrọ_valuu = 후보[0]
            datà = 웹읽기(ebenhọrọ_valuu['url'], 4194304)
            if hashlib.sha256(datà).hexdigest() != ebenhọrọ_valuu['digests']['sha256']:
                raise ValueError('PyPI 배포 Faịlụ SHA-256 불일치')
            ndekọ_NDEKỌ = {'name': Aha, 'version': Ozi_Sistèm['info']['version'], 'filename': ebenhọrọ_valuu['filename'],
                    'url': ebenhọrọ_valuu['url'], 'sha256': ebenhọrọ_valuu['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ndekọ_NDEKỌ['filename'], datà, Aha, ndekọ_NDEKỌ['version'])
            배포경로.write_bytes(datà)
            ndekọ_ụzọ_ozi.write_text(json.dumps(ndekọ_NDEKỌ, ensure_ascii=False, indent=2) + '\n')
        if ndekọ_NDEKỌ['name'] != Aha or ụdị_valuu and ndekọ_NDEKỌ['version'] != ụdị_valuu:
            raise ValueError('저장소 Aha·버전 불일치')
        파일들 = 압축풀기(ndekọ_NDEKỌ['filename'], datà, Aha, ndekọ_NDEKỌ['version'])
        return dògharịa_ngwungwu(Aha, ndekọ_NDEKỌ['version'], 파일들, ndekọ_NDEKỌ['url'])


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
                raise ValueError('잘못된 ngwungwu 요청')
            nzaghachi = 자신.server.저장소.Kwado(요청[:-1].decode('ascii'))
        except Exception as mmejọ:
            머리 = json.dumps({'error': str(mmejọ)[:500]}, ensure_ascii=False).encode()
            nzaghachi = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(nzaghachi)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, ụzọ_ozi=None, 오프라인=False):
        자신.savà_valuu = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.savà_valuu.allow_reuse_address = True
        자신.savà_valuu.server_bind()
        자신.savà_valuu.server_activate()
        자신.savà_valuu.저장소 = 꾸러미저장소(ụzọ_ozi or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.savà_valuu.server_address[1]
        자신.treèd_valuu = threading.Thread(target=자신.savà_valuu.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.treèd_valuu.start()
        return 자신

    def __exit__(자신, *인수):
        자신.savà_valuu.shutdown()
        자신.savà_valuu.server_close()
        자신.treèd_valuu.join(timeout=2)


def Bido():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='mee_nnyemiwu 없이 호환 배포 파일을 내려받아 검사·Store_valuu')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        datà = 꾸러미저장소(인수.cache, 인수.offline).Kwado(인수.fetch)
        print('ngwungwu Kwado 완료:', 인수.fetch, len(datà), 'baịtị_valuu')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ngwungwu 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.treèd_valuu.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Bido()
