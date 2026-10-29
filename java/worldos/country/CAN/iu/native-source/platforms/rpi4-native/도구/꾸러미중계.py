#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ilili_atuutilik·실행한다."""
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
        raise ValueError('꾸러미 atiq 또는 atiq==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def naammannirarli_aqqut(atiq, ilisiniq_aqqut=True):
    aqqut = PurePosixPath(atiq)
    if aqqut.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in atiq.split('/')):
        raise ValueError('허용하지 않는 꾸러미 aqqut: ' + atiq)
    if '\\' in atiq or any(ord(immikkuuqtuq_atuutilik) < 32 or ord(immikkuuqtuq_atuutilik) == 127 for immikkuuqtuq_atuutilik in atiq):
        raise ValueError('잘못된 꾸러미 aqqut 문자')
    if ilisiniq_aqqut and (len(('/lib/' + atiq).encode()) > 63 or atiq in ('한국어.py', '꾸러미.py')):
        raise ValueError('꾸러미 aqqut 제한 또는 Aturniliuvagiiqtut tukisiurvik 충돌: ' + atiq)
    return atiq


def 압축풀기(ini_Iliniku_atiq, titiqqat, atiq, imaittuuninga_atuutilik):
    파일들 = {}
    명세들 = []
    def 추가(aqqut, Ilulingit_atuutilik):
        naammannirarli_aqqut(aqqut)
        if aqqut in 파일들:
            raise ValueError('중복 꾸러미 aqqut: ' + aqqut)
        if len(Ilulingit_atuutilik) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + aqqut)
        Ilulingit_atuutilik.decode('utf-8')
        파일들[aqqut] = Ilulingit_atuutilik
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 pivviujuq_attavigiit 16개·합계 64 KiB 이하여야 합니다.')
    if ini_Iliniku_atiq.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(titiqqat)) as 꾸러미:
            항목들 = 꾸러미.infolist()
            if len(항목들) > 256 or sum(Iliniku_atuutilik.file_size for Iliniku_atuutilik in 항목들) > 1048576:
                raise ValueError('tuqqurli_atuutilik_e917f8d5 해제 anininga 제한 초과')
            pijatsaq_Titiqpalliagaq = [Iliniku_atuutilik for Iliniku_atuutilik in 항목들 if Iliniku_atuutilik.filename.endswith('.dist-info/WHEEL')]
            if len(pijatsaq_Titiqpalliagaq) != 1:
                raise ValueError('wheel pijatsaq_atuutilik 명세가 필요합니다.')
            pijatsaq_atuutilik = email.parser.Parser().parsestr(꾸러미.read(pijatsaq_Titiqpalliagaq[0]).decode())
            if pijatsaq_atuutilik.get('Root-Is-Purelib', '').lower() != 'true' or not ini_Iliniku_atiq.endswith('-none-any.whl'):
                raise ValueError('C uigu_atuutilik·플랫폼 전용 wheel은 지원하지 않습니다.')
            for Iliniku_atuutilik in 항목들:
                aqqut = Iliniku_atuutilik.filename.rstrip('/')
                naammannirarli_aqqut(aqqut, False)
                if (Iliniku_atuutilik.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if Iliniku_atuutilik.filename.endswith('/'):
                    continue
                if '.dist-info/' in aqqut:
                    if aqqut.endswith('/METADATA'):
                        명세들.append(꾸러미.read(Iliniku_atuutilik).decode())
                    continue
                if not aqqut.endswith('.py') or '.data/' in aqqut:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + aqqut)
                추가(aqqut, 꾸러미.read(Iliniku_atuutilik))
    elif ini_Iliniku_atiq.endswith('.tar.gz') and atiq.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py 실행 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(titiqqat), mode='r|gz') as 꾸러미:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for Iliniku_atuutilik in 꾸러미:
                항목수 += 1
                전체크기 += Iliniku_atuutilik.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('tuqqurli_atuutilik_e917f8d5 해제 anininga 제한 초과')
                naammannirarli_aqqut(Iliniku_atuutilik.name, False)
                부분들 = Iliniku_atuutilik.name.split('/')
                뿌리들.add(부분들[0])
                if Iliniku_atuutilik.isdir():
                    continue
                if not Iliniku_atuutilik.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython pivviujuq_attavigiit 배포형')
                aqqut = '/'.join(부분들[1:])
                Ilulingit_atuutilik = 꾸러미.extractfile(Iliniku_atuutilik).read()
                if aqqut.endswith('PKG-INFO'):
                    명세들.append(Ilulingit_atuutilik.decode())
                elif aqqut.endswith('.py') and aqqut not in ('setup.py',):
                    추가(aqqut, Ilulingit_atuutilik)
                elif '.egg-info/' not in aqqut and not aqqut.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + aqqut)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* pivviujuq_attavigiit 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != atiq or 명세.get('Version') != imaittuuninga_atuutilik:
        raise ValueError('배포 메타데이터의 atiq·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(turaarut, 한도):
    if not turaarut.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(turaarut, timeout=30) as 응답:
        if not 응답.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 turaarut nuulli_atuutilik')
        titiqqat = 응답.read(한도 + 1)
    if len(titiqqat) > 한도:
        raise ValueError('배포 ini anininga 제한 초과')
    return titiqqat


def 전송묶음(atiq, imaittuuninga_atuutilik, 파일들, 출처):
    명세 = {'name': atiq, 'version': imaittuuninga_atuutilik, 'source': 출처, 'files': [
        {'path': aqqut, 'size': len(titiqqat), 'sha256': hashlib.sha256(titiqqat).hexdigest()}
        for aqqut, titiqqat in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('꾸러미 명세 anininga 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[Iliniku_atuutilik['path']] for Iliniku_atuutilik in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, aqqut, 오프라인=False):
        자신.aqqut = Path(aqqut)
        자신.aqqut.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Parnalli(자신, 요청):
        atiq, imaittuuninga_atuutilik = 요청해석(요청)
        열쇠 = atiq + ('==' + imaittuuninga_atuutilik if imaittuuninga_atuutilik else '')
        papattivik_aqqut = 자신.aqqut / (열쇠 + '.json')
        배포경로 = 자신.aqqut / (열쇠 + '.archive')
        if papattivik_aqqut.is_file() and 배포경로.is_file():
            papattivik_sanimukutaak = json.loads(papattivik_aqqut.read_text())
            titiqqat = 배포경로.read_bytes()
            if hashlib.sha256(titiqqat).hexdigest() != papattivik_sanimukutaak['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 꾸러미: ' + 요청)
            turaarut = 'https://pypi.org/pypi/' + atiq + ('/' + imaittuuninga_atuutilik if imaittuuninga_atuutilik else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(turaarut, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [Iliniku_atuutilik for Iliniku_atuutilik in msinfo32_exe['urls'] if not Iliniku_atuutilik.get('yanked') and Iliniku_atuutilik['filename'].endswith('-none-any.whl')]
            if not 후보 and atiq.startswith('micropython-'):
                후보 = [Iliniku_atuutilik for Iliniku_atuutilik in msinfo32_exe['urls'] if not Iliniku_atuutilik.get('yanked') and Iliniku_atuutilik['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            nirulussimaniq_atuutilik = 후보[0]
            titiqqat = 웹읽기(nirulussimaniq_atuutilik['url'], 4194304)
            if hashlib.sha256(titiqqat).hexdigest() != nirulussimaniq_atuutilik['digests']['sha256']:
                raise ValueError('PyPI 배포 ini SHA-256 불일치')
            papattivik_sanimukutaak = {'name': atiq, 'version': msinfo32_exe['info']['version'], 'filename': nirulussimaniq_atuutilik['filename'],
                    'url': nirulussimaniq_atuutilik['url'], 'sha256': nirulussimaniq_atuutilik['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(papattivik_sanimukutaak['filename'], titiqqat, atiq, papattivik_sanimukutaak['version'])
            배포경로.write_bytes(titiqqat)
            papattivik_aqqut.write_text(json.dumps(papattivik_sanimukutaak, ensure_ascii=False, indent=2) + '\n')
        if papattivik_sanimukutaak['name'] != atiq or imaittuuninga_atuutilik and papattivik_sanimukutaak['version'] != imaittuuninga_atuutilik:
            raise ValueError('저장소 atiq·버전 불일치')
        파일들 = 압축풀기(papattivik_sanimukutaak['filename'], titiqqat, atiq, papattivik_sanimukutaak['version'])
        return 전송묶음(atiq, papattivik_sanimukutaak['version'], 파일들, papattivik_sanimukutaak['url'])


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
                raise ValueError('잘못된 꾸러미 요청')
            응답 = 자신.server.저장소.Parnalli(요청[:-1].decode('ascii'))
        except Exception as tammarniq:
            머리 = json.dumps({'error': str(tammarniq)[:500]}, ensure_ascii=False).encode()
            응답 = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(응답)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, aqqut=None, 오프라인=False):
        자신.ikiaqqitittivik_atuutilik = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.ikiaqqitittivik_atuutilik.allow_reuse_address = True
        자신.ikiaqqitittivik_atuutilik.server_bind()
        자신.ikiaqqitittivik_atuutilik.server_activate()
        자신.ikiaqqitittivik_atuutilik.저장소 = 꾸러미저장소(aqqut or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.ikiaqqitittivik_atuutilik.server_address[1]
        자신.aqqusiqtarvik_atuutilik = threading.Thread(target=자신.ikiaqqitittivik_atuutilik.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.aqqusiqtarvik_atuutilik.start()
        return 자신

    def __exit__(자신, *인수):
        자신.ikiaqqitittivik_atuutilik.shutdown()
        자신.ikiaqqitittivik_atuutilik.server_close()
        자신.aqqusiqtarvik_atuutilik.join(timeout=2)


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='실행 없이 호환 배포 파일을 내려받아 검사·tuqqurli_atuutilik')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        titiqqat = 꾸러미저장소(인수.cache, 인수.offline).Parnalli(인수.fetch)
        print('꾸러미 Parnalli 완료:', 인수.fetch, len(titiqqat), 'byte_atuutilik')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('꾸러미 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.aqqusiqtarvik_atuutilik.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    시작()
