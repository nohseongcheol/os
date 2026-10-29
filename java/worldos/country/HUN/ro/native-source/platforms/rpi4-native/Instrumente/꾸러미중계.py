#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instala_VALUE·실행한다."""
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

Project_rădăcină = Path(__file__).resolve().parents[1]


def analiza_cerere(cerere):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', cerere)
    if not 맞음:
        raise ValueError('set Nume 또는 Nume==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def valida_cale(Nume, instalare_cale=True):
    Cale = PurePosixPath(Nume)
    if Cale.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nume.split('/')):
        raise ValueError('허용하지 않는 set Cale: ' + Nume)
    if '\\' in Nume or any(ord(caracter_VALUE) < 32 or ord(caracter_VALUE) == 127 for caracter_VALUE in Nume):
        raise ValueError('잘못된 set Cale 문자')
    if instalare_cale and (len(('/lib/' + Nume).encode()) > 63 or Nume in ('Română.py', 'set.py')):
        raise ValueError('set Cale 제한 또는 valoare_implicită bibliotecă 충돌: ' + Nume)
    return Nume


def decomprima(Fișier_intrare_nume, date, Nume, versiune_VALUE):
    파일들 = {}
    명세들 = []
    def adăuga_intrare(Cale, Conținut_VALUE):
        valida_cale(Cale)
        if Cale in 파일들:
            raise ValueError('중복 set Cale: ' + Cale)
        if len(Conținut_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Cale)
        Conținut_VALUE.decode('utf-8')
        파일들[Cale] = Conținut_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 sursă_arborescență 16개·total_VALUE 64 KiB 이하여야 합니다.')
    if Fișier_intrare_nume.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(date)) as set:
            항목들 = set.infolist()
            if len(항목들) > 256 or sum(intrare_VALUE.file_size for intrare_VALUE in 항목들) > 1048576:
                raise ValueError('Arhivă_VALUE lansa_Stocare Mărime 제한 초과')
            caz_Listă = [intrare_VALUE for intrare_VALUE in 항목들 if intrare_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(caz_Listă) != 1:
                raise ValueError('wheel caz_VALUE 명세가 필요합니다.')
            caz_VALUE = email.parser.Parser().parsestr(set.read(caz_Listă[0]).decode())
            if caz_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not Fișier_intrare_nume.endswith('-none-any.whl'):
                raise ValueError('C extensie_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for intrare_VALUE in 항목들:
                Cale = intrare_VALUE.filename.rstrip('/')
                valida_cale(Cale, False)
                if (intrare_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if intrare_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in Cale:
                    if Cale.endswith('/METADATA'):
                        명세들.append(set.read(intrare_VALUE).decode())
                    continue
                if not Cale.endswith('.py') or '.data/' in Cale:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Cale)
                adăuga_intrare(Cale, set.read(intrare_VALUE))
    elif Fișier_intrare_nume.endswith('.tar.gz') and Nume.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py executa_comandă 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(date), mode='r|gz') as set:
            뿌리들 = set()
            intrare_COUNT = 0
            total_dimensiona = 0
            for intrare_VALUE in set:
                intrare_COUNT += 1
                total_dimensiona += intrare_VALUE.size
                if intrare_COUNT > 256 or total_dimensiona > 1048576:
                    raise ValueError('Arhivă_VALUE lansa_Stocare Mărime 제한 초과')
                valida_cale(intrare_VALUE.name, False)
                부분들 = intrare_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if intrare_VALUE.isdir():
                    continue
                if not intrare_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython sursă_arborescență 배포형')
                Cale = '/'.join(부분들[1:])
                Conținut_VALUE = set.extractfile(intrare_VALUE).read()
                if Cale.endswith('PKG-INFO'):
                    명세들.append(Conținut_VALUE.decode())
                elif Cale.endswith('.py') and Cale not in ('setup.py',):
                    adăuga_intrare(Cale, Conținut_VALUE)
                elif '.egg-info/' not in Cale and not Cale.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Cale)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 rădăcină_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* sursă_arborescență 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if analiza_cerere(명세.get('Name', ''))[0] != Nume or 명세.get('Version') != versiune_VALUE:
        raise ValueError('배포 메타데이터의 Nume·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(adresa, 한도):
    if not adresa.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(adresa, timeout=30) as replică:
        if not replică.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 adresa muta_VALUE_83b651b8')
        date = replică.read(한도 + 1)
    if len(date) > 한도:
        raise ValueError('배포 Fișier Mărime 제한 초과')
    return date


def Transfer_set(Nume, versiune_VALUE, 파일들, 출처):
    명세 = {'name': Nume, 'version': versiune_VALUE, 'source': 출처, 'files': [
        {'path': Cale, 'size': len(date), 'sha256': hashlib.sha256(date).hexdigest()}
        for Cale, date in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('set 명세 Mărime 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[intrare_VALUE['path']] for intrare_VALUE in 명세['files'])


class set_depozit:
    def __init__(자신, Cale, sisteme_de_informații_offline=False):
        자신.Cale = Path(Cale)
        자신.Cale.mkdir(parents=True, exist_ok=True)
        자신.sisteme_de_informații_offline = sisteme_de_informații_offline

    def Pregătiți(자신, cerere):
        Nume, versiune_VALUE = analiza_cerere(cerere)
        열쇠 = Nume + ('==' + versiune_VALUE if versiune_VALUE else '')
        LOG_cale = 자신.Cale / (열쇠 + '.json')
        배포경로 = 자신.Cale / (열쇠 + '.archive')
        if LOG_cale.is_file() and 배포경로.is_file():
            LOG_RECORD = json.loads(LOG_cale.read_text())
            date = 배포경로.read_bytes()
            if hashlib.sha256(date).hexdigest() != LOG_RECORD['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.sisteme_de_informații_offline:
                raise ValueError('sisteme_de_informații_offline 저장소에 없는 set: ' + cerere)
            adresa = 'https://pypi.org/pypi/' + Nume + ('/' + versiune_VALUE if versiune_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(adresa, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [intrare_VALUE for intrare_VALUE in msinfo32_exe['urls'] if not intrare_VALUE.get('yanked') and intrare_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Nume.startswith('micropython-'):
                후보 = [intrare_VALUE for intrare_VALUE in msinfo32_exe['urls'] if not intrare_VALUE.get('yanked') and intrare_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            selecție_VALUE = 후보[0]
            date = 웹읽기(selecție_VALUE['url'], 4194304)
            if hashlib.sha256(date).hexdigest() != selecție_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Fișier SHA-256 불일치')
            LOG_RECORD = {'name': Nume, 'version': msinfo32_exe['info']['version'], 'filename': selecție_VALUE['filename'],
                    'url': selecție_VALUE['url'], 'sha256': selecție_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            decomprima(LOG_RECORD['filename'], date, Nume, LOG_RECORD['version'])
            배포경로.write_bytes(date)
            LOG_cale.write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_RECORD['name'] != Nume or versiune_VALUE and LOG_RECORD['version'] != versiune_VALUE:
            raise ValueError('depozit_rădăcină Nume·버전 불일치')
        파일들 = decomprima(LOG_RECORD['filename'], date, Nume, LOG_RECORD['version'])
        return Transfer_set(Nume, LOG_RECORD['version'], 파일들, LOG_RECORD['url'])


class set_cerere(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            cerere = bytearray()
            while b'\n' not in cerere and len(cerere) < 100:
                조각 = 자신.request.recv(100 - len(cerere))
                if not 조각:
                    return
                cerere.extend(조각)
            if not cerere.endswith(b'\n') or cerere.count(b'\n') != 1:
                raise ValueError('잘못된 set cerere')
            replică = 자신.server.depozit_rădăcină.Pregătiți(cerere[:-1].decode('ascii'))
        except Exception as eroare:
            머리 = json.dumps({'error': str(eroare)[:500]}, ensure_ascii=False).encode()
            replică = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(replică)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, număr_port=8027, Cale=None, sisteme_de_informații_offline=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', număr_port), set_cerere, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.depozit_rădăcină = set_depozit(Cale or Project_rădăcină/'build/pip-cache', sisteme_de_informații_offline)
        자신.număr_port = 자신.server_VALUE.server_address[1]
        자신.fir_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.fir_VALUE.start()
        return 자신

    def __exit__(자신, *Argumente):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.fir_VALUE.join(timeout=2)


def Pornește():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=Project_rădăcină/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='executa_comandă 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Argumente = parser_48ee4b1b.parse_args()
    if Argumente.fetch:
        date = set_depozit(Argumente.cache, Argumente.offline).Pregătiți(Argumente.fetch)
        print('set Pregătiți 완료:', Argumente.fetch, len(date), 'byte_VALUE')
        return
    with 꾸러미중계(Argumente.port, Argumente.cache, Argumente.offline) as 중계:
        print('set 중계: 127.0.0.1:' + str(중계.număr_port), flush=True)
        try:
            중계.fir_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Pornește()
