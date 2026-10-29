#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 namesti_VALUE·실행한다."""
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

pobuda_koren = Path(__file__).resolve().parents[1]


def razčlenjevati_zahteva(zahteva):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', zahteva)
    if not 맞음:
        raise ValueError('sveženj Ime 또는 Ime==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def preveriti_veljavnost_pot(Ime, namestitev_pot=True):
    POT = PurePosixPath(Ime)
    if POT.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Ime.split('/')):
        raise ValueError('허용하지 않는 sveženj POT: ' + Ime)
    if '\\' in Ime or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in Ime):
        raise ValueError('잘못된 sveženj POT 문자')
    if namestitev_pot and (len(('/lib/' + Ime).encode()) > 63 or Ime in ('slovenščina.py', 'sveženj.py')):
        raise ValueError('sveženj POT 제한 또는 privzeta_vrednost knjižnica 충돌: ' + Ime)
    return Ime


def razširiti(Datoteka_vnos_ime, podatki, Ime, različica_VALUE):
    파일들 = {}
    명세들 = []
    def dodati_vnos(POT, vsebina_VALUE):
        preveriti_veljavnost_pot(POT)
        if POT in 파일들:
            raise ValueError('중복 sveženj POT: ' + POT)
        if len(vsebina_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + POT)
        vsebina_VALUE.decode('utf-8')
        파일들[POT] = vsebina_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 vir_drevo 16개·skupaj_VALUE 64 KiB 이하여야 합니다.')
    if Datoteka_vnos_ime.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(podatki)) as sveženj:
            항목들 = sveženj.infolist()
            if len(항목들) > 256 or sum(vnos_VALUE.file_size for vnos_VALUE in 항목들) > 1048576:
                raise ValueError('Arhiv_VALUE izdaja_Senzor_prostora Velikost 제한 초과')
            primer_Seznam = [vnos_VALUE for vnos_VALUE in 항목들 if vnos_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(primer_Seznam) != 1:
                raise ValueError('wheel primer_VALUE 명세가 필요합니다.')
            primer_VALUE = email.parser.Parser().parsestr(sveženj.read(primer_Seznam[0]).decode())
            if primer_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not Datoteka_vnos_ime.endswith('-none-any.whl'):
                raise ValueError('C pripona_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for vnos_VALUE in 항목들:
                POT = vnos_VALUE.filename.rstrip('/')
                preveriti_veljavnost_pot(POT, False)
                if (vnos_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if vnos_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in POT:
                    if POT.endswith('/METADATA'):
                        명세들.append(sveženj.read(vnos_VALUE).decode())
                    continue
                if not POT.endswith('.py') or '.data/' in POT:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + POT)
                dodati_vnos(POT, sveženj.read(vnos_VALUE))
    elif Datoteka_vnos_ime.endswith('.tar.gz') and Ime.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Izvedi_ukaz 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(podatki), mode='r|gz') as sveženj:
            뿌리들 = set()
            vnos_COUNT = 0
            skupaj_spremeniti_velikost = 0
            for vnos_VALUE in sveženj:
                vnos_COUNT += 1
                skupaj_spremeniti_velikost += vnos_VALUE.size
                if vnos_COUNT > 256 or skupaj_spremeniti_velikost > 1048576:
                    raise ValueError('Arhiv_VALUE izdaja_Senzor_prostora Velikost 제한 초과')
                preveriti_veljavnost_pot(vnos_VALUE.name, False)
                부분들 = vnos_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if vnos_VALUE.isdir():
                    continue
                if not vnos_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython vir_drevo 배포형')
                POT = '/'.join(부분들[1:])
                vsebina_VALUE = sveženj.extractfile(vnos_VALUE).read()
                if POT.endswith('PKG-INFO'):
                    명세들.append(vsebina_VALUE.decode())
                elif POT.endswith('.py') and POT not in ('setup.py',):
                    dodati_vnos(POT, vsebina_VALUE)
                elif '.egg-info/' not in POT and not POT.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + POT)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 koren_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* vir_drevo 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if razčlenjevati_zahteva(명세.get('Name', ''))[0] != Ime or 명세.get('Version') != različica_VALUE:
        raise ValueError('배포 메타데이터의 Ime·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(naslov, 한도):
    if not naslov.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(naslov, timeout=30) as odgovor:
        if not odgovor.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 naslov premikati_VALUE')
        podatki = odgovor.read(한도 + 1)
    if len(podatki) > 한도:
        raise ValueError('배포 Datoteka Velikost 제한 초과')
    return podatki


def Prenos_sveženj(Ime, različica_VALUE, 파일들, 출처):
    명세 = {'name': Ime, 'version': različica_VALUE, 'source': 출처, 'files': [
        {'path': POT, 'size': len(podatki), 'sha256': hashlib.sha256(podatki).hexdigest()}
        for POT, podatki in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('sveženj 명세 Velikost 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[vnos_VALUE['path']] for vnos_VALUE in 명세['files'])


class sveženj_shramba:
    def __init__(자신, POT, informacijska_tehnologija_Nedosegljiv=False):
        자신.POT = Path(POT)
        자신.POT.mkdir(parents=True, exist_ok=True)
        자신.informacijska_tehnologija_Nedosegljiv = informacijska_tehnologija_Nedosegljiv

    def Pripravi(자신, zahteva):
        Ime, različica_VALUE = razčlenjevati_zahteva(zahteva)
        열쇠 = Ime + ('==' + različica_VALUE if različica_VALUE else '')
        LOG_pot = 자신.POT / (열쇠 + '.json')
        배포경로 = 자신.POT / (열쇠 + '.archive')
        if LOG_pot.is_file() and 배포경로.is_file():
            LOG_zapis = json.loads(LOG_pot.read_text())
            podatki = 배포경로.read_bytes()
            if hashlib.sha256(podatki).hexdigest() != LOG_zapis['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.informacijska_tehnologija_Nedosegljiv:
                raise ValueError('informacijska_tehnologija_Nedosegljiv 저장소에 없는 sveženj: ' + zahteva)
            naslov = 'https://pypi.org/pypi/' + Ime + ('/' + različica_VALUE if različica_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(naslov, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [vnos_VALUE for vnos_VALUE in msinfo32_exe['urls'] if not vnos_VALUE.get('yanked') and vnos_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Ime.startswith('micropython-'):
                후보 = [vnos_VALUE for vnos_VALUE in msinfo32_exe['urls'] if not vnos_VALUE.get('yanked') and vnos_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            izbor_VALUE = 후보[0]
            podatki = 웹읽기(izbor_VALUE['url'], 4194304)
            if hashlib.sha256(podatki).hexdigest() != izbor_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Datoteka SHA-256 불일치')
            LOG_zapis = {'name': Ime, 'version': msinfo32_exe['info']['version'], 'filename': izbor_VALUE['filename'],
                    'url': izbor_VALUE['url'], 'sha256': izbor_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            razširiti(LOG_zapis['filename'], podatki, Ime, LOG_zapis['version'])
            배포경로.write_bytes(podatki)
            LOG_pot.write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2) + '\n')
        if LOG_zapis['name'] != Ime or različica_VALUE and LOG_zapis['version'] != različica_VALUE:
            raise ValueError('shramba_koren Ime·버전 불일치')
        파일들 = razširiti(LOG_zapis['filename'], podatki, Ime, LOG_zapis['version'])
        return Prenos_sveženj(Ime, LOG_zapis['version'], 파일들, LOG_zapis['url'])


class sveženj_zahteva(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            zahteva = bytearray()
            while b'\n' not in zahteva and len(zahteva) < 100:
                조각 = 자신.request.recv(100 - len(zahteva))
                if not 조각:
                    return
                zahteva.extend(조각)
            if not zahteva.endswith(b'\n') or zahteva.count(b'\n') != 1:
                raise ValueError('잘못된 sveženj zahteva')
            odgovor = 자신.server.shramba_koren.Pripravi(zahteva[:-1].decode('ascii'))
        except Exception as NAPAKA:
            머리 = json.dumps({'error': str(NAPAKA)[:500]}, ensure_ascii=False).encode()
            odgovor = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(odgovor)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, številka_vrat=8027, POT=None, informacijska_tehnologija_Nedosegljiv=False):
        자신.strežnik_VALUE = socketserver.TCPServer(('127.0.0.1', številka_vrat), sveženj_zahteva, bind_and_activate=False)
        자신.strežnik_VALUE.allow_reuse_address = True
        자신.strežnik_VALUE.server_bind()
        자신.strežnik_VALUE.server_activate()
        자신.strežnik_VALUE.shramba_koren = sveženj_shramba(POT or pobuda_koren/'build/pip-cache', informacijska_tehnologija_Nedosegljiv)
        자신.številka_vrat = 자신.strežnik_VALUE.server_address[1]
        자신.nit_VALUE = threading.Thread(target=자신.strežnik_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.nit_VALUE.start()
        return 자신

    def __exit__(자신, *Argumenti):
        자신.strežnik_VALUE.shutdown()
        자신.strežnik_VALUE.server_close()
        자신.nit_VALUE.join(timeout=2)


def Zaženi():
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik_48ee4b1b.add_argument('--port', type=int, default=8027)
    razčlenjevalnik_48ee4b1b.add_argument('--cache', type=Path, default=pobuda_koren/'build/pip-cache')
    razčlenjevalnik_48ee4b1b.add_argument('--offline', action='store_true')
    razčlenjevalnik_48ee4b1b.add_argument('--fetch', help='Izvedi_ukaz 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Argumenti = razčlenjevalnik_48ee4b1b.parse_args()
    if Argumenti.fetch:
        podatki = sveženj_shramba(Argumenti.cache, Argumenti.offline).Pripravi(Argumenti.fetch)
        print('sveženj Pripravi 완료:', Argumenti.fetch, len(podatki), 'bajt_VALUE')
        return
    with 꾸러미중계(Argumenti.port, Argumenti.cache, Argumenti.offline) as 중계:
        print('sveženj 중계: 127.0.0.1:' + str(중계.številka_vrat), flush=True)
        try:
            중계.nit_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Zaženi()
