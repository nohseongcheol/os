#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 hloma_boleng·실행한다."""
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
        raise ValueError('sehlopha Leina 또는 Leina==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def kgonthiša_tsela(Leina, tsentšho_tsela=True):
    Tsejana = PurePosixPath(Leina)
    if Tsejana.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Leina.split('/')):
        raise ValueError('허용하지 않는 sehlopha Tsejana: ' + Leina)
    if '\\' in Leina or any(ord(tlhaka_boleng) < 32 or ord(tlhaka_boleng) == 127 for tlhaka_boleng in Leina):
        raise ValueError('잘못된 sehlopha Tsejana 문자')
    if tsentšho_tsela and (len(('/lib/' + Leina).encode()) > 63 or Leina in ('한국어.py', 'sehlopha.py')):
        raise ValueError('sehlopha Tsejana 제한 또는 setsenywa_sa_tirelwa Bokgobadata 충돌: ' + Leina)
    return Leina


def 압축풀기(faele_go_tsenya_tshedimošo_leina, data, Leina, bešene_boleng):
    파일들 = {}
    명세들 = []
    def 추가(Tsejana, Diteng_boleng):
        kgonthiša_tsela(Tsejana)
        if Tsejana in 파일들:
            raise ValueError('중복 sehlopha Tsejana: ' + Tsejana)
        if len(Diteng_boleng) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Tsejana)
        Diteng_boleng.decode('utf-8')
        파일들[Tsejana] = Diteng_boleng
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 mohlodi_mohlare 16개·합계 64 KiB 이하여야 합니다.')
    if faele_go_tsenya_tshedimošo_leina.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as sehlopha:
            항목들 = sehlopha.infolist()
            if len(항목들) > 256 or sum(go_tsenya_tshedimošo_boleng.file_size for go_tsenya_tshedimošo_boleng in 항목들) > 1048576:
                raise ValueError('Akhaebe_boleng lokolla_Bobolokelo Bogolo 제한 초과')
            taba_Lenaneo = [go_tsenya_tshedimošo_boleng for go_tsenya_tshedimošo_boleng in 항목들 if go_tsenya_tshedimošo_boleng.filename.endswith('.dist-info/WHEEL')]
            if len(taba_Lenaneo) != 1:
                raise ValueError('wheel taba_boleng 명세가 필요합니다.')
            taba_boleng = email.parser.Parser().parsestr(sehlopha.read(taba_Lenaneo[0]).decode())
            if taba_boleng.get('Root-Is-Purelib', '').lower() != 'true' or not faele_go_tsenya_tshedimošo_leina.endswith('-none-any.whl'):
                raise ValueError('C koketšo_boleng·플랫폼 전용 wheel은 지원하지 않습니다.')
            for go_tsenya_tshedimošo_boleng in 항목들:
                Tsejana = go_tsenya_tshedimošo_boleng.filename.rstrip('/')
                kgonthiša_tsela(Tsejana, False)
                if (go_tsenya_tshedimošo_boleng.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if go_tsenya_tshedimošo_boleng.filename.endswith('/'):
                    continue
                if '.dist-info/' in Tsejana:
                    if Tsejana.endswith('/METADATA'):
                        명세들.append(sehlopha.read(go_tsenya_tshedimošo_boleng).decode())
                    continue
                if not Tsejana.endswith('.py') or '.data/' in Tsejana:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Tsejana)
                추가(Tsejana, sehlopha.read(go_tsenya_tshedimošo_boleng))
    elif faele_go_tsenya_tshedimošo_leina.endswith('.tar.gz') and Leina.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py phethagatša_taelo 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as sehlopha:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for go_tsenya_tshedimošo_boleng in sehlopha:
                항목수 += 1
                전체크기 += go_tsenya_tshedimošo_boleng.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Akhaebe_boleng lokolla_Bobolokelo Bogolo 제한 초과')
                kgonthiša_tsela(go_tsenya_tshedimošo_boleng.name, False)
                부분들 = go_tsenya_tshedimošo_boleng.name.split('/')
                뿌리들.add(부분들[0])
                if go_tsenya_tshedimošo_boleng.isdir():
                    continue
                if not go_tsenya_tshedimošo_boleng.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython mohlodi_mohlare 배포형')
                Tsejana = '/'.join(부분들[1:])
                Diteng_boleng = sehlopha.extractfile(go_tsenya_tshedimošo_boleng).read()
                if Tsejana.endswith('PKG-INFO'):
                    명세들.append(Diteng_boleng.decode())
                elif Tsejana.endswith('.py') and Tsejana not in ('setup.py',):
                    추가(Tsejana, Diteng_boleng)
                elif '.egg-info/' not in Tsejana and not Tsejana.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Tsejana)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* mohlodi_mohlare 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Leina or 명세.get('Version') != bešene_boleng:
        raise ValueError('배포 메타데이터의 Leina·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(atrese, 한도):
    if not atrese.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(atrese, timeout=30) as fetola:
        if not fetola.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 atrese šuthiša_boleng')
        data = fetola.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 Faele Bogolo 제한 초과')
    return data


def fetišetša_sehlopha(Leina, bešene_boleng, 파일들, 출처):
    명세 = {'name': Leina, 'version': bešene_boleng, 'source': 출처, 'files': [
        {'path': Tsejana, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for Tsejana, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('sehlopha 명세 Bogolo 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[go_tsenya_tshedimošo_boleng['path']] for go_tsenya_tshedimošo_boleng in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Tsejana, 오프라인=False):
        자신.Tsejana = Path(Tsejana)
        자신.Tsejana.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Lokišetša(자신, 요청):
        Leina, bešene_boleng = 요청해석(요청)
        열쇠 = Leina + ('==' + bešene_boleng if bešene_boleng else '')
        pego_tsela = 자신.Tsejana / (열쇠 + '.json')
        배포경로 = 자신.Tsejana / (열쇠 + '.archive')
        if pego_tsela.is_file() and 배포경로.is_file():
            pego_rei = json.loads(pego_tsela.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != pego_rei['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 sehlopha: ' + 요청)
            atrese = 'https://pypi.org/pypi/' + Leina + ('/' + bešene_boleng if bešene_boleng else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(atrese, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [go_tsenya_tshedimošo_boleng for go_tsenya_tshedimošo_boleng in msinfo32_exe['urls'] if not go_tsenya_tshedimošo_boleng.get('yanked') and go_tsenya_tshedimošo_boleng['filename'].endswith('-none-any.whl')]
            if not 후보 and Leina.startswith('micropython-'):
                후보 = [go_tsenya_tshedimošo_boleng for go_tsenya_tshedimošo_boleng in msinfo32_exe['urls'] if not go_tsenya_tshedimošo_boleng.get('yanked') and go_tsenya_tshedimošo_boleng['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            kgetho_boleng = 후보[0]
            data = 웹읽기(kgetho_boleng['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != kgetho_boleng['digests']['sha256']:
                raise ValueError('PyPI 배포 Faele SHA-256 불일치')
            pego_rei = {'name': Leina, 'version': msinfo32_exe['info']['version'], 'filename': kgetho_boleng['filename'],
                    'url': kgetho_boleng['url'], 'sha256': kgetho_boleng['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(pego_rei['filename'], data, Leina, pego_rei['version'])
            배포경로.write_bytes(data)
            pego_tsela.write_text(json.dumps(pego_rei, ensure_ascii=False, indent=2) + '\n')
        if pego_rei['name'] != Leina or bešene_boleng and pego_rei['version'] != bešene_boleng:
            raise ValueError('저장소 Leina·버전 불일치')
        파일들 = 압축풀기(pego_rei['filename'], data, Leina, pego_rei['version'])
        return fetišetša_sehlopha(Leina, pego_rei['version'], 파일들, pego_rei['url'])


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
                raise ValueError('잘못된 sehlopha 요청')
            fetola = 자신.server.저장소.Lokišetša(요청[:-1].decode('ascii'))
        except Exception as Phošo:
            머리 = json.dumps({'error': str(Phošo)[:500]}, ensure_ascii=False).encode()
            fetola = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(fetola)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Tsejana=None, 오프라인=False):
        자신.seba_boleng = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.seba_boleng.allow_reuse_address = True
        자신.seba_boleng.server_bind()
        자신.seba_boleng.server_activate()
        자신.seba_boleng.저장소 = 꾸러미저장소(Tsejana or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.seba_boleng.server_address[1]
        자신.threte_boleng = threading.Thread(target=자신.seba_boleng.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.threte_boleng.start()
        return 자신

    def __exit__(자신, *인수):
        자신.seba_boleng.shutdown()
        자신.seba_boleng.server_close()
        자신.threte_boleng.join(timeout=2)


def Diriša():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='phethagatša_taelo 없이 호환 배포 파일을 내려받아 검사·lota_boleng')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        data = 꾸러미저장소(인수.cache, 인수.offline).Lokišetša(인수.fetch)
        print('sehlopha Lokišetša 완료:', 인수.fetch, len(data), 'paete_boleng')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('sehlopha 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.threte_boleng.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Diriša()
