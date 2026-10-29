#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 samp_xëyma·실행한다."""
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
        raise ValueError('takku_xéewël tur_253d1510 또는 tur_253d1510==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def wéral_Yoonu_jëmale_f98b46e1(tur_253d1510, samp_Yoonu_jëmale=True):
    Yoonu_jëmale = PurePosixPath(tur_253d1510)
    if Yoonu_jëmale.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in tur_253d1510.split('/')):
        raise ValueError('허용하지 않는 takku_xéewël Yoonu_jëmale: ' + tur_253d1510)
    if '\\' in tur_253d1510 or any(ord(Araf_xëyma) < 32 or ord(Araf_xëyma) == 127 for Araf_xëyma in tur_253d1510):
        raise ValueError('잘못된 takku_xéewël Yoonu_jëmale 문자')
    if samp_Yoonu_jëmale and (len(('/lib/' + tur_253d1510).encode()) > 63 or tur_253d1510 in ('한국어.py', 'takku_xéewël.py')):
        raise ValueError('takku_xéewël Yoonu_jëmale 제한 또는 xayma_bi_teew daaray_téere 충돌: ' + tur_253d1510)
    return tur_253d1510


def 압축풀기(bara_denc_dugal_xabaar_tur, mbir, tur_253d1510, taalif_xëyma):
    파일들 = {}
    명세들 = []
    def 추가(Yoonu_jëmale, Këmb_xëyma):
        wéral_Yoonu_jëmale_f98b46e1(Yoonu_jëmale)
        if Yoonu_jëmale in 파일들:
            raise ValueError('중복 takku_xéewël Yoonu_jëmale: ' + Yoonu_jëmale)
        if len(Këmb_xëyma) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Yoonu_jëmale)
        Këmb_xëyma.decode('utf-8')
        파일들[Yoonu_jëmale] = Këmb_xëyma
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 Cosaan_tëralinuy_pàcc 16개·합계 64 KiB 이하여야 합니다.')
    if bara_denc_dugal_xabaar_tur.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(mbir)) as takku_xéewël:
            항목들 = takku_xéewël.infolist()
            if len(항목들) > 256 or sum(dugal_xabaar_xëyma.file_size for dugal_xabaar_xëyma in 항목들) > 1048576:
                raise ValueError('denc_xëyma yewwi_Dencukaay tolluwaay 제한 초과')
            ay_lim = [dugal_xabaar_xëyma for dugal_xabaar_xëyma in 항목들 if dugal_xabaar_xëyma.filename.endswith('.dist-info/WHEEL')]
            if len(ay_lim) != 1:
                raise ValueError('wheel ay_xëyma 명세가 필요합니다.')
            ay_xëyma = email.parser.Parser().parsestr(takku_xéewël.read(ay_lim[0]).decode())
            if ay_xëyma.get('Root-Is-Purelib', '').lower() != 'true' or not bara_denc_dugal_xabaar_tur.endswith('-none-any.whl'):
                raise ValueError('C ñàmbaas_xëyma·플랫폼 전용 wheel은 지원하지 않습니다.')
            for dugal_xabaar_xëyma in 항목들:
                Yoonu_jëmale = dugal_xabaar_xëyma.filename.rstrip('/')
                wéral_Yoonu_jëmale_f98b46e1(Yoonu_jëmale, False)
                if (dugal_xabaar_xëyma.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if dugal_xabaar_xëyma.filename.endswith('/'):
                    continue
                if '.dist-info/' in Yoonu_jëmale:
                    if Yoonu_jëmale.endswith('/METADATA'):
                        명세들.append(takku_xéewël.read(dugal_xabaar_xëyma).decode())
                    continue
                if not Yoonu_jëmale.endswith('.py') or '.data/' in Yoonu_jëmale:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Yoonu_jëmale)
                추가(Yoonu_jëmale, takku_xéewël.read(dugal_xabaar_xëyma))
    elif bara_denc_dugal_xabaar_tur.endswith('.tar.gz') and tur_253d1510.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py def_ndigel 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(mbir), mode='r|gz') as takku_xéewël:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for dugal_xabaar_xëyma in takku_xéewël:
                항목수 += 1
                전체크기 += dugal_xabaar_xëyma.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('denc_xëyma yewwi_Dencukaay tolluwaay 제한 초과')
                wéral_Yoonu_jëmale_f98b46e1(dugal_xabaar_xëyma.name, False)
                부분들 = dugal_xabaar_xëyma.name.split('/')
                뿌리들.add(부분들[0])
                if dugal_xabaar_xëyma.isdir():
                    continue
                if not dugal_xabaar_xëyma.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython Cosaan_tëralinuy_pàcc 배포형')
                Yoonu_jëmale = '/'.join(부분들[1:])
                Këmb_xëyma = takku_xéewël.extractfile(dugal_xabaar_xëyma).read()
                if Yoonu_jëmale.endswith('PKG-INFO'):
                    명세들.append(Këmb_xëyma.decode())
                elif Yoonu_jëmale.endswith('.py') and Yoonu_jëmale not in ('setup.py',):
                    추가(Yoonu_jëmale, Këmb_xëyma)
                elif '.egg-info/' not in Yoonu_jëmale and not Yoonu_jëmale.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Yoonu_jëmale)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* Cosaan_tëralinuy_pàcc 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != tur_253d1510 or 명세.get('Version') != taalif_xëyma:
        raise ValueError('배포 메타데이터의 tur_253d1510·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(dëkkuwaay, 한도):
    if not dëkkuwaay.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(dëkkuwaay, timeout=30) as tontu:
        if not tontu.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 dëkkuwaay toxal_xëyma')
        mbir = tontu.read(한도 + 1)
    if len(mbir) > 한도:
        raise ValueError('배포 bara_denc tolluwaay 제한 초과')
    return mbir


def toxal_takku_xéewël(tur_253d1510, taalif_xëyma, 파일들, 출처):
    명세 = {'name': tur_253d1510, 'version': taalif_xëyma, 'source': 출처, 'files': [
        {'path': Yoonu_jëmale, 'size': len(mbir), 'sha256': hashlib.sha256(mbir).hexdigest()}
        for Yoonu_jëmale, mbir in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('takku_xéewël 명세 tolluwaay 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[dugal_xabaar_xëyma['path']] for dugal_xabaar_xëyma in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Yoonu_jëmale, 오프라인=False):
        자신.Yoonu_jëmale = Path(Yoonu_jëmale)
        자신.Yoonu_jëmale.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def jël_matuwaay(자신, 요청):
        tur_253d1510, taalif_xëyma = 요청해석(요청)
        열쇠 = tur_253d1510 + ('==' + taalif_xëyma if taalif_xëyma else '')
        làq_Yoonu_jëmale = 자신.Yoonu_jëmale / (열쇠 + '.json')
        배포경로 = 자신.Yoonu_jëmale / (열쇠 + '.archive')
        if làq_Yoonu_jëmale.is_file() and 배포경로.is_file():
            làq_Dënk = json.loads(làq_Yoonu_jëmale.read_text())
            mbir = 배포경로.read_bytes()
            if hashlib.sha256(mbir).hexdigest() != làq_Dënk['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 takku_xéewël: ' + 요청)
            dëkkuwaay = 'https://pypi.org/pypi/' + tur_253d1510 + ('/' + taalif_xëyma if taalif_xëyma else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(dëkkuwaay, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [dugal_xabaar_xëyma for dugal_xabaar_xëyma in msinfo32_exe['urls'] if not dugal_xabaar_xëyma.get('yanked') and dugal_xabaar_xëyma['filename'].endswith('-none-any.whl')]
            if not 후보 and tur_253d1510.startswith('micropython-'):
                후보 = [dugal_xabaar_xëyma for dugal_xabaar_xëyma in msinfo32_exe['urls'] if not dugal_xabaar_xëyma.get('yanked') and dugal_xabaar_xëyma['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            tanneef_xëyma = 후보[0]
            mbir = 웹읽기(tanneef_xëyma['url'], 4194304)
            if hashlib.sha256(mbir).hexdigest() != tanneef_xëyma['digests']['sha256']:
                raise ValueError('PyPI 배포 bara_denc SHA-256 불일치')
            làq_Dënk = {'name': tur_253d1510, 'version': msinfo32_exe['info']['version'], 'filename': tanneef_xëyma['filename'],
                    'url': tanneef_xëyma['url'], 'sha256': tanneef_xëyma['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(làq_Dënk['filename'], mbir, tur_253d1510, làq_Dënk['version'])
            배포경로.write_bytes(mbir)
            làq_Yoonu_jëmale.write_text(json.dumps(làq_Dënk, ensure_ascii=False, indent=2) + '\n')
        if làq_Dënk['name'] != tur_253d1510 or taalif_xëyma and làq_Dënk['version'] != taalif_xëyma:
            raise ValueError('저장소 tur_253d1510·버전 불일치')
        파일들 = 압축풀기(làq_Dënk['filename'], mbir, tur_253d1510, làq_Dënk['version'])
        return toxal_takku_xéewël(tur_253d1510, làq_Dënk['version'], 파일들, làq_Dënk['url'])


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
                raise ValueError('잘못된 takku_xéewël 요청')
            tontu = 자신.server.저장소.jël_matuwaay(요청[:-1].decode('ascii'))
        except Exception as njumte:
            머리 = json.dumps({'error': str(njumte)[:500]}, ensure_ascii=False).encode()
            tontu = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(tontu)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Yoonu_jëmale=None, 오프라인=False):
        자신.dëggu_xëyma = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.dëggu_xëyma.allow_reuse_address = True
        자신.dëggu_xëyma.server_bind()
        자신.dëggu_xëyma.server_activate()
        자신.dëggu_xëyma.저장소 = 꾸러미저장소(Yoonu_jëmale or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.dëggu_xëyma.server_address[1]
        자신.buumug_jokkale_xëyma = threading.Thread(target=자신.dëggu_xëyma.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.buumug_jokkale_xëyma.start()
        return 자신

    def __exit__(자신, *인수):
        자신.dëggu_xëyma.shutdown()
        자신.dëggu_xëyma.server_close()
        자신.buumug_jokkale_xëyma.join(timeout=2)


def daw():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='def_ndigel 없이 호환 배포 파일을 내려받아 검사·Store_xëyma')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        mbir = 꾸러미저장소(인수.cache, 인수.offline).jël_matuwaay(인수.fetch)
        print('takku_xéewël jël_matuwaay 완료:', 인수.fetch, len(mbir), 'okte_xëyma')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('takku_xéewël 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.buumug_jokkale_xëyma.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    daw()
