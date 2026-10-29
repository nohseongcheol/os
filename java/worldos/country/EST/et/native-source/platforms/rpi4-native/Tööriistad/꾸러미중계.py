#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installima_VALUE·실행한다."""
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

Project_juur = Path(__file__).resolve().parents[1]


def sõeluma_päring(päring):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', päring)
    if not 맞음:
        raise ValueError('kogum Nimi_2 또는 Nimi_2==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def valideerima_tee(Nimi_2, installimine_tee=True):
    RADA = PurePosixPath(Nimi_2)
    if RADA.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nimi_2.split('/')):
        raise ValueError('허용하지 않는 kogum RADA: ' + Nimi_2)
    if '\\' in Nimi_2 or any(ord(märk_VALUE) < 32 or ord(märk_VALUE) == 127 for märk_VALUE in Nimi_2):
        raise ValueError('잘못된 kogum RADA 문자')
    if installimine_tee and (len(('/lib/' + Nimi_2).encode()) > 63 or Nimi_2 in ('Eesti.py', 'kogum.py')):
        raise ValueError('kogum RADA 제한 또는 vaikeväärtus teek 충돌: ' + Nimi_2)
    return Nimi_2


def lahti_pakkima(Fail_kirje_nimetus, andmed, Nimi_2, versioon_VALUE):
    파일들 = {}
    명세들 = []
    def Lisa_kirje(RADA, Sisu_VALUE):
        valideerima_tee(RADA)
        if RADA in 파일들:
            raise ValueError('중복 kogum RADA: ' + RADA)
        if len(Sisu_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + RADA)
        Sisu_VALUE.decode('utf-8')
        파일들[RADA] = Sisu_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 lähe_puu 16개·kokku_VALUE 64 KiB 이하여야 합니다.')
    if Fail_kirje_nimetus.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(andmed)) as kogum:
            항목들 = kogum.infolist()
            if len(항목들) > 256 or sum(kirje_VALUE.file_size for kirje_VALUE in 항목들) > 1048576:
                raise ValueError('Arhiiv_VALUE vabastama_salvesti Suurus 제한 초과')
            kaasus_Loend = [kirje_VALUE for kirje_VALUE in 항목들 if kirje_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(kaasus_Loend) != 1:
                raise ValueError('wheel lepingu_väärtus 명세가 필요합니다.')
            lepingu_väärtus = email.parser.Parser().parsestr(kogum.read(kaasus_Loend[0]).decode())
            if lepingu_väärtus.get('Root-Is-Purelib', '').lower() != 'true' or not Fail_kirje_nimetus.endswith('-none-any.whl'):
                raise ValueError('C laiendus_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for kirje_VALUE in 항목들:
                RADA = kirje_VALUE.filename.rstrip('/')
                valideerima_tee(RADA, False)
                if (kirje_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 number 없습니다.')
                if kirje_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in RADA:
                    if RADA.endswith('/METADATA'):
                        명세들.append(kogum.read(kirje_VALUE).decode())
                    continue
                if not RADA.endswith('.py') or '.data/' in RADA:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + RADA)
                Lisa_kirje(RADA, kogum.read(kirje_VALUE))
    elif Fail_kirje_nimetus.endswith('.tar.gz') and Nimi_2.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Täida_käsk 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(andmed), mode='r|gz') as kogum:
            뿌리들 = set()
            kirje_COUNT = 0
            kokku_suurust_muutma = 0
            for kirje_VALUE in kogum:
                kirje_COUNT += 1
                kokku_suurust_muutma += kirje_VALUE.size
                if kirje_COUNT > 256 or kokku_suurust_muutma > 1048576:
                    raise ValueError('Arhiiv_VALUE vabastama_salvesti Suurus 제한 초과')
                valideerima_tee(kirje_VALUE.name, False)
                부분들 = kirje_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if kirje_VALUE.isdir():
                    continue
                if not kirje_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython lähe_puu 배포형')
                RADA = '/'.join(부분들[1:])
                Sisu_VALUE = kogum.extractfile(kirje_VALUE).read()
                if RADA.endswith('PKG-INFO'):
                    명세들.append(Sisu_VALUE.decode())
                elif RADA.endswith('.py') and RADA not in ('setup.py',):
                    Lisa_kirje(RADA, Sisu_VALUE)
                elif '.egg-info/' not in RADA and not RADA.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + RADA)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 juur_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* lähe_puu 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 turustus_VALUE 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if sõeluma_päring(명세.get('Name', ''))[0] != Nimi_2 or 명세.get('Version') != versioon_VALUE:
        raise ValueError('turustus_VALUE 메타데이터의 Nimi_2·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADDRESS, 한도):
    if not ADDRESS.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS turustus_VALUE 주소만 허용합니다.')
    with urllib.request.urlopen(ADDRESS, timeout=30) as vastus:
        if not vastus.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 turustus_VALUE ADDRESS liigutama_VALUE')
        andmed = vastus.read(한도 + 1)
    if len(andmed) > 한도:
        raise ValueError('turustus_VALUE Fail Suurus 제한 초과')
    return andmed


def Edasta_kogum(Nimi_2, versioon_VALUE, 파일들, 출처):
    명세 = {'name': Nimi_2, 'version': versioon_VALUE, 'source': 출처, 'files': [
        {'path': RADA, 'size': len(andmed), 'sha256': hashlib.sha256(andmed).hexdigest()}
        for RADA, andmed in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('kogum 명세 Suurus 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[kirje_VALUE['path']] for kirje_VALUE in 명세['files'])


class kogum_hoidla:
    def __init__(자신, RADA, infotehnoloogia_Väljas=False):
        자신.RADA = Path(RADA)
        자신.RADA.mkdir(parents=True, exist_ok=True)
        자신.infotehnoloogia_Väljas = infotehnoloogia_Väljas

    def Ettevalmistamine(자신, päring):
        Nimi_2, versioon_VALUE = sõeluma_päring(päring)
        열쇠 = Nimi_2 + ('==' + versioon_VALUE if versioon_VALUE else '')
        LOG_tee = 자신.RADA / (열쇠 + '.json')
        turustus_tee = 자신.RADA / (열쇠 + '.archive')
        if LOG_tee.is_file() and turustus_tee.is_file():
            LOG_kirje = json.loads(LOG_tee.read_text())
            andmed = turustus_tee.read_bytes()
            if hashlib.sha256(andmed).hexdigest() != LOG_kirje['sha256']:
                raise ValueError('저장된 turustus_VALUE 파일의 SHA-256 불일치')
        else:
            if 자신.infotehnoloogia_Väljas:
                raise ValueError('infotehnoloogia_Väljas 저장소에 없는 kogum: ' + päring)
            ADDRESS = 'https://pypi.org/pypi/' + Nimi_2 + ('/' + versioon_VALUE if versioon_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADDRESS, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [kirje_VALUE for kirje_VALUE in msinfo32_exe['urls'] if not kirje_VALUE.get('yanked') and kirje_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Nimi_2.startswith('micropython-'):
                후보 = [kirje_VALUE for kirje_VALUE in msinfo32_exe['urls'] if not kirje_VALUE.get('yanked') and kirje_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python turustus_VALUE 파일이 없습니다.')
            valim_VALUE = 후보[0]
            andmed = 웹읽기(valim_VALUE['url'], 4194304)
            if hashlib.sha256(andmed).hexdigest() != valim_VALUE['digests']['sha256']:
                raise ValueError('PyPI turustus_VALUE Fail SHA-256 불일치')
            LOG_kirje = {'name': Nimi_2, 'version': msinfo32_exe['info']['version'], 'filename': valim_VALUE['filename'],
                    'url': valim_VALUE['url'], 'sha256': valim_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            lahti_pakkima(LOG_kirje['filename'], andmed, Nimi_2, LOG_kirje['version'])
            turustus_tee.write_bytes(andmed)
            LOG_tee.write_text(json.dumps(LOG_kirje, ensure_ascii=False, indent=2) + '\n')
        if LOG_kirje['name'] != Nimi_2 or versioon_VALUE and LOG_kirje['version'] != versioon_VALUE:
            raise ValueError('hoidla_juur Nimi_2·버전 불일치')
        파일들 = lahti_pakkima(LOG_kirje['filename'], andmed, Nimi_2, LOG_kirje['version'])
        return Edasta_kogum(Nimi_2, LOG_kirje['version'], 파일들, LOG_kirje['url'])


class kogum_päring(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            päring = bytearray()
            while b'\n' not in päring and len(päring) < 100:
                조각 = 자신.request.recv(100 - len(päring))
                if not 조각:
                    return
                päring.extend(조각)
            if not päring.endswith(b'\n') or päring.count(b'\n') != 1:
                raise ValueError('잘못된 kogum päring')
            vastus = 자신.server.hoidla_juur.Ettevalmistamine(päring[:-1].decode('ascii'))
        except Exception as VIGA:
            머리 = json.dumps({'error': str(VIGA)[:500]}, ensure_ascii=False).encode()
            vastus = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(vastus)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, pordinumber=8027, RADA=None, infotehnoloogia_Väljas=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', pordinumber), kogum_päring, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.hoidla_juur = kogum_hoidla(RADA or Project_juur/'build/pip-cache', infotehnoloogia_Väljas)
        자신.pordinumber = 자신.server_VALUE.server_address[1]
        자신.lõim_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.lõim_VALUE.start()
        return 자신

    def __exit__(자신, *Argumendid):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.lõim_VALUE.join(timeout=2)


def Käivita_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=Project_juur/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='Täida_käsk 없이 호환 turustus_VALUE 파일을 내려받아 검사·salv_VALUE')
    Argumendid = parser_48ee4b1b.parse_args()
    if Argumendid.fetch:
        andmed = kogum_hoidla(Argumendid.cache, Argumendid.offline).Ettevalmistamine(Argumendid.fetch)
        print('kogum Ettevalmistamine 완료:', Argumendid.fetch, len(andmed), 'bait_VALUE')
        return
    with 꾸러미중계(Argumendid.port, Argumendid.cache, Argumendid.offline) as 중계:
        print('kogum 중계: 127.0.0.1:' + str(중계.pordinumber), flush=True)
        try:
            중계.lõim_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Käivita_2()
