#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost Przekazywanie_WARTOŚĆ. 게스트는 TCP로 받은 소스를 직접 instalować_WARTOŚĆ·실행한다."""
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

Project_korzeń = Path(__file__).resolve().parents[1]


def analizować_żądanie(żądanie):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', żądanie)
    if not 맞음:
        raise ValueError('pakiet Nazwa 또는 Nazwa==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def walidować_ścieżka(Nazwa, instalacja_ścieżka=True):
    ścieżka_2 = PurePosixPath(Nazwa)
    if ścieżka_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nazwa.split('/')):
        raise ValueError('허용하지 않는 pakiet ścieżka_2: ' + Nazwa)
    if '\\' in Nazwa or any(ord(znak_WARTOŚĆ) < 32 or ord(znak_WARTOŚĆ) == 127 for znak_WARTOŚĆ in Nazwa):
        raise ValueError('잘못된 pakiet ścieżka_2 문자')
    if instalacja_ścieżka and (len(('/lib/' + Nazwa).encode()) > 63 or Nazwa in ('polski.py', 'pakiet.py')):
        raise ValueError('pakiet ścieżka_2 제한 또는 wartość_domyślna biblioteka 충돌: ' + Nazwa)
    return Nazwa


def dekompresować(Plik_wpis_nazwa, dane, Nazwa, wersja_WARTOŚĆ):
    파일들 = {}
    명세들 = []
    def dołączać_wpis(ścieżka_2, treść_WARTOŚĆ_cb0f2404):
        walidować_ścieżka(ścieżka_2)
        if ścieżka_2 in 파일들:
            raise ValueError('중복 pakiet ścieżka_2: ' + ścieżka_2)
        if len(treść_WARTOŚĆ_cb0f2404) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ścieżka_2)
        treść_WARTOŚĆ_cb0f2404.decode('utf-8')
        파일들[ścieżka_2] = treść_WARTOŚĆ_cb0f2404
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 źródło_drzewo 16개·suma_WARTOŚĆ 64 KiB 이하여야 합니다.')
    if Plik_wpis_nazwa.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(dane)) as pakiet:
            항목들 = pakiet.infolist()
            if len(항목들) > 256 or sum(wpis_WARTOŚĆ.file_size for wpis_WARTOŚĆ in 항목들) > 1048576:
                raise ValueError('Archiwum_WARTOŚĆ wersja_Pamięć Rozmiar 제한 초과')
            sprawa_Lista = [wpis_WARTOŚĆ for wpis_WARTOŚĆ in 항목들 if wpis_WARTOŚĆ.filename.endswith('.dist-info/WHEEL')]
            if len(sprawa_Lista) != 1:
                raise ValueError('wheel wartość_kontraktu 명세가 필요합니다.')
            wartość_kontraktu = email.parser.Parser().parsestr(pakiet.read(sprawa_Lista[0]).decode())
            if wartość_kontraktu.get('Root-Is-Purelib', '').lower() != 'true' or not Plik_wpis_nazwa.endswith('-none-any.whl'):
                raise ValueError('C rozszerzenie_WARTOŚĆ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for wpis_WARTOŚĆ in 항목들:
                ścieżka_2 = wpis_WARTOŚĆ.filename.rstrip('/')
                walidować_ścieżka(ścieżka_2, False)
                if (wpis_WARTOŚĆ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 identyfikator 없습니다.')
                if wpis_WARTOŚĆ.filename.endswith('/'):
                    continue
                if '.dist-info/' in ścieżka_2:
                    if ścieżka_2.endswith('/METADATA'):
                        명세들.append(pakiet.read(wpis_WARTOŚĆ).decode())
                    continue
                if not ścieżka_2.endswith('.py') or '.data/' in ścieżka_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ścieżka_2)
                dołączać_wpis(ścieżka_2, pakiet.read(wpis_WARTOŚĆ))
    elif Plik_wpis_nazwa.endswith('.tar.gz') and Nazwa.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Wykonaj_polecenie 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(dane), mode='r|gz') as pakiet:
            뿌리들 = set()
            wpis_ILE_LICZB = 0
            suma_zmienić_rozmiar = 0
            for wpis_WARTOŚĆ in pakiet:
                wpis_ILE_LICZB += 1
                suma_zmienić_rozmiar += wpis_WARTOŚĆ.size
                if wpis_ILE_LICZB > 256 or suma_zmienić_rozmiar > 1048576:
                    raise ValueError('Archiwum_WARTOŚĆ wersja_Pamięć Rozmiar 제한 초과')
                walidować_ścieżka(wpis_WARTOŚĆ.name, False)
                부분들 = wpis_WARTOŚĆ.name.split('/')
                뿌리들.add(부분들[0])
                if wpis_WARTOŚĆ.isdir():
                    continue
                if not wpis_WARTOŚĆ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython źródło_drzewo 배포형')
                ścieżka_2 = '/'.join(부분들[1:])
                treść_WARTOŚĆ_cb0f2404 = pakiet.extractfile(wpis_WARTOŚĆ).read()
                if ścieżka_2.endswith('PKG-INFO'):
                    명세들.append(treść_WARTOŚĆ_cb0f2404.decode())
                elif ścieżka_2.endswith('.py') and ścieżka_2 not in ('setup.py',):
                    dołączać_wpis(ścieżka_2, treść_WARTOŚĆ_cb0f2404)
                elif '.egg-info/' not in ścieżka_2 and not ścieżka_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ścieżka_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 korzeń_WARTOŚĆ 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* źródło_drzewo 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 dystrybucja_WARTOŚĆ 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if analizować_żądanie(명세.get('Name', ''))[0] != Nazwa or 명세.get('Version') != wersja_WARTOŚĆ:
        raise ValueError('dystrybucja_WARTOŚĆ 메타데이터의 Nazwa·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(Adres, 한도):
    if not Adres.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS dystrybucja_WARTOŚĆ 주소만 허용합니다.')
    with urllib.request.urlopen(Adres, timeout=30) as odpowiedź:
        if not odpowiedź.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 dystrybucja_WARTOŚĆ Adres przenosić_WARTOŚĆ')
        dane = odpowiedź.read(한도 + 1)
    if len(dane) > 한도:
        raise ValueError('dystrybucja_WARTOŚĆ nazwa_pliku Rozmiar 제한 초과')
    return dane


def transfer_pakiet(Nazwa, wersja_WARTOŚĆ, 파일들, źródło_WARTOŚĆ):
    명세 = {'name': Nazwa, 'version': wersja_WARTOŚĆ, 'source': źródło_WARTOŚĆ, 'files': [
        {'path': ścieżka_2, 'size': len(dane), 'sha256': hashlib.sha256(dane).hexdigest()}
        for ścieżka_2, dane in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('pakiet 명세 Rozmiar 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[wpis_WARTOŚĆ['path']] for wpis_WARTOŚĆ in 명세['files'])


class pakiet_repozytorium:
    def __init__(자신, ścieżka_2, systemy_informacyjne_offline=False):
        자신.ścieżka_2 = Path(ścieżka_2)
        자신.ścieżka_2.mkdir(parents=True, exist_ok=True)
        자신.systemy_informacyjne_offline = systemy_informacyjne_offline

    def Przygotuj(자신, żądanie):
        Nazwa, wersja_WARTOŚĆ = analizować_żądanie(żądanie)
        Klucz_materiał = Nazwa + ('==' + wersja_WARTOŚĆ if wersja_WARTOŚĆ else '')
        LOG_ścieżka = 자신.ścieżka_2 / (Klucz_materiał + '.json')
        dystrybucja_ścieżka = 자신.ścieżka_2 / (Klucz_materiał + '.archive')
        if LOG_ścieżka.is_file() and dystrybucja_ścieżka.is_file():
            LOG_zapis = json.loads(LOG_ścieżka.read_text())
            dane = dystrybucja_ścieżka.read_bytes()
            if hashlib.sha256(dane).hexdigest() != LOG_zapis['sha256']:
                raise ValueError('저장된 dystrybucja_WARTOŚĆ 파일의 SHA-256 불일치')
        else:
            if 자신.systemy_informacyjne_offline:
                raise ValueError('systemy_informacyjne_offline 저장소에 없는 pakiet: ' + żądanie)
            Adres = 'https://pypi.org/pypi/' + Nazwa + ('/' + wersja_WARTOŚĆ if wersja_WARTOŚĆ else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(Adres, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            kandydat = [wpis_WARTOŚĆ for wpis_WARTOŚĆ in msinfo32_exe['urls'] if not wpis_WARTOŚĆ.get('yanked') and wpis_WARTOŚĆ['filename'].endswith('-none-any.whl')]
            if not kandydat and Nazwa.startswith('micropython-'):
                kandydat = [wpis_WARTOŚĆ for wpis_WARTOŚĆ in msinfo32_exe['urls'] if not wpis_WARTOŚĆ.get('yanked') and wpis_WARTOŚĆ['filename'].endswith('.tar.gz')]
            if not kandydat:
                raise ValueError('지원되는 순수 Python dystrybucja_WARTOŚĆ 파일이 없습니다.')
            zaznaczenie_WARTOŚĆ = kandydat[0]
            dane = 웹읽기(zaznaczenie_WARTOŚĆ['url'], 4194304)
            if hashlib.sha256(dane).hexdigest() != zaznaczenie_WARTOŚĆ['digests']['sha256']:
                raise ValueError('PyPI dystrybucja_WARTOŚĆ nazwa_pliku SHA-256 불일치')
            LOG_zapis = {'name': Nazwa, 'version': msinfo32_exe['info']['version'], 'filename': zaznaczenie_WARTOŚĆ['filename'],
                    'url': zaznaczenie_WARTOŚĆ['url'], 'sha256': zaznaczenie_WARTOŚĆ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            dekompresować(LOG_zapis['filename'], dane, Nazwa, LOG_zapis['version'])
            dystrybucja_ścieżka.write_bytes(dane)
            LOG_ścieżka.write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2) + '\n')
        if LOG_zapis['name'] != Nazwa or wersja_WARTOŚĆ and LOG_zapis['version'] != wersja_WARTOŚĆ:
            raise ValueError('repozytorium_korzeń Nazwa·버전 불일치')
        파일들 = dekompresować(LOG_zapis['filename'], dane, Nazwa, LOG_zapis['version'])
        return transfer_pakiet(Nazwa, LOG_zapis['version'], 파일들, LOG_zapis['url'])


class pakiet_żądanie(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            żądanie = bytearray()
            while b'\n' not in żądanie and len(żądanie) < 100:
                fragment_WARTOŚĆ_652d4b53 = 자신.request.recv(100 - len(żądanie))
                if not fragment_WARTOŚĆ_652d4b53:
                    return
                żądanie.extend(fragment_WARTOŚĆ_652d4b53)
            if not żądanie.endswith(b'\n') or żądanie.count(b'\n') != 1:
                raise ValueError('잘못된 pakiet żądanie')
            odpowiedź = 자신.server.repozytorium_korzeń.Przygotuj(żądanie[:-1].decode('ascii'))
        except Exception as błąd:
            머리 = json.dumps({'error': str(błąd)[:500]}, ensure_ascii=False).encode()
            odpowiedź = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(odpowiedź)
        except OSError:
            pass


class pakiet_Przekazywanie:
    def __init__(자신, numer_portu=8027, ścieżka_2=None, systemy_informacyjne_offline=False):
        자신.serwer_WARTOŚĆ = socketserver.TCPServer(('127.0.0.1', numer_portu), pakiet_żądanie, bind_and_activate=False)
        자신.serwer_WARTOŚĆ.allow_reuse_address = True
        자신.serwer_WARTOŚĆ.server_bind()
        자신.serwer_WARTOŚĆ.server_activate()
        자신.serwer_WARTOŚĆ.repozytorium_korzeń = pakiet_repozytorium(ścieżka_2 or Project_korzeń/'build/pip-cache', systemy_informacyjne_offline)
        자신.numer_portu = 자신.serwer_WARTOŚĆ.server_address[1]
        자신.wątek_WARTOŚĆ = threading.Thread(target=자신.serwer_WARTOŚĆ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.wątek_WARTOŚĆ.start()
        return 자신

    def __exit__(자신, *argumenty):
        자신.serwer_WARTOŚĆ.shutdown()
        자신.serwer_WARTOŚĆ.server_close()
        자신.wątek_WARTOŚĆ.join(timeout=2)


def Uruchom_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=Project_korzeń/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='Wykonaj_polecenie 없이 호환 dystrybucja_WARTOŚĆ 파일을 내려받아 검사·Store_WARTOŚĆ')
    argumenty = parser_48ee4b1b.parse_args()
    if argumenty.fetch:
        dane = pakiet_repozytorium(argumenty.cache, argumenty.offline).Przygotuj(argumenty.fetch)
        print('pakiet Przygotuj 완료:', argumenty.fetch, len(dane), 'bajt_WARTOŚĆ')
        return
    with pakiet_Przekazywanie(argumenty.port, argumenty.cache, argumenty.offline) as Przekazywanie_WARTOŚĆ:
        print('pakiet Przekazywanie_WARTOŚĆ: 127.0.0.1:' + str(Przekazywanie_WARTOŚĆ.numer_portu), flush=True)
        try:
            Przekazywanie_WARTOŚĆ.wątek_WARTOŚĆ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Uruchom_2()
