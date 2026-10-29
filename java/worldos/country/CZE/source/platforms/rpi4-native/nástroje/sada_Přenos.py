#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost Přenos_HODNOTA. 게스트는 TCP로 받은 소스를 직접 instalovat_HODNOTA·실행한다."""
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

akce_kořen = Path(__file__).resolve().parents[1]


def parsovat_žádost(žádost):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', žádost)
    if not 맞음:
        raise ValueError('sada Název 또는 Název==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ověřit_cesta(Název, instalace_cesta=True):
    cesta_2 = PurePosixPath(Název)
    if cesta_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Název.split('/')):
        raise ValueError('허용하지 않는 sada cesta_2: ' + Název)
    if '\\' in Název or any(ord(znak_HODNOTA) < 32 or ord(znak_HODNOTA) == 127 for znak_HODNOTA in Název):
        raise ValueError('잘못된 sada cesta_2 문자')
    if instalace_cesta and (len(('/lib/' + Název).encode()) > 63 or Název in ('čeština.py', 'sada.py')):
        raise ValueError('sada cesta_2 제한 또는 výchozí_hodnota knihovna 충돌: ' + Název)
    return Název


def dekomprimovat(Soubor_položka_název, data, Název, verze_HODNOTA):
    파일들 = {}
    명세들 = []
    def Připojit_položka(cesta_2, Obsah_HODNOTA):
        ověřit_cesta(cesta_2)
        if cesta_2 in 파일들:
            raise ValueError('중복 sada cesta_2: ' + cesta_2)
        if len(Obsah_HODNOTA) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + cesta_2)
        Obsah_HODNOTA.decode('utf-8')
        파일들[cesta_2] = Obsah_HODNOTA
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 zdroj_strom 16개·celkem_HODNOTA 64 KiB 이하여야 합니다.')
    if Soubor_položka_název.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as sada:
            항목들 = sada.infolist()
            if len(항목들) > 256 or sum(položka_HODNOTA.file_size for položka_HODNOTA in 항목들) > 1048576:
                raise ValueError('Archiv_HODNOTA verze_Storage Velikost 제한 초과')
            případ_Seznam = [položka_HODNOTA for položka_HODNOTA in 항목들 if položka_HODNOTA.filename.endswith('.dist-info/WHEEL')]
            if len(případ_Seznam) != 1:
                raise ValueError('wheel hodnota_smlouvy 명세가 필요합니다.')
            hodnota_smlouvy = email.parser.Parser().parsestr(sada.read(případ_Seznam[0]).decode())
            if hodnota_smlouvy.get('Root-Is-Purelib', '').lower() != 'true' or not Soubor_položka_název.endswith('-none-any.whl'):
                raise ValueError('C přípona_HODNOTA·플랫폼 전용 wheel은 지원하지 않습니다.')
            for položka_HODNOTA in 항목들:
                cesta_2 = položka_HODNOTA.filename.rstrip('/')
                ověřit_cesta(cesta_2, False)
                if (položka_HODNOTA.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 číslo 없습니다.')
                if položka_HODNOTA.filename.endswith('/'):
                    continue
                if '.dist-info/' in cesta_2:
                    if cesta_2.endswith('/METADATA'):
                        명세들.append(sada.read(položka_HODNOTA).decode())
                    continue
                if not cesta_2.endswith('.py') or '.data/' in cesta_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + cesta_2)
                Připojit_položka(cesta_2, sada.read(položka_HODNOTA))
    elif Soubor_položka_název.endswith('.tar.gz') and Název.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Provést_příkaz 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as sada:
            뿌리들 = set()
            položka_POČET = 0
            celkem_změnit_velikost = 0
            for položka_HODNOTA in sada:
                položka_POČET += 1
                celkem_změnit_velikost += položka_HODNOTA.size
                if položka_POČET > 256 or celkem_změnit_velikost > 1048576:
                    raise ValueError('Archiv_HODNOTA verze_Storage Velikost 제한 초과')
                ověřit_cesta(položka_HODNOTA.name, False)
                부분들 = položka_HODNOTA.name.split('/')
                뿌리들.add(부분들[0])
                if položka_HODNOTA.isdir():
                    continue
                if not položka_HODNOTA.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython zdroj_strom 배포형')
                cesta_2 = '/'.join(부분들[1:])
                Obsah_HODNOTA = sada.extractfile(položka_HODNOTA).read()
                if cesta_2.endswith('PKG-INFO'):
                    명세들.append(Obsah_HODNOTA.decode())
                elif cesta_2.endswith('.py') and cesta_2 not in ('setup.py',):
                    Připojit_položka(cesta_2, Obsah_HODNOTA)
                elif '.egg-info/' not in cesta_2 and not cesta_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + cesta_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 kořen_HODNOTA 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* zdroj_strom 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 distribuce_HODNOTA 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if parsovat_žádost(명세.get('Name', ''))[0] != Název or 명세.get('Version') != verze_HODNOTA:
        raise ValueError('distribuce_HODNOTA 메타데이터의 Název·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(Adresa, 한도):
    if not Adresa.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS distribuce_HODNOTA 주소만 허용합니다.')
    with urllib.request.urlopen(Adresa, timeout=30) as odezva:
        if not odezva.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 distribuce_HODNOTA Adresa přesunout_HODNOTA')
        data = odezva.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('distribuce_HODNOTA název_souboru Velikost 제한 초과')
    return data


def přenos_sada(Název, verze_HODNOTA, 파일들, origin_HODNOTA):
    명세 = {'name': Název, 'version': verze_HODNOTA, 'source': origin_HODNOTA, 'files': [
        {'path': cesta_2, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for cesta_2, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('sada 명세 Velikost 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[položka_HODNOTA['path']] for položka_HODNOTA in 명세['files'])


class sada_úložiště:
    def __init__(자신, cesta_2, informační_systémy_Offline=False):
        자신.cesta_2 = Path(cesta_2)
        자신.cesta_2.mkdir(parents=True, exist_ok=True)
        자신.informační_systémy_Offline = informační_systémy_Offline

    def Připravit(자신, žádost):
        Název, verze_HODNOTA = parsovat_žádost(žádost)
        Klíč_materiál = Název + ('==' + verze_HODNOTA if verze_HODNOTA else '')
        LOGZ_cesta = 자신.cesta_2 / (Klíč_materiál + '.json')
        distribuce_cesta = 자신.cesta_2 / (Klíč_materiál + '.archive')
        if LOGZ_cesta.is_file() and distribuce_cesta.is_file():
            LOGZ_ZÁZNAM = json.loads(LOGZ_cesta.read_text())
            data = distribuce_cesta.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOGZ_ZÁZNAM['sha256']:
                raise ValueError('저장된 distribuce_HODNOTA 파일의 SHA-256 불일치')
        else:
            if 자신.informační_systémy_Offline:
                raise ValueError('informační_systémy_Offline 저장소에 없는 sada: ' + žádost)
            Adresa = 'https://pypi.org/pypi/' + Název + ('/' + verze_HODNOTA if verze_HODNOTA else '') + '/json'
            Informace_o_systému = json.loads(웹읽기(Adresa, 4194304).decode())
            if Informace_o_systému['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [položka_HODNOTA for položka_HODNOTA in Informace_o_systému['urls'] if not položka_HODNOTA.get('yanked') and položka_HODNOTA['filename'].endswith('-none-any.whl')]
            if not 후보 and Název.startswith('micropython-'):
                후보 = [položka_HODNOTA for položka_HODNOTA in Informace_o_systému['urls'] if not položka_HODNOTA.get('yanked') and položka_HODNOTA['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python distribuce_HODNOTA 파일이 없습니다.')
            výběr_HODNOTA = 후보[0]
            data = 웹읽기(výběr_HODNOTA['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != výběr_HODNOTA['digests']['sha256']:
                raise ValueError('PyPI distribuce_HODNOTA název_souboru SHA-256 불일치')
            LOGZ_ZÁZNAM = {'name': Název, 'version': Informace_o_systému['info']['version'], 'filename': výběr_HODNOTA['filename'],
                    'url': výběr_HODNOTA['url'], 'sha256': výběr_HODNOTA['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            dekomprimovat(LOGZ_ZÁZNAM['filename'], data, Název, LOGZ_ZÁZNAM['version'])
            distribuce_cesta.write_bytes(data)
            LOGZ_cesta.write_text(json.dumps(LOGZ_ZÁZNAM, ensure_ascii=False, indent=2) + '\n')
        if LOGZ_ZÁZNAM['name'] != Název or verze_HODNOTA and LOGZ_ZÁZNAM['version'] != verze_HODNOTA:
            raise ValueError('úložiště_kořen Název·버전 불일치')
        파일들 = dekomprimovat(LOGZ_ZÁZNAM['filename'], data, Název, LOGZ_ZÁZNAM['version'])
        return přenos_sada(Název, LOGZ_ZÁZNAM['version'], 파일들, LOGZ_ZÁZNAM['url'])


class sada_žádost(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            žádost = bytearray()
            while b'\n' not in žádost and len(žádost) < 100:
                조각 = 자신.request.recv(100 - len(žádost))
                if not 조각:
                    return
                žádost.extend(조각)
            if not žádost.endswith(b'\n') or žádost.count(b'\n') != 1:
                raise ValueError('잘못된 sada žádost')
            odezva = 자신.server.úložiště_kořen.Připravit(žádost[:-1].decode('ascii'))
        except Exception as chyba:
            머리 = json.dumps({'error': str(chyba)[:500]}, ensure_ascii=False).encode()
            odezva = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(odezva)
        except OSError:
            pass


class sada_Přenos:
    def __init__(자신, číslo_portu=8027, cesta_2=None, informační_systémy_Offline=False):
        자신.server_HODNOTA = socketserver.TCPServer(('127.0.0.1', číslo_portu), sada_žádost, bind_and_activate=False)
        자신.server_HODNOTA.allow_reuse_address = True
        자신.server_HODNOTA.server_bind()
        자신.server_HODNOTA.server_activate()
        자신.server_HODNOTA.úložiště_kořen = sada_úložiště(cesta_2 or akce_kořen/'build/pip-cache', informační_systémy_Offline)
        자신.číslo_portu = 자신.server_HODNOTA.server_address[1]
        자신.vlákno_HODNOTA = threading.Thread(target=자신.server_HODNOTA.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.vlákno_HODNOTA.start()
        return 자신

    def __exit__(자신, *argumenty):
        자신.server_HODNOTA.shutdown()
        자신.server_HODNOTA.server_close()
        자신.vlákno_HODNOTA.join(timeout=2)


def Spustit_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--port', type=int, default=8027)
    analyzátor_48ee4b1b.add_argument('--cache', type=Path, default=akce_kořen/'build/pip-cache')
    analyzátor_48ee4b1b.add_argument('--offline', action='store_true')
    analyzátor_48ee4b1b.add_argument('--fetch', help='Provést_příkaz 없이 호환 distribuce_HODNOTA 파일을 내려받아 검사·Store_HODNOTA')
    argumenty = analyzátor_48ee4b1b.parse_args()
    if argumenty.fetch:
        data = sada_úložiště(argumenty.cache, argumenty.offline).Připravit(argumenty.fetch)
        print('sada Připravit 완료:', argumenty.fetch, len(data), 'bajt_HODNOTA')
        return
    with sada_Přenos(argumenty.port, argumenty.cache, argumenty.offline) as Přenos_HODNOTA:
        print('sada Přenos_HODNOTA: 127.0.0.1:' + str(Přenos_HODNOTA.číslo_portu), flush=True)
        try:
            Přenos_HODNOTA.vlákno_HODNOTA.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Spustit_2()
