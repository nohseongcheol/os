#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 Girka_Daraja·실행한다."""
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
        raise ValueError('dami Suna 또는 Suna==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def inganta_Hanyar_shiga(Suna, Girkawa_Hanyar_shiga=True):
    Hanyar_shiga = PurePosixPath(Suna)
    if Hanyar_shiga.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Suna.split('/')):
        raise ValueError('허용하지 않는 dami Hanyar_shiga: ' + Suna)
    if '\\' in Suna or any(ord(Harafi_Daraja) < 32 or ord(Harafi_Daraja) == 127 for Harafi_Daraja in Suna):
        raise ValueError('잘못된 dami Hanyar_shiga 문자')
    if Girkawa_Hanyar_shiga and (len(('/lib/' + Suna).encode()) > 63 or Suna in ('한국어.py', 'dami.py')):
        raise ValueError('dami Hanyar_shiga 제한 또는 Tanadaddiyar_daraja laburare 충돌: ' + Suna)
    return Suna


def 압축풀기(Fayil_Mashigar_bayanai_Suna, Tarin_bayani, Suna, siga_Daraja):
    파일들 = {}
    명세들 = []
    def 추가(Hanyar_shiga, kunshiya_Daraja):
        inganta_Hanyar_shiga(Hanyar_shiga)
        if Hanyar_shiga in 파일들:
            raise ValueError('중복 dami Hanyar_shiga: ' + Hanyar_shiga)
        if len(kunshiya_Daraja) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Hanyar_shiga)
        kunshiya_Daraja.decode('utf-8')
        파일들[Hanyar_shiga] = kunshiya_Daraja
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 tushe_Li_irabin_tarin_bayanai 16개·합계 64 KiB 이하여야 합니다.')
    if Fayil_Mashigar_bayanai_Suna.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(Tarin_bayani)) as dami:
            항목들 = dami.infolist()
            if len(항목들) > 256 or sum(Mashigar_bayanai_Daraja.file_size for Mashigar_bayanai_Daraja in 항목들) > 1048576:
                raise ValueError('Rumbun_ajiya_Daraja saka_Wurin_adana Girma 제한 초과')
            Kes_Jeri = [Mashigar_bayanai_Daraja for Mashigar_bayanai_Daraja in 항목들 if Mashigar_bayanai_Daraja.filename.endswith('.dist-info/WHEEL')]
            if len(Kes_Jeri) != 1:
                raise ValueError('wheel Kes_Daraja 명세가 필요합니다.')
            Kes_Daraja = email.parser.Parser().parsestr(dami.read(Kes_Jeri[0]).decode())
            if Kes_Daraja.get('Root-Is-Purelib', '').lower() != 'true' or not Fayil_Mashigar_bayanai_Suna.endswith('-none-any.whl'):
                raise ValueError('C faɗi_Daraja·플랫폼 전용 wheel은 지원하지 않습니다.')
            for Mashigar_bayanai_Daraja in 항목들:
                Hanyar_shiga = Mashigar_bayanai_Daraja.filename.rstrip('/')
                inganta_Hanyar_shiga(Hanyar_shiga, False)
                if (Mashigar_bayanai_Daraja.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if Mashigar_bayanai_Daraja.filename.endswith('/'):
                    continue
                if '.dist-info/' in Hanyar_shiga:
                    if Hanyar_shiga.endswith('/METADATA'):
                        명세들.append(dami.read(Mashigar_bayanai_Daraja).decode())
                    continue
                if not Hanyar_shiga.endswith('.py') or '.data/' in Hanyar_shiga:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Hanyar_shiga)
                추가(Hanyar_shiga, dami.read(Mashigar_bayanai_Daraja))
    elif Fayil_Mashigar_bayanai_Suna.endswith('.tar.gz') and Suna.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py gudanar_Umarni 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(Tarin_bayani), mode='r|gz') as dami:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for Mashigar_bayanai_Daraja in dami:
                항목수 += 1
                전체크기 += Mashigar_bayanai_Daraja.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Rumbun_ajiya_Daraja saka_Wurin_adana Girma 제한 초과')
                inganta_Hanyar_shiga(Mashigar_bayanai_Daraja.name, False)
                부분들 = Mashigar_bayanai_Daraja.name.split('/')
                뿌리들.add(부분들[0])
                if Mashigar_bayanai_Daraja.isdir():
                    continue
                if not Mashigar_bayanai_Daraja.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython tushe_Li_irabin_tarin_bayanai 배포형')
                Hanyar_shiga = '/'.join(부분들[1:])
                kunshiya_Daraja = dami.extractfile(Mashigar_bayanai_Daraja).read()
                if Hanyar_shiga.endswith('PKG-INFO'):
                    명세들.append(kunshiya_Daraja.decode())
                elif Hanyar_shiga.endswith('.py') and Hanyar_shiga not in ('setup.py',):
                    추가(Hanyar_shiga, kunshiya_Daraja)
                elif '.egg-info/' not in Hanyar_shiga and not Hanyar_shiga.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Hanyar_shiga)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* tushe_Li_irabin_tarin_bayanai 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Suna or 명세.get('Version') != siga_Daraja:
        raise ValueError('배포 메타데이터의 Suna·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(imel, 한도):
    if not imel.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(imel, timeout=30) as mayar_da_martani:
        if not mayar_da_martani.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 imel Matsar_da_Daraja')
        Tarin_bayani = mayar_da_martani.read(한도 + 1)
    if len(Tarin_bayani) > 한도:
        raise ValueError('배포 Fayil Girma 제한 초과')
    return Tarin_bayani


def Gusar_da_dami(Suna, siga_Daraja, 파일들, 출처):
    명세 = {'name': Suna, 'version': siga_Daraja, 'source': 출처, 'files': [
        {'path': Hanyar_shiga, 'size': len(Tarin_bayani), 'sha256': hashlib.sha256(Tarin_bayani).hexdigest()}
        for Hanyar_shiga, Tarin_bayani in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('dami 명세 Girma 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[Mashigar_bayanai_Daraja['path']] for Mashigar_bayanai_Daraja in 명세['files'])


class dami_matattara:
    def __init__(자신, Hanyar_shiga, kimiyar_bayanai_Wajen_layi=False):
        자신.Hanyar_shiga = Path(Hanyar_shiga)
        자신.Hanyar_shiga.mkdir(parents=True, exist_ok=True)
        자신.kimiyar_bayanai_Wajen_layi = kimiyar_bayanai_Wajen_layi

    def Shirya(자신, 요청):
        Suna, siga_Daraja = 요청해석(요청)
        열쇠 = Suna + ('==' + siga_Daraja if siga_Daraja else '')
        logu_Hanyar_shiga = 자신.Hanyar_shiga / (열쇠 + '.json')
        배포경로 = 자신.Hanyar_shiga / (열쇠 + '.archive')
        if logu_Hanyar_shiga.is_file() and 배포경로.is_file():
            logu_naɗa = json.loads(logu_Hanyar_shiga.read_text())
            Tarin_bayani = 배포경로.read_bytes()
            if hashlib.sha256(Tarin_bayani).hexdigest() != logu_naɗa['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.kimiyar_bayanai_Wajen_layi:
                raise ValueError('kimiyar_bayanai_Wajen_layi 저장소에 없는 dami: ' + 요청)
            imel = 'https://pypi.org/pypi/' + Suna + ('/' + siga_Daraja if siga_Daraja else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(imel, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [Mashigar_bayanai_Daraja for Mashigar_bayanai_Daraja in msinfo32_exe['urls'] if not Mashigar_bayanai_Daraja.get('yanked') and Mashigar_bayanai_Daraja['filename'].endswith('-none-any.whl')]
            if not 후보 and Suna.startswith('micropython-'):
                후보 = [Mashigar_bayanai_Daraja for Mashigar_bayanai_Daraja in msinfo32_exe['urls'] if not Mashigar_bayanai_Daraja.get('yanked') and Mashigar_bayanai_Daraja['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            bangaren_zaɓi_Daraja = 후보[0]
            Tarin_bayani = 웹읽기(bangaren_zaɓi_Daraja['url'], 4194304)
            if hashlib.sha256(Tarin_bayani).hexdigest() != bangaren_zaɓi_Daraja['digests']['sha256']:
                raise ValueError('PyPI 배포 Fayil SHA-256 불일치')
            logu_naɗa = {'name': Suna, 'version': msinfo32_exe['info']['version'], 'filename': bangaren_zaɓi_Daraja['filename'],
                    'url': bangaren_zaɓi_Daraja['url'], 'sha256': bangaren_zaɓi_Daraja['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(logu_naɗa['filename'], Tarin_bayani, Suna, logu_naɗa['version'])
            배포경로.write_bytes(Tarin_bayani)
            logu_Hanyar_shiga.write_text(json.dumps(logu_naɗa, ensure_ascii=False, indent=2) + '\n')
        if logu_naɗa['name'] != Suna or siga_Daraja and logu_naɗa['version'] != siga_Daraja:
            raise ValueError('저장소 Suna·버전 불일치')
        파일들 = 압축풀기(logu_naɗa['filename'], Tarin_bayani, Suna, logu_naɗa['version'])
        return Gusar_da_dami(Suna, logu_naɗa['version'], 파일들, logu_naɗa['url'])


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
                raise ValueError('잘못된 dami 요청')
            mayar_da_martani = 자신.server.저장소.Shirya(요청[:-1].decode('ascii'))
        except Exception as Kuskure:
            머리 = json.dumps({'error': str(Kuskure)[:500]}, ensure_ascii=False).encode()
            mayar_da_martani = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(mayar_da_martani)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, lambar_kafa=8027, Hanyar_shiga=None, kimiyar_bayanai_Wajen_layi=False):
        자신.Saba_Daraja = socketserver.TCPServer(('127.0.0.1', lambar_kafa), 꾸러미요청, bind_and_activate=False)
        자신.Saba_Daraja.allow_reuse_address = True
        자신.Saba_Daraja.server_bind()
        자신.Saba_Daraja.server_activate()
        자신.Saba_Daraja.저장소 = dami_matattara(Hanyar_shiga or 기준/'build/pip-cache', kimiyar_bayanai_Wajen_layi)
        자신.lambar_kafa = 자신.Saba_Daraja.server_address[1]
        자신.hira_Daraja = threading.Thread(target=자신.Saba_Daraja.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.hira_Daraja.start()
        return 자신

    def __exit__(자신, *인수):
        자신.Saba_Daraja.shutdown()
        자신.Saba_Daraja.server_close()
        자신.hira_Daraja.join(timeout=2)


def Tafiyar_da():
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('--port', type=int, default=8027)
    tatsar_manhaja_48ee4b1b.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    tatsar_manhaja_48ee4b1b.add_argument('--offline', action='store_true')
    tatsar_manhaja_48ee4b1b.add_argument('--fetch', help='gudanar_Umarni 없이 호환 배포 파일을 내려받아 검사·Ajiye_Daraja')
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    if 인수.fetch:
        Tarin_bayani = dami_matattara(인수.cache, 인수.offline).Shirya(인수.fetch)
        print('dami Shirya 완료:', 인수.fetch, len(Tarin_bayani), 'bayit_Daraja')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('dami 중계: 127.0.0.1:' + str(중계.lambar_kafa), flush=True)
        try:
            중계.hira_Daraja.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Tafiyar_da()
