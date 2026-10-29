#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installeren_WAARDE·실행한다."""
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

Taken_wortel = Path(__file__).resolve().parents[1]


def parseren_aanvraag(aanvraag):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', aanvraag)
    if not 맞음:
        raise ValueError('bundel Naam 또는 Naam==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def valideren_pad(Naam, installatie_pad=True):
    pad = PurePosixPath(Naam)
    if pad.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Naam.split('/')):
        raise ValueError('허용하지 않는 bundel pad: ' + Naam)
    if '\\' in Naam or any(ord(teken_WAARDE) < 32 or ord(teken_WAARDE) == 127 for teken_WAARDE in Naam):
        raise ValueError('잘못된 bundel pad 문자')
    if installatie_pad and (len(('/lib/' + Naam).encode()) > 63 or Naam in ('Nederlands.py', 'bundel.py')):
        raise ValueError('bundel pad 제한 또는 standaardwaarde bibliotheek 충돌: ' + Naam)
    return Naam


def decomprimeren(Bestand_invoer_naam, gegevens, Naam, versie_WAARDE):
    파일들 = {}
    명세들 = []
    def toevoegen_invoer(pad, Inhoud_WAARDE):
        valideren_pad(pad)
        if pad in 파일들:
            raise ValueError('중복 bundel pad: ' + pad)
        if len(Inhoud_WAARDE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + pad)
        Inhoud_WAARDE.decode('utf-8')
        파일들[pad] = Inhoud_WAARDE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 bron_structuur 16개·totaal_WAARDE 64 KiB 이하여야 합니다.')
    if Bestand_invoer_naam.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(gegevens)) as bundel:
            항목들 = bundel.infolist()
            if len(항목들) > 256 or sum(invoer_WAARDE_962f286b.file_size for invoer_WAARDE_962f286b in 항목들) > 1048576:
                raise ValueError('Archief_WAARDE versie_Opslag Grootte 제한 초과')
            taak_Lijst = [invoer_WAARDE_962f286b for invoer_WAARDE_962f286b in 항목들 if invoer_WAARDE_962f286b.filename.endswith('.dist-info/WHEEL')]
            if len(taak_Lijst) != 1:
                raise ValueError('wheel contractwaarde 명세가 필요합니다.')
            contractwaarde = email.parser.Parser().parsestr(bundel.read(taak_Lijst[0]).decode())
            if contractwaarde.get('Root-Is-Purelib', '').lower() != 'true' or not Bestand_invoer_naam.endswith('-none-any.whl'):
                raise ValueError('C extensie_WAARDE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for invoer_WAARDE_962f286b in 항목들:
                pad = invoer_WAARDE_962f286b.filename.rstrip('/')
                valideren_pad(pad, False)
                if (invoer_WAARDE_962f286b.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 nummer 없습니다.')
                if invoer_WAARDE_962f286b.filename.endswith('/'):
                    continue
                if '.dist-info/' in pad:
                    if pad.endswith('/METADATA'):
                        명세들.append(bundel.read(invoer_WAARDE_962f286b).decode())
                    continue
                if not pad.endswith('.py') or '.data/' in pad:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + pad)
                toevoegen_invoer(pad, bundel.read(invoer_WAARDE_962f286b))
    elif Bestand_invoer_naam.endswith('.tar.gz') and Naam.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Uitvoeren_opdracht 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(gegevens), mode='r|gz') as bundel:
            뿌리들 = set()
            invoer_AANTAL_8f7753a1 = 0
            totaal_formaat_wijzigen = 0
            for invoer_WAARDE_962f286b in bundel:
                invoer_AANTAL_8f7753a1 += 1
                totaal_formaat_wijzigen += invoer_WAARDE_962f286b.size
                if invoer_AANTAL_8f7753a1 > 256 or totaal_formaat_wijzigen > 1048576:
                    raise ValueError('Archief_WAARDE versie_Opslag Grootte 제한 초과')
                valideren_pad(invoer_WAARDE_962f286b.name, False)
                부분들 = invoer_WAARDE_962f286b.name.split('/')
                뿌리들.add(부분들[0])
                if invoer_WAARDE_962f286b.isdir():
                    continue
                if not invoer_WAARDE_962f286b.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython bron_structuur 배포형')
                pad = '/'.join(부분들[1:])
                Inhoud_WAARDE = bundel.extractfile(invoer_WAARDE_962f286b).read()
                if pad.endswith('PKG-INFO'):
                    명세들.append(Inhoud_WAARDE.decode())
                elif pad.endswith('.py') and pad not in ('setup.py',):
                    toevoegen_invoer(pad, Inhoud_WAARDE)
                elif '.egg-info/' not in pad and not pad.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + pad)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 wortel_WAARDE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* bron_structuur 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 distributie_WAARDE 메타데이터가 필요합니다.')
    specificatie = email.parser.Parser().parsestr(명세들[0])
    if parseren_aanvraag(specificatie.get('Name', ''))[0] != Naam or specificatie.get('Version') != versie_WAARDE:
        raise ValueError('distributie_WAARDE 메타데이터의 Naam·버전 불일치')
    if specificatie.get_all('Requires-Dist') or specificatie.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADRES, 한도):
    if not ADRES.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS distributie_WAARDE 주소만 허용합니다.')
    with urllib.request.urlopen(ADRES, timeout=30) as reactie:
        if not reactie.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 distributie_WAARDE ADRES verplaatsen_WAARDE_83b651b8')
        gegevens = reactie.read(한도 + 1)
    if len(gegevens) > 한도:
        raise ValueError('distributie_WAARDE bestand Grootte 제한 초과')
    return gegevens


def transfer_bundel(Naam, versie_WAARDE, 파일들, oorsprong_WAARDE):
    specificatie = {'name': Naam, 'version': versie_WAARDE, 'source': oorsprong_WAARDE, 'files': [
        {'path': pad, 'size': len(gegevens), 'sha256': hashlib.sha256(gegevens).hexdigest()}
        for pad, gegevens in sorted(파일들.items())]}
    kop_WAARDE = json.dumps(specificatie, ensure_ascii=False).encode()
    if len(kop_WAARDE) > 8192:
        raise ValueError('bundel specificatie Grootte 초과')
    return b'JKP1' + struct.pack('>I', len(kop_WAARDE)) + kop_WAARDE + b''.join(파일들[invoer_WAARDE_962f286b['path']] for invoer_WAARDE_962f286b in specificatie['files'])


class bundel_opslagplaats:
    def __init__(자신, pad, informatie_Offline=False):
        자신.pad = Path(pad)
        자신.pad.mkdir(parents=True, exist_ok=True)
        자신.informatie_Offline = informatie_Offline

    def Bereid_voor(자신, aanvraag):
        Naam, versie_WAARDE = parseren_aanvraag(aanvraag)
        열쇠 = Naam + ('==' + versie_WAARDE if versie_WAARDE else '')
        LOG_pad = 자신.pad / (열쇠 + '.json')
        distributie_pad = 자신.pad / (열쇠 + '.archive')
        if LOG_pad.is_file() and distributie_pad.is_file():
            LOG_RECORD = json.loads(LOG_pad.read_text())
            gegevens = distributie_pad.read_bytes()
            if hashlib.sha256(gegevens).hexdigest() != LOG_RECORD['sha256']:
                raise ValueError('저장된 distributie_WAARDE 파일의 SHA-256 불일치')
        else:
            if 자신.informatie_Offline:
                raise ValueError('informatie_Offline 저장소에 없는 bundel: ' + aanvraag)
            ADRES = 'https://pypi.org/pypi/' + Naam + ('/' + versie_WAARDE if versie_WAARDE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADRES, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            sollicitant = [invoer_WAARDE_962f286b for invoer_WAARDE_962f286b in msinfo32_exe['urls'] if not invoer_WAARDE_962f286b.get('yanked') and invoer_WAARDE_962f286b['filename'].endswith('-none-any.whl')]
            if not sollicitant and Naam.startswith('micropython-'):
                sollicitant = [invoer_WAARDE_962f286b for invoer_WAARDE_962f286b in msinfo32_exe['urls'] if not invoer_WAARDE_962f286b.get('yanked') and invoer_WAARDE_962f286b['filename'].endswith('.tar.gz')]
            if not sollicitant:
                raise ValueError('지원되는 순수 Python distributie_WAARDE 파일이 없습니다.')
            selectie_WAARDE = sollicitant[0]
            gegevens = 웹읽기(selectie_WAARDE['url'], 4194304)
            if hashlib.sha256(gegevens).hexdigest() != selectie_WAARDE['digests']['sha256']:
                raise ValueError('PyPI distributie_WAARDE bestand SHA-256 불일치')
            LOG_RECORD = {'name': Naam, 'version': msinfo32_exe['info']['version'], 'filename': selectie_WAARDE['filename'],
                    'url': selectie_WAARDE['url'], 'sha256': selectie_WAARDE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            decomprimeren(LOG_RECORD['filename'], gegevens, Naam, LOG_RECORD['version'])
            distributie_pad.write_bytes(gegevens)
            LOG_pad.write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_RECORD['name'] != Naam or versie_WAARDE and LOG_RECORD['version'] != versie_WAARDE:
            raise ValueError('opslagplaats_wortel Naam·버전 불일치')
        파일들 = decomprimeren(LOG_RECORD['filename'], gegevens, Naam, LOG_RECORD['version'])
        return transfer_bundel(Naam, LOG_RECORD['version'], 파일들, LOG_RECORD['url'])


class bundel_aanvraag(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            aanvraag = bytearray()
            while b'\n' not in aanvraag and len(aanvraag) < 100:
                조각 = 자신.request.recv(100 - len(aanvraag))
                if not 조각:
                    return
                aanvraag.extend(조각)
            if not aanvraag.endswith(b'\n') or aanvraag.count(b'\n') != 1:
                raise ValueError('잘못된 bundel aanvraag')
            reactie = 자신.server.opslagplaats_wortel.Bereid_voor(aanvraag[:-1].decode('ascii'))
        except Exception as fout:
            kop_WAARDE = json.dumps({'error': str(fout)[:500]}, ensure_ascii=False).encode()
            reactie = b'JKP1' + struct.pack('>I', len(kop_WAARDE)) + kop_WAARDE
        try:
            자신.request.sendall(reactie)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, poortnummer=8027, pad=None, informatie_Offline=False):
        자신.server_WAARDE = socketserver.TCPServer(('127.0.0.1', poortnummer), bundel_aanvraag, bind_and_activate=False)
        자신.server_WAARDE.allow_reuse_address = True
        자신.server_WAARDE.server_bind()
        자신.server_WAARDE.server_activate()
        자신.server_WAARDE.opslagplaats_wortel = bundel_opslagplaats(pad or Taken_wortel/'build/pip-cache', informatie_Offline)
        자신.poortnummer = 자신.server_WAARDE.server_address[1]
        자신.thread_WAARDE = threading.Thread(target=자신.server_WAARDE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.thread_WAARDE.start()
        return 자신

    def __exit__(자신, *argumenten):
        자신.server_WAARDE.shutdown()
        자신.server_WAARDE.server_close()
        자신.thread_WAARDE.join(timeout=2)


def starten():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=Taken_wortel/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='Uitvoeren_opdracht 없이 호환 distributie_WAARDE 파일을 내려받아 검사·Store_WAARDE')
    argumenten = parser_48ee4b1b.parse_args()
    if argumenten.fetch:
        gegevens = bundel_opslagplaats(argumenten.cache, argumenten.offline).Bereid_voor(argumenten.fetch)
        print('bundel Bereid_voor 완료:', argumenten.fetch, len(gegevens), 'byte_WAARDE')
        return
    with 꾸러미중계(argumenten.port, argumenten.cache, argumenten.offline) as 중계:
        print('bundel 중계: 127.0.0.1:' + str(중계.poortnummer), flush=True)
        try:
            중계.thread_WAARDE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    starten()
