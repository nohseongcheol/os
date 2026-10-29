#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 asentaa_ARVO·실행한다."""
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

aloite_juuri = Path(__file__).resolve().parents[1]


def jäsentää_pyyntö(pyyntö):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', pyyntö)
    if not 맞음:
        raise ValueError('nippu Nimi 또는 Nimi==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def vahvista_polku(Nimi, asennus_polku=True):
    polku_2 = PurePosixPath(Nimi)
    if polku_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nimi.split('/')):
        raise ValueError('허용하지 않는 nippu polku_2: ' + Nimi)
    if '\\' in Nimi or any(ord(merkki_ARVO) < 32 or ord(merkki_ARVO) == 127 for merkki_ARVO in Nimi):
        raise ValueError('잘못된 nippu polku_2 문자')
    if asennus_polku and (len(('/lib/' + Nimi).encode()) > 63 or Nimi in ('suomi.py', 'nippu.py')):
        raise ValueError('nippu polku_2 제한 또는 oletusarvo kirjasto 충돌: ' + Nimi)
    return Nimi


def purkaa_794097ae(Tiedosto_merkintä_nimi, data, Nimi, versio_ARVO):
    파일들 = {}
    명세들 = []
    def liitä_merkintä(polku_2, Sisältö_ARVO):
        vahvista_polku(polku_2)
        if polku_2 in 파일들:
            raise ValueError('중복 nippu polku_2: ' + polku_2)
        if len(Sisältö_ARVO) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + polku_2)
        Sisältö_ARVO.decode('utf-8')
        파일들[polku_2] = Sisältö_ARVO
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 lähde_puu 16개·summa_ARVO 64 KiB 이하여야 합니다.')
    if Tiedosto_merkintä_nimi.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as nippu:
            항목들 = nippu.infolist()
            if len(항목들) > 256 or sum(merkintä_ARVO_962f286b.file_size for merkintä_ARVO_962f286b in 항목들) > 1048576:
                raise ValueError('Arkisto_ARVO julkaista_Tallennus Koko 제한 초과')
            työ_luettelo = [merkintä_ARVO_962f286b for merkintä_ARVO_962f286b in 항목들 if merkintä_ARVO_962f286b.filename.endswith('.dist-info/WHEEL')]
            if len(työ_luettelo) != 1:
                raise ValueError('wheel sopimuksen_arvo 명세가 필요합니다.')
            sopimuksen_arvo = email.parser.Parser().parsestr(nippu.read(työ_luettelo[0]).decode())
            if sopimuksen_arvo.get('Root-Is-Purelib', '').lower() != 'true' or not Tiedosto_merkintä_nimi.endswith('-none-any.whl'):
                raise ValueError('C tarkenne_ARVO·플랫폼 전용 wheel은 지원하지 않습니다.')
            for merkintä_ARVO_962f286b in 항목들:
                polku_2 = merkintä_ARVO_962f286b.filename.rstrip('/')
                vahvista_polku(polku_2, False)
                if (merkintä_ARVO_962f286b.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 numero 없습니다.')
                if merkintä_ARVO_962f286b.filename.endswith('/'):
                    continue
                if '.dist-info/' in polku_2:
                    if polku_2.endswith('/METADATA'):
                        명세들.append(nippu.read(merkintä_ARVO_962f286b).decode())
                    continue
                if not polku_2.endswith('.py') or '.data/' in polku_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + polku_2)
                liitä_merkintä(polku_2, nippu.read(merkintä_ARVO_962f286b))
    elif Tiedosto_merkintä_nimi.endswith('.tar.gz') and Nimi.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Suorita_komento 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as nippu:
            뿌리들 = set()
            merkintä_LASKE = 0
            summa_muuttaa_kokoa = 0
            for merkintä_ARVO_962f286b in nippu:
                merkintä_LASKE += 1
                summa_muuttaa_kokoa += merkintä_ARVO_962f286b.size
                if merkintä_LASKE > 256 or summa_muuttaa_kokoa > 1048576:
                    raise ValueError('Arkisto_ARVO julkaista_Tallennus Koko 제한 초과')
                vahvista_polku(merkintä_ARVO_962f286b.name, False)
                부분들 = merkintä_ARVO_962f286b.name.split('/')
                뿌리들.add(부분들[0])
                if merkintä_ARVO_962f286b.isdir():
                    continue
                if not merkintä_ARVO_962f286b.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython lähde_puu 배포형')
                polku_2 = '/'.join(부분들[1:])
                Sisältö_ARVO = nippu.extractfile(merkintä_ARVO_962f286b).read()
                if polku_2.endswith('PKG-INFO'):
                    명세들.append(Sisältö_ARVO.decode())
                elif polku_2.endswith('.py') and polku_2 not in ('setup.py',):
                    liitä_merkintä(polku_2, Sisältö_ARVO)
                elif '.egg-info/' not in polku_2 and not polku_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + polku_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 juuri_ARVO 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* lähde_puu 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 jakelu_ARVO 메타데이터가 필요합니다.')
    määritys = email.parser.Parser().parsestr(명세들[0])
    if jäsentää_pyyntö(määritys.get('Name', ''))[0] != Nimi or määritys.get('Version') != versio_ARVO:
        raise ValueError('jakelu_ARVO 메타데이터의 Nimi·버전 불일치')
    if määritys.get_all('Requires-Dist') or määritys.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def lukea_Verkko(OSOITE, 한도):
    if not OSOITE.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS jakelu_ARVO 주소만 허용합니다.')
    with urllib.request.urlopen(OSOITE, timeout=30) as palaute:
        if not palaute.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 jakelu_ARVO OSOITE siirrä_ARVO_83b651b8')
        data = palaute.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('jakelu_ARVO tiedoston_nimi Koko 제한 초과')
    return data


def Siirrä_nippu(Nimi, versio_ARVO, 파일들, origo_ARVO):
    määritys = {'name': Nimi, 'version': versio_ARVO, 'source': origo_ARVO, 'files': [
        {'path': polku_2, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for polku_2, data in sorted(파일들.items())]}
    머리 = json.dumps(määritys, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('nippu määritys Koko 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[merkintä_ARVO_962f286b['path']] for merkintä_ARVO_962f286b in määritys['files'])


class nippu_säilö:
    def __init__(자신, polku_2, tietojärjestelmät_offline=False):
        자신.polku_2 = Path(polku_2)
        자신.polku_2.mkdir(parents=True, exist_ok=True)
        자신.tietojärjestelmät_offline = tietojärjestelmät_offline

    def Valmistele(자신, pyyntö):
        Nimi, versio_ARVO = jäsentää_pyyntö(pyyntö)
        열쇠 = Nimi + ('==' + versio_ARVO if versio_ARVO else '')
        LOG_polku = 자신.polku_2 / (열쇠 + '.json')
        jakelu_polku = 자신.polku_2 / (열쇠 + '.archive')
        if LOG_polku.is_file() and jakelu_polku.is_file():
            LOG_TIETUE = json.loads(LOG_polku.read_text())
            data = jakelu_polku.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_TIETUE['sha256']:
                raise ValueError('저장된 jakelu_ARVO 파일의 SHA-256 불일치')
        else:
            if 자신.tietojärjestelmät_offline:
                raise ValueError('tietojärjestelmät_offline 저장소에 없는 nippu: ' + pyyntö)
            OSOITE = 'https://pypi.org/pypi/' + Nimi + ('/' + versio_ARVO if versio_ARVO else '') + '/json'
            msinfo32_exe = json.loads(lukea_Verkko(OSOITE, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [merkintä_ARVO_962f286b for merkintä_ARVO_962f286b in msinfo32_exe['urls'] if not merkintä_ARVO_962f286b.get('yanked') and merkintä_ARVO_962f286b['filename'].endswith('-none-any.whl')]
            if not 후보 and Nimi.startswith('micropython-'):
                후보 = [merkintä_ARVO_962f286b for merkintä_ARVO_962f286b in msinfo32_exe['urls'] if not merkintä_ARVO_962f286b.get('yanked') and merkintä_ARVO_962f286b['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python jakelu_ARVO 파일이 없습니다.')
            valinta_ARVO = 후보[0]
            data = lukea_Verkko(valinta_ARVO['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != valinta_ARVO['digests']['sha256']:
                raise ValueError('PyPI jakelu_ARVO tiedoston_nimi SHA-256 불일치')
            LOG_TIETUE = {'name': Nimi, 'version': msinfo32_exe['info']['version'], 'filename': valinta_ARVO['filename'],
                    'url': valinta_ARVO['url'], 'sha256': valinta_ARVO['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            purkaa_794097ae(LOG_TIETUE['filename'], data, Nimi, LOG_TIETUE['version'])
            jakelu_polku.write_bytes(data)
            LOG_polku.write_text(json.dumps(LOG_TIETUE, ensure_ascii=False, indent=2) + '\n')
        if LOG_TIETUE['name'] != Nimi or versio_ARVO and LOG_TIETUE['version'] != versio_ARVO:
            raise ValueError('säilö_juuri Nimi·버전 불일치')
        파일들 = purkaa_794097ae(LOG_TIETUE['filename'], data, Nimi, LOG_TIETUE['version'])
        return Siirrä_nippu(Nimi, LOG_TIETUE['version'], 파일들, LOG_TIETUE['url'])


class nippu_pyyntö(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            pyyntö = bytearray()
            while b'\n' not in pyyntö and len(pyyntö) < 100:
                조각 = 자신.request.recv(100 - len(pyyntö))
                if not 조각:
                    return
                pyyntö.extend(조각)
            if not pyyntö.endswith(b'\n') or pyyntö.count(b'\n') != 1:
                raise ValueError('잘못된 nippu pyyntö')
            palaute = 자신.server.säilö_juuri.Valmistele(pyyntö[:-1].decode('ascii'))
        except Exception as VIRHE:
            머리 = json.dumps({'error': str(VIRHE)[:500]}, ensure_ascii=False).encode()
            palaute = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(palaute)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, portin_numero=8027, polku_2=None, tietojärjestelmät_offline=False):
        자신.palvelin_ARVO = socketserver.TCPServer(('127.0.0.1', portin_numero), nippu_pyyntö, bind_and_activate=False)
        자신.palvelin_ARVO.allow_reuse_address = True
        자신.palvelin_ARVO.server_bind()
        자신.palvelin_ARVO.server_activate()
        자신.palvelin_ARVO.säilö_juuri = nippu_säilö(polku_2 or aloite_juuri/'build/pip-cache', tietojärjestelmät_offline)
        자신.portin_numero = 자신.palvelin_ARVO.server_address[1]
        자신.säie_ARVO = threading.Thread(target=자신.palvelin_ARVO.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.säie_ARVO.start()
        return 자신

    def __exit__(자신, *argumentit):
        자신.palvelin_ARVO.shutdown()
        자신.palvelin_ARVO.server_close()
        자신.säie_ARVO.join(timeout=2)


def Suorita_2():
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('--port', type=int, default=8027)
    jäsennin_48ee4b1b.add_argument('--cache', type=Path, default=aloite_juuri/'build/pip-cache')
    jäsennin_48ee4b1b.add_argument('--offline', action='store_true')
    jäsennin_48ee4b1b.add_argument('--fetch', help='Suorita_komento 없이 호환 jakelu_ARVO 파일을 내려받아 검사·Store_ARVO')
    argumentit = jäsennin_48ee4b1b.parse_args()
    if argumentit.fetch:
        data = nippu_säilö(argumentit.cache, argumentit.offline).Valmistele(argumentit.fetch)
        print('nippu Valmistele 완료:', argumentit.fetch, len(data), 'tavu_ARVO')
        return
    with 꾸러미중계(argumentit.port, argumentit.cache, argumentit.offline) as 중계:
        print('nippu 중계: 127.0.0.1:' + str(중계.portin_numero), flush=True)
        try:
            중계.säie_ARVO.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Suorita_2()
