#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 sakinisha_thamani·실행한다."""
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

기준 = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('fungasha Jina 또는 Jina==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def hakikisha_njia(Jina, usakinishaji_njia=True):
    njia = PurePosixPath(Jina)
    if njia.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Jina.split('/')):
        raise ValueError('허용하지 않는 fungasha njia: ' + Jina)
    if '\\' in Jina or any(ord(kibambo_thamani) < 32 or ord(kibambo_thamani) == 127 for kibambo_thamani in Jina):
        raise ValueError('잘못된 fungasha njia 문자')
    if usakinishaji_njia and (len(('/lib/' + Jina).encode()) > 63 or Jina in ('한국어.py', 'fungasha.py')):
        raise ValueError('fungasha njia 제한 또는 hali_ya_chaguo_msingi maktaba 충돌: ' + Jina)
    return Jina


def 압축풀기(faili_ingizo_jina, data, Jina, toleo_thamani):
    파일들 = {}
    명세들 = []
    def 추가(njia, maudhui_thamani):
        hakikisha_njia(njia)
        if njia in 파일들:
            raise ValueError('중복 fungasha njia: ' + njia)
        if len(maudhui_thamani) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + njia)
        maudhui_thamani.decode('utf-8')
        파일들[njia] = maudhui_thamani
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 chanzo_mti 16개·합계 64 KiB 이하여야 합니다.')
    if faili_ingizo_jina.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as fungasha:
            항목들 = fungasha.infolist()
            if len(항목들) > 256 or sum(ingizo_thamani.file_size for ingizo_thamani in 항목들) > 1048576:
                raise ValueError('Hifadhi_thamani toleo_Hifadhi panga_ukubwa 제한 초과')
            Kazi_Orodha = [ingizo_thamani for ingizo_thamani in 항목들 if ingizo_thamani.filename.endswith('.dist-info/WHEEL')]
            if len(Kazi_Orodha) != 1:
                raise ValueError('wheel Kazi_thamani 명세가 필요합니다.')
            Kazi_thamani = email.parser.Parser().parsestr(fungasha.read(Kazi_Orodha[0]).decode())
            if Kazi_thamani.get('Root-Is-Purelib', '').lower() != 'true' or not faili_ingizo_jina.endswith('-none-any.whl'):
                raise ValueError('C kiendelezi_thamani·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ingizo_thamani in 항목들:
                njia = ingizo_thamani.filename.rstrip('/')
                hakikisha_njia(njia, False)
                if (ingizo_thamani.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ingizo_thamani.filename.endswith('/'):
                    continue
                if '.dist-info/' in njia:
                    if njia.endswith('/METADATA'):
                        명세들.append(fungasha.read(ingizo_thamani).decode())
                    continue
                if not njia.endswith('.py') or '.data/' in njia:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + njia)
                추가(njia, fungasha.read(ingizo_thamani))
    elif faili_ingizo_jina.endswith('.tar.gz') and Jina.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py tekeleza_amri 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as fungasha:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ingizo_thamani in fungasha:
                항목수 += 1
                전체크기 += ingizo_thamani.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Hifadhi_thamani toleo_Hifadhi panga_ukubwa 제한 초과')
                hakikisha_njia(ingizo_thamani.name, False)
                부분들 = ingizo_thamani.name.split('/')
                뿌리들.add(부분들[0])
                if ingizo_thamani.isdir():
                    continue
                if not ingizo_thamani.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython chanzo_mti 배포형')
                njia = '/'.join(부분들[1:])
                maudhui_thamani = fungasha.extractfile(ingizo_thamani).read()
                if njia.endswith('PKG-INFO'):
                    명세들.append(maudhui_thamani.decode())
                elif njia.endswith('.py') and njia not in ('setup.py',):
                    추가(njia, maudhui_thamani)
                elif '.egg-info/' not in njia and not njia.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + njia)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* chanzo_mti 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Jina or 명세.get('Version') != toleo_thamani:
        raise ValueError('배포 메타데이터의 Jina·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(anwani, 한도):
    if not anwani.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(anwani, timeout=30) as jibu:
        if not jibu.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 anwani hamisha_thamani')
        data = jibu.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 faili panga_ukubwa 제한 초과')
    return data


def hamisha_fungasha(Jina, toleo_thamani, 파일들, 출처):
    명세 = {'name': Jina, 'version': toleo_thamani, 'source': 출처, 'files': [
        {'path': njia, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for njia, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('fungasha 명세 panga_ukubwa 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ingizo_thamani['path']] for ingizo_thamani in 명세['files'])


class fungasha_uwekaji:
    def __init__(자신, njia, teknolojia_ya_maelezo_Nje_ya_mtandao=False):
        자신.njia = Path(njia)
        자신.njia.mkdir(parents=True, exist_ok=True)
        자신.teknolojia_ya_maelezo_Nje_ya_mtandao = teknolojia_ya_maelezo_Nje_ya_mtandao

    def Andaa(자신, 요청):
        Jina, toleo_thamani = 요청해석(요청)
        열쇠 = Jina + ('==' + toleo_thamani if toleo_thamani else '')
        batli_njia = 자신.njia / (열쇠 + '.json')
        배포경로 = 자신.njia / (열쇠 + '.archive')
        if batli_njia.is_file() and 배포경로.is_file():
            batli_REKODI = json.loads(batli_njia.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != batli_REKODI['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.teknolojia_ya_maelezo_Nje_ya_mtandao:
                raise ValueError('teknolojia_ya_maelezo_Nje_ya_mtandao 저장소에 없는 fungasha: ' + 요청)
            anwani = 'https://pypi.org/pypi/' + Jina + ('/' + toleo_thamani if toleo_thamani else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(anwani, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ingizo_thamani for ingizo_thamani in msinfo32_exe['urls'] if not ingizo_thamani.get('yanked') and ingizo_thamani['filename'].endswith('-none-any.whl')]
            if not 후보 and Jina.startswith('micropython-'):
                후보 = [ingizo_thamani for ingizo_thamani in msinfo32_exe['urls'] if not ingizo_thamani.get('yanked') and ingizo_thamani['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            uteuzi_thamani = 후보[0]
            data = 웹읽기(uteuzi_thamani['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != uteuzi_thamani['digests']['sha256']:
                raise ValueError('PyPI 배포 faili SHA-256 불일치')
            batli_REKODI = {'name': Jina, 'version': msinfo32_exe['info']['version'], 'filename': uteuzi_thamani['filename'],
                    'url': uteuzi_thamani['url'], 'sha256': uteuzi_thamani['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(batli_REKODI['filename'], data, Jina, batli_REKODI['version'])
            배포경로.write_bytes(data)
            batli_njia.write_text(json.dumps(batli_REKODI, ensure_ascii=False, indent=2) + '\n')
        if batli_REKODI['name'] != Jina or toleo_thamani and batli_REKODI['version'] != toleo_thamani:
            raise ValueError('저장소 Jina·버전 불일치')
        파일들 = 압축풀기(batli_REKODI['filename'], data, Jina, batli_REKODI['version'])
        return hamisha_fungasha(Jina, batli_REKODI['version'], 파일들, batli_REKODI['url'])


class 꾸러미요청(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            요청 = bytearray()
            while b'\n' not in 요청 and len(요청) < 100:
                조각 = 자신.request.recv(100 - len(요청))
                if not 조각:
                    return
                요청.extend(조각)
            if not 요청.endswith(b'\n') or 요청.count(b'\n') != 1:
                raise ValueError('잘못된 fungasha 요청')
            jibu = 자신.server.저장소.Andaa(요청[:-1].decode('ascii'))
        except Exception as kosa:
            머리 = json.dumps({'error': str(kosa)[:500]}, ensure_ascii=False).encode()
            jibu = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(jibu)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, namba_ya_kituo=8027, njia=None, teknolojia_ya_maelezo_Nje_ya_mtandao=False):
        자신.seva_thamani = socketserver.TCPServer(('127.0.0.1', namba_ya_kituo), 꾸러미요청, bind_and_activate=False)
        자신.seva_thamani.allow_reuse_address = True
        자신.seva_thamani.server_bind()
        자신.seva_thamani.server_activate()
        자신.seva_thamani.저장소 = fungasha_uwekaji(njia or 기준/'build/pip-cache', teknolojia_ya_maelezo_Nje_ya_mtandao)
        자신.namba_ya_kituo = 자신.seva_thamani.server_address[1]
        자신.mtungo_thamani = threading.Thread(target=자신.seva_thamani.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.mtungo_thamani.start()
        return 자신

    def __exit__(자신, *인수):
        자신.seva_thamani.shutdown()
        자신.seva_thamani.server_close()
        자신.mtungo_thamani.join(timeout=2)


def endesha():
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    kichanganuzi_48ee4b1b.add_argument('--port', type=int, default=8027)
    kichanganuzi_48ee4b1b.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    kichanganuzi_48ee4b1b.add_argument('--offline', action='store_true')
    kichanganuzi_48ee4b1b.add_argument('--fetch', help='tekeleza_amri 없이 호환 배포 파일을 내려받아 검사·Store_thamani')
    인수 = kichanganuzi_48ee4b1b.parse_args()
    if 인수.fetch:
        data = fungasha_uwekaji(인수.cache, 인수.offline).Andaa(인수.fetch)
        print('fungasha Andaa 완료:', 인수.fetch, len(data), 'baiti_thamani')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('fungasha 중계: 127.0.0.1:' + str(중계.namba_ya_kituo), flush=True)
        try:
            중계.mtungo_thamani.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    endesha()
