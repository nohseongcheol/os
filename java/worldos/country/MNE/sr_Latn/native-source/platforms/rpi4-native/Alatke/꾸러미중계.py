#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instaliraj_VALUE·실행한다."""
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

radnja_koren = Path(__file__).resolve().parents[1]


def raščlaniti_zahtev(zahtev):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', zahtev)
    if not 맞음:
        raise ValueError('komplet ime 또는 ime==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def potvrditi_putanja(ime, instalacija_putanja=True):
    putanja = PurePosixPath(ime)
    if putanja.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ime.split('/')):
        raise ValueError('허용하지 않는 komplet putanja: ' + ime)
    if '\\' in ime or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in ime):
        raise ValueError('잘못된 komplet putanja 문자')
    if instalacija_putanja and (len(('/lib/' + ime).encode()) > 63 or ime in ('한국어.py', 'komplet.py')):
        raise ValueError('komplet putanja 제한 또는 podrazumevana_vrednost biblioteka 충돌: ' + ime)
    return ime


def 압축풀기(Datoteka_stavka_ime, podaci, ime, verzija_VALUE):
    파일들 = {}
    명세들 = []
    def dodati_stavka(putanja, Sadržaj_VALUE):
        potvrditi_putanja(putanja)
        if putanja in 파일들:
            raise ValueError('중복 komplet putanja: ' + putanja)
        if len(Sadržaj_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + putanja)
        Sadržaj_VALUE.decode('utf-8')
        파일들[putanja] = Sadržaj_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 izvor_stablo 16개·ukupan_VALUE 64 KiB 이하여야 합니다.')
    if Datoteka_stavka_ime.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(podaci)) as komplet:
            항목들 = komplet.infolist()
            if len(항목들) > 256 or sum(stavka_VALUE.file_size for stavka_VALUE in 항목들) > 1048576:
                raise ValueError('Arhiva_VALUE izdanje_Skladište promeniti_veličinu 제한 초과')
            ugovor_Lista = [stavka_VALUE for stavka_VALUE in 항목들 if stavka_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(ugovor_Lista) != 1:
                raise ValueError('wheel ugovor_VALUE 명세가 필요합니다.')
            ugovor_VALUE = email.parser.Parser().parsestr(komplet.read(ugovor_Lista[0]).decode())
            if ugovor_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not Datoteka_stavka_ime.endswith('-none-any.whl'):
                raise ValueError('C ekstenzija_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for stavka_VALUE in 항목들:
                putanja = stavka_VALUE.filename.rstrip('/')
                potvrditi_putanja(putanja, False)
                if (stavka_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if stavka_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in putanja:
                    if putanja.endswith('/METADATA'):
                        명세들.append(komplet.read(stavka_VALUE).decode())
                    continue
                if not putanja.endswith('.py') or '.data/' in putanja:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + putanja)
                dodati_stavka(putanja, komplet.read(stavka_VALUE))
    elif Datoteka_stavka_ime.endswith('.tar.gz') and ime.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Izvrši_komanda 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(podaci), mode='r|gz') as komplet:
            뿌리들 = set()
            stavka_COUNT_8f7753a1 = 0
            ukupan_promeniti_veličinu = 0
            for stavka_VALUE in komplet:
                stavka_COUNT_8f7753a1 += 1
                ukupan_promeniti_veličinu += stavka_VALUE.size
                if stavka_COUNT_8f7753a1 > 256 or ukupan_promeniti_veličinu > 1048576:
                    raise ValueError('Arhiva_VALUE izdanje_Skladište promeniti_veličinu 제한 초과')
                potvrditi_putanja(stavka_VALUE.name, False)
                부분들 = stavka_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if stavka_VALUE.isdir():
                    continue
                if not stavka_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython izvor_stablo 배포형')
                putanja = '/'.join(부분들[1:])
                Sadržaj_VALUE = komplet.extractfile(stavka_VALUE).read()
                if putanja.endswith('PKG-INFO'):
                    명세들.append(Sadržaj_VALUE.decode())
                elif putanja.endswith('.py') and putanja not in ('setup.py',):
                    dodati_stavka(putanja, Sadržaj_VALUE)
                elif '.egg-info/' not in putanja and not putanja.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + putanja)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 koren_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* izvor_stablo 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if raščlaniti_zahtev(명세.get('Name', ''))[0] != ime or 명세.get('Version') != verzija_VALUE:
        raise ValueError('배포 메타데이터의 ime·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(adresa, 한도):
    if not adresa.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(adresa, timeout=30) as odgovor:
        if not odgovor.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 adresa premestiti_VALUE')
        podaci = odgovor.read(한도 + 1)
    if len(podaci) > 한도:
        raise ValueError('배포 Datoteka promeniti_veličinu 제한 초과')
    return podaci


def prenos_komplet(ime, verzija_VALUE, 파일들, 출처):
    명세 = {'name': ime, 'version': verzija_VALUE, 'source': 출처, 'files': [
        {'path': putanja, 'size': len(podaci), 'sha256': hashlib.sha256(podaci).hexdigest()}
        for putanja, podaci in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('komplet 명세 promeniti_veličinu 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[stavka_VALUE['path']] for stavka_VALUE in 명세['files'])


class komplet_depo:
    def __init__(자신, putanja, informatičko_odeljenje_Van_mreže=False):
        자신.putanja = Path(putanja)
        자신.putanja.mkdir(parents=True, exist_ok=True)
        자신.informatičko_odeljenje_Van_mreže = informatičko_odeljenje_Van_mreže

    def Pripremi(자신, zahtev):
        ime, verzija_VALUE = raščlaniti_zahtev(zahtev)
        열쇠 = ime + ('==' + verzija_VALUE if verzija_VALUE else '')
        LOG_putanja = 자신.putanja / (열쇠 + '.json')
        배포경로 = 자신.putanja / (열쇠 + '.archive')
        if LOG_putanja.is_file() and 배포경로.is_file():
            LOG_snimi = json.loads(LOG_putanja.read_text())
            podaci = 배포경로.read_bytes()
            if hashlib.sha256(podaci).hexdigest() != LOG_snimi['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.informatičko_odeljenje_Van_mreže:
                raise ValueError('informatičko_odeljenje_Van_mreže 저장소에 없는 komplet: ' + zahtev)
            adresa = 'https://pypi.org/pypi/' + ime + ('/' + verzija_VALUE if verzija_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(adresa, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [stavka_VALUE for stavka_VALUE in msinfo32_exe['urls'] if not stavka_VALUE.get('yanked') and stavka_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and ime.startswith('micropython-'):
                후보 = [stavka_VALUE for stavka_VALUE in msinfo32_exe['urls'] if not stavka_VALUE.get('yanked') and stavka_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            izbor_VALUE = 후보[0]
            podaci = 웹읽기(izbor_VALUE['url'], 4194304)
            if hashlib.sha256(podaci).hexdigest() != izbor_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Datoteka SHA-256 불일치')
            LOG_snimi = {'name': ime, 'version': msinfo32_exe['info']['version'], 'filename': izbor_VALUE['filename'],
                    'url': izbor_VALUE['url'], 'sha256': izbor_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_snimi['filename'], podaci, ime, LOG_snimi['version'])
            배포경로.write_bytes(podaci)
            LOG_putanja.write_text(json.dumps(LOG_snimi, ensure_ascii=False, indent=2) + '\n')
        if LOG_snimi['name'] != ime or verzija_VALUE and LOG_snimi['version'] != verzija_VALUE:
            raise ValueError('depo_koren ime·버전 불일치')
        파일들 = 압축풀기(LOG_snimi['filename'], podaci, ime, LOG_snimi['version'])
        return prenos_komplet(ime, LOG_snimi['version'], 파일들, LOG_snimi['url'])


class komplet_zahtev(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            zahtev = bytearray()
            while b'\n' not in zahtev and len(zahtev) < 100:
                조각 = 자신.request.recv(100 - len(zahtev))
                if not 조각:
                    return
                zahtev.extend(조각)
            if not zahtev.endswith(b'\n') or zahtev.count(b'\n') != 1:
                raise ValueError('잘못된 komplet zahtev')
            odgovor = 자신.server.depo_koren.Pripremi(zahtev[:-1].decode('ascii'))
        except Exception as greška:
            머리 = json.dumps({'error': str(greška)[:500]}, ensure_ascii=False).encode()
            odgovor = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(odgovor)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, broj_porta=8027, putanja=None, informatičko_odeljenje_Van_mreže=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', broj_porta), komplet_zahtev, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.depo_koren = komplet_depo(putanja or radnja_koren/'build/pip-cache', informatičko_odeljenje_Van_mreže)
        자신.broj_porta = 자신.server_VALUE.server_address[1]
        자신.nit_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.nit_VALUE.start()
        return 자신

    def __exit__(자신, *인수):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.nit_VALUE.join(timeout=2)


def koristiti():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--port', type=int, default=8027)
    analizator_48ee4b1b.add_argument('--cache', type=Path, default=radnja_koren/'build/pip-cache')
    analizator_48ee4b1b.add_argument('--offline', action='store_true')
    analizator_48ee4b1b.add_argument('--fetch', help='Izvrši_komanda 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = analizator_48ee4b1b.parse_args()
    if 인수.fetch:
        podaci = komplet_depo(인수.cache, 인수.offline).Pripremi(인수.fetch)
        print('komplet Pripremi 완료:', 인수.fetch, len(podaci), 'bajt_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('komplet 중계: 127.0.0.1:' + str(중계.broj_porta), flush=True)
        try:
            중계.nit_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    koristiti()
