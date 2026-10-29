#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 инсталирам_стойност·실행한다."""
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

проект_корен = Path(__file__).resolve().parents[1]


def анализирам_искане(искане):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', искане)
    if not 맞음:
        raise ValueError('пакет Име 또는 Име==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def проверка_път_f98b46e1(Име, инсталиране_път=True):
    ПЪТ = PurePosixPath(Име)
    if ПЪТ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Име.split('/')):
        raise ValueError('허용하지 않는 пакет ПЪТ: ' + Име)
    if '\\' in Име or any(ord(знак_стойност) < 32 or ord(знак_стойност) == 127 for знак_стойност in Име):
        raise ValueError('잘못된 пакет ПЪТ 문자')
    if инсталиране_път and (len(('/lib/' + Име).encode()) > 63 or Име in ('Български.py', 'пакет.py')):
        raise ValueError('пакет ПЪТ 제한 또는 стойност_по_подразбиране библиотека 충돌: ' + Име)
    return Име


def декомпресирам(Файл_запис_препратка_към_клетка, данни, Име, версия_стойност):
    파일들 = {}
    명세들 = []
    def добавям_запис(ПЪТ, Съдържание_стойност):
        проверка_път_f98b46e1(ПЪТ)
        if ПЪТ in 파일들:
            raise ValueError('중복 пакет ПЪТ: ' + ПЪТ)
        if len(Съдържание_стойност) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ПЪТ)
        Съдържание_стойност.decode('utf-8')
        파일들[ПЪТ] = Съдържание_стойност
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 източник_дърво 16개·общо_стойност 64 KiB 이하여야 합니다.')
    if Файл_запис_препратка_към_клетка.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(данни)) as пакет:
            항목들 = пакет.infolist()
            if len(항목들) > 256 or sum(запис_стойност.file_size for запис_стойност in 항목들) > 1048576:
                raise ValueError('Архив_стойност издание_Памет Размер 제한 초과')
            случай_Списък = [запис_стойност for запис_стойност in 항목들 if запис_стойност.filename.endswith('.dist-info/WHEEL')]
            if len(случай_Списък) != 1:
                raise ValueError('wheel случай_стойност 명세가 필요합니다.')
            случай_стойност = email.parser.Parser().parsestr(пакет.read(случай_Списък[0]).decode())
            if случай_стойност.get('Root-Is-Purelib', '').lower() != 'true' or not Файл_запис_препратка_към_клетка.endswith('-none-any.whl'):
                raise ValueError('C разширение_стойност·플랫폼 전용 wheel은 지원하지 않습니다.')
            for запис_стойност in 항목들:
                ПЪТ = запис_стойност.filename.rstrip('/')
                проверка_път_f98b46e1(ПЪТ, False)
                if (запис_стойност.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if запис_стойност.filename.endswith('/'):
                    continue
                if '.dist-info/' in ПЪТ:
                    if ПЪТ.endswith('/METADATA'):
                        명세들.append(пакет.read(запис_стойност).decode())
                    continue
                if not ПЪТ.endswith('.py') or '.data/' in ПЪТ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ПЪТ)
                добавям_запис(ПЪТ, пакет.read(запис_стойност))
    elif Файл_запис_препратка_към_клетка.endswith('.tar.gz') and Име.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py изпълнявам_команда 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(данни), mode='r|gz') as пакет:
            뿌리들 = set()
            항목수 = 0
            общо_размер = 0
            for запис_стойност in пакет:
                항목수 += 1
                общо_размер += запис_стойност.size
                if 항목수 > 256 or общо_размер > 1048576:
                    raise ValueError('Архив_стойност издание_Памет Размер 제한 초과')
                проверка_път_f98b46e1(запис_стойност.name, False)
                부분들 = запис_стойност.name.split('/')
                뿌리들.add(부분들[0])
                if запис_стойност.isdir():
                    continue
                if not запис_стойност.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython източник_дърво 배포형')
                ПЪТ = '/'.join(부분들[1:])
                Съдържание_стойност = пакет.extractfile(запис_стойност).read()
                if ПЪТ.endswith('PKG-INFO'):
                    명세들.append(Съдържание_стойност.decode())
                elif ПЪТ.endswith('.py') and ПЪТ not in ('setup.py',):
                    добавям_запис(ПЪТ, Съдържание_стойност)
                elif '.egg-info/' not in ПЪТ and not ПЪТ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ПЪТ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 корен_стойност 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* източник_дърво 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if анализирам_искане(명세.get('Name', ''))[0] != Име or 명세.get('Version') != версия_стойност:
        raise ValueError('배포 메타데이터의 Име·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(адрес, 한도):
    if not адрес.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(адрес, timeout=30) as отговор:
        if not отговор.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 адрес движа_се_стойност')
        данни = отговор.read(한도 + 1)
    if len(данни) > 한도:
        raise ValueError('배포 Файл Размер 제한 초과')
    return данни


def прехвърлям_пакет(Име, версия_стойност, 파일들, 출처):
    명세 = {'name': Име, 'version': версия_стойност, 'source': 출처, 'files': [
        {'path': ПЪТ, 'size': len(данни), 'sha256': hashlib.sha256(данни).hexdigest()}
        for ПЪТ, данни in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('пакет 명세 Размер 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[запис_стойност['path']] for запис_стойност in 명세['files'])


class пакет_хранилище:
    def __init__(자신, ПЪТ, информационни_технологии_Офлайн=False):
        자신.ПЪТ = Path(ПЪТ)
        자신.ПЪТ.mkdir(parents=True, exist_ok=True)
        자신.информационни_технологии_Офлайн = информационни_технологии_Офлайн

    def Подготвяне(자신, искане):
        Име, версия_стойност = анализирам_искане(искане)
        열쇠 = Име + ('==' + версия_стойност if версия_стойност else '')
        регистрирам_път = 자신.ПЪТ / (열쇠 + '.json')
        배포경로 = 자신.ПЪТ / (열쇠 + '.archive')
        if регистрирам_път.is_file() and 배포경로.is_file():
            регистрирам_запис = json.loads(регистрирам_път.read_text())
            данни = 배포경로.read_bytes()
            if hashlib.sha256(данни).hexdigest() != регистрирам_запис['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.информационни_технологии_Офлайн:
                raise ValueError('информационни_технологии_Офлайн 저장소에 없는 пакет: ' + искане)
            адрес = 'https://pypi.org/pypi/' + Име + ('/' + версия_стойност if версия_стойност else '') + '/json'
            Системна_информация = json.loads(웹읽기(адрес, 4194304).decode())
            if Системна_информация['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [запис_стойност for запис_стойност in Системна_информация['urls'] if not запис_стойност.get('yanked') and запис_стойност['filename'].endswith('-none-any.whl')]
            if not 후보 and Име.startswith('micropython-'):
                후보 = [запис_стойност for запис_стойност in Системна_информация['urls'] if not запис_стойност.get('yanked') and запис_стойност['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            избор_стойност = 후보[0]
            данни = 웹읽기(избор_стойност['url'], 4194304)
            if hashlib.sha256(данни).hexdigest() != избор_стойност['digests']['sha256']:
                raise ValueError('PyPI 배포 Файл SHA-256 불일치')
            регистрирам_запис = {'name': Име, 'version': Системна_информация['info']['version'], 'filename': избор_стойност['filename'],
                    'url': избор_стойност['url'], 'sha256': избор_стойност['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            декомпресирам(регистрирам_запис['filename'], данни, Име, регистрирам_запис['version'])
            배포경로.write_bytes(данни)
            регистрирам_път.write_text(json.dumps(регистрирам_запис, ensure_ascii=False, indent=2) + '\n')
        if регистрирам_запис['name'] != Име or версия_стойност and регистрирам_запис['version'] != версия_стойност:
            raise ValueError('хранилище_корен Име·버전 불일치')
        파일들 = декомпресирам(регистрирам_запис['filename'], данни, Име, регистрирам_запис['version'])
        return прехвърлям_пакет(Име, регистрирам_запис['version'], 파일들, регистрирам_запис['url'])


class пакет_искане(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            искане = bytearray()
            while b'\n' not in искане and len(искане) < 100:
                조각 = 자신.request.recv(100 - len(искане))
                if not 조각:
                    return
                искане.extend(조각)
            if not искане.endswith(b'\n') or искане.count(b'\n') != 1:
                raise ValueError('잘못된 пакет искане')
            отговор = 자신.server.хранилище_корен.Подготвяне(искане[:-1].decode('ascii'))
        except Exception as ГРЕШКА:
            머리 = json.dumps({'error': str(ГРЕШКА)[:500]}, ensure_ascii=False).encode()
            отговор = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(отговор)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, номер_на_порт=8027, ПЪТ=None, информационни_технологии_Офлайн=False):
        자신.сървър_стойност = socketserver.TCPServer(('127.0.0.1', номер_на_порт), пакет_искане, bind_and_activate=False)
        자신.сървър_стойност.allow_reuse_address = True
        자신.сървър_стойност.server_bind()
        자신.сървър_стойност.server_activate()
        자신.сървър_стойност.хранилище_корен = пакет_хранилище(ПЪТ or проект_корен/'build/pip-cache', информационни_технологии_Офлайн)
        자신.номер_на_порт = 자신.сървър_стойност.server_address[1]
        자신.нишка_стойност = threading.Thread(target=자신.сървър_стойност.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.нишка_стойност.start()
        return 자신

    def __exit__(자신, *Параметри):
        자신.сървър_стойност.shutdown()
        자신.сървър_стойност.server_close()
        자신.нишка_стойност.join(timeout=2)


def Стартиране():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--port', type=int, default=8027)
    анализатор_48ee4b1b.add_argument('--cache', type=Path, default=проект_корен/'build/pip-cache')
    анализатор_48ee4b1b.add_argument('--offline', action='store_true')
    анализатор_48ee4b1b.add_argument('--fetch', help='изпълнявам_команда 없이 호환 배포 파일을 내려받아 검사·хранилище_стойност')
    Параметри = анализатор_48ee4b1b.parse_args()
    if Параметри.fetch:
        данни = пакет_хранилище(Параметри.cache, Параметри.offline).Подготвяне(Параметри.fetch)
        print('пакет Подготвяне 완료:', Параметри.fetch, len(данни), 'байт_стойност')
        return
    with 꾸러미중계(Параметри.port, Параметри.cache, Параметри.offline) as 중계:
        print('пакет 중계: 127.0.0.1:' + str(중계.номер_на_порт), flush=True)
        try:
            중계.нишка_стойност.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Стартиране()
