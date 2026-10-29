#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 e_itawaa_ajutuu·실행한다."""
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
        raise ValueError('꾸러미 이름 또는 이름==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def 경로확인(이름, e_itaayaa_wopu_a_ttaaleemüin=True):
    wopu_a_ttaaleemüin = PurePosixPath(이름)
    if wopu_a_ttaaleemüin.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in 이름.split('/')):
        raise ValueError('허용하지 않는 꾸러미 wopu_a_ttaaleemüin: ' + 이름)
    if '\\' in 이름 or any(ord(jeerü_ajutuu) < 32 or ord(jeerü_ajutuu) == 127 for jeerü_ajutuu in 이름):
        raise ValueError('잘못된 꾸러미 wopu_a_ttaaleemüin 문자')
    if e_itaayaa_wopu_a_ttaaleemüin and (len(('/lib/' + 이름).encode()) > 63 or 이름 in ('한국어.py', '꾸러미.py')):
        raise ValueError('꾸러미 wopu_a_ttaaleemüin 제한 또는 ajutuu_aneekuushitüjülia anaajaalee 충돌: ' + 이름)
    return 이름


def 압축풀기(파일이름, atijaaya, 이름, 판):
    파일들 = {}
    명세들 = []
    def 추가(wopu_a_ttaaleemüin, alu_ujatüü_ajutuu):
        경로확인(wopu_a_ttaaleemüin)
        if wopu_a_ttaaleemüin in 파일들:
            raise ValueError('중복 꾸러미 wopu_a_ttaaleemüin: ' + wopu_a_ttaaleemüin)
        if len(alu_ujatüü_ajutuu) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + wopu_a_ttaaleemüin)
        alu_ujatüü_ajutuu.decode('utf-8')
        파일들[wopu_a_ttaaleemüin] = alu_ujatüü_ajutuu
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 eejeejetülein_wunu_ulia 16개·합계 64 KiB 이하여야 합니다.')
    if 파일이름.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(atijaaya)) as 꾸러미:
            항목들 = 꾸러미.infolist()
            if len(항목들) > 256 or sum(ekeroliaa_ajutuu.file_size for ekeroliaa_ajutuu in 항목들) > 1048576:
                raise ValueError('anaajawaa_ajutuu 해제 크기 제한 초과')
            규약들 = [ekeroliaa_ajutuu for ekeroliaa_ajutuu in 항목들 if ekeroliaa_ajutuu.filename.endswith('.dist-info/WHEEL')]
            if len(규약들) != 1:
                raise ValueError('wheel achikii_ajutuu 명세가 필요합니다.')
            achikii_ajutuu = email.parser.Parser().parsestr(꾸러미.read(규약들[0]).decode())
            if achikii_ajutuu.get('Root-Is-Purelib', '').lower() != 'true' or not 파일이름.endswith('-none-any.whl'):
                raise ValueError('C e_irukuu_ajutuu·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ekeroliaa_ajutuu in 항목들:
                wopu_a_ttaaleemüin = ekeroliaa_ajutuu.filename.rstrip('/')
                경로확인(wopu_a_ttaaleemüin, False)
                if (ekeroliaa_ajutuu.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ekeroliaa_ajutuu.filename.endswith('/'):
                    continue
                if '.dist-info/' in wopu_a_ttaaleemüin:
                    if wopu_a_ttaaleemüin.endswith('/METADATA'):
                        명세들.append(꾸러미.read(ekeroliaa_ajutuu).decode())
                    continue
                if not wopu_a_ttaaleemüin.endswith('.py') or '.data/' in wopu_a_ttaaleemüin:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + wopu_a_ttaaleemüin)
                추가(wopu_a_ttaaleemüin, 꾸러미.read(ekeroliaa_ajutuu))
    elif 파일이름.endswith('.tar.gz') and 이름.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py 실행 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(atijaaya), mode='r|gz') as 꾸러미:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ekeroliaa_ajutuu in 꾸러미:
                항목수 += 1
                전체크기 += ekeroliaa_ajutuu.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('anaajawaa_ajutuu 해제 크기 제한 초과')
                경로확인(ekeroliaa_ajutuu.name, False)
                부분들 = ekeroliaa_ajutuu.name.split('/')
                뿌리들.add(부분들[0])
                if ekeroliaa_ajutuu.isdir():
                    continue
                if not ekeroliaa_ajutuu.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython eejeejetülein_wunu_ulia 배포형')
                wopu_a_ttaaleemüin = '/'.join(부분들[1:])
                alu_ujatüü_ajutuu = 꾸러미.extractfile(ekeroliaa_ajutuu).read()
                if wopu_a_ttaaleemüin.endswith('PKG-INFO'):
                    명세들.append(alu_ujatüü_ajutuu.decode())
                elif wopu_a_ttaaleemüin.endswith('.py') and wopu_a_ttaaleemüin not in ('setup.py',):
                    추가(wopu_a_ttaaleemüin, alu_ujatüü_ajutuu)
                elif '.egg-info/' not in wopu_a_ttaaleemüin and not wopu_a_ttaaleemüin.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + wopu_a_ttaaleemüin)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* eejeejetülein_wunu_ulia 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != 이름 or 명세.get('Version') != 판:
        raise ValueError('배포 메타데이터의 이름·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ejepüsee, 한도):
    if not ejepüsee.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ejepüsee, timeout=30) as 응답:
        if not 응답.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ejepüsee 이동')
        atijaaya = 응답.read(한도 + 1)
    if len(atijaaya) > 한도:
        raise ValueError('배포 anaajaalaa 크기 제한 초과')
    return atijaaya


def 전송묶음(이름, 판, 파일들, 출처):
    명세 = {'name': 이름, 'version': 판, 'source': 출처, 'files': [
        {'path': wopu_a_ttaaleemüin, 'size': len(atijaaya), 'sha256': hashlib.sha256(atijaaya).hexdigest()}
        for wopu_a_ttaaleemüin, atijaaya in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('꾸러미 명세 크기 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ekeroliaa_ajutuu['path']] for ekeroliaa_ajutuu in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, wopu_a_ttaaleemüin, 오프라인=False):
        자신.wopu_a_ttaaleemüin = Path(wopu_a_ttaaleemüin)
        자신.wopu_a_ttaaleemüin.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def 준비(자신, 요청):
        이름, 판 = 요청해석(요청)
        열쇠 = 이름 + ('==' + 판 if 판 else '')
        aa_innachikimaajatü_wopu_a_ttaaleemüin = 자신.wopu_a_ttaaleemüin / (열쇠 + '.json')
        배포경로 = 자신.wopu_a_ttaaleemüin / (열쇠 + '.archive')
        if aa_innachikimaajatü_wopu_a_ttaaleemüin.is_file() and 배포경로.is_file():
            aa_innachikimaajatü_aparatsee = json.loads(aa_innachikimaajatü_wopu_a_ttaaleemüin.read_text())
            atijaaya = 배포경로.read_bytes()
            if hashlib.sha256(atijaaya).hexdigest() != aa_innachikimaajatü_aparatsee['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 꾸러미: ' + 요청)
            ejepüsee = 'https://pypi.org/pypi/' + 이름 + ('/' + 판 if 판 else '') + '/json'
            정보 = json.loads(웹읽기(ejepüsee, 4194304).decode())
            if 정보['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ekeroliaa_ajutuu for ekeroliaa_ajutuu in 정보['urls'] if not ekeroliaa_ajutuu.get('yanked') and ekeroliaa_ajutuu['filename'].endswith('-none-any.whl')]
            if not 후보 and 이름.startswith('micropython-'):
                후보 = [ekeroliaa_ajutuu for ekeroliaa_ajutuu in 정보['urls'] if not ekeroliaa_ajutuu.get('yanked') and ekeroliaa_ajutuu['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            선택 = 후보[0]
            atijaaya = 웹읽기(선택['url'], 4194304)
            if hashlib.sha256(atijaaya).hexdigest() != 선택['digests']['sha256']:
                raise ValueError('PyPI 배포 anaajaalaa SHA-256 불일치')
            aa_innachikimaajatü_aparatsee = {'name': 이름, 'version': 정보['info']['version'], 'filename': 선택['filename'],
                    'url': 선택['url'], 'sha256': 선택['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(aa_innachikimaajatü_aparatsee['filename'], atijaaya, 이름, aa_innachikimaajatü_aparatsee['version'])
            배포경로.write_bytes(atijaaya)
            aa_innachikimaajatü_wopu_a_ttaaleemüin.write_text(json.dumps(aa_innachikimaajatü_aparatsee, ensure_ascii=False, indent=2) + '\n')
        if aa_innachikimaajatü_aparatsee['name'] != 이름 or 판 and aa_innachikimaajatü_aparatsee['version'] != 판:
            raise ValueError('저장소 이름·버전 불일치')
        파일들 = 압축풀기(aa_innachikimaajatü_aparatsee['filename'], atijaaya, 이름, aa_innachikimaajatü_aparatsee['version'])
        return 전송묶음(이름, aa_innachikimaajatü_aparatsee['version'], 파일들, aa_innachikimaajatü_aparatsee['url'])


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
            응답 = 자신.server.저장소.준비(요청[:-1].decode('ascii'))
        except Exception as ajachitia:
            머리 = json.dumps({'error': str(ajachitia)[:500]}, ensure_ascii=False).encode()
            응답 = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(응답)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, wopu_a_ttaaleemüin=None, 오프라인=False):
        자신.서버 = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.서버.allow_reuse_address = True
        자신.서버.server_bind()
        자신.서버.server_activate()
        자신.서버.저장소 = 꾸러미저장소(wopu_a_ttaaleemüin or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.서버.server_address[1]
        자신.akumajia_ipa_ajutuu = threading.Thread(target=자신.서버.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.akumajia_ipa_ajutuu.start()
        return 자신

    def __exit__(자신, *인수):
        자신.서버.shutdown()
        자신.서버.server_close()
        자신.akumajia_ipa_ajutuu.join(timeout=2)


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='실행 없이 호환 배포 파일을 내려받아 검사·저장')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        atijaaya = 꾸러미저장소(인수.cache, 인수.offline).준비(인수.fetch)
        print('꾸러미 준비 완료:', 인수.fetch, len(atijaaya), 'waai_ajutuu')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('꾸러미 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.akumajia_ipa_ajutuu.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    시작()
