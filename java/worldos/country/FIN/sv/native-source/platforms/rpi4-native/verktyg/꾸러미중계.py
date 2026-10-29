#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installera_värde·실행한다."""
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

åtgärd_rot = Path(__file__).resolve().parents[1]


def parsa_begäran(begäran):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', begäran)
    if not 맞음:
        raise ValueError('bunt Namn 또는 Namn==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def validera_väg(Namn, installation_väg=True):
    sökväg_2 = PurePosixPath(Namn)
    if sökväg_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Namn.split('/')):
        raise ValueError('허용하지 않는 bunt sökväg_2: ' + Namn)
    if '\\' in Namn or any(ord(tecken_värde) < 32 or ord(tecken_värde) == 127 for tecken_värde in Namn):
        raise ValueError('잘못된 bunt sökväg_2 문자')
    if installation_väg and (len(('/lib/' + Namn).encode()) > 63 or Namn in ('Svenska.py', 'bunt.py')):
        raise ValueError('bunt sökväg_2 제한 또는 standardvärde bibliotek 충돌: ' + Namn)
    return Namn


def dekomprimera(fil_post_namn, data, Namn, version_värde):
    파일들 = {}
    명세들 = []
    def Lägga_till_post(sökväg_2, Innehåll_värde):
        validera_väg(sökväg_2)
        if sökväg_2 in 파일들:
            raise ValueError('중복 bunt sökväg_2: ' + sökväg_2)
        if len(Innehåll_värde) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + sökväg_2)
        Innehåll_värde.decode('utf-8')
        파일들[sökväg_2] = Innehåll_värde
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 källa_träd 16개·summa_värde 64 KiB 이하여야 합니다.')
    if fil_post_namn.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as bunt:
            항목들 = bunt.infolist()
            if len(항목들) > 256 or sum(post_värde.file_size for post_värde in 항목들) > 1048576:
                raise ValueError('Arkiv_värde släppa_minne Storlek 제한 초과')
            jobb_ange = [post_värde for post_värde in 항목들 if post_värde.filename.endswith('.dist-info/WHEEL')]
            if len(jobb_ange) != 1:
                raise ValueError('wheel kontraktsvärde 명세가 필요합니다.')
            kontraktsvärde = email.parser.Parser().parsestr(bunt.read(jobb_ange[0]).decode())
            if kontraktsvärde.get('Root-Is-Purelib', '').lower() != 'true' or not fil_post_namn.endswith('-none-any.whl'):
                raise ValueError('C tillägg_värde·플랫폼 전용 wheel은 지원하지 않습니다.')
            for post_värde in 항목들:
                sökväg_2 = post_värde.filename.rstrip('/')
                validera_väg(sökväg_2, False)
                if (post_värde.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 nummer 없습니다.')
                if post_värde.filename.endswith('/'):
                    continue
                if '.dist-info/' in sökväg_2:
                    if sökväg_2.endswith('/METADATA'):
                        명세들.append(bunt.read(post_värde).decode())
                    continue
                if not sökväg_2.endswith('.py') or '.data/' in sökväg_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + sökväg_2)
                Lägga_till_post(sökväg_2, bunt.read(post_värde))
    elif fil_post_namn.endswith('.tar.gz') and Namn.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py köra_kommando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as bunt:
            뿌리들 = set()
            post_ANTAL = 0
            summa_storlek = 0
            for post_värde in bunt:
                post_ANTAL += 1
                summa_storlek += post_värde.size
                if post_ANTAL > 256 or summa_storlek > 1048576:
                    raise ValueError('Arkiv_värde släppa_minne Storlek 제한 초과')
                validera_väg(post_värde.name, False)
                부분들 = post_värde.name.split('/')
                뿌리들.add(부분들[0])
                if post_värde.isdir():
                    continue
                if not post_värde.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython källa_träd 배포형')
                sökväg_2 = '/'.join(부분들[1:])
                Innehåll_värde = bunt.extractfile(post_värde).read()
                if sökväg_2.endswith('PKG-INFO'):
                    명세들.append(Innehåll_värde.decode())
                elif sökväg_2.endswith('.py') and sökväg_2 not in ('setup.py',):
                    Lägga_till_post(sökväg_2, Innehåll_värde)
                elif '.egg-info/' not in sökväg_2 and not sökväg_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + sökväg_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 rot_värde 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* källa_träd 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 fördelning_värde 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if parsa_begäran(명세.get('Name', ''))[0] != Namn or 명세.get('Version') != version_värde:
        raise ValueError('fördelning_värde 메타데이터의 Namn·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def läsa_W3(Adress, 한도):
    if not Adress.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS fördelning_värde 주소만 허용합니다.')
    with urllib.request.urlopen(Adress, timeout=30) as svara:
        if not svara.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 fördelning_värde Adress flytta_värde')
        data = svara.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('fördelning_värde filnamn Storlek 제한 초과')
    return data


def Överför_bunt(Namn, version_värde, 파일들, origo_värde):
    명세 = {'name': Namn, 'version': version_värde, 'source': origo_värde, 'files': [
        {'path': sökväg_2, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for sökväg_2, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('bunt 명세 Storlek 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[post_värde['path']] for post_värde in 명세['files'])


class bunt_centrallager:
    def __init__(자신, sökväg_2, informationsteknik_Offline=False):
        자신.sökväg_2 = Path(sökväg_2)
        자신.sökväg_2.mkdir(parents=True, exist_ok=True)
        자신.informationsteknik_Offline = informationsteknik_Offline

    def Förbereda(자신, begäran):
        Namn, version_värde = parsa_begäran(begäran)
        열쇠 = Namn + ('==' + version_värde if version_värde else '')
        LOG_väg = 자신.sökväg_2 / (열쇠 + '.json')
        fördelning_väg = 자신.sökväg_2 / (열쇠 + '.archive')
        if LOG_väg.is_file() and fördelning_väg.is_file():
            LOG_POST = json.loads(LOG_väg.read_text())
            data = fördelning_väg.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_POST['sha256']:
                raise ValueError('저장된 fördelning_värde 파일의 SHA-256 불일치')
        else:
            if 자신.informationsteknik_Offline:
                raise ValueError('informationsteknik_Offline 저장소에 없는 bunt: ' + begäran)
            Adress = 'https://pypi.org/pypi/' + Namn + ('/' + version_värde if version_värde else '') + '/json'
            msinfo32_exe = json.loads(läsa_W3(Adress, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            kandidat = [post_värde for post_värde in msinfo32_exe['urls'] if not post_värde.get('yanked') and post_värde['filename'].endswith('-none-any.whl')]
            if not kandidat and Namn.startswith('micropython-'):
                kandidat = [post_värde for post_värde in msinfo32_exe['urls'] if not post_värde.get('yanked') and post_värde['filename'].endswith('.tar.gz')]
            if not kandidat:
                raise ValueError('지원되는 순수 Python fördelning_värde 파일이 없습니다.')
            markering_värde = kandidat[0]
            data = läsa_W3(markering_värde['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != markering_värde['digests']['sha256']:
                raise ValueError('PyPI fördelning_värde filnamn SHA-256 불일치')
            LOG_POST = {'name': Namn, 'version': msinfo32_exe['info']['version'], 'filename': markering_värde['filename'],
                    'url': markering_värde['url'], 'sha256': markering_värde['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            dekomprimera(LOG_POST['filename'], data, Namn, LOG_POST['version'])
            fördelning_väg.write_bytes(data)
            LOG_väg.write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2) + '\n')
        if LOG_POST['name'] != Namn or version_värde and LOG_POST['version'] != version_värde:
            raise ValueError('centrallager_rot Namn·버전 불일치')
        파일들 = dekomprimera(LOG_POST['filename'], data, Namn, LOG_POST['version'])
        return Överför_bunt(Namn, LOG_POST['version'], 파일들, LOG_POST['url'])


class bunt_begäran(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            begäran = bytearray()
            while b'\n' not in begäran and len(begäran) < 100:
                조각 = 자신.request.recv(100 - len(begäran))
                if not 조각:
                    return
                begäran.extend(조각)
            if not begäran.endswith(b'\n') or begäran.count(b'\n') != 1:
                raise ValueError('잘못된 bunt begäran')
            svara = 자신.server.centrallager_rot.Förbereda(begäran[:-1].decode('ascii'))
        except Exception as fel:
            머리 = json.dumps({'error': str(fel)[:500]}, ensure_ascii=False).encode()
            svara = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(svara)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, portnummer=8027, sökväg_2=None, informationsteknik_Offline=False):
        자신.server_värde = socketserver.TCPServer(('127.0.0.1', portnummer), bunt_begäran, bind_and_activate=False)
        자신.server_värde.allow_reuse_address = True
        자신.server_värde.server_bind()
        자신.server_värde.server_activate()
        자신.server_värde.centrallager_rot = bunt_centrallager(sökväg_2 or åtgärd_rot/'build/pip-cache', informationsteknik_Offline)
        자신.portnummer = 자신.server_värde.server_address[1]
        자신.tråd_värde = threading.Thread(target=자신.server_värde.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.tråd_värde.start()
        return 자신

    def __exit__(자신, *argument):
        자신.server_värde.shutdown()
        자신.server_värde.server_close()
        자신.tråd_värde.join(timeout=2)


def Kör():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=åtgärd_rot/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='köra_kommando 없이 호환 fördelning_värde 파일을 내려받아 검사·Store_värde')
    argument = parser_48ee4b1b.parse_args()
    if argument.fetch:
        data = bunt_centrallager(argument.cache, argument.offline).Förbereda(argument.fetch)
        print('bunt Förbereda 완료:', argument.fetch, len(data), 'byte_värde')
        return
    with 꾸러미중계(argument.port, argument.cache, argument.offline) as 중계:
        print('bunt 중계: 127.0.0.1:' + str(중계.portnummer), flush=True)
        try:
            중계.tråd_värde.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Kör()
