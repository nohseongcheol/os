#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instalirati_VALUE·실행한다."""
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

projicirati_koijen = Path(__file__).resolve().parents[1]


def raščlanjivati_HTTP_zahtjev(HTTP_zahtjev):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', HTTP_zahtjev)
    if not 맞음:
        raise ValueError('paket Naziv 또는 Naziv==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ovjeriti_put(Naziv, instalacija_put=True):
    Putanja = PurePosixPath(Naziv)
    if Putanja.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Naziv.split('/')):
        raise ValueError('허용하지 않는 paket Putanja: ' + Naziv)
    if '\\' in Naziv or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in Naziv):
        raise ValueError('잘못된 paket Putanja 문자')
    if instalacija_put and (len(('/lib/' + Naziv).encode()) > 63 or Naziv in ('한국어.py', 'paket.py')):
        raise ValueError('paket Putanja 제한 또는 zadana_vrijednost biblioteka 충돌: ' + Naziv)
    return Naziv


def 압축풀기(fajl_unos_naziv, podaci, Naziv, verzija_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(Putanja, Sadržaj_VALUE):
        ovjeriti_put(Putanja)
        if Putanja in 파일들:
            raise ValueError('중복 paket Putanja: ' + Putanja)
        if len(Sadržaj_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Putanja)
        Sadržaj_VALUE.decode('utf-8')
        파일들[Putanja] = Sadržaj_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 izvor_stablo 16개·합계 64 KiB 이하여야 합니다.')
    if fajl_unos_naziv.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(podaci)) as paket:
            항목들 = paket.infolist()
            if len(항목들) > 256 or sum(unos_VALUE.file_size for unos_VALUE in 항목들) > 1048576:
                raise ValueError('Arhiva_VALUE izdanje_Pohrana Veličina 제한 초과')
            slučaj_spisak = [unos_VALUE for unos_VALUE in 항목들 if unos_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(slučaj_spisak) != 1:
                raise ValueError('wheel slučaj_VALUE 명세가 필요합니다.')
            slučaj_VALUE = email.parser.Parser().parsestr(paket.read(slučaj_spisak[0]).decode())
            if slučaj_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not fajl_unos_naziv.endswith('-none-any.whl'):
                raise ValueError('C ekstenzija_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for unos_VALUE in 항목들:
                Putanja = unos_VALUE.filename.rstrip('/')
                ovjeriti_put(Putanja, False)
                if (unos_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if unos_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in Putanja:
                    if Putanja.endswith('/METADATA'):
                        명세들.append(paket.read(unos_VALUE).decode())
                    continue
                if not Putanja.endswith('.py') or '.data/' in Putanja:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Putanja)
                추가(Putanja, paket.read(unos_VALUE))
    elif fajl_unos_naziv.endswith('.tar.gz') and Naziv.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Izvrši_komanda 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(podaci), mode='r|gz') as paket:
            뿌리들 = set()
            unos_COUNT = 0
            전체크기 = 0
            for unos_VALUE in paket:
                unos_COUNT += 1
                전체크기 += unos_VALUE.size
                if unos_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Arhiva_VALUE izdanje_Pohrana Veličina 제한 초과')
                ovjeriti_put(unos_VALUE.name, False)
                부분들 = unos_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if unos_VALUE.isdir():
                    continue
                if not unos_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython izvor_stablo 배포형')
                Putanja = '/'.join(부분들[1:])
                Sadržaj_VALUE = paket.extractfile(unos_VALUE).read()
                if Putanja.endswith('PKG-INFO'):
                    명세들.append(Sadržaj_VALUE.decode())
                elif Putanja.endswith('.py') and Putanja not in ('setup.py',):
                    추가(Putanja, Sadržaj_VALUE)
                elif '.egg-info/' not in Putanja and not Putanja.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Putanja)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 koijen_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* izvor_stablo 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if raščlanjivati_HTTP_zahtjev(명세.get('Name', ''))[0] != Naziv or 명세.get('Version') != verzija_VALUE:
        raise ValueError('배포 메타데이터의 Naziv·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(adresa, 한도):
    if not adresa.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(adresa, timeout=30) as odgovoriti:
        if not odgovoriti.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 adresa pomaći_VALUE')
        podaci = odgovoriti.read(한도 + 1)
    if len(podaci) > 한도:
        raise ValueError('배포 Fajl Veličina 제한 초과')
    return podaci


def prijenos_paket(Naziv, verzija_VALUE, 파일들, 출처):
    명세 = {'name': Naziv, 'version': verzija_VALUE, 'source': 출처, 'files': [
        {'path': Putanja, 'size': len(podaci), 'sha256': hashlib.sha256(podaci).hexdigest()}
        for Putanja, podaci in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('paket 명세 Veličina 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[unos_VALUE['path']] for unos_VALUE in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Putanja, odjel_za_informacijske_tehnologije_Van_mreže=False):
        자신.Putanja = Path(Putanja)
        자신.Putanja.mkdir(parents=True, exist_ok=True)
        자신.odjel_za_informacijske_tehnologije_Van_mreže = odjel_za_informacijske_tehnologije_Van_mreže

    def Pripremiti(자신, HTTP_zahtjev):
        Naziv, verzija_VALUE = raščlanjivati_HTTP_zahtjev(HTTP_zahtjev)
        열쇠 = Naziv + ('==' + verzija_VALUE if verzija_VALUE else '')
        LOG_put = 자신.Putanja / (열쇠 + '.json')
        배포경로 = 자신.Putanja / (열쇠 + '.archive')
        if LOG_put.is_file() and 배포경로.is_file():
            LOG_red = json.loads(LOG_put.read_text())
            podaci = 배포경로.read_bytes()
            if hashlib.sha256(podaci).hexdigest() != LOG_red['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.odjel_za_informacijske_tehnologije_Van_mreže:
                raise ValueError('odjel_za_informacijske_tehnologije_Van_mreže 저장소에 없는 paket: ' + HTTP_zahtjev)
            adresa = 'https://pypi.org/pypi/' + Naziv + ('/' + verzija_VALUE if verzija_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(adresa, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [unos_VALUE for unos_VALUE in msinfo32_exe['urls'] if not unos_VALUE.get('yanked') and unos_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Naziv.startswith('micropython-'):
                후보 = [unos_VALUE for unos_VALUE in msinfo32_exe['urls'] if not unos_VALUE.get('yanked') and unos_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            izbor_VALUE = 후보[0]
            podaci = 웹읽기(izbor_VALUE['url'], 4194304)
            if hashlib.sha256(podaci).hexdigest() != izbor_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Fajl SHA-256 불일치')
            LOG_red = {'name': Naziv, 'version': msinfo32_exe['info']['version'], 'filename': izbor_VALUE['filename'],
                    'url': izbor_VALUE['url'], 'sha256': izbor_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_red['filename'], podaci, Naziv, LOG_red['version'])
            배포경로.write_bytes(podaci)
            LOG_put.write_text(json.dumps(LOG_red, ensure_ascii=False, indent=2) + '\n')
        if LOG_red['name'] != Naziv or verzija_VALUE and LOG_red['version'] != verzija_VALUE:
            raise ValueError('저장소 Naziv·버전 불일치')
        파일들 = 압축풀기(LOG_red['filename'], podaci, Naziv, LOG_red['version'])
        return prijenos_paket(Naziv, LOG_red['version'], 파일들, LOG_red['url'])


class paket_HTTP_zahtjev(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            HTTP_zahtjev = bytearray()
            while b'\n' not in HTTP_zahtjev and len(HTTP_zahtjev) < 100:
                조각 = 자신.request.recv(100 - len(HTTP_zahtjev))
                if not 조각:
                    return
                HTTP_zahtjev.extend(조각)
            if not HTTP_zahtjev.endswith(b'\n') or HTTP_zahtjev.count(b'\n') != 1:
                raise ValueError('잘못된 paket HTTP_zahtjev')
            odgovoriti = 자신.server.저장소.Pripremiti(HTTP_zahtjev[:-1].decode('ascii'))
        except Exception as GRESKA:
            머리 = json.dumps({'error': str(GRESKA)[:500]}, ensure_ascii=False).encode()
            odgovoriti = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(odgovoriti)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, broj_priključka=8027, Putanja=None, odjel_za_informacijske_tehnologije_Van_mreže=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', broj_priključka), paket_HTTP_zahtjev, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.저장소 = 꾸러미저장소(Putanja or projicirati_koijen/'build/pip-cache', odjel_za_informacijske_tehnologije_Van_mreže)
        자신.broj_priključka = 자신.server_VALUE.server_address[1]
        자신.nit_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.nit_VALUE.start()
        return 자신

    def __exit__(자신, *Argumenti):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.nit_VALUE.join(timeout=2)


def Pokreni():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=projicirati_koijen/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='Izvrši_komanda 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Argumenti = 해석기.parse_args()
    if Argumenti.fetch:
        podaci = 꾸러미저장소(Argumenti.cache, Argumenti.offline).Pripremiti(Argumenti.fetch)
        print('paket Pripremiti 완료:', Argumenti.fetch, len(podaci), 'bajt_VALUE')
        return
    with 꾸러미중계(Argumenti.port, Argumenti.cache, Argumenti.offline) as 중계:
        print('paket 중계: 127.0.0.1:' + str(중계.broj_priključka), flush=True)
        try:
            중계.nit_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Pokreni()
