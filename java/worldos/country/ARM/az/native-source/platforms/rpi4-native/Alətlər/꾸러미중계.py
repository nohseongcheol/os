#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 quraşdır_VALUE·실행한다."""
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

Project_kök = Path(__file__).resolve().parents[1]


def parselləmək_HTTP_sorğusu(HTTP_sorğusu):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', HTTP_sorğusu)
    if not 맞음:
        raise ValueError('paket Ad 또는 Ad==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def təsdiqlə_yol(Ad, quraşdırma_yol=True):
    Cığır = PurePosixPath(Ad)
    if Cığır.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Ad.split('/')):
        raise ValueError('허용하지 않는 paket Cığır: ' + Ad)
    if '\\' in Ad or any(ord(simvol_VALUE_068c2631) < 32 or ord(simvol_VALUE_068c2631) == 127 for simvol_VALUE_068c2631 in Ad):
        raise ValueError('잘못된 paket Cığır 문자')
    if quraşdırma_yol and (len(('/lib/' + Ad).encode()) > 63 or Ad in ('한국어.py', 'paket.py')):
        raise ValueError('paket Cığır 제한 또는 standart_qiymət kitabxana 충돌: ' + Ad)
    return Ad


def 압축풀기(fayl_daxiletmə_ad, verilənlər, Ad, versiya_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(Cığır, Məzmun_VALUE):
        təsdiqlə_yol(Cığır)
        if Cığır in 파일들:
            raise ValueError('중복 paket Cığır: ' + Cığır)
        if len(Məzmun_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Cığır)
        Məzmun_VALUE.decode('utf-8')
        파일들[Cığır] = Məzmun_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 mənbə_ağac 16개·합계 64 KiB 이하여야 합니다.')
    if fayl_daxiletmə_ad.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(verilənlər)) as paket:
            항목들 = paket.infolist()
            if len(항목들) > 256 or sum(daxiletmə_VALUE.file_size for daxiletmə_VALUE in 항목들) > 1048576:
                raise ValueError('Arxiv_VALUE burax_Yaddaş Böyüklük 제한 초과')
            müqavilə_Siyahı = [daxiletmə_VALUE for daxiletmə_VALUE in 항목들 if daxiletmə_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(müqavilə_Siyahı) != 1:
                raise ValueError('wheel müqavilə_VALUE 명세가 필요합니다.')
            müqavilə_VALUE = email.parser.Parser().parsestr(paket.read(müqavilə_Siyahı[0]).decode())
            if müqavilə_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not fayl_daxiletmə_ad.endswith('-none-any.whl'):
                raise ValueError('C genişlənmə_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for daxiletmə_VALUE in 항목들:
                Cığır = daxiletmə_VALUE.filename.rstrip('/')
                təsdiqlə_yol(Cığır, False)
                if (daxiletmə_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if daxiletmə_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in Cığır:
                    if Cığır.endswith('/METADATA'):
                        명세들.append(paket.read(daxiletmə_VALUE).decode())
                    continue
                if not Cığır.endswith('.py') or '.data/' in Cığır:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Cığır)
                추가(Cığır, paket.read(daxiletmə_VALUE))
    elif fayl_daxiletmə_ad.endswith('.tar.gz') and Ad.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py icra_etmək_əmr 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(verilənlər), mode='r|gz') as paket:
            뿌리들 = set()
            daxiletmə_COUNT = 0
            전체크기 = 0
            for daxiletmə_VALUE in paket:
                daxiletmə_COUNT += 1
                전체크기 += daxiletmə_VALUE.size
                if daxiletmə_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Arxiv_VALUE burax_Yaddaş Böyüklük 제한 초과')
                təsdiqlə_yol(daxiletmə_VALUE.name, False)
                부분들 = daxiletmə_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if daxiletmə_VALUE.isdir():
                    continue
                if not daxiletmə_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython mənbə_ağac 배포형')
                Cığır = '/'.join(부분들[1:])
                Məzmun_VALUE = paket.extractfile(daxiletmə_VALUE).read()
                if Cığır.endswith('PKG-INFO'):
                    명세들.append(Məzmun_VALUE.decode())
                elif Cığır.endswith('.py') and Cığır not in ('setup.py',):
                    추가(Cığır, Məzmun_VALUE)
                elif '.egg-info/' not in Cığır and not Cığır.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Cığır)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 kök_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* mənbə_ağac 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if parselləmək_HTTP_sorğusu(명세.get('Name', ''))[0] != Ad or 명세.get('Version') != versiya_VALUE:
        raise ValueError('배포 메타데이터의 Ad·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ünvan, 한도):
    if not ünvan.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ünvan, timeout=30) as cavab:
        if not cavab.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ünvan hərəkət_etdir_VALUE')
        verilənlər = cavab.read(한도 + 1)
    if len(verilənlər) > 한도:
        raise ValueError('배포 FAYL Böyüklük 제한 초과')
    return verilənlər


def ötürmə_paket(Ad, versiya_VALUE, 파일들, 출처):
    명세 = {'name': Ad, 'version': versiya_VALUE, 'source': 출처, 'files': [
        {'path': Cığır, 'size': len(verilənlər), 'sha256': hashlib.sha256(verilənlər).hexdigest()}
        for Cığır, verilənlər in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('paket 명세 Böyüklük 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[daxiletmə_VALUE['path']] for daxiletmə_VALUE in 명세['files'])


class paket_anbar:
    def __init__(자신, Cığır, 오프라인=False):
        자신.Cığır = Path(Cığır)
        자신.Cığır.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Hazırla(자신, HTTP_sorğusu):
        Ad, versiya_VALUE = parselləmək_HTTP_sorğusu(HTTP_sorğusu)
        열쇠 = Ad + ('==' + versiya_VALUE if versiya_VALUE else '')
        LOG_yol = 자신.Cığır / (열쇠 + '.json')
        배포경로 = 자신.Cığır / (열쇠 + '.archive')
        if LOG_yol.is_file() and 배포경로.is_file():
            LOG_yaz = json.loads(LOG_yol.read_text())
            verilənlər = 배포경로.read_bytes()
            if hashlib.sha256(verilənlər).hexdigest() != LOG_yaz['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 paket: ' + HTTP_sorğusu)
            ünvan = 'https://pypi.org/pypi/' + Ad + ('/' + versiya_VALUE if versiya_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ünvan, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [daxiletmə_VALUE for daxiletmə_VALUE in msinfo32_exe['urls'] if not daxiletmə_VALUE.get('yanked') and daxiletmə_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Ad.startswith('micropython-'):
                후보 = [daxiletmə_VALUE for daxiletmə_VALUE in msinfo32_exe['urls'] if not daxiletmə_VALUE.get('yanked') and daxiletmə_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            seçilmiş_sahə_VALUE = 후보[0]
            verilənlər = 웹읽기(seçilmiş_sahə_VALUE['url'], 4194304)
            if hashlib.sha256(verilənlər).hexdigest() != seçilmiş_sahə_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 FAYL SHA-256 불일치')
            LOG_yaz = {'name': Ad, 'version': msinfo32_exe['info']['version'], 'filename': seçilmiş_sahə_VALUE['filename'],
                    'url': seçilmiş_sahə_VALUE['url'], 'sha256': seçilmiş_sahə_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_yaz['filename'], verilənlər, Ad, LOG_yaz['version'])
            배포경로.write_bytes(verilənlər)
            LOG_yol.write_text(json.dumps(LOG_yaz, ensure_ascii=False, indent=2) + '\n')
        if LOG_yaz['name'] != Ad or versiya_VALUE and LOG_yaz['version'] != versiya_VALUE:
            raise ValueError('anbar_kök Ad·버전 불일치')
        파일들 = 압축풀기(LOG_yaz['filename'], verilənlər, Ad, LOG_yaz['version'])
        return ötürmə_paket(Ad, LOG_yaz['version'], 파일들, LOG_yaz['url'])


class paket_HTTP_sorğusu(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            HTTP_sorğusu = bytearray()
            while b'\n' not in HTTP_sorğusu and len(HTTP_sorğusu) < 100:
                조각 = 자신.request.recv(100 - len(HTTP_sorğusu))
                if not 조각:
                    return
                HTTP_sorğusu.extend(조각)
            if not HTTP_sorğusu.endswith(b'\n') or HTTP_sorğusu.count(b'\n') != 1:
                raise ValueError('잘못된 paket HTTP_sorğusu')
            cavab = 자신.server.anbar_kök.Hazırla(HTTP_sorğusu[:-1].decode('ascii'))
        except Exception as XƏTA:
            머리 = json.dumps({'error': str(XƏTA)[:500]}, ensure_ascii=False).encode()
            cavab = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(cavab)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Cığır=None, 오프라인=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', 접속번호), paket_HTTP_sorğusu, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.anbar_kök = paket_anbar(Cığır or Project_kök/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.server_VALUE.server_address[1]
        자신.axın_VALUE_5b72a632 = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.axın_VALUE_5b72a632.start()
        return 자신

    def __exit__(자신, *인수):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.axın_VALUE_5b72a632.join(timeout=2)


def İcra_Et():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=Project_kök/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='icra_etmək_əmr 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = parser_48ee4b1b.parse_args()
    if 인수.fetch:
        verilənlər = paket_anbar(인수.cache, 인수.offline).Hazırla(인수.fetch)
        print('paket Hazırla 완료:', 인수.fetch, len(verilənlər), 'bayt_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('paket 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.axın_VALUE_5b72a632.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    İcra_Et()
