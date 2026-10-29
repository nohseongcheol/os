#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 o_rnatish_VALUE·실행한다."""
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

Project_ildiz = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('to_plam Nomi 또는 Nomi==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def tasdiqlash_yo_l(Nomi, o_rnatish_yo_l=True):
    yo_l = PurePosixPath(Nomi)
    if yo_l.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nomi.split('/')):
        raise ValueError('허용하지 않는 to_plam yo_l: ' + Nomi)
    if '\\' in Nomi or any(ord(belgi_VALUE) < 32 or ord(belgi_VALUE) == 127 for belgi_VALUE in Nomi):
        raise ValueError('잘못된 to_plam yo_l 문자')
    if o_rnatish_yo_l and (len(('/lib/' + Nomi).encode()) > 63 or Nomi in ('한국어.py', 'to_plam.py')):
        raise ValueError('to_plam yo_l 제한 또는 sukut_bo_yicha_qiymat kutubxona 충돌: ' + Nomi)
    return Nomi


def 압축풀기(fayl_kiritish_nom, ma_lumotlar, Nomi, versiya_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(yo_l, tarkib_VALUE):
        tasdiqlash_yo_l(yo_l)
        if yo_l in 파일들:
            raise ValueError('중복 to_plam yo_l: ' + yo_l)
        if len(tarkib_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + yo_l)
        tarkib_VALUE.decode('utf-8')
        파일들[yo_l] = tarkib_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 manba_daraxt 16개·합계 64 KiB 이하여야 합니다.')
    if fayl_kiritish_nom.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ma_lumotlar)) as to_plam:
            항목들 = to_plam.infolist()
            if len(항목들) > 256 or sum(kiritish_VALUE.file_size for kiritish_VALUE in 항목들) > 1048576:
                raise ValueError('Arxiv_VALUE nashr_Xotira Hajmi 제한 초과')
            murojaat_Ro_yxat = [kiritish_VALUE for kiritish_VALUE in 항목들 if kiritish_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(murojaat_Ro_yxat) != 1:
                raise ValueError('wheel murojaat_VALUE 명세가 필요합니다.')
            murojaat_VALUE = email.parser.Parser().parsestr(to_plam.read(murojaat_Ro_yxat[0]).decode())
            if murojaat_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not fayl_kiritish_nom.endswith('-none-any.whl'):
                raise ValueError('C kengaytma_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for kiritish_VALUE in 항목들:
                yo_l = kiritish_VALUE.filename.rstrip('/')
                tasdiqlash_yo_l(yo_l, False)
                if (kiritish_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if kiritish_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in yo_l:
                    if yo_l.endswith('/METADATA'):
                        명세들.append(to_plam.read(kiritish_VALUE).decode())
                    continue
                if not yo_l.endswith('.py') or '.data/' in yo_l:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + yo_l)
                추가(yo_l, to_plam.read(kiritish_VALUE))
    elif fayl_kiritish_nom.endswith('.tar.gz') and Nomi.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py bajarmoq_buyruq 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ma_lumotlar), mode='r|gz') as to_plam:
            뿌리들 = set()
            kiritish_COUNT = 0
            전체크기 = 0
            for kiritish_VALUE in to_plam:
                kiritish_COUNT += 1
                전체크기 += kiritish_VALUE.size
                if kiritish_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Arxiv_VALUE nashr_Xotira Hajmi 제한 초과')
                tasdiqlash_yo_l(kiritish_VALUE.name, False)
                부분들 = kiritish_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if kiritish_VALUE.isdir():
                    continue
                if not kiritish_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython manba_daraxt 배포형')
                yo_l = '/'.join(부분들[1:])
                tarkib_VALUE = to_plam.extractfile(kiritish_VALUE).read()
                if yo_l.endswith('PKG-INFO'):
                    명세들.append(tarkib_VALUE.decode())
                elif yo_l.endswith('.py') and yo_l not in ('setup.py',):
                    추가(yo_l, tarkib_VALUE)
                elif '.egg-info/' not in yo_l and not yo_l.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + yo_l)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ildiz_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* manba_daraxt 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Nomi or 명세.get('Version') != versiya_VALUE:
        raise ValueError('배포 메타데이터의 Nomi·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(manzil, 한도):
    if not manzil.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(manzil, timeout=30) as javob_berish:
        if not javob_berish.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 manzil ko_chirmoq_VALUE')
        ma_lumotlar = javob_berish.read(한도 + 1)
    if len(ma_lumotlar) > 한도:
        raise ValueError('배포 Fayl Hajmi 제한 초과')
    return ma_lumotlar


def uzatish_to_plam(Nomi, versiya_VALUE, 파일들, 출처):
    명세 = {'name': Nomi, 'version': versiya_VALUE, 'source': 출처, 'files': [
        {'path': yo_l, 'size': len(ma_lumotlar), 'sha256': hashlib.sha256(ma_lumotlar).hexdigest()}
        for yo_l, ma_lumotlar in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('to_plam 명세 Hajmi 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[kiritish_VALUE['path']] for kiritish_VALUE in 명세['files'])


class to_plam_repozitoriy:
    def __init__(자신, yo_l, 오프라인=False):
        자신.yo_l = Path(yo_l)
        자신.yo_l.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Tayyorlamoq(자신, 요청):
        Nomi, versiya_VALUE = 요청해석(요청)
        열쇠 = Nomi + ('==' + versiya_VALUE if versiya_VALUE else '')
        LOG_yo_l = 자신.yo_l / (열쇠 + '.json')
        배포경로 = 자신.yo_l / (열쇠 + '.archive')
        if LOG_yo_l.is_file() and 배포경로.is_file():
            LOG_satr = json.loads(LOG_yo_l.read_text())
            ma_lumotlar = 배포경로.read_bytes()
            if hashlib.sha256(ma_lumotlar).hexdigest() != LOG_satr['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 to_plam: ' + 요청)
            manzil = 'https://pypi.org/pypi/' + Nomi + ('/' + versiya_VALUE if versiya_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(manzil, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [kiritish_VALUE for kiritish_VALUE in msinfo32_exe['urls'] if not kiritish_VALUE.get('yanked') and kiritish_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Nomi.startswith('micropython-'):
                후보 = [kiritish_VALUE for kiritish_VALUE in msinfo32_exe['urls'] if not kiritish_VALUE.get('yanked') and kiritish_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            tanlanma_VALUE = 후보[0]
            ma_lumotlar = 웹읽기(tanlanma_VALUE['url'], 4194304)
            if hashlib.sha256(ma_lumotlar).hexdigest() != tanlanma_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Fayl SHA-256 불일치')
            LOG_satr = {'name': Nomi, 'version': msinfo32_exe['info']['version'], 'filename': tanlanma_VALUE['filename'],
                    'url': tanlanma_VALUE['url'], 'sha256': tanlanma_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_satr['filename'], ma_lumotlar, Nomi, LOG_satr['version'])
            배포경로.write_bytes(ma_lumotlar)
            LOG_yo_l.write_text(json.dumps(LOG_satr, ensure_ascii=False, indent=2) + '\n')
        if LOG_satr['name'] != Nomi or versiya_VALUE and LOG_satr['version'] != versiya_VALUE:
            raise ValueError('repozitoriy_ildiz Nomi·버전 불일치')
        파일들 = 압축풀기(LOG_satr['filename'], ma_lumotlar, Nomi, LOG_satr['version'])
        return uzatish_to_plam(Nomi, LOG_satr['version'], 파일들, LOG_satr['url'])


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
                raise ValueError('잘못된 to_plam 요청')
            javob_berish = 자신.server.repozitoriy_ildiz.Tayyorlamoq(요청[:-1].decode('ascii'))
        except Exception as Xato:
            머리 = json.dumps({'error': str(Xato)[:500]}, ensure_ascii=False).encode()
            javob_berish = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(javob_berish)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, yo_l=None, 오프라인=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.repozitoriy_ildiz = to_plam_repozitoriy(yo_l or Project_ildiz/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.server_VALUE.server_address[1]
        자신.oqim_VALUE_5b72a632 = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.oqim_VALUE_5b72a632.start()
        return 자신

    def __exit__(자신, *인수):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.oqim_VALUE_5b72a632.join(timeout=2)


def Bajarish():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=Project_ildiz/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='bajarmoq_buyruq 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = parser_48ee4b1b.parse_args()
    if 인수.fetch:
        ma_lumotlar = to_plam_repozitoriy(인수.cache, 인수.offline).Tayyorlamoq(인수.fetch)
        print('to_plam Tayyorlamoq 완료:', 인수.fetch, len(ma_lumotlar), 'bayt_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('to_plam 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.oqim_VALUE_5b72a632.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Bajarish()
