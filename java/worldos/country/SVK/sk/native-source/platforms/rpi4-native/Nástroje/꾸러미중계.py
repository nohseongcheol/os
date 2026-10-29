#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 inštalovať_VALUE·실행한다."""
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

akcia_koreň = Path(__file__).resolve().parents[1]


def analyzovať_požiadavka(požiadavka):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', požiadavka)
    if not 맞음:
        raise ValueError('zväzok Názov 또는 Názov==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def overiť_cesta(Názov, inštalácia_cesta=True):
    Cesta = PurePosixPath(Názov)
    if Cesta.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Názov.split('/')):
        raise ValueError('허용하지 않는 zväzok Cesta: ' + Názov)
    if '\\' in Názov or any(ord(znak_VALUE) < 32 or ord(znak_VALUE) == 127 for znak_VALUE in Názov):
        raise ValueError('잘못된 zväzok Cesta 문자')
    if inštalácia_cesta and (len(('/lib/' + Názov).encode()) > 63 or Názov in ('Slovenský.py', 'zväzok.py')):
        raise ValueError('zväzok Cesta 제한 또는 predvolená_hodnota knižnica 충돌: ' + Názov)
    return Názov


def 압축풀기(Súbor_položka_názov, údaje, Názov, verzia_VALUE):
    파일들 = {}
    명세들 = []
    def Pripojiť_položka(Cesta, obsah_VALUE):
        overiť_cesta(Cesta)
        if Cesta in 파일들:
            raise ValueError('중복 zväzok Cesta: ' + Cesta)
        if len(obsah_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Cesta)
        obsah_VALUE.decode('utf-8')
        파일들[Cesta] = obsah_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 zdroj_strom 16개·celkovo_VALUE 64 KiB 이하여야 합니다.')
    if Súbor_položka_názov.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(údaje)) as zväzok:
            항목들 = zväzok.infolist()
            if len(항목들) > 256 or sum(položka_VALUE.file_size for položka_VALUE in 항목들) > 1048576:
                raise ValueError('Archív_VALUE vydať_Úložisko Veľkosť 제한 초과')
            prípad_Zoznam = [položka_VALUE for položka_VALUE in 항목들 if položka_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(prípad_Zoznam) != 1:
                raise ValueError('wheel prípad_VALUE 명세가 필요합니다.')
            prípad_VALUE = email.parser.Parser().parsestr(zväzok.read(prípad_Zoznam[0]).decode())
            if prípad_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not Súbor_položka_názov.endswith('-none-any.whl'):
                raise ValueError('C prípona_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for položka_VALUE in 항목들:
                Cesta = položka_VALUE.filename.rstrip('/')
                overiť_cesta(Cesta, False)
                if (položka_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if položka_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in Cesta:
                    if Cesta.endswith('/METADATA'):
                        명세들.append(zväzok.read(položka_VALUE).decode())
                    continue
                if not Cesta.endswith('.py') or '.data/' in Cesta:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Cesta)
                Pripojiť_položka(Cesta, zväzok.read(položka_VALUE))
    elif Súbor_položka_názov.endswith('.tar.gz') and Názov.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Vykonať_príkaz 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(údaje), mode='r|gz') as zväzok:
            뿌리들 = set()
            položka_COUNT_8f7753a1 = 0
            celkovo_zmeniť_veľkosť = 0
            for položka_VALUE in zväzok:
                položka_COUNT_8f7753a1 += 1
                celkovo_zmeniť_veľkosť += položka_VALUE.size
                if položka_COUNT_8f7753a1 > 256 or celkovo_zmeniť_veľkosť > 1048576:
                    raise ValueError('Archív_VALUE vydať_Úložisko Veľkosť 제한 초과')
                overiť_cesta(položka_VALUE.name, False)
                부분들 = položka_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if položka_VALUE.isdir():
                    continue
                if not položka_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython zdroj_strom 배포형')
                Cesta = '/'.join(부분들[1:])
                obsah_VALUE = zväzok.extractfile(položka_VALUE).read()
                if Cesta.endswith('PKG-INFO'):
                    명세들.append(obsah_VALUE.decode())
                elif Cesta.endswith('.py') and Cesta not in ('setup.py',):
                    Pripojiť_položka(Cesta, obsah_VALUE)
                elif '.egg-info/' not in Cesta and not Cesta.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Cesta)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 koreň_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* zdroj_strom 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if analyzovať_požiadavka(명세.get('Name', ''))[0] != Názov or 명세.get('Version') != verzia_VALUE:
        raise ValueError('배포 메타데이터의 Názov·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(adresa, 한도):
    if not adresa.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(adresa, timeout=30) as odozva:
        if not odozva.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 adresa premiestniť_VALUE')
        údaje = odozva.read(한도 + 1)
    if len(údaje) > 한도:
        raise ValueError('배포 Súbor Veľkosť 제한 초과')
    return údaje


def prenos_zväzok(Názov, verzia_VALUE, 파일들, 출처):
    명세 = {'name': Názov, 'version': verzia_VALUE, 'source': 출처, 'files': [
        {'path': Cesta, 'size': len(údaje), 'sha256': hashlib.sha256(údaje).hexdigest()}
        for Cesta, údaje in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('zväzok 명세 Veľkosť 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[položka_VALUE['path']] for položka_VALUE in 명세['files'])


class zväzok_odkladací_priestor:
    def __init__(자신, Cesta, Informačné_systémy_Offline=False):
        자신.Cesta = Path(Cesta)
        자신.Cesta.mkdir(parents=True, exist_ok=True)
        자신.Informačné_systémy_Offline = Informačné_systémy_Offline

    def Pripraviť(자신, požiadavka):
        Názov, verzia_VALUE = analyzovať_požiadavka(požiadavka)
        열쇠 = Názov + ('==' + verzia_VALUE if verzia_VALUE else '')
        LOG_cesta = 자신.Cesta / (열쇠 + '.json')
        배포경로 = 자신.Cesta / (열쇠 + '.archive')
        if LOG_cesta.is_file() and 배포경로.is_file():
            LOG_RECORD = json.loads(LOG_cesta.read_text())
            údaje = 배포경로.read_bytes()
            if hashlib.sha256(údaje).hexdigest() != LOG_RECORD['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.Informačné_systémy_Offline:
                raise ValueError('Informačné_systémy_Offline 저장소에 없는 zväzok: ' + požiadavka)
            adresa = 'https://pypi.org/pypi/' + Názov + ('/' + verzia_VALUE if verzia_VALUE else '') + '/json'
            Systémové_informácie = json.loads(웹읽기(adresa, 4194304).decode())
            if Systémové_informácie['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [položka_VALUE for položka_VALUE in Systémové_informácie['urls'] if not položka_VALUE.get('yanked') and položka_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Názov.startswith('micropython-'):
                후보 = [položka_VALUE for položka_VALUE in Systémové_informácie['urls'] if not položka_VALUE.get('yanked') and položka_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            výber_VALUE = 후보[0]
            údaje = 웹읽기(výber_VALUE['url'], 4194304)
            if hashlib.sha256(údaje).hexdigest() != výber_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Súbor SHA-256 불일치')
            LOG_RECORD = {'name': Názov, 'version': Systémové_informácie['info']['version'], 'filename': výber_VALUE['filename'],
                    'url': výber_VALUE['url'], 'sha256': výber_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_RECORD['filename'], údaje, Názov, LOG_RECORD['version'])
            배포경로.write_bytes(údaje)
            LOG_cesta.write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_RECORD['name'] != Názov or verzia_VALUE and LOG_RECORD['version'] != verzia_VALUE:
            raise ValueError('odkladací_priestor_koreň Názov·버전 불일치')
        파일들 = 압축풀기(LOG_RECORD['filename'], údaje, Názov, LOG_RECORD['version'])
        return prenos_zväzok(Názov, LOG_RECORD['version'], 파일들, LOG_RECORD['url'])


class zväzok_požiadavka(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            požiadavka = bytearray()
            while b'\n' not in požiadavka and len(požiadavka) < 100:
                조각 = 자신.request.recv(100 - len(požiadavka))
                if not 조각:
                    return
                požiadavka.extend(조각)
            if not požiadavka.endswith(b'\n') or požiadavka.count(b'\n') != 1:
                raise ValueError('잘못된 zväzok požiadavka')
            odozva = 자신.server.odkladací_priestor_koreň.Pripraviť(požiadavka[:-1].decode('ascii'))
        except Exception as chyba:
            머리 = json.dumps({'error': str(chyba)[:500]}, ensure_ascii=False).encode()
            odozva = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(odozva)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, číslo_portu=8027, Cesta=None, Informačné_systémy_Offline=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', číslo_portu), zväzok_požiadavka, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.odkladací_priestor_koreň = zväzok_odkladací_priestor(Cesta or akcia_koreň/'build/pip-cache', Informačné_systémy_Offline)
        자신.číslo_portu = 자신.server_VALUE.server_address[1]
        자신.vlákno_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.vlákno_VALUE.start()
        return 자신

    def __exit__(자신, *Argumenty):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.vlákno_VALUE.join(timeout=2)


def Spustiť_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--port', type=int, default=8027)
    analyzátor_48ee4b1b.add_argument('--cache', type=Path, default=akcia_koreň/'build/pip-cache')
    analyzátor_48ee4b1b.add_argument('--offline', action='store_true')
    analyzátor_48ee4b1b.add_argument('--fetch', help='Vykonať_príkaz 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Argumenty = analyzátor_48ee4b1b.parse_args()
    if Argumenty.fetch:
        údaje = zväzok_odkladací_priestor(Argumenty.cache, Argumenty.offline).Pripraviť(Argumenty.fetch)
        print('zväzok Pripraviť 완료:', Argumenty.fetch, len(údaje), 'Byte_VALUE')
        return
    with 꾸러미중계(Argumenty.port, Argumenty.cache, Argumenty.offline) as 중계:
        print('zväzok 중계: 127.0.0.1:' + str(중계.číslo_portu), flush=True)
        try:
            중계.vlákno_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Spustiť_2()
