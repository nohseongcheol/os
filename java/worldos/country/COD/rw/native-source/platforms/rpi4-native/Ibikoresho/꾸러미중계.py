#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 kwinjiza_agaciro·실행한다."""
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
        raise ValueError('ipaki Izina 또는 Izina==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def kwemeza_inzira(Izina, iyinjiza_inzira=True):
    Inzira = PurePosixPath(Izina)
    if Inzira.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Izina.split('/')):
        raise ValueError('허용하지 않는 ipaki Inzira: ' + Izina)
    if '\\' in Izina or any(ord(inyuguti_agaciro) < 32 or ord(inyuguti_agaciro) == 127 for inyuguti_agaciro in Izina):
        raise ValueError('잘못된 ipaki Inzira 문자')
    if iyinjiza_inzira and (len(('/lib/' + Izina).encode()) > 63 or Izina in ('Ikinyarwanda.py', 'ipaki.py')):
        raise ValueError('ipaki Inzira 제한 또는 agaciro_gasanzweho isomero 충돌: ' + Izina)
    return Izina


def 압축풀기(dosiye_icyinjizwa_izina, amakurushingiro, Izina, verisiyo_agaciro):
    파일들 = {}
    명세들 = []
    def 추가(Inzira, Ibirimo_agaciro):
        kwemeza_inzira(Inzira)
        if Inzira in 파일들:
            raise ValueError('중복 ipaki Inzira: ' + Inzira)
        if len(Ibirimo_agaciro) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Inzira)
        Ibirimo_agaciro.decode('utf-8')
        파일들[Inzira] = Ibirimo_agaciro
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 inkomoko_igiti 16개·합계 64 KiB 이하여야 합니다.')
    if dosiye_icyinjizwa_izina.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(amakurushingiro)) as ipaki:
            항목들 = ipaki.infolist()
            if len(항목들) > 256 or sum(icyinjizwa_agaciro.file_size for icyinjizwa_agaciro in 항목들) > 1048576:
                raise ValueError('gushyingura_agaciro kurekura_Ububiko Ingano 제한 초과')
            ikibazo_Urutonde = [icyinjizwa_agaciro for icyinjizwa_agaciro in 항목들 if icyinjizwa_agaciro.filename.endswith('.dist-info/WHEEL')]
            if len(ikibazo_Urutonde) != 1:
                raise ValueError('wheel ikibazo_agaciro 명세가 필요합니다.')
            ikibazo_agaciro = email.parser.Parser().parsestr(ipaki.read(ikibazo_Urutonde[0]).decode())
            if ikibazo_agaciro.get('Root-Is-Purelib', '').lower() != 'true' or not dosiye_icyinjizwa_izina.endswith('-none-any.whl'):
                raise ValueError('C umugereka_agaciro·플랫폼 전용 wheel은 지원하지 않습니다.')
            for icyinjizwa_agaciro in 항목들:
                Inzira = icyinjizwa_agaciro.filename.rstrip('/')
                kwemeza_inzira(Inzira, False)
                if (icyinjizwa_agaciro.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if icyinjizwa_agaciro.filename.endswith('/'):
                    continue
                if '.dist-info/' in Inzira:
                    if Inzira.endswith('/METADATA'):
                        명세들.append(ipaki.read(icyinjizwa_agaciro).decode())
                    continue
                if not Inzira.endswith('.py') or '.data/' in Inzira:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Inzira)
                추가(Inzira, ipaki.read(icyinjizwa_agaciro))
    elif dosiye_icyinjizwa_izina.endswith('.tar.gz') and Izina.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py gukora_ibwiriza 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(amakurushingiro), mode='r|gz') as ipaki:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for icyinjizwa_agaciro in ipaki:
                항목수 += 1
                전체크기 += icyinjizwa_agaciro.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('gushyingura_agaciro kurekura_Ububiko Ingano 제한 초과')
                kwemeza_inzira(icyinjizwa_agaciro.name, False)
                부분들 = icyinjizwa_agaciro.name.split('/')
                뿌리들.add(부분들[0])
                if icyinjizwa_agaciro.isdir():
                    continue
                if not icyinjizwa_agaciro.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython inkomoko_igiti 배포형')
                Inzira = '/'.join(부분들[1:])
                Ibirimo_agaciro = ipaki.extractfile(icyinjizwa_agaciro).read()
                if Inzira.endswith('PKG-INFO'):
                    명세들.append(Ibirimo_agaciro.decode())
                elif Inzira.endswith('.py') and Inzira not in ('setup.py',):
                    추가(Inzira, Ibirimo_agaciro)
                elif '.egg-info/' not in Inzira and not Inzira.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Inzira)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* inkomoko_igiti 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Izina or 명세.get('Version') != verisiyo_agaciro:
        raise ValueError('배포 메타데이터의 Izina·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(aderesi, 한도):
    if not aderesi.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(aderesi, timeout=30) as gusubiza:
        if not gusubiza.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 aderesi kwimura_agaciro')
        amakurushingiro = gusubiza.read(한도 + 1)
    if len(amakurushingiro) > 한도:
        raise ValueError('배포 Idosiye Ingano 제한 초과')
    return amakurushingiro


def iyimura_ipaki(Izina, verisiyo_agaciro, 파일들, 출처):
    명세 = {'name': Izina, 'version': verisiyo_agaciro, 'source': 출처, 'files': [
        {'path': Inzira, 'size': len(amakurushingiro), 'sha256': hashlib.sha256(amakurushingiro).hexdigest()}
        for Inzira, amakurushingiro in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ipaki 명세 Ingano 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[icyinjizwa_agaciro['path']] for icyinjizwa_agaciro in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Inzira, 오프라인=False):
        자신.Inzira = Path(Inzira)
        자신.Inzira.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Gutegura(자신, 요청):
        Izina, verisiyo_agaciro = 요청해석(요청)
        열쇠 = Izina + ('==' + verisiyo_agaciro if verisiyo_agaciro else '')
        kubika_inzira = 자신.Inzira / (열쇠 + '.json')
        배포경로 = 자신.Inzira / (열쇠 + '.archive')
        if kubika_inzira.is_file() and 배포경로.is_file():
            kubika_umurongo = json.loads(kubika_inzira.read_text())
            amakurushingiro = 배포경로.read_bytes()
            if hashlib.sha256(amakurushingiro).hexdigest() != kubika_umurongo['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 ipaki: ' + 요청)
            aderesi = 'https://pypi.org/pypi/' + Izina + ('/' + verisiyo_agaciro if verisiyo_agaciro else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(aderesi, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [icyinjizwa_agaciro for icyinjizwa_agaciro in msinfo32_exe['urls'] if not icyinjizwa_agaciro.get('yanked') and icyinjizwa_agaciro['filename'].endswith('-none-any.whl')]
            if not 후보 and Izina.startswith('micropython-'):
                후보 = [icyinjizwa_agaciro for icyinjizwa_agaciro in msinfo32_exe['urls'] if not icyinjizwa_agaciro.get('yanked') and icyinjizwa_agaciro['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ihitamo_agaciro = 후보[0]
            amakurushingiro = 웹읽기(ihitamo_agaciro['url'], 4194304)
            if hashlib.sha256(amakurushingiro).hexdigest() != ihitamo_agaciro['digests']['sha256']:
                raise ValueError('PyPI 배포 Idosiye SHA-256 불일치')
            kubika_umurongo = {'name': Izina, 'version': msinfo32_exe['info']['version'], 'filename': ihitamo_agaciro['filename'],
                    'url': ihitamo_agaciro['url'], 'sha256': ihitamo_agaciro['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(kubika_umurongo['filename'], amakurushingiro, Izina, kubika_umurongo['version'])
            배포경로.write_bytes(amakurushingiro)
            kubika_inzira.write_text(json.dumps(kubika_umurongo, ensure_ascii=False, indent=2) + '\n')
        if kubika_umurongo['name'] != Izina or verisiyo_agaciro and kubika_umurongo['version'] != verisiyo_agaciro:
            raise ValueError('저장소 Izina·버전 불일치')
        파일들 = 압축풀기(kubika_umurongo['filename'], amakurushingiro, Izina, kubika_umurongo['version'])
        return iyimura_ipaki(Izina, kubika_umurongo['version'], 파일들, kubika_umurongo['url'])


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
                raise ValueError('잘못된 ipaki 요청')
            gusubiza = 자신.server.저장소.Gutegura(요청[:-1].decode('ascii'))
        except Exception as IKOSA:
            머리 = json.dumps({'error': str(IKOSA)[:500]}, ensure_ascii=False).encode()
            gusubiza = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(gusubiza)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Inzira=None, 오프라인=False):
        자신.seriveri_agaciro = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.seriveri_agaciro.allow_reuse_address = True
        자신.seriveri_agaciro.server_bind()
        자신.seriveri_agaciro.server_activate()
        자신.seriveri_agaciro.저장소 = 꾸러미저장소(Inzira or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.seriveri_agaciro.server_address[1]
        자신.mugenaporogaramu_agaciro = threading.Thread(target=자신.seriveri_agaciro.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.mugenaporogaramu_agaciro.start()
        return 자신

    def __exit__(자신, *인수):
        자신.seriveri_agaciro.shutdown()
        자신.seriveri_agaciro.server_close()
        자신.mugenaporogaramu_agaciro.join(timeout=2)


def ihuriro():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='gukora_ibwiriza 없이 호환 배포 파일을 내려받아 검사·Store_agaciro')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        amakurushingiro = 꾸러미저장소(인수.cache, 인수.offline).Gutegura(인수.fetch)
        print('ipaki Gutegura 완료:', 인수.fetch, len(amakurushingiro), 'bayiti_agaciro')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ipaki 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.mugenaporogaramu_agaciro.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ihuriro()
