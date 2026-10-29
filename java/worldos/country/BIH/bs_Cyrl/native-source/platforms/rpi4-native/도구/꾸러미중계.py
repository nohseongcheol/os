#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 инсталирати_вриједност·실행한다."""
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
        raise ValueError('пакет назив 또는 назив==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def овјерити_пут(назив, инсталација_пут=True):
    пут = PurePosixPath(назив)
    if пут.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in назив.split('/')):
        raise ValueError('허용하지 않는 пакет пут: ' + назив)
    if '\\' in назив or any(ord(знак_вриједност) < 32 or ord(знак_вриједност) == 127 for знак_вриједност in назив):
        raise ValueError('잘못된 пакет пут 문자')
    if инсталација_пут and (len(('/lib/' + назив).encode()) > 63 or назив in ('한국어.py', 'пакет.py')):
        raise ValueError('пакет пут 제한 또는 задана_вриједност библиотека 충돌: ' + назив)
    return назив


def 압축풀기(фајл_унос_назив, подаци, назив, верзија_вриједност):
    파일들 = {}
    명세들 = []
    def 추가(пут, Садржај_вриједност):
        овјерити_пут(пут)
        if пут in 파일들:
            raise ValueError('중복 пакет пут: ' + пут)
        if len(Садржај_вриједност) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + пут)
        Садржај_вриједност.decode('utf-8')
        파일들[пут] = Садржај_вриједност
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 извор_стабло 16개·합계 64 KiB 이하여야 합니다.')
    if фајл_унос_назив.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(подаци)) as пакет:
            항목들 = пакет.infolist()
            if len(항목들) > 256 or sum(унос_вриједност.file_size for унос_вриједност in 항목들) > 1048576:
                raise ValueError('архива_вриједност 해제 подесити_величину 제한 초과')
            Уговор_списак = [унос_вриједност for унос_вриједност in 항목들 if унос_вриједност.filename.endswith('.dist-info/WHEEL')]
            if len(Уговор_списак) != 1:
                raise ValueError('wheel Уговор_вриједност 명세가 필요합니다.')
            Уговор_вриједност = email.parser.Parser().parsestr(пакет.read(Уговор_списак[0]).decode())
            if Уговор_вриједност.get('Root-Is-Purelib', '').lower() != 'true' or not фајл_унос_назив.endswith('-none-any.whl'):
                raise ValueError('C екстензија_вриједност·플랫폼 전용 wheel은 지원하지 않습니다.')
            for унос_вриједност in 항목들:
                пут = унос_вриједност.filename.rstrip('/')
                овјерити_пут(пут, False)
                if (унос_вриједност.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if унос_вриједност.filename.endswith('/'):
                    continue
                if '.dist-info/' in пут:
                    if пут.endswith('/METADATA'):
                        명세들.append(пакет.read(унос_вриједност).decode())
                    continue
                if not пут.endswith('.py') or '.data/' in пут:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + пут)
                추가(пут, пакет.read(унос_вриједност))
    elif фајл_унос_назив.endswith('.tar.gz') and назив.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py 실행 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(подаци), mode='r|gz') as пакет:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for унос_вриједност in пакет:
                항목수 += 1
                전체크기 += унос_вриједност.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('архива_вриједност 해제 подесити_величину 제한 초과')
                овјерити_пут(унос_вриједност.name, False)
                부분들 = унос_вриједност.name.split('/')
                뿌리들.add(부분들[0])
                if унос_вриједност.isdir():
                    continue
                if not унос_вриједност.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython извор_стабло 배포형')
                пут = '/'.join(부분들[1:])
                Садржај_вриједност = пакет.extractfile(унос_вриједност).read()
                if пут.endswith('PKG-INFO'):
                    명세들.append(Садржај_вриједност.decode())
                elif пут.endswith('.py') and пут not in ('setup.py',):
                    추가(пут, Садржај_вриједност)
                elif '.egg-info/' not in пут and not пут.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + пут)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* извор_стабло 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != назив or 명세.get('Version') != верзија_вриједност:
        raise ValueError('배포 메타데이터의 назив·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(адреса, 한도):
    if not адреса.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(адреса, timeout=30) as 응답:
        if not 응답.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 адреса помаћи_вриједност')
        подаци = 응답.read(한도 + 1)
    if len(подаци) > 한도:
        raise ValueError('배포 фајл подесити_величину 제한 초과')
    return подаци


def пријенос_пакет(назив, верзија_вриједност, 파일들, 출처):
    명세 = {'name': назив, 'version': верзија_вриједност, 'source': 출처, 'files': [
        {'path': пут, 'size': len(подаци), 'sha256': hashlib.sha256(подаци).hexdigest()}
        for пут, подаци in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('пакет 명세 подесити_величину 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[унос_вриједност['path']] for унос_вриједност in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, пут, 오프라인=False):
        자신.пут = Path(пут)
        자신.пут.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Припремити(자신, 요청):
        назив, верзија_вриједност = 요청해석(요청)
        열쇠 = назив + ('==' + верзија_вриједност if верзија_вриједност else '')
        дневник_рада_пут = 자신.пут / (열쇠 + '.json')
        배포경로 = 자신.пут / (열쇠 + '.archive')
        if дневник_рада_пут.is_file() and 배포경로.is_file():
            дневник_рада_ред = json.loads(дневник_рада_пут.read_text())
            подаци = 배포경로.read_bytes()
            if hashlib.sha256(подаци).hexdigest() != дневник_рада_ред['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 пакет: ' + 요청)
            адреса = 'https://pypi.org/pypi/' + назив + ('/' + верзија_вриједност if верзија_вриједност else '') + '/json'
            систем_информација = json.loads(웹읽기(адреса, 4194304).decode())
            if систем_информација['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [унос_вриједност for унос_вриједност in систем_информација['urls'] if not унос_вриједност.get('yanked') and унос_вриједност['filename'].endswith('-none-any.whl')]
            if not 후보 and назив.startswith('micropython-'):
                후보 = [унос_вриједност for унос_вриједност in систем_информација['urls'] if not унос_вриједност.get('yanked') and унос_вриједност['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            избор_вриједност = 후보[0]
            подаци = 웹읽기(избор_вриједност['url'], 4194304)
            if hashlib.sha256(подаци).hexdigest() != избор_вриједност['digests']['sha256']:
                raise ValueError('PyPI 배포 фајл SHA-256 불일치')
            дневник_рада_ред = {'name': назив, 'version': систем_информација['info']['version'], 'filename': избор_вриједност['filename'],
                    'url': избор_вриједност['url'], 'sha256': избор_вриједност['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(дневник_рада_ред['filename'], подаци, назив, дневник_рада_ред['version'])
            배포경로.write_bytes(подаци)
            дневник_рада_пут.write_text(json.dumps(дневник_рада_ред, ensure_ascii=False, indent=2) + '\n')
        if дневник_рада_ред['name'] != назив or верзија_вриједност and дневник_рада_ред['version'] != верзија_вриједност:
            raise ValueError('저장소 назив·버전 불일치')
        파일들 = 압축풀기(дневник_рада_ред['filename'], подаци, назив, дневник_рада_ред['version'])
        return пријенос_пакет(назив, дневник_рада_ред['version'], 파일들, дневник_рада_ред['url'])


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
                raise ValueError('잘못된 пакет 요청')
            응답 = 자신.server.저장소.Припремити(요청[:-1].decode('ascii'))
        except Exception as грешка:
            머리 = json.dumps({'error': str(грешка)[:500]}, ensure_ascii=False).encode()
            응답 = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(응답)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, пут=None, 오프라인=False):
        자신.сервер_вриједност = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.сервер_вриједност.allow_reuse_address = True
        자신.сервер_вриједност.server_bind()
        자신.сервер_вриједност.server_activate()
        자신.сервер_вриједност.저장소 = 꾸러미저장소(пут or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.сервер_вриједност.server_address[1]
        자신.нит_вриједност = threading.Thread(target=자신.сервер_вриједност.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.нит_вриједност.start()
        return 자신

    def __exit__(자신, *인수):
        자신.сервер_вриједност.shutdown()
        자신.сервер_вриједност.server_close()
        자신.нит_вриједност.join(timeout=2)


def 시작():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='실행 없이 호환 배포 파일을 내려받아 검사·похранити_вриједност')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        подаци = 꾸러미저장소(인수.cache, 인수.offline).Припремити(인수.fetch)
        print('пакет Припремити 완료:', 인수.fetch, len(подаци), 'бајт_вриједност')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('пакет 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.нит_вриједност.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    시작()
