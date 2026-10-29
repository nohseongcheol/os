#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 інсталювати_значення·실행한다."""
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

Дії_корінь = Path(__file__).resolve().parents[1]


def аналізувати_запит(запит):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', запит)
    if not 맞음:
        raise ValueError('набір Назва 또는 Назва==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def затвердити_шлях(Назва, інсталяція_шлях=True):
    шлях = PurePosixPath(Назва)
    if шлях.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Назва.split('/')):
        raise ValueError('허용하지 않는 набір шлях: ' + Назва)
    if '\\' in Назва or any(ord(символ_значення_068c2631) < 32 or ord(символ_значення_068c2631) == 127 for символ_значення_068c2631 in Назва):
        raise ValueError('잘못된 набір шлях 문자')
    if інсталяція_шлях and (len(('/lib/' + Назва).encode()) > 63 or Назва in ('українська.py', 'набір.py')):
        raise ValueError('набір шлях 제한 또는 стандартне_значення бібліотека 충돌: ' + Назва)
    return Назва


def розпакувати(Файл_запис_ім_я, дані, Назва, версія_значення):
    파일들 = {}
    명세들 = []
    def додавати_запис(шлях, Вміст_значення):
        затвердити_шлях(шлях)
        if шлях in 파일들:
            raise ValueError('중복 набір шлях: ' + шлях)
        if len(Вміст_значення) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + шлях)
        Вміст_значення.decode('utf-8')
        파일들[шлях] = Вміст_значення
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 джерело_дерево 16개·усього_значення 64 KiB 이하여야 합니다.')
    if Файл_запис_ім_я.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(дані)) as набір:
            항목들 = набір.infolist()
            if len(항목들) > 256 or sum(запис_значення_962f286b.file_size for запис_значення_962f286b in 항목들) > 1048576:
                raise ValueError('Архів_значення випуск_місце Розмір 제한 초과')
            контракт_список = [запис_значення_962f286b for запис_значення_962f286b in 항목들 if запис_значення_962f286b.filename.endswith('.dist-info/WHEEL')]
            if len(контракт_список) != 1:
                raise ValueError('wheel контракт_значення 명세가 필요합니다.')
            контракт_значення = email.parser.Parser().parsestr(набір.read(контракт_список[0]).decode())
            if контракт_значення.get('Root-Is-Purelib', '').lower() != 'true' or not Файл_запис_ім_я.endswith('-none-any.whl'):
                raise ValueError('C розширення_значення·플랫폼 전용 wheel은 지원하지 않습니다.')
            for запис_значення_962f286b in 항목들:
                шлях = запис_значення_962f286b.filename.rstrip('/')
                затвердити_шлях(шлях, False)
                if (запис_значення_962f286b.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if запис_значення_962f286b.filename.endswith('/'):
                    continue
                if '.dist-info/' in шлях:
                    if шлях.endswith('/METADATA'):
                        명세들.append(набір.read(запис_значення_962f286b).decode())
                    continue
                if not шлях.endswith('.py') or '.data/' in шлях:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + шлях)
                додавати_запис(шлях, набір.read(запис_значення_962f286b))
    elif Файл_запис_ім_я.endswith('.tar.gz') and Назва.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Виконати_команда 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(дані), mode='r|gz') as набір:
            뿌리들 = set()
            항목수 = 0
            усього_змінювати_розмір = 0
            for запис_значення_962f286b in набір:
                항목수 += 1
                усього_змінювати_розмір += запис_значення_962f286b.size
                if 항목수 > 256 or усього_змінювати_розмір > 1048576:
                    raise ValueError('Архів_значення випуск_місце Розмір 제한 초과')
                затвердити_шлях(запис_значення_962f286b.name, False)
                부분들 = запис_значення_962f286b.name.split('/')
                뿌리들.add(부분들[0])
                if запис_значення_962f286b.isdir():
                    continue
                if not запис_значення_962f286b.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython джерело_дерево 배포형')
                шлях = '/'.join(부분들[1:])
                Вміст_значення = набір.extractfile(запис_значення_962f286b).read()
                if шлях.endswith('PKG-INFO'):
                    명세들.append(Вміст_значення.decode())
                elif шлях.endswith('.py') and шлях not in ('setup.py',):
                    додавати_запис(шлях, Вміст_значення)
                elif '.egg-info/' not in шлях and not шлях.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + шлях)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 корінь_значення 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* джерело_дерево 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if аналізувати_запит(명세.get('Name', ''))[0] != Назва or 명세.get('Version') != версія_значення:
        raise ValueError('배포 메타데이터의 Назва·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(Адреса, 한도):
    if not Адреса.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(Адреса, timeout=30) as відповідь:
        if not відповідь.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 Адреса переміщати_значення')
        дані = відповідь.read(한도 + 1)
    if len(дані) > 한도:
        raise ValueError('배포 файл Розмір 제한 초과')
    return дані


def передача_набір(Назва, версія_значення, 파일들, 출처):
    명세 = {'name': Назва, 'version': версія_значення, 'source': 출처, 'files': [
        {'path': шлях, 'size': len(дані), 'sha256': hashlib.sha256(дані).hexdigest()}
        for шлях, дані in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('набір 명세 Розмір 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[запис_значення_962f286b['path']] for запис_значення_962f286b in 명세['files'])


class набір_репозиторій:
    def __init__(자신, шлях, ІТ_відділ_Офлайн=False):
        자신.шлях = Path(шлях)
        자신.шлях.mkdir(parents=True, exist_ok=True)
        자신.ІТ_відділ_Офлайн = ІТ_відділ_Офлайн

    def Готувати(자신, запит):
        Назва, версія_значення = аналізувати_запит(запит)
        열쇠 = Назва + ('==' + версія_значення if версія_значення else '')
        журнал_шлях = 자신.шлях / (열쇠 + '.json')
        배포경로 = 자신.шлях / (열쇠 + '.archive')
        if журнал_шлях.is_file() and 배포경로.is_file():
            журнал_запис = json.loads(журнал_шлях.read_text())
            дані = 배포경로.read_bytes()
            if hashlib.sha256(дані).hexdigest() != журнал_запис['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.ІТ_відділ_Офлайн:
                raise ValueError('ІТ_відділ_Офлайн 저장소에 없는 набір: ' + запит)
            Адреса = 'https://pypi.org/pypi/' + Назва + ('/' + версія_значення if версія_значення else '') + '/json'
            Відомості_про_систему = json.loads(웹읽기(Адреса, 4194304).decode())
            if Відомості_про_систему['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            кандидат = [запис_значення_962f286b for запис_значення_962f286b in Відомості_про_систему['urls'] if not запис_значення_962f286b.get('yanked') and запис_значення_962f286b['filename'].endswith('-none-any.whl')]
            if not кандидат and Назва.startswith('micropython-'):
                кандидат = [запис_значення_962f286b for запис_значення_962f286b in Відомості_про_систему['urls'] if not запис_значення_962f286b.get('yanked') and запис_значення_962f286b['filename'].endswith('.tar.gz')]
            if not кандидат:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            вибране_значення = кандидат[0]
            дані = 웹읽기(вибране_значення['url'], 4194304)
            if hashlib.sha256(дані).hexdigest() != вибране_значення['digests']['sha256']:
                raise ValueError('PyPI 배포 файл SHA-256 불일치')
            журнал_запис = {'name': Назва, 'version': Відомості_про_систему['info']['version'], 'filename': вибране_значення['filename'],
                    'url': вибране_значення['url'], 'sha256': вибране_значення['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            розпакувати(журнал_запис['filename'], дані, Назва, журнал_запис['version'])
            배포경로.write_bytes(дані)
            журнал_шлях.write_text(json.dumps(журнал_запис, ensure_ascii=False, indent=2) + '\n')
        if журнал_запис['name'] != Назва or версія_значення and журнал_запис['version'] != версія_значення:
            raise ValueError('репозиторій_корінь Назва·버전 불일치')
        파일들 = розпакувати(журнал_запис['filename'], дані, Назва, журнал_запис['version'])
        return передача_набір(Назва, журнал_запис['version'], 파일들, журнал_запис['url'])


class набір_запит(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            запит = bytearray()
            while b'\n' not in запит and len(запит) < 100:
                조각 = 자신.request.recv(100 - len(запит))
                if not 조각:
                    return
                запит.extend(조각)
            if not запит.endswith(b'\n') or запит.count(b'\n') != 1:
                raise ValueError('잘못된 набір запит')
            відповідь = 자신.server.репозиторій_корінь.Готувати(запит[:-1].decode('ascii'))
        except Exception as ПОМИЛКА:
            머리 = json.dumps({'error': str(ПОМИЛКА)[:500]}, ensure_ascii=False).encode()
            відповідь = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(відповідь)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, номер_порту=8027, шлях=None, ІТ_відділ_Офлайн=False):
        자신.сервер_значення = socketserver.TCPServer(('127.0.0.1', номер_порту), набір_запит, bind_and_activate=False)
        자신.сервер_значення.allow_reuse_address = True
        자신.сервер_значення.server_bind()
        자신.сервер_значення.server_activate()
        자신.сервер_значення.репозиторій_корінь = набір_репозиторій(шлях or Дії_корінь/'build/pip-cache', ІТ_відділ_Офлайн)
        자신.номер_порту = 자신.сервер_значення.server_address[1]
        자신.потік_значення_5b72a632 = threading.Thread(target=자신.сервер_значення.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.потік_значення_5b72a632.start()
        return 자신

    def __exit__(자신, *аргументи):
        자신.сервер_значення.shutdown()
        자신.сервер_значення.server_close()
        자신.потік_значення_5b72a632.join(timeout=2)


def запустити():
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('--port', type=int, default=8027)
    аналізатор_48ee4b1b.add_argument('--cache', type=Path, default=Дії_корінь/'build/pip-cache')
    аналізатор_48ee4b1b.add_argument('--offline', action='store_true')
    аналізатор_48ee4b1b.add_argument('--fetch', help='Виконати_команда 없이 호환 배포 파일을 내려받아 검사·сховище_значення')
    аргументи = аналізатор_48ee4b1b.parse_args()
    if аргументи.fetch:
        дані = набір_репозиторій(аргументи.cache, аргументи.offline).Готувати(аргументи.fetch)
        print('набір Готувати 완료:', аргументи.fetch, len(дані), 'байт_значення')
        return
    with 꾸러미중계(аргументи.port, аргументи.cache, аргументи.offline) as 중계:
        print('набір 중계: 127.0.0.1:' + str(중계.номер_порту), flush=True)
        try:
            중계.потік_значення_5b72a632.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    запустити()
