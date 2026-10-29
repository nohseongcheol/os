#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 telepít_ÉRTÉK·실행한다."""
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

teendő_gyök = Path(__file__).resolve().parents[1]


def elemez_kérés(kérés):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', kérés)
    if not 맞음:
        raise ValueError('köteg Név 또는 Név==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ellenőriz_útvonal(Név, telepítés_útvonal=True):
    ÚTVONAL = PurePosixPath(Név)
    if ÚTVONAL.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Név.split('/')):
        raise ValueError('허용하지 않는 köteg ÚTVONAL: ' + Név)
    if '\\' in Név or any(ord(karakter_ÉRTÉK) < 32 or ord(karakter_ÉRTÉK) == 127 for karakter_ÉRTÉK in Név):
        raise ValueError('잘못된 köteg ÚTVONAL 문자')
    if telepítés_útvonal and (len(('/lib/' + Név).encode()) > 63 or Név in ('magyar.py', 'köteg.py')):
        raise ValueError('köteg ÚTVONAL 제한 또는 alapértelmezett_érték kódtár 충돌: ' + Név)
    return Név


def kicsomagol(Fájl_bejegyzés_név, adat, Név, verzió_ÉRTÉK):
    파일들 = {}
    명세들 = []
    def hozzáfűz_bejegyzés(ÚTVONAL, Tartalom_ÉRTÉK):
        ellenőriz_útvonal(ÚTVONAL)
        if ÚTVONAL in 파일들:
            raise ValueError('중복 köteg ÚTVONAL: ' + ÚTVONAL)
        if len(Tartalom_ÉRTÉK) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ÚTVONAL)
        Tartalom_ÉRTÉK.decode('utf-8')
        파일들[ÚTVONAL] = Tartalom_ÉRTÉK
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 forrás_fa 16개·összesen_ÉRTÉK 64 KiB 이하여야 합니다.')
    if Fájl_bejegyzés_név.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(adat)) as köteg:
            항목들 = köteg.infolist()
            if len(항목들) > 256 or sum(bejegyzés_ÉRTÉK.file_size for bejegyzés_ÉRTÉK in 항목들) > 1048576:
                raise ValueError('archív_ÉRTÉK kiad_tár Méret 제한 초과')
            eset_Lista = [bejegyzés_ÉRTÉK for bejegyzés_ÉRTÉK in 항목들 if bejegyzés_ÉRTÉK.filename.endswith('.dist-info/WHEEL')]
            if len(eset_Lista) != 1:
                raise ValueError('wheel szerződés_értéke 명세가 필요합니다.')
            szerződés_értéke = email.parser.Parser().parsestr(köteg.read(eset_Lista[0]).decode())
            if szerződés_értéke.get('Root-Is-Purelib', '').lower() != 'true' or not Fájl_bejegyzés_név.endswith('-none-any.whl'):
                raise ValueError('C bővítmény_ÉRTÉK·플랫폼 전용 wheel은 지원하지 않습니다.')
            for bejegyzés_ÉRTÉK in 항목들:
                ÚTVONAL = bejegyzés_ÉRTÉK.filename.rstrip('/')
                ellenőriz_útvonal(ÚTVONAL, False)
                if (bejegyzés_ÉRTÉK.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 szám 없습니다.')
                if bejegyzés_ÉRTÉK.filename.endswith('/'):
                    continue
                if '.dist-info/' in ÚTVONAL:
                    if ÚTVONAL.endswith('/METADATA'):
                        명세들.append(köteg.read(bejegyzés_ÉRTÉK).decode())
                    continue
                if not ÚTVONAL.endswith('.py') or '.data/' in ÚTVONAL:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ÚTVONAL)
                hozzáfűz_bejegyzés(ÚTVONAL, köteg.read(bejegyzés_ÉRTÉK))
    elif Fájl_bejegyzés_név.endswith('.tar.gz') and Név.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py végrehajt_parancs 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(adat), mode='r|gz') as köteg:
            뿌리들 = set()
            bejegyzés_DARAB = 0
            összesen_méretez = 0
            for bejegyzés_ÉRTÉK in köteg:
                bejegyzés_DARAB += 1
                összesen_méretez += bejegyzés_ÉRTÉK.size
                if bejegyzés_DARAB > 256 or összesen_méretez > 1048576:
                    raise ValueError('archív_ÉRTÉK kiad_tár Méret 제한 초과')
                ellenőriz_útvonal(bejegyzés_ÉRTÉK.name, False)
                부분들 = bejegyzés_ÉRTÉK.name.split('/')
                뿌리들.add(부분들[0])
                if bejegyzés_ÉRTÉK.isdir():
                    continue
                if not bejegyzés_ÉRTÉK.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython forrás_fa 배포형')
                ÚTVONAL = '/'.join(부분들[1:])
                Tartalom_ÉRTÉK = köteg.extractfile(bejegyzés_ÉRTÉK).read()
                if ÚTVONAL.endswith('PKG-INFO'):
                    명세들.append(Tartalom_ÉRTÉK.decode())
                elif ÚTVONAL.endswith('.py') and ÚTVONAL not in ('setup.py',):
                    hozzáfűz_bejegyzés(ÚTVONAL, Tartalom_ÉRTÉK)
                elif '.egg-info/' not in ÚTVONAL and not ÚTVONAL.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ÚTVONAL)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 gyök_ÉRTÉK 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* forrás_fa 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 elosztás_ÉRTÉK 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if elemez_kérés(명세.get('Name', ''))[0] != Név or 명세.get('Version') != verzió_ÉRTÉK:
        raise ValueError('elosztás_ÉRTÉK 메타데이터의 Név·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(CÍM, 한도):
    if not CÍM.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS elosztás_ÉRTÉK 주소만 허용합니다.')
    with urllib.request.urlopen(CÍM, timeout=30) as válasz:
        if not válasz.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 elosztás_ÉRTÉK CÍM áthelyez_ÉRTÉK')
        adat = válasz.read(한도 + 1)
    if len(adat) > 한도:
        raise ValueError('elosztás_ÉRTÉK Fájl Méret 제한 초과')
    return adat


def átvisz_köteg(Név, verzió_ÉRTÉK, 파일들, eredet_ÉRTÉK):
    명세 = {'name': Név, 'version': verzió_ÉRTÉK, 'source': eredet_ÉRTÉK, 'files': [
        {'path': ÚTVONAL, 'size': len(adat), 'sha256': hashlib.sha256(adat).hexdigest()}
        for ÚTVONAL, adat in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('köteg 명세 Méret 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[bejegyzés_ÉRTÉK['path']] for bejegyzés_ÉRTÉK in 명세['files'])


class köteg_adattár:
    def __init__(자신, ÚTVONAL, informatikai_részleg_offline=False):
        자신.ÚTVONAL = Path(ÚTVONAL)
        자신.ÚTVONAL.mkdir(parents=True, exist_ok=True)
        자신.informatikai_részleg_offline = informatikai_részleg_offline

    def Előkészítés(자신, kérés):
        Név, verzió_ÉRTÉK = elemez_kérés(kérés)
        열쇠 = Név + ('==' + verzió_ÉRTÉK if verzió_ÉRTÉK else '')
        LOG_útvonal = 자신.ÚTVONAL / (열쇠 + '.json')
        elosztás_útvonal = 자신.ÚTVONAL / (열쇠 + '.archive')
        if LOG_útvonal.is_file() and elosztás_útvonal.is_file():
            LOG_REKORD = json.loads(LOG_útvonal.read_text())
            adat = elosztás_útvonal.read_bytes()
            if hashlib.sha256(adat).hexdigest() != LOG_REKORD['sha256']:
                raise ValueError('저장된 elosztás_ÉRTÉK 파일의 SHA-256 불일치')
        else:
            if 자신.informatikai_részleg_offline:
                raise ValueError('informatikai_részleg_offline 저장소에 없는 köteg: ' + kérés)
            CÍM = 'https://pypi.org/pypi/' + Név + ('/' + verzió_ÉRTÉK if verzió_ÉRTÉK else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(CÍM, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [bejegyzés_ÉRTÉK for bejegyzés_ÉRTÉK in msinfo32_exe['urls'] if not bejegyzés_ÉRTÉK.get('yanked') and bejegyzés_ÉRTÉK['filename'].endswith('-none-any.whl')]
            if not 후보 and Név.startswith('micropython-'):
                후보 = [bejegyzés_ÉRTÉK for bejegyzés_ÉRTÉK in msinfo32_exe['urls'] if not bejegyzés_ÉRTÉK.get('yanked') and bejegyzés_ÉRTÉK['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python elosztás_ÉRTÉK 파일이 없습니다.')
            kijelölés_ÉRTÉK = 후보[0]
            adat = 웹읽기(kijelölés_ÉRTÉK['url'], 4194304)
            if hashlib.sha256(adat).hexdigest() != kijelölés_ÉRTÉK['digests']['sha256']:
                raise ValueError('PyPI elosztás_ÉRTÉK Fájl SHA-256 불일치')
            LOG_REKORD = {'name': Név, 'version': msinfo32_exe['info']['version'], 'filename': kijelölés_ÉRTÉK['filename'],
                    'url': kijelölés_ÉRTÉK['url'], 'sha256': kijelölés_ÉRTÉK['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            kicsomagol(LOG_REKORD['filename'], adat, Név, LOG_REKORD['version'])
            elosztás_útvonal.write_bytes(adat)
            LOG_útvonal.write_text(json.dumps(LOG_REKORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_REKORD['name'] != Név or verzió_ÉRTÉK and LOG_REKORD['version'] != verzió_ÉRTÉK:
            raise ValueError('adattár_gyök Név·버전 불일치')
        파일들 = kicsomagol(LOG_REKORD['filename'], adat, Név, LOG_REKORD['version'])
        return átvisz_köteg(Név, LOG_REKORD['version'], 파일들, LOG_REKORD['url'])


class köteg_kérés(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            kérés = bytearray()
            while b'\n' not in kérés and len(kérés) < 100:
                조각 = 자신.request.recv(100 - len(kérés))
                if not 조각:
                    return
                kérés.extend(조각)
            if not kérés.endswith(b'\n') or kérés.count(b'\n') != 1:
                raise ValueError('잘못된 köteg kérés')
            válasz = 자신.server.adattár_gyök.Előkészítés(kérés[:-1].decode('ascii'))
        except Exception as HIBA:
            머리 = json.dumps({'error': str(HIBA)[:500]}, ensure_ascii=False).encode()
            válasz = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(válasz)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, portszám=8027, ÚTVONAL=None, informatikai_részleg_offline=False):
        자신.kiszolgáló_ÉRTÉK = socketserver.TCPServer(('127.0.0.1', portszám), köteg_kérés, bind_and_activate=False)
        자신.kiszolgáló_ÉRTÉK.allow_reuse_address = True
        자신.kiszolgáló_ÉRTÉK.server_bind()
        자신.kiszolgáló_ÉRTÉK.server_activate()
        자신.kiszolgáló_ÉRTÉK.adattár_gyök = köteg_adattár(ÚTVONAL or teendő_gyök/'build/pip-cache', informatikai_részleg_offline)
        자신.portszám = 자신.kiszolgáló_ÉRTÉK.server_address[1]
        자신.szál_ÉRTÉK = threading.Thread(target=자신.kiszolgáló_ÉRTÉK.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.szál_ÉRTÉK.start()
        return 자신

    def __exit__(자신, *Argumentumok):
        자신.kiszolgáló_ÉRTÉK.shutdown()
        자신.kiszolgáló_ÉRTÉK.server_close()
        자신.szál_ÉRTÉK.join(timeout=2)


def Futtatás():
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('--port', type=int, default=8027)
    elemző_48ee4b1b.add_argument('--cache', type=Path, default=teendő_gyök/'build/pip-cache')
    elemző_48ee4b1b.add_argument('--offline', action='store_true')
    elemző_48ee4b1b.add_argument('--fetch', help='végrehajt_parancs 없이 호환 elosztás_ÉRTÉK 파일을 내려받아 검사·tár_ÉRTÉK')
    Argumentumok = elemző_48ee4b1b.parse_args()
    if Argumentumok.fetch:
        adat = köteg_adattár(Argumentumok.cache, Argumentumok.offline).Előkészítés(Argumentumok.fetch)
        print('köteg Előkészítés 완료:', Argumentumok.fetch, len(adat), 'bájt_ÉRTÉK')
        return
    with 꾸러미중계(Argumentumok.port, Argumentumok.cache, Argumentumok.offline) as 중계:
        print('köteg 중계: 127.0.0.1:' + str(중계.portszám), flush=True)
        try:
            중계.szál_ÉRTÉK.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Futtatás()
