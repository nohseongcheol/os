#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instalēt_VALUE·실행한다."""
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

Project_sakne = Path(__file__).resolve().parents[1]


def parsēt_pieprasījums(pieprasījums):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', pieprasījums)
    if not 맞음:
        raise ValueError('saistīt Nosaukums 또는 Nosaukums==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def validēt_ceļš(Nosaukums, instalēšana_ceļš=True):
    CEĻŠ = PurePosixPath(Nosaukums)
    if CEĻŠ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nosaukums.split('/')):
        raise ValueError('허용하지 않는 saistīt CEĻŠ: ' + Nosaukums)
    if '\\' in Nosaukums or any(ord(rakstzīme_VALUE) < 32 or ord(rakstzīme_VALUE) == 127 for rakstzīme_VALUE in Nosaukums):
        raise ValueError('잘못된 saistīt CEĻŠ 문자')
    if instalēšana_ceļš and (len(('/lib/' + Nosaukums).encode()) > 63 or Nosaukums in ('Latviešu.py', 'saistīt.py')):
        raise ValueError('saistīt CEĻŠ 제한 또는 noklusējuma_vērtība bibliotēka 충돌: ' + Nosaukums)
    return Nosaukums


def atspiest(Fails_ievade_nosaukums, dati, Nosaukums, versija_VALUE):
    파일들 = {}
    명세들 = []
    def Pievienot_ievade(CEĻŠ, Saturs_VALUE):
        validēt_ceļš(CEĻŠ)
        if CEĻŠ in 파일들:
            raise ValueError('중복 saistīt CEĻŠ: ' + CEĻŠ)
        if len(Saturs_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + CEĻŠ)
        Saturs_VALUE.decode('utf-8')
        파일들[CEĻŠ] = Saturs_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 avots_koks 16개·kopsumma_VALUE 64 KiB 이하여야 합니다.')
    if Fails_ievade_nosaukums.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(dati)) as saistīt:
            항목들 = saistīt.infolist()
            if len(항목들) > 256 or sum(ievade_VALUE.file_size for ievade_VALUE in 항목들) > 1048576:
                raise ValueError('Arhīvs_VALUE izlaist_Krātuve Izmērs 제한 초과')
            līgums_Saraksts = [ievade_VALUE for ievade_VALUE in 항목들 if ievade_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(līgums_Saraksts) != 1:
                raise ValueError('wheel līguma_vērtība 명세가 필요합니다.')
            līguma_vērtība = email.parser.Parser().parsestr(saistīt.read(līgums_Saraksts[0]).decode())
            if līguma_vērtība.get('Root-Is-Purelib', '').lower() != 'true' or not Fails_ievade_nosaukums.endswith('-none-any.whl'):
                raise ValueError('C paplašinājums_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ievade_VALUE in 항목들:
                CEĻŠ = ievade_VALUE.filename.rstrip('/')
                validēt_ceļš(CEĻŠ, False)
                if (ievade_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 numurs 없습니다.')
                if ievade_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in CEĻŠ:
                    if CEĻŠ.endswith('/METADATA'):
                        명세들.append(saistīt.read(ievade_VALUE).decode())
                    continue
                if not CEĻŠ.endswith('.py') or '.data/' in CEĻŠ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + CEĻŠ)
                Pievienot_ievade(CEĻŠ, saistīt.read(ievade_VALUE))
    elif Fails_ievade_nosaukums.endswith('.tar.gz') and Nosaukums.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Izpildīt_komanda 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(dati), mode='r|gz') as saistīt:
            뿌리들 = set()
            ievade_COUNT = 0
            kopsumma_mainīt_izmērus = 0
            for ievade_VALUE in saistīt:
                ievade_COUNT += 1
                kopsumma_mainīt_izmērus += ievade_VALUE.size
                if ievade_COUNT > 256 or kopsumma_mainīt_izmērus > 1048576:
                    raise ValueError('Arhīvs_VALUE izlaist_Krātuve Izmērs 제한 초과')
                validēt_ceļš(ievade_VALUE.name, False)
                부분들 = ievade_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if ievade_VALUE.isdir():
                    continue
                if not ievade_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython avots_koks 배포형')
                CEĻŠ = '/'.join(부분들[1:])
                Saturs_VALUE = saistīt.extractfile(ievade_VALUE).read()
                if CEĻŠ.endswith('PKG-INFO'):
                    명세들.append(Saturs_VALUE.decode())
                elif CEĻŠ.endswith('.py') and CEĻŠ not in ('setup.py',):
                    Pievienot_ievade(CEĻŠ, Saturs_VALUE)
                elif '.egg-info/' not in CEĻŠ and not CEĻŠ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + CEĻŠ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 sakne_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* avots_koks 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 sadale_VALUE 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if parsēt_pieprasījums(명세.get('Name', ''))[0] != Nosaukums or 명세.get('Version') != versija_VALUE:
        raise ValueError('sadale_VALUE 메타데이터의 Nosaukums·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(adrese, 한도):
    if not adrese.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS sadale_VALUE 주소만 허용합니다.')
    with urllib.request.urlopen(adrese, timeout=30) as atbilde:
        if not atbilde.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 sadale_VALUE adrese pārvietot_VALUE')
        dati = atbilde.read(한도 + 1)
    if len(dati) > 한도:
        raise ValueError('sadale_VALUE Fails Izmērs 제한 초과')
    return dati


def nodot_saistīt(Nosaukums, versija_VALUE, 파일들, 출처):
    명세 = {'name': Nosaukums, 'version': versija_VALUE, 'source': 출처, 'files': [
        {'path': CEĻŠ, 'size': len(dati), 'sha256': hashlib.sha256(dati).hexdigest()}
        for CEĻŠ, dati in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('saistīt 명세 Izmērs 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ievade_VALUE['path']] for ievade_VALUE in 명세['files'])


class saistīt_repozitorijs:
    def __init__(자신, CEĻŠ, informācijas_tehnoloģija_Bezsaistē=False):
        자신.CEĻŠ = Path(CEĻŠ)
        자신.CEĻŠ.mkdir(parents=True, exist_ok=True)
        자신.informācijas_tehnoloģija_Bezsaistē = informācijas_tehnoloģija_Bezsaistē

    def Sagatavot(자신, pieprasījums):
        Nosaukums, versija_VALUE = parsēt_pieprasījums(pieprasījums)
        열쇠 = Nosaukums + ('==' + versija_VALUE if versija_VALUE else '')
        LOG_ceļš = 자신.CEĻŠ / (열쇠 + '.json')
        sadale_ceļš = 자신.CEĻŠ / (열쇠 + '.archive')
        if LOG_ceļš.is_file() and sadale_ceļš.is_file():
            LOG_RECORD = json.loads(LOG_ceļš.read_text())
            dati = sadale_ceļš.read_bytes()
            if hashlib.sha256(dati).hexdigest() != LOG_RECORD['sha256']:
                raise ValueError('저장된 sadale_VALUE 파일의 SHA-256 불일치')
        else:
            if 자신.informācijas_tehnoloģija_Bezsaistē:
                raise ValueError('informācijas_tehnoloģija_Bezsaistē 저장소에 없는 saistīt: ' + pieprasījums)
            adrese = 'https://pypi.org/pypi/' + Nosaukums + ('/' + versija_VALUE if versija_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(adrese, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ievade_VALUE for ievade_VALUE in msinfo32_exe['urls'] if not ievade_VALUE.get('yanked') and ievade_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Nosaukums.startswith('micropython-'):
                후보 = [ievade_VALUE for ievade_VALUE in msinfo32_exe['urls'] if not ievade_VALUE.get('yanked') and ievade_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python sadale_VALUE 파일이 없습니다.')
            atlase_VALUE = 후보[0]
            dati = 웹읽기(atlase_VALUE['url'], 4194304)
            if hashlib.sha256(dati).hexdigest() != atlase_VALUE['digests']['sha256']:
                raise ValueError('PyPI sadale_VALUE Fails SHA-256 불일치')
            LOG_RECORD = {'name': Nosaukums, 'version': msinfo32_exe['info']['version'], 'filename': atlase_VALUE['filename'],
                    'url': atlase_VALUE['url'], 'sha256': atlase_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            atspiest(LOG_RECORD['filename'], dati, Nosaukums, LOG_RECORD['version'])
            sadale_ceļš.write_bytes(dati)
            LOG_ceļš.write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2) + '\n')
        if LOG_RECORD['name'] != Nosaukums or versija_VALUE and LOG_RECORD['version'] != versija_VALUE:
            raise ValueError('repozitorijs_sakne Nosaukums·버전 불일치')
        파일들 = atspiest(LOG_RECORD['filename'], dati, Nosaukums, LOG_RECORD['version'])
        return nodot_saistīt(Nosaukums, LOG_RECORD['version'], 파일들, LOG_RECORD['url'])


class saistīt_pieprasījums(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            pieprasījums = bytearray()
            while b'\n' not in pieprasījums and len(pieprasījums) < 100:
                조각 = 자신.request.recv(100 - len(pieprasījums))
                if not 조각:
                    return
                pieprasījums.extend(조각)
            if not pieprasījums.endswith(b'\n') or pieprasījums.count(b'\n') != 1:
                raise ValueError('잘못된 saistīt pieprasījums')
            atbilde = 자신.server.repozitorijs_sakne.Sagatavot(pieprasījums[:-1].decode('ascii'))
        except Exception as Kļūda:
            머리 = json.dumps({'error': str(Kļūda)[:500]}, ensure_ascii=False).encode()
            atbilde = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(atbilde)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, porta_numurs=8027, CEĻŠ=None, informācijas_tehnoloģija_Bezsaistē=False):
        자신.serveris_VALUE = socketserver.TCPServer(('127.0.0.1', porta_numurs), saistīt_pieprasījums, bind_and_activate=False)
        자신.serveris_VALUE.allow_reuse_address = True
        자신.serveris_VALUE.server_bind()
        자신.serveris_VALUE.server_activate()
        자신.serveris_VALUE.repozitorijs_sakne = saistīt_repozitorijs(CEĻŠ or Project_sakne/'build/pip-cache', informācijas_tehnoloģija_Bezsaistē)
        자신.porta_numurs = 자신.serveris_VALUE.server_address[1]
        자신.saruna_VALUE = threading.Thread(target=자신.serveris_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.saruna_VALUE.start()
        return 자신

    def __exit__(자신, *Parametri):
        자신.serveris_VALUE.shutdown()
        자신.serveris_VALUE.server_close()
        자신.saruna_VALUE.join(timeout=2)


def Palaist():
    parsētājs_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parsētājs_48ee4b1b.add_argument('--port', type=int, default=8027)
    parsētājs_48ee4b1b.add_argument('--cache', type=Path, default=Project_sakne/'build/pip-cache')
    parsētājs_48ee4b1b.add_argument('--offline', action='store_true')
    parsētājs_48ee4b1b.add_argument('--fetch', help='Izpildīt_komanda 없이 호환 sadale_VALUE 파일을 내려받아 검사·Store_VALUE')
    Parametri = parsētājs_48ee4b1b.parse_args()
    if Parametri.fetch:
        dati = saistīt_repozitorijs(Parametri.cache, Parametri.offline).Sagatavot(Parametri.fetch)
        print('saistīt Sagatavot 완료:', Parametri.fetch, len(dati), 'byte_VALUE')
        return
    with 꾸러미중계(Parametri.port, Parametri.cache, Parametri.offline) as 중계:
        print('saistīt 중계: 127.0.0.1:' + str(중계.porta_numurs), flush=True)
        try:
            중계.saruna_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Palaist()
