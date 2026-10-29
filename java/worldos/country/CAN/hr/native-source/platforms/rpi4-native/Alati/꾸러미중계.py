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

akcija_korijen = Path(__file__).resolve().parents[1]


def rastavljati_zahtjev(zahtjev):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', zahtjev)
    if not 맞음:
        raise ValueError('komplet Ime 또는 Ime==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def potvrditi_put(Ime, instalacija_put=True):
    PUTANJA = PurePosixPath(Ime)
    if PUTANJA.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Ime.split('/')):
        raise ValueError('허용하지 않는 komplet PUTANJA: ' + Ime)
    if '\\' in Ime or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in Ime):
        raise ValueError('잘못된 komplet PUTANJA 문자')
    if instalacija_put and (len(('/lib/' + Ime).encode()) > 63 or Ime in ('hrvatski.py', 'komplet.py')):
        raise ValueError('komplet PUTANJA 제한 또는 zadana_vrijednost biblioteka 충돌: ' + Ime)
    return Ime


def dekomprimirati(Datoteka_unos_naziv, podaci, Ime, verzija_VALUE):
    파일들 = {}
    명세들 = []
    def dodati_unos(PUTANJA, Sadržaj_VALUE):
        potvrditi_put(PUTANJA)
        if PUTANJA in 파일들:
            raise ValueError('중복 komplet PUTANJA: ' + PUTANJA)
        if len(Sadržaj_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + PUTANJA)
        Sadržaj_VALUE.decode('utf-8')
        파일들[PUTANJA] = Sadržaj_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 izvor_stablo 16개·ukupni_zbroj_VALUE 64 KiB 이하여야 합니다.')
    if Datoteka_unos_naziv.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(podaci)) as komplet:
            항목들 = komplet.infolist()
            if len(항목들) > 256 or sum(unos_VALUE.file_size for unos_VALUE in 항목들) > 1048576:
                raise ValueError('Arhiva_VALUE izdati_Pohrana Veličina 제한 초과')
            slučaj_Popis = [unos_VALUE for unos_VALUE in 항목들 if unos_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(slučaj_Popis) != 1:
                raise ValueError('wheel slučaj_VALUE 명세가 필요합니다.')
            slučaj_VALUE = email.parser.Parser().parsestr(komplet.read(slučaj_Popis[0]).decode())
            if slučaj_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not Datoteka_unos_naziv.endswith('-none-any.whl'):
                raise ValueError('C nastavak_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for unos_VALUE in 항목들:
                PUTANJA = unos_VALUE.filename.rstrip('/')
                potvrditi_put(PUTANJA, False)
                if (unos_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if unos_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in PUTANJA:
                    if PUTANJA.endswith('/METADATA'):
                        명세들.append(komplet.read(unos_VALUE).decode())
                    continue
                if not PUTANJA.endswith('.py') or '.data/' in PUTANJA:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + PUTANJA)
                dodati_unos(PUTANJA, komplet.read(unos_VALUE))
    elif Datoteka_unos_naziv.endswith('.tar.gz') and Ime.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Izvrši_naredba 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(podaci), mode='r|gz') as komplet:
            뿌리들 = set()
            unos_COUNT = 0
            ukupni_zbroj_promijeniti_veličinu = 0
            for unos_VALUE in komplet:
                unos_COUNT += 1
                ukupni_zbroj_promijeniti_veličinu += unos_VALUE.size
                if unos_COUNT > 256 or ukupni_zbroj_promijeniti_veličinu > 1048576:
                    raise ValueError('Arhiva_VALUE izdati_Pohrana Veličina 제한 초과')
                potvrditi_put(unos_VALUE.name, False)
                부분들 = unos_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if unos_VALUE.isdir():
                    continue
                if not unos_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython izvor_stablo 배포형')
                PUTANJA = '/'.join(부분들[1:])
                Sadržaj_VALUE = komplet.extractfile(unos_VALUE).read()
                if PUTANJA.endswith('PKG-INFO'):
                    명세들.append(Sadržaj_VALUE.decode())
                elif PUTANJA.endswith('.py') and PUTANJA not in ('setup.py',):
                    dodati_unos(PUTANJA, Sadržaj_VALUE)
                elif '.egg-info/' not in PUTANJA and not PUTANJA.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + PUTANJA)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 korijen_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* izvor_stablo 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if rastavljati_zahtjev(명세.get('Name', ''))[0] != Ime or 명세.get('Version') != verzija_VALUE:
        raise ValueError('배포 메타데이터의 Ime·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(adresa, 한도):
    if not adresa.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(adresa, timeout=30) as odgovor:
        if not odgovor.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 adresa pomicati_se_VALUE')
        podaci = odgovor.read(한도 + 1)
    if len(podaci) > 한도:
        raise ValueError('배포 Datoteka Veličina 제한 초과')
    return podaci


def Prijenos_komplet(Ime, verzija_VALUE, 파일들, 출처):
    명세 = {'name': Ime, 'version': verzija_VALUE, 'source': 출처, 'files': [
        {'path': PUTANJA, 'size': len(podaci), 'sha256': hashlib.sha256(podaci).hexdigest()}
        for PUTANJA, podaci in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('komplet 명세 Veličina 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[unos_VALUE['path']] for unos_VALUE in 명세['files'])


class komplet_spremište:
    def __init__(자신, PUTANJA, odjel_informacijske_tehnologije_Izvan_mreže=False):
        자신.PUTANJA = Path(PUTANJA)
        자신.PUTANJA.mkdir(parents=True, exist_ok=True)
        자신.odjel_informacijske_tehnologije_Izvan_mreže = odjel_informacijske_tehnologije_Izvan_mreže

    def Pripremi(자신, zahtjev):
        Ime, verzija_VALUE = rastavljati_zahtjev(zahtjev)
        열쇠 = Ime + ('==' + verzija_VALUE if verzija_VALUE else '')
        LOG_put = 자신.PUTANJA / (열쇠 + '.json')
        배포경로 = 자신.PUTANJA / (열쇠 + '.archive')
        if LOG_put.is_file() and 배포경로.is_file():
            LOG_zapis = json.loads(LOG_put.read_text())
            podaci = 배포경로.read_bytes()
            if hashlib.sha256(podaci).hexdigest() != LOG_zapis['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.odjel_informacijske_tehnologije_Izvan_mreže:
                raise ValueError('odjel_informacijske_tehnologije_Izvan_mreže 저장소에 없는 komplet: ' + zahtjev)
            adresa = 'https://pypi.org/pypi/' + Ime + ('/' + verzija_VALUE if verzija_VALUE else '') + '/json'
            Podaci_o_sustavu = json.loads(웹읽기(adresa, 4194304).decode())
            if Podaci_o_sustavu['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [unos_VALUE for unos_VALUE in Podaci_o_sustavu['urls'] if not unos_VALUE.get('yanked') and unos_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Ime.startswith('micropython-'):
                후보 = [unos_VALUE for unos_VALUE in Podaci_o_sustavu['urls'] if not unos_VALUE.get('yanked') and unos_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            odabir_VALUE = 후보[0]
            podaci = 웹읽기(odabir_VALUE['url'], 4194304)
            if hashlib.sha256(podaci).hexdigest() != odabir_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Datoteka SHA-256 불일치')
            LOG_zapis = {'name': Ime, 'version': Podaci_o_sustavu['info']['version'], 'filename': odabir_VALUE['filename'],
                    'url': odabir_VALUE['url'], 'sha256': odabir_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            dekomprimirati(LOG_zapis['filename'], podaci, Ime, LOG_zapis['version'])
            배포경로.write_bytes(podaci)
            LOG_put.write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2) + '\n')
        if LOG_zapis['name'] != Ime or verzija_VALUE and LOG_zapis['version'] != verzija_VALUE:
            raise ValueError('spremište_korijen Ime·버전 불일치')
        파일들 = dekomprimirati(LOG_zapis['filename'], podaci, Ime, LOG_zapis['version'])
        return Prijenos_komplet(Ime, LOG_zapis['version'], 파일들, LOG_zapis['url'])


class komplet_zahtjev(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            zahtjev = bytearray()
            while b'\n' not in zahtjev and len(zahtjev) < 100:
                fragment_VALUE = 자신.request.recv(100 - len(zahtjev))
                if not fragment_VALUE:
                    return
                zahtjev.extend(fragment_VALUE)
            if not zahtjev.endswith(b'\n') or zahtjev.count(b'\n') != 1:
                raise ValueError('잘못된 komplet zahtjev')
            odgovor = 자신.server.spremište_korijen.Pripremi(zahtjev[:-1].decode('ascii'))
        except Exception as GREŠKA:
            머리 = json.dumps({'error': str(GREŠKA)[:500]}, ensure_ascii=False).encode()
            odgovor = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(odgovor)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, broj_priključka=8027, PUTANJA=None, odjel_informacijske_tehnologije_Izvan_mreže=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', broj_priključka), komplet_zahtjev, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.spremište_korijen = komplet_spremište(PUTANJA or akcija_korijen/'build/pip-cache', odjel_informacijske_tehnologije_Izvan_mreže)
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
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--port', type=int, default=8027)
    analizator_48ee4b1b.add_argument('--cache', type=Path, default=akcija_korijen/'build/pip-cache')
    analizator_48ee4b1b.add_argument('--offline', action='store_true')
    analizator_48ee4b1b.add_argument('--fetch', help='Izvrši_naredba 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Argumenti = analizator_48ee4b1b.parse_args()
    if Argumenti.fetch:
        podaci = komplet_spremište(Argumenti.cache, Argumenti.offline).Pripremi(Argumenti.fetch)
        print('komplet Pripremi 완료:', Argumenti.fetch, len(podaci), 'bajt_VALUE')
        return
    with 꾸러미중계(Argumenti.port, Argumenti.cache, Argumenti.offline) as 중계:
        print('komplet 중계: 127.0.0.1:' + str(중계.broj_priključka), flush=True)
        try:
            중계.nit_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Pokreni()
