#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 инсталирај_вриједност·실행한다."""
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

пројектовати_корен = Path(__file__).resolve().parents[1]


def рашчланити_захтев(захтев):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', захтев)
    if not 맞음:
        raise ValueError('пакет Назив 또는 Назив==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def потврдити_пут(Назив, инсталација_пут=True):
    ПУТАЊА = PurePosixPath(Назив)
    if ПУТАЊА.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Назив.split('/')):
        raise ValueError('허용하지 않는 пакет ПУТАЊА: ' + Назив)
    if '\\' in Назив or any(ord(знак_вриједност) < 32 or ord(знак_вриједност) == 127 for знак_вриједност in Назив):
        raise ValueError('잘못된 пакет ПУТАЊА 문자')
    if инсталација_пут and (len(('/lib/' + Назив).encode()) > 63 or Назив in ('한국어.py', 'пакет.py')):
        raise ValueError('пакет ПУТАЊА 제한 또는 задана_вриједност библиотека 충돌: ' + Назив)
    return Назив


def 압축풀기(фајл_унос_име, подаци, Назив, верзија_вриједност):
    파일들 = {}
    명세들 = []
    def додати_унос(ПУТАЊА, Садржај_вриједност):
        потврдити_пут(ПУТАЊА)
        if ПУТАЊА in 파일들:
            raise ValueError('중복 пакет ПУТАЊА: ' + ПУТАЊА)
        if len(Садржај_вриједност) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ПУТАЊА)
        Садржај_вриједност.decode('utf-8')
        파일들[ПУТАЊА] = Садржај_вриједност
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 извор_стабло 16개·합계 64 KiB 이하여야 합니다.')
    if фајл_унос_име.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(подаци)) as пакет:
            항목들 = пакет.infolist()
            if len(항목들) > 256 or sum(унос_вриједност.file_size for унос_вриједност in 항목들) > 1048576:
                raise ValueError('Архива_вриједност издање_похрана Величина 제한 초과')
            случај_Листа = [унос_вриједност for унос_вриједност in 항목들 if унос_вриједност.filename.endswith('.dist-info/WHEEL')]
            if len(случај_Листа) != 1:
                raise ValueError('wheel случај_вриједност 명세가 필요합니다.')
            случај_вриједност = email.parser.Parser().parsestr(пакет.read(случај_Листа[0]).decode())
            if случај_вриједност.get('Root-Is-Purelib', '').lower() != 'true' or not фајл_унос_име.endswith('-none-any.whl'):
                raise ValueError('C проширење_вриједност·플랫폼 전용 wheel은 지원하지 않습니다.')
            for унос_вриједност in 항목들:
                ПУТАЊА = унос_вриједност.filename.rstrip('/')
                потврдити_пут(ПУТАЊА, False)
                if (унос_вриједност.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if унос_вриједност.filename.endswith('/'):
                    continue
                if '.dist-info/' in ПУТАЊА:
                    if ПУТАЊА.endswith('/METADATA'):
                        명세들.append(пакет.read(унос_вриједност).decode())
                    continue
                if not ПУТАЊА.endswith('.py') or '.data/' in ПУТАЊА:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ПУТАЊА)
                додати_унос(ПУТАЊА, пакет.read(унос_вриједност))
    elif фајл_унос_име.endswith('.tar.gz') and Назив.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Изврши_команда 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(подаци), mode='r|gz') as пакет:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for унос_вриједност in пакет:
                항목수 += 1
                전체크기 += унос_вриједност.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Архива_вриједност издање_похрана Величина 제한 초과')
                потврдити_пут(унос_вриједност.name, False)
                부분들 = унос_вриједност.name.split('/')
                뿌리들.add(부분들[0])
                if унос_вриједност.isdir():
                    continue
                if not унос_вриједност.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython извор_стабло 배포형')
                ПУТАЊА = '/'.join(부분들[1:])
                Садржај_вриједност = пакет.extractfile(унос_вриједност).read()
                if ПУТАЊА.endswith('PKG-INFO'):
                    명세들.append(Садржај_вриједност.decode())
                elif ПУТАЊА.endswith('.py') and ПУТАЊА not in ('setup.py',):
                    додати_унос(ПУТАЊА, Садржај_вриједност)
                elif '.egg-info/' not in ПУТАЊА and not ПУТАЊА.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ПУТАЊА)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 корен_вриједност 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* извор_стабло 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if рашчланити_захтев(명세.get('Name', ''))[0] != Назив or 명세.get('Version') != верзија_вриједност:
        raise ValueError('배포 메타데이터의 Назив·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(адреса, 한도):
    if not адреса.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(адреса, timeout=30) as одговор:
        if not одговор.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 адреса помаћи_вриједност')
        подаци = одговор.read(한도 + 1)
    if len(подаци) > 한도:
        raise ValueError('배포 Датотека Величина 제한 초과')
    return подаци


def пренос_пакет(Назив, верзија_вриједност, 파일들, 출처):
    명세 = {'name': Назив, 'version': верзија_вриједност, 'source': 출처, 'files': [
        {'path': ПУТАЊА, 'size': len(подаци), 'sha256': hashlib.sha256(подаци).hexdigest()}
        for ПУТАЊА, подаци in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('пакет 명세 Величина 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[унос_вриједност['path']] for унос_вриједност in 명세['files'])


class пакет_депо:
    def __init__(자신, ПУТАЊА, информатичко_одељење_Ван_мреже=False):
        자신.ПУТАЊА = Path(ПУТАЊА)
        자신.ПУТАЊА.mkdir(parents=True, exist_ok=True)
        자신.информатичко_одељење_Ван_мреже = информатичко_одељење_Ван_мреже

    def Припремити(자신, захтев):
        Назив, верзија_вриједност = рашчланити_захтев(захтев)
        열쇠 = Назив + ('==' + верзија_вриједност if верзија_вриједност else '')
        евиденција_пут = 자신.ПУТАЊА / (열쇠 + '.json')
        배포경로 = 자신.ПУТАЊА / (열쇠 + '.archive')
        if евиденција_пут.is_file() and 배포경로.is_file():
            евиденција_ред = json.loads(евиденција_пут.read_text())
            подаци = 배포경로.read_bytes()
            if hashlib.sha256(подаци).hexdigest() != евиденција_ред['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.информатичко_одељење_Ван_мреже:
                raise ValueError('информатичко_одељење_Ван_мреже 저장소에 없는 пакет: ' + захтев)
            адреса = 'https://pypi.org/pypi/' + Назив + ('/' + верзија_вриједност if верзија_вриједност else '') + '/json'
            Информације_о_систему = json.loads(웹읽기(адреса, 4194304).decode())
            if Информације_о_систему['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [унос_вриједност for унос_вриједност in Информације_о_систему['urls'] if not унос_вриједност.get('yanked') and унос_вриједност['filename'].endswith('-none-any.whl')]
            if not 후보 and Назив.startswith('micropython-'):
                후보 = [унос_вриједност for унос_вриједност in Информације_о_систему['urls'] if not унос_вриједност.get('yanked') and унос_вриједност['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            избор_вриједност = 후보[0]
            подаци = 웹읽기(избор_вриједност['url'], 4194304)
            if hashlib.sha256(подаци).hexdigest() != избор_вриједност['digests']['sha256']:
                raise ValueError('PyPI 배포 Датотека SHA-256 불일치')
            евиденција_ред = {'name': Назив, 'version': Информације_о_систему['info']['version'], 'filename': избор_вриједност['filename'],
                    'url': избор_вриједност['url'], 'sha256': избор_вриједност['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(евиденција_ред['filename'], подаци, Назив, евиденција_ред['version'])
            배포경로.write_bytes(подаци)
            евиденција_пут.write_text(json.dumps(евиденција_ред, ensure_ascii=False, indent=2) + '\n')
        if евиденција_ред['name'] != Назив or верзија_вриједност and евиденција_ред['version'] != верзија_вриједност:
            raise ValueError('депо_корен Назив·버전 불일치')
        파일들 = 압축풀기(евиденција_ред['filename'], подаци, Назив, евиденција_ред['version'])
        return пренос_пакет(Назив, евиденција_ред['version'], 파일들, евиденција_ред['url'])


class пакет_захтев(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            захтев = bytearray()
            while b'\n' not in захтев and len(захтев) < 100:
                조각 = 자신.request.recv(100 - len(захтев))
                if not 조각:
                    return
                захтев.extend(조각)
            if not захтев.endswith(b'\n') or захтев.count(b'\n') != 1:
                raise ValueError('잘못된 пакет захтев')
            одговор = 자신.server.депо_корен.Припремити(захтев[:-1].decode('ascii'))
        except Exception as ГРЕШКА:
            머리 = json.dumps({'error': str(ГРЕШКА)[:500]}, ensure_ascii=False).encode()
            одговор = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(одговор)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, број_порта=8027, ПУТАЊА=None, информатичко_одељење_Ван_мреже=False):
        자신.сервер_вриједност = socketserver.TCPServer(('127.0.0.1', број_порта), пакет_захтев, bind_and_activate=False)
        자신.сервер_вриједност.allow_reuse_address = True
        자신.сервер_вриједност.server_bind()
        자신.сервер_вриједност.server_activate()
        자신.сервер_вриједност.депо_корен = пакет_депо(ПУТАЊА or пројектовати_корен/'build/pip-cache', информатичко_одељење_Ван_мреже)
        자신.број_порта = 자신.сервер_вриједност.server_address[1]
        자신.нит_вриједност = threading.Thread(target=자신.сервер_вриједност.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.нит_вриједност.start()
        return 자신

    def __exit__(자신, *Аргументи):
        자신.сервер_вриједност.shutdown()
        자신.сервер_вриједност.server_close()
        자신.нит_вриједност.join(timeout=2)


def Покрени():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--port', type=int, default=8027)
    анализатор_48ee4b1b.add_argument('--cache', type=Path, default=пројектовати_корен/'build/pip-cache')
    анализатор_48ee4b1b.add_argument('--offline', action='store_true')
    анализатор_48ee4b1b.add_argument('--fetch', help='Изврши_команда 없이 호환 배포 파일을 내려받아 검사·похранити_вриједност')
    Аргументи = анализатор_48ee4b1b.parse_args()
    if Аргументи.fetch:
        подаци = пакет_депо(Аргументи.cache, Аргументи.offline).Припремити(Аргументи.fetch)
        print('пакет Припремити 완료:', Аргументи.fetch, len(подаци), 'бајт_вриједност')
        return
    with 꾸러미중계(Аргументи.port, Аргументи.cache, Аргументи.offline) as 중계:
        print('пакет 중계: 127.0.0.1:' + str(중계.број_порта), flush=True)
        try:
            중계.нит_вриједност.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Покрени()
