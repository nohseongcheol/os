#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 installér_VÆRDI·실행한다."""
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

To_do_rod = Path(__file__).resolve().parents[1]


def opdele_tekst_anmodning(anmodning):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', anmodning)
    if not 맞음:
        raise ValueError('bundt Navn 또는 Navn==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def bekræfte_sti(Navn, installation_sti=True):
    Sti = PurePosixPath(Navn)
    if Sti.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Navn.split('/')):
        raise ValueError('허용하지 않는 bundt Sti: ' + Navn)
    if '\\' in Navn or any(ord(tegn_VÆRDI) < 32 or ord(tegn_VÆRDI) == 127 for tegn_VÆRDI in Navn):
        raise ValueError('잘못된 bundt Sti 문자')
    if installation_sti and (len(('/lib/' + Navn).encode()) > 63 or Navn in ('Dansk.py', 'bundt.py')):
        raise ValueError('bundt Sti 제한 또는 standardværdi bibliotek 충돌: ' + Navn)
    return Navn


def dekomprimere(fil_post_navn, data, Navn, version_VÆRDI):
    파일들 = {}
    명세들 = []
    def tilføj_post(Sti, Indhold_VÆRDI):
        bekræfte_sti(Sti)
        if Sti in 파일들:
            raise ValueError('중복 bundt Sti: ' + Sti)
        if len(Indhold_VÆRDI) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Sti)
        Indhold_VÆRDI.decode('utf-8')
        파일들[Sti] = Indhold_VÆRDI
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 kilde_træ 16개·i_alt_VÆRDI 64 KiB 이하여야 합니다.')
    if fil_post_navn.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as bundt:
            항목들 = bundt.infolist()
            if len(항목들) > 256 or sum(post_VÆRDI_962f286b.file_size for post_VÆRDI_962f286b in 항목들) > 1048576:
                raise ValueError('Arkiv_VÆRDI udgive_Lager Størrelse 제한 초과')
            job_Liste = [post_VÆRDI_962f286b for post_VÆRDI_962f286b in 항목들 if post_VÆRDI_962f286b.filename.endswith('.dist-info/WHEEL')]
            if len(job_Liste) != 1:
                raise ValueError('wheel kontraktværdi 명세가 필요합니다.')
            kontraktværdi = email.parser.Parser().parsestr(bundt.read(job_Liste[0]).decode())
            if kontraktværdi.get('Root-Is-Purelib', '').lower() != 'true' or not fil_post_navn.endswith('-none-any.whl'):
                raise ValueError('C udvidelse_VÆRDI·플랫폼 전용 wheel은 지원하지 않습니다.')
            for post_VÆRDI_962f286b in 항목들:
                Sti = post_VÆRDI_962f286b.filename.rstrip('/')
                bekræfte_sti(Sti, False)
                if (post_VÆRDI_962f286b.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 tal 없습니다.')
                if post_VÆRDI_962f286b.filename.endswith('/'):
                    continue
                if '.dist-info/' in Sti:
                    if Sti.endswith('/METADATA'):
                        명세들.append(bundt.read(post_VÆRDI_962f286b).decode())
                    continue
                if not Sti.endswith('.py') or '.data/' in Sti:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Sti)
                tilføj_post(Sti, bundt.read(post_VÆRDI_962f286b))
    elif fil_post_navn.endswith('.tar.gz') and Navn.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Udfør_kommando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as bundt:
            뿌리들 = set()
            post_TÆL_8f7753a1 = 0
            i_alt_tilpasse_størrelse = 0
            for post_VÆRDI_962f286b in bundt:
                post_TÆL_8f7753a1 += 1
                i_alt_tilpasse_størrelse += post_VÆRDI_962f286b.size
                if post_TÆL_8f7753a1 > 256 or i_alt_tilpasse_størrelse > 1048576:
                    raise ValueError('Arkiv_VÆRDI udgive_Lager Størrelse 제한 초과')
                bekræfte_sti(post_VÆRDI_962f286b.name, False)
                부분들 = post_VÆRDI_962f286b.name.split('/')
                뿌리들.add(부분들[0])
                if post_VÆRDI_962f286b.isdir():
                    continue
                if not post_VÆRDI_962f286b.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython kilde_træ 배포형')
                Sti = '/'.join(부분들[1:])
                Indhold_VÆRDI = bundt.extractfile(post_VÆRDI_962f286b).read()
                if Sti.endswith('PKG-INFO'):
                    명세들.append(Indhold_VÆRDI.decode())
                elif Sti.endswith('.py') and Sti not in ('setup.py',):
                    tilføj_post(Sti, Indhold_VÆRDI)
                elif '.egg-info/' not in Sti and not Sti.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Sti)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 rod_VÆRDI 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* kilde_træ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 distribution_VÆRDI 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if opdele_tekst_anmodning(명세.get('Name', ''))[0] != Navn or 명세.get('Version') != version_VÆRDI:
        raise ValueError('distribution_VÆRDI 메타데이터의 Navn·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(mail, 한도):
    if not mail.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS distribution_VÆRDI 주소만 허용합니다.')
    with urllib.request.urlopen(mail, timeout=30) as svar:
        if not svar.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 distribution_VÆRDI mail flytte_VÆRDI_83b651b8')
        data = svar.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('distribution_VÆRDI Fil Størrelse 제한 초과')
    return data


def overføre_bundt(Navn, version_VÆRDI, 파일들, begyndelsespunkt_VÆRDI):
    명세 = {'name': Navn, 'version': version_VÆRDI, 'source': begyndelsespunkt_VÆRDI, 'files': [
        {'path': Sti, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for Sti, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('bundt 명세 Størrelse 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[post_VÆRDI_962f286b['path']] for post_VÆRDI_962f286b in 명세['files'])


class bundt_lager:
    def __init__(자신, Sti, it_Offline=False):
        자신.Sti = Path(Sti)
        자신.Sti.mkdir(parents=True, exist_ok=True)
        자신.it_Offline = it_Offline

    def Tilrettelæg(자신, anmodning):
        Navn, version_VÆRDI = opdele_tekst_anmodning(anmodning)
        열쇠 = Navn + ('==' + version_VÆRDI if version_VÆRDI else '')
        LOG_sti = 자신.Sti / (열쇠 + '.json')
        distribution_sti = 자신.Sti / (열쇠 + '.archive')
        if LOG_sti.is_file() and distribution_sti.is_file():
            LOG_post = json.loads(LOG_sti.read_text())
            data = distribution_sti.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_post['sha256']:
                raise ValueError('저장된 distribution_VÆRDI 파일의 SHA-256 불일치')
        else:
            if 자신.it_Offline:
                raise ValueError('it_Offline 저장소에 없는 bundt: ' + anmodning)
            mail = 'https://pypi.org/pypi/' + Navn + ('/' + version_VÆRDI if version_VÆRDI else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(mail, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [post_VÆRDI_962f286b for post_VÆRDI_962f286b in msinfo32_exe['urls'] if not post_VÆRDI_962f286b.get('yanked') and post_VÆRDI_962f286b['filename'].endswith('-none-any.whl')]
            if not 후보 and Navn.startswith('micropython-'):
                후보 = [post_VÆRDI_962f286b for post_VÆRDI_962f286b in msinfo32_exe['urls'] if not post_VÆRDI_962f286b.get('yanked') and post_VÆRDI_962f286b['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python distribution_VÆRDI 파일이 없습니다.')
            markering_VÆRDI = 후보[0]
            data = 웹읽기(markering_VÆRDI['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != markering_VÆRDI['digests']['sha256']:
                raise ValueError('PyPI distribution_VÆRDI Fil SHA-256 불일치')
            LOG_post = {'name': Navn, 'version': msinfo32_exe['info']['version'], 'filename': markering_VÆRDI['filename'],
                    'url': markering_VÆRDI['url'], 'sha256': markering_VÆRDI['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            dekomprimere(LOG_post['filename'], data, Navn, LOG_post['version'])
            distribution_sti.write_bytes(data)
            LOG_sti.write_text(json.dumps(LOG_post, ensure_ascii=False, indent=2) + '\n')
        if LOG_post['name'] != Navn or version_VÆRDI and LOG_post['version'] != version_VÆRDI:
            raise ValueError('lager_rod Navn·버전 불일치')
        파일들 = dekomprimere(LOG_post['filename'], data, Navn, LOG_post['version'])
        return overføre_bundt(Navn, LOG_post['version'], 파일들, LOG_post['url'])


class bundt_anmodning(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            anmodning = bytearray()
            while b'\n' not in anmodning and len(anmodning) < 100:
                조각 = 자신.request.recv(100 - len(anmodning))
                if not 조각:
                    return
                anmodning.extend(조각)
            if not anmodning.endswith(b'\n') or anmodning.count(b'\n') != 1:
                raise ValueError('잘못된 bundt anmodning')
            svar = 자신.server.lager_rod.Tilrettelæg(anmodning[:-1].decode('ascii'))
        except Exception as fejl:
            머리 = json.dumps({'error': str(fejl)[:500]}, ensure_ascii=False).encode()
            svar = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(svar)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, portnummer=8027, Sti=None, it_Offline=False):
        자신.server_VÆRDI = socketserver.TCPServer(('127.0.0.1', portnummer), bundt_anmodning, bind_and_activate=False)
        자신.server_VÆRDI.allow_reuse_address = True
        자신.server_VÆRDI.server_bind()
        자신.server_VÆRDI.server_activate()
        자신.server_VÆRDI.lager_rod = bundt_lager(Sti or To_do_rod/'build/pip-cache', it_Offline)
        자신.portnummer = 자신.server_VÆRDI.server_address[1]
        자신.tråd_VÆRDI = threading.Thread(target=자신.server_VÆRDI.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.tråd_VÆRDI.start()
        return 자신

    def __exit__(자신, *Argumenter):
        자신.server_VÆRDI.shutdown()
        자신.server_VÆRDI.server_close()
        자신.tråd_VÆRDI.join(timeout=2)


def Kør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=To_do_rod/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='Udfør_kommando 없이 호환 distribution_VÆRDI 파일을 내려받아 검사·Store_VÆRDI')
    Argumenter = parser_48ee4b1b.parse_args()
    if Argumenter.fetch:
        data = bundt_lager(Argumenter.cache, Argumenter.offline).Tilrettelæg(Argumenter.fetch)
        print('bundt Tilrettelæg 완료:', Argumenter.fetch, len(data), 'byte_VÆRDI')
        return
    with 꾸러미중계(Argumenter.port, Argumenter.cache, Argumenter.offline) as 중계:
        print('bundt 중계: 127.0.0.1:' + str(중계.portnummer), flush=True)
        try:
            중계.tråd_VÆRDI.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Kør_2()
