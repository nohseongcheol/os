#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installer_VERDI·실행한다."""
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

speile_rot = Path(__file__).resolve().parents[1]


def dele_opp_forespørsel(forespørsel):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', forespørsel)
    if not 맞음:
        raise ValueError('bunt Navn 또는 Navn==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def bekrefte_bane(Navn, installasjon_bane=True):
    Sti = PurePosixPath(Navn)
    if Sti.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Navn.split('/')):
        raise ValueError('허용하지 않는 bunt Sti: ' + Navn)
    if '\\' in Navn or any(ord(tegn_VERDI) < 32 or ord(tegn_VERDI) == 127 for tegn_VERDI in Navn):
        raise ValueError('잘못된 bunt Sti 문자')
    if installasjon_bane and (len(('/lib/' + Navn).encode()) > 63 or Navn in ('norsk.py', 'bunt.py')):
        raise ValueError('bunt Sti 제한 또는 standardverdi bibliotek 충돌: ' + Navn)
    return Navn


def 압축풀기(Fil_oppføring_navn, data, Navn, versjon_VERDI):
    파일들 = {}
    명세들 = []
    def Tilføye_oppføring(Sti, Innhold_VERDI):
        bekrefte_bane(Sti)
        if Sti in 파일들:
            raise ValueError('중복 bunt Sti: ' + Sti)
        if len(Innhold_VERDI) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Sti)
        Innhold_VERDI.decode('utf-8')
        파일들[Sti] = Innhold_VERDI
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 kilde_tre 16개·total_VERDI 64 KiB 이하여야 합니다.')
    if Fil_oppføring_navn.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as bunt:
            항목들 = bunt.infolist()
            if len(항목들) > 256 or sum(oppføring_VERDI.file_size for oppføring_VERDI in 항목들) > 1048576:
                raise ValueError('Arkiv_VERDI frigi_lager Størrelse 제한 초과')
            sak_Liste = [oppføring_VERDI for oppføring_VERDI in 항목들 if oppføring_VERDI.filename.endswith('.dist-info/WHEEL')]
            if len(sak_Liste) != 1:
                raise ValueError('wheel kontraktverdi 명세가 필요합니다.')
            kontraktverdi = email.parser.Parser().parsestr(bunt.read(sak_Liste[0]).decode())
            if kontraktverdi.get('Root-Is-Purelib', '').lower() != 'true' or not Fil_oppføring_navn.endswith('-none-any.whl'):
                raise ValueError('C filtype_VERDI·플랫폼 전용 wheel은 지원하지 않습니다.')
            for oppføring_VERDI in 항목들:
                Sti = oppføring_VERDI.filename.rstrip('/')
                bekrefte_bane(Sti, False)
                if (oppføring_VERDI.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 nummer 없습니다.')
                if oppføring_VERDI.filename.endswith('/'):
                    continue
                if '.dist-info/' in Sti:
                    if Sti.endswith('/METADATA'):
                        명세들.append(bunt.read(oppføring_VERDI).decode())
                    continue
                if not Sti.endswith('.py') or '.data/' in Sti:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Sti)
                Tilføye_oppføring(Sti, bunt.read(oppføring_VERDI))
    elif Fil_oppføring_navn.endswith('.tar.gz') and Navn.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Utfør_kommando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as bunt:
            뿌리들 = set()
            oppføring_ANTALL = 0
            total_skalere = 0
            for oppføring_VERDI in bunt:
                oppføring_ANTALL += 1
                total_skalere += oppføring_VERDI.size
                if oppføring_ANTALL > 256 or total_skalere > 1048576:
                    raise ValueError('Arkiv_VERDI frigi_lager Størrelse 제한 초과')
                bekrefte_bane(oppføring_VERDI.name, False)
                부분들 = oppføring_VERDI.name.split('/')
                뿌리들.add(부분들[0])
                if oppføring_VERDI.isdir():
                    continue
                if not oppføring_VERDI.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython kilde_tre 배포형')
                Sti = '/'.join(부분들[1:])
                Innhold_VERDI = bunt.extractfile(oppføring_VERDI).read()
                if Sti.endswith('PKG-INFO'):
                    명세들.append(Innhold_VERDI.decode())
                elif Sti.endswith('.py') and Sti not in ('setup.py',):
                    Tilføye_oppføring(Sti, Innhold_VERDI)
                elif '.egg-info/' not in Sti and not Sti.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Sti)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 rot_VERDI 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* kilde_tre 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 distribusjon_VERDI 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if dele_opp_forespørsel(명세.get('Name', ''))[0] != Navn or 명세.get('Version') != versjon_VERDI:
        raise ValueError('distribusjon_VERDI 메타데이터의 Navn·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(e_post, 한도):
    if not e_post.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS distribusjon_VERDI 주소만 허용합니다.')
    with urllib.request.urlopen(e_post, timeout=30) as svar:
        if not svar.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 distribusjon_VERDI e_post flytte_VERDI_83b651b8')
        data = svar.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('distribusjon_VERDI Fil Størrelse 제한 초과')
    return data


def overføre_bunt(Navn, versjon_VERDI, 파일들, origo_VERDI):
    명세 = {'name': Navn, 'version': versjon_VERDI, 'source': origo_VERDI, 'files': [
        {'path': Sti, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for Sti, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('bunt 명세 Størrelse 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[oppføring_VERDI['path']] for oppføring_VERDI in 명세['files'])


class bunt_repositorium:
    def __init__(자신, Sti, informasjonssystemer_Frakoblet=False):
        자신.Sti = Path(Sti)
        자신.Sti.mkdir(parents=True, exist_ok=True)
        자신.informasjonssystemer_Frakoblet = informasjonssystemer_Frakoblet

    def Forbered(자신, forespørsel):
        Navn, versjon_VERDI = dele_opp_forespørsel(forespørsel)
        열쇠 = Navn + ('==' + versjon_VERDI if versjon_VERDI else '')
        LOG_bane = 자신.Sti / (열쇠 + '.json')
        distribusjon_bane = 자신.Sti / (열쇠 + '.archive')
        if LOG_bane.is_file() and distribusjon_bane.is_file():
            LOG_POST = json.loads(LOG_bane.read_text())
            data = distribusjon_bane.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_POST['sha256']:
                raise ValueError('저장된 distribusjon_VERDI 파일의 SHA-256 불일치')
        else:
            if 자신.informasjonssystemer_Frakoblet:
                raise ValueError('informasjonssystemer_Frakoblet 저장소에 없는 bunt: ' + forespørsel)
            e_post = 'https://pypi.org/pypi/' + Navn + ('/' + versjon_VERDI if versjon_VERDI else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(e_post, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [oppføring_VERDI for oppføring_VERDI in msinfo32_exe['urls'] if not oppføring_VERDI.get('yanked') and oppføring_VERDI['filename'].endswith('-none-any.whl')]
            if not 후보 and Navn.startswith('micropython-'):
                후보 = [oppføring_VERDI for oppføring_VERDI in msinfo32_exe['urls'] if not oppføring_VERDI.get('yanked') and oppføring_VERDI['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python distribusjon_VERDI 파일이 없습니다.')
            merket_område_VERDI = 후보[0]
            data = 웹읽기(merket_område_VERDI['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != merket_område_VERDI['digests']['sha256']:
                raise ValueError('PyPI distribusjon_VERDI Fil SHA-256 불일치')
            LOG_POST = {'name': Navn, 'version': msinfo32_exe['info']['version'], 'filename': merket_område_VERDI['filename'],
                    'url': merket_område_VERDI['url'], 'sha256': merket_område_VERDI['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_POST['filename'], data, Navn, LOG_POST['version'])
            distribusjon_bane.write_bytes(data)
            LOG_bane.write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2) + '\n')
        if LOG_POST['name'] != Navn or versjon_VERDI and LOG_POST['version'] != versjon_VERDI:
            raise ValueError('repositorium_rot Navn·버전 불일치')
        파일들 = 압축풀기(LOG_POST['filename'], data, Navn, LOG_POST['version'])
        return overføre_bunt(Navn, LOG_POST['version'], 파일들, LOG_POST['url'])


class bunt_forespørsel(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            forespørsel = bytearray()
            while b'\n' not in forespørsel and len(forespørsel) < 100:
                조각 = 자신.request.recv(100 - len(forespørsel))
                if not 조각:
                    return
                forespørsel.extend(조각)
            if not forespørsel.endswith(b'\n') or forespørsel.count(b'\n') != 1:
                raise ValueError('잘못된 bunt forespørsel')
            svar = 자신.server.repositorium_rot.Forbered(forespørsel[:-1].decode('ascii'))
        except Exception as feil:
            머리 = json.dumps({'error': str(feil)[:500]}, ensure_ascii=False).encode()
            svar = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(svar)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, portnummer=8027, Sti=None, informasjonssystemer_Frakoblet=False):
        자신.server_VERDI = socketserver.TCPServer(('127.0.0.1', portnummer), bunt_forespørsel, bind_and_activate=False)
        자신.server_VERDI.allow_reuse_address = True
        자신.server_VERDI.server_bind()
        자신.server_VERDI.server_activate()
        자신.server_VERDI.repositorium_rot = bunt_repositorium(Sti or speile_rot/'build/pip-cache', informasjonssystemer_Frakoblet)
        자신.portnummer = 자신.server_VERDI.server_address[1]
        자신.tråd_VERDI = threading.Thread(target=자신.server_VERDI.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.tråd_VERDI.start()
        return 자신

    def __exit__(자신, *Argumenter):
        자신.server_VERDI.shutdown()
        자신.server_VERDI.server_close()
        자신.tråd_VERDI.join(timeout=2)


def Kjør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=speile_rot/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='Utfør_kommando 없이 호환 distribusjon_VERDI 파일을 내려받아 검사·Store_VERDI')
    Argumenter = parser_48ee4b1b.parse_args()
    if Argumenter.fetch:
        data = bunt_repositorium(Argumenter.cache, Argumenter.offline).Forbered(Argumenter.fetch)
        print('bunt Forbered 완료:', Argumenter.fetch, len(data), 'byte_VERDI')
        return
    with 꾸러미중계(Argumenter.port, Argumenter.cache, Argumenter.offline) as 중계:
        print('bunt 중계: 127.0.0.1:' + str(중계.portnummer), flush=True)
        try:
            중계.tråd_VERDI.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Kjør_2()
