#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost wertWeitergeben. 게스트는 TCP로 받은 소스를 직접 wertEinrichten·실행한다."""
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

projektWurzel = Path(__file__).resolve().parents[1]


def anfrageAnalysieren(anfrage):
    istÜbereinstimmend = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', anfrage)
    if not istÜbereinstimmend:
        raise ValueError('Paket Name 또는 Name==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', istÜbereinstimmend[1]).lower(), istÜbereinstimmend[2]


def pfadValidieren(Name, einrichtungPfad=True):
    pfad = PurePosixPath(Name)
    if pfad.is_absolute() or any(unterteilWert in ('', '.', '..') or unterteilWert.startswith('.') for unterteilWert in Name.split('/')):
        raise ValueError('허용하지 않는 Paket pfad: ' + Name)
    if '\\' in Name or any(ord(zeichenWert) < 32 or ord(zeichenWert) == 127 for zeichenWert in Name):
        raise ValueError('잘못된 Paket pfad Zeichen')
    if einrichtungPfad and (len(('/lib/' + Name).encode()) > 63 or Name in ('Deutsch.py', 'Paket.py')):
        raise ValueError('Paket pfad grenzwertWert 또는 standardwertWert bibliothek 충돌: ' + Name)
    return Name


def entpacken(dateiEintragName, Daten, Name, versionWert):
    dateiEinträge = {}
    vorgaben = []
    def eintragAnhängen(pfad, inhaltswertWert):
        pfadValidieren(pfad)
        if pfad in dateiEinträge:
            raise ValueError('중복 Paket pfad: ' + pfad)
        if len(inhaltswertWert) > 16384:
            raise ValueError('파일당 16 KiB grenzwertWert 초과: ' + pfad)
        inhaltswertWert.decode('utf-8')
        dateiEinträge[pfad] = inhaltswertWert
        if len(dateiEinträge) > 16 or sum(map(len, dateiEinträge.values())) > 65536:
            raise ValueError('꾸러미는 quelltextBaum 16개·gesamtwertWert 64 KiB 이하여야 합니다.')
    if dateiEintragName.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(Daten)) as Paket:
            einträgeListe = Paket.infolist()
            if len(einträgeListe) > 256 or sum(eintragWert.file_size for eintragWert in einträgeListe) > 1048576:
                raise ValueError('archivWert speichergerätFreigeben größe grenzwertWert 초과')
            vertragListe = [eintragWert for eintragWert in einträgeListe if eintragWert.filename.endswith('.dist-info/WHEEL')]
            if len(vertragListe) != 1:
                raise ValueError('wheel vertragWert 명세가 필요합니다.')
            vertragWert = email.parser.Parser().parsestr(Paket.read(vertragListe[0]).decode())
            if vertragWert.get('Root-Is-Purelib', '').lower() != 'true' or not dateiEintragName.endswith('-none-any.whl'):
                raise ValueError('C erweiterungWert·플랫폼 전용 wheel은 지원하지 않습니다.')
            for eintragWert in einträgeListe:
                pfad = eintragWert.filename.rstrip('/')
                pfadValidieren(pfad, False)
                if (eintragWert.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 Zahl 없습니다.')
                if eintragWert.filename.endswith('/'):
                    continue
                if '.dist-info/' in pfad:
                    if pfad.endswith('/METADATA'):
                        vorgaben.append(Paket.read(eintragWert).decode())
                    continue
                if not pfad.endswith('.py') or '.data/' in pfad:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + pfad)
                eintragAnhängen(pfad, Paket.read(eintragWert))
    elif dateiEintragName.endswith('.tar.gz') and Name.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py befehlAusführen 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(Daten), mode='r|gz') as Paket:
            wurzelnListe = set()
            eintragAnzahl = 0
            gesamtwertGröße = 0
            for eintragWert in Paket:
                eintragAnzahl += 1
                gesamtwertGröße += eintragWert.size
                if eintragAnzahl > 256 or gesamtwertGröße > 1048576:
                    raise ValueError('archivWert speichergerätFreigeben größe grenzwertWert 초과')
                pfadValidieren(eintragWert.name, False)
                teile = eintragWert.name.split('/')
                wurzelnListe.add(teile[0])
                if eintragWert.isdir():
                    continue
                if not eintragWert.isfile() or len(teile) < 2:
                    raise ValueError('잘못된 MicroPython quelltextBaum 배포형')
                pfad = '/'.join(teile[1:])
                inhaltswertWert = Paket.extractfile(eintragWert).read()
                if pfad.endswith('PKG-INFO'):
                    vorgaben.append(inhaltswertWert.decode())
                elif pfad.endswith('.py') and pfad not in ('setup.py',):
                    eintragAnhängen(pfad, inhaltswertWert)
                elif '.egg-info/' not in pfad and not pfad.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + pfad)
            if len(wurzelnListe) != 1:
                raise ValueError('MicroPython 소스의 wurzelWert 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* quelltextBaum 배포형이 필요합니다.')
    if not dateiEinträge or len(vorgaben) != 1:
        raise ValueError('소스와 verteilungWert 메타데이터가 필요합니다.')
    vorgabe = email.parser.Parser().parsestr(vorgaben[0])
    if anfrageAnalysieren(vorgabe.get('Name', ''))[0] != Name or vorgabe.get('Version') != versionWert:
        raise ValueError('verteilungWert 메타데이터의 Name·버전 불일치')
    if vorgabe.get_all('Requires-Dist') or vorgabe.get_all('Requires'):
        raise ValueError('자동 abhängigkeiten 해결은 아직 지원하지 않습니다. abhängigkeiten 없는 호환 꾸러미를 사용하십시오.')
    return dateiEinträge


def webLesen(adresse, kapazitätGrenzwert):
    if not adresse.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS verteilungWert 주소만 허용합니다.')
    with urllib.request.urlopen(adresse, timeout=30) as antwort:
        if not antwort.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 verteilungWert adresse bewegenWert')
        Daten = antwort.read(kapazitätGrenzwert + 1)
    if len(Daten) > kapazitätGrenzwert:
        raise ValueError('verteilungWert Datei größe grenzwertWert 초과')
    return Daten


def übertragungBündel(Name, versionWert, dateiEinträge, ursprungWert):
    vorgabe = {'name': Name, 'version': versionWert, 'source': ursprungWert, 'files': [
        {'path': pfad, 'size': len(Daten), 'sha256': hashlib.sha256(Daten).hexdigest()}
        for pfad, Daten in sorted(dateiEinträge.items())]}
    kopfWert = json.dumps(vorgabe, ensure_ascii=False).encode()
    if len(kopfWert) > 8192:
        raise ValueError('Paket vorgabe größe 초과')
    return b'JKP1' + struct.pack('>I', len(kopfWert)) + kopfWert + b''.join(dateiEinträge[eintragWert['path']] for eintragWert in vorgabe['files'])


class bündelAblage:
    def __init__(selbstWert, pfad, istGetrenntBetrieben=False):
        selbstWert.pfad = Path(pfad)
        selbstWert.pfad.mkdir(parents=True, exist_ok=True)
        selbstWert.istGetrenntBetrieben = istGetrenntBetrieben

    def vorbereiten(selbstWert, anfrage):
        Name, versionWert = anfrageAnalysieren(anfrage)
        tasteMaterial = Name + ('==' + versionWert if versionWert else '')
        protokolldateiPfad = selbstWert.pfad / (tasteMaterial + '.json')
        verteilungPfad = selbstWert.pfad / (tasteMaterial + '.archive')
        if protokolldateiPfad.is_file() and verteilungPfad.is_file():
            protokolldateiAufzeichnung = json.loads(protokolldateiPfad.read_text())
            Daten = verteilungPfad.read_bytes()
            if hashlib.sha256(Daten).hexdigest() != protokolldateiAufzeichnung['sha256']:
                raise ValueError('저장된 verteilungWert 파일의 SHA-256 불일치')
        else:
            if selbstWert.istGetrenntBetrieben:
                raise ValueError('istGetrenntBetrieben 저장소에 없는 Paket: ' + anfrage)
            adresse = 'https://pypi.org/pypi/' + Name + ('/' + versionWert if versionWert else '') + '/json'
            systemInformation = json.loads(webLesen(adresse, 4194304).decode())
            if systemInformation['info'].get('requires_dist'):
                raise ValueError('자동 abhängigkeiten 해결은 아직 지원하지 않습니다.')
            kandidat = [eintragWert for eintragWert in systemInformation['urls'] if not eintragWert.get('yanked') and eintragWert['filename'].endswith('-none-any.whl')]
            if not kandidat and Name.startswith('micropython-'):
                kandidat = [eintragWert for eintragWert in systemInformation['urls'] if not eintragWert.get('yanked') and eintragWert['filename'].endswith('.tar.gz')]
            if not kandidat:
                raise ValueError('지원되는 순수 Python verteilungWert 파일이 없습니다.')
            auswahlWert = kandidat[0]
            Daten = webLesen(auswahlWert['url'], 4194304)
            if hashlib.sha256(Daten).hexdigest() != auswahlWert['digests']['sha256']:
                raise ValueError('PyPI verteilungWert Datei SHA-256 불일치')
            protokolldateiAufzeichnung = {'name': Name, 'version': systemInformation['info']['version'], 'filename': auswahlWert['filename'],
                    'url': auswahlWert['url'], 'sha256': auswahlWert['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            entpacken(protokolldateiAufzeichnung['filename'], Daten, Name, protokolldateiAufzeichnung['version'])
            verteilungPfad.write_bytes(Daten)
            protokolldateiPfad.write_text(json.dumps(protokolldateiAufzeichnung, ensure_ascii=False, indent=2) + '\n')
        if protokolldateiAufzeichnung['name'] != Name or versionWert and protokolldateiAufzeichnung['version'] != versionWert:
            raise ValueError('ablageWurzel Name·버전 불일치')
        dateiEinträge = entpacken(protokolldateiAufzeichnung['filename'], Daten, Name, protokolldateiAufzeichnung['version'])
        return übertragungBündel(Name, protokolldateiAufzeichnung['version'], dateiEinträge, protokolldateiAufzeichnung['url'])


class bündelAnfrage(socketserver.BaseRequestHandler):
    def handle(selbstWert):
        selbstWert.request.settimeout(10)
        try:
            anfrage = bytearray()
            while b'\n' not in anfrage and len(anfrage) < 100:
                fragmentWert = selbstWert.request.recv(100 - len(anfrage))
                if not fragmentWert:
                    return
                anfrage.extend(fragmentWert)
            if not anfrage.endswith(b'\n') or anfrage.count(b'\n') != 1:
                raise ValueError('잘못된 Paket anfrage')
            antwort = selbstWert.server.ablageWurzel.vorbereiten(anfrage[:-1].decode('ascii'))
        except Exception as fehler:
            kopfWert = json.dumps({'error': str(fehler)[:500]}, ensure_ascii=False).encode()
            antwort = b'JKP1' + struct.pack('>I', len(kopfWert)) + kopfWert
        try:
            selbstWert.request.sendall(antwort)
        except OSError:
            pass


class bündelWeitergeben:
    def __init__(selbstWert, portNummer=8027, pfad=None, istGetrenntBetrieben=False):
        selbstWert.dienstanbieterWert = socketserver.TCPServer(('127.0.0.1', portNummer), bündelAnfrage, bind_and_activate=False)
        selbstWert.dienstanbieterWert.allow_reuse_address = True
        selbstWert.dienstanbieterWert.server_bind()
        selbstWert.dienstanbieterWert.server_activate()
        selbstWert.dienstanbieterWert.ablageWurzel = bündelAblage(pfad or projektWurzel/'build/pip-cache', istGetrenntBetrieben)
        selbstWert.portNummer = selbstWert.dienstanbieterWert.server_address[1]
        selbstWert.ausführungsfadenWert = threading.Thread(target=selbstWert.dienstanbieterWert.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(selbstWert):
        selbstWert.ausführungsfadenWert.start()
        return selbstWert

    def __exit__(selbstWert, *argumente):
        selbstWert.dienstanbieterWert.shutdown()
        selbstWert.dienstanbieterWert.server_close()
        selbstWert.ausführungsfadenWert.join(timeout=2)


def ausführenVorgang():
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('--port', type=int, default=8027)
    Strukturanalysierer.add_argument('--cache', type=Path, default=projektWurzel/'build/pip-cache')
    Strukturanalysierer.add_argument('--offline', action='store_true')
    Strukturanalysierer.add_argument('--fetch', help='befehlAusführen 없이 호환 verteilungWert 파일을 내려받아 Prüfpunkte·ablegenDatenWert')
    argumente = Strukturanalysierer.parse_args()
    if argumente.fetch:
        Daten = bündelAblage(argumente.cache, argumente.offline).vorbereiten(argumente.fetch)
        print('Paket vorbereiten istFertig:', argumente.fetch, len(Daten), 'byteWert')
        return
    with bündelWeitergeben(argumente.port, argumente.cache, argumente.offline) as wertWeitergeben:
        print('Paket wertWeitergeben: 127.0.0.1:' + str(wertWeitergeben.portNummer), flush=True)
        try:
            wertWeitergeben.ausführungsfadenWert.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ausführenVorgang()
