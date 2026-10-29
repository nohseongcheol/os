#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost Ретрансляция_ЗНАЧЕН. 게스트는 TCP로 받은 소스를 직접 установить_ЗНАЧЕН·실행한다."""
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

задача_корень = Path(__file__).resolve().parents[1]


def анализировать_запрос(запрос):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', запрос)
    if not 맞음:
        raise ValueError('пакет Название 또는 Название==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def проверить_путь(Название, установка_путь=True):
    путь = PurePosixPath(Название)
    if путь.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Название.split('/')):
        raise ValueError('허용하지 않는 пакет путь: ' + Название)
    if '\\' in Название or any(ord(знак_ЗНАЧЕН) < 32 or ord(знак_ЗНАЧЕН) == 127 for знак_ЗНАЧЕН in Название):
        raise ValueError('잘못된 пакет путь 문자')
    if установка_путь and (len(('/lib/' + Название).encode()) > 63 or Название in ('русский.py', 'пакет.py')):
        raise ValueError('пакет путь 제한 또는 значение_по_умолчанию библиотека 충돌: ' + Название)
    return Название


def распаковать(файл_ввод_имя, данные, Название, версия_ЗНАЧЕН_65c6ecdc):
    파일들 = {}
    명세들 = []
    def добавить_ввод(путь, контент_ЗНАЧЕН):
        проверить_путь(путь)
        if путь in 파일들:
            raise ValueError('중복 пакет путь: ' + путь)
        if len(контент_ЗНАЧЕН) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + путь)
        контент_ЗНАЧЕН.decode('utf-8')
        파일들[путь] = контент_ЗНАЧЕН
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 источник_дерево 16개·итог_ЗНАЧЕН 64 KiB 이하여야 합니다.')
    if файл_ввод_имя.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(данные)) as пакет:
            항목들 = пакет.infolist()
            if len(항목들) > 256 or sum(ввод_ЗНАЧЕН.file_size for ввод_ЗНАЧЕН in 항목들) > 1048576:
                raise ValueError('Архив_ЗНАЧЕН выпуск_Память_293182ec Размер 제한 초과')
            задание_Список = [ввод_ЗНАЧЕН for ввод_ЗНАЧЕН in 항목들 if ввод_ЗНАЧЕН.filename.endswith('.dist-info/WHEEL')]
            if len(задание_Список) != 1:
                raise ValueError('wheel сумма_контракта 명세가 필요합니다.')
            сумма_контракта = email.parser.Parser().parsestr(пакет.read(задание_Список[0]).decode())
            if сумма_контракта.get('Root-Is-Purelib', '').lower() != 'true' or not файл_ввод_имя.endswith('-none-any.whl'):
                raise ValueError('C расширение_ЗНАЧЕН·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ввод_ЗНАЧЕН in 항목들:
                путь = ввод_ЗНАЧЕН.filename.rstrip('/')
                проверить_путь(путь, False)
                if (ввод_ЗНАЧЕН.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ввод_ЗНАЧЕН.filename.endswith('/'):
                    continue
                if '.dist-info/' in путь:
                    if путь.endswith('/METADATA'):
                        명세들.append(пакет.read(ввод_ЗНАЧЕН).decode())
                    continue
                if not путь.endswith('.py') or '.data/' in путь:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + путь)
                добавить_ввод(путь, пакет.read(ввод_ЗНАЧЕН))
    elif файл_ввод_имя.endswith('.tar.gz') and Название.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py 실행 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(данные), mode='r|gz') as пакет:
            뿌리들 = set()
            ввод_СЧЁТ = 0
            итог_изменить_размер = 0
            for ввод_ЗНАЧЕН in пакет:
                ввод_СЧЁТ += 1
                итог_изменить_размер += ввод_ЗНАЧЕН.size
                if ввод_СЧЁТ > 256 or итог_изменить_размер > 1048576:
                    raise ValueError('Архив_ЗНАЧЕН выпуск_Память_293182ec Размер 제한 초과')
                проверить_путь(ввод_ЗНАЧЕН.name, False)
                부분들 = ввод_ЗНАЧЕН.name.split('/')
                뿌리들.add(부분들[0])
                if ввод_ЗНАЧЕН.isdir():
                    continue
                if not ввод_ЗНАЧЕН.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython источник_дерево 배포형')
                путь = '/'.join(부분들[1:])
                контент_ЗНАЧЕН = пакет.extractfile(ввод_ЗНАЧЕН).read()
                if путь.endswith('PKG-INFO'):
                    명세들.append(контент_ЗНАЧЕН.decode())
                elif путь.endswith('.py') and путь not in ('setup.py',):
                    добавить_ввод(путь, контент_ЗНАЧЕН)
                elif '.egg-info/' not in путь and not путь.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + путь)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 корень_ЗНАЧЕН 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* источник_дерево 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 распределение_ЗНАЧЕН 메타데이터가 필요합니다.')
    спецификация = email.parser.Parser().parsestr(명세들[0])
    if анализировать_запрос(спецификация.get('Name', ''))[0] != Название or спецификация.get('Version') != версия_ЗНАЧЕН_65c6ecdc:
        raise ValueError('распределение_ЗНАЧЕН 메타데이터의 Название·버전 불일치')
    if спецификация.get_all('Requires-Dist') or спецификация.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def чтение_веб(АДРЕС, 한도):
    if not АДРЕС.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS распределение_ЗНАЧЕН 주소만 허용합니다.')
    with urllib.request.urlopen(АДРЕС, timeout=30) as ответ:
        if not ответ.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 распределение_ЗНАЧЕН АДРЕС переместить_ЗНАЧЕН')
        данные = ответ.read(한도 + 1)
    if len(данные) > 한도:
        raise ValueError('распределение_ЗНАЧЕН файл Размер 제한 초과')
    return данные


def передать_пакет(Название, версия_ЗНАЧЕН_65c6ecdc, 파일들, origin_ЗНАЧЕН):
    спецификация = {'name': Название, 'version': версия_ЗНАЧЕН_65c6ecdc, 'source': origin_ЗНАЧЕН, 'files': [
        {'path': путь, 'size': len(данные), 'sha256': hashlib.sha256(данные).hexdigest()}
        for путь, данные in sorted(파일들.items())]}
    HEAD_ЗНАЧЕН = json.dumps(спецификация, ensure_ascii=False).encode()
    if len(HEAD_ЗНАЧЕН) > 8192:
        raise ValueError('пакет спецификация Размер 초과')
    return b'JKP1' + struct.pack('>I', len(HEAD_ЗНАЧЕН)) + HEAD_ЗНАЧЕН + b''.join(파일들[ввод_ЗНАЧЕН['path']] for ввод_ЗНАЧЕН in спецификация['files'])


class пакет_репозиторий:
    def __init__(자신, путь, ИТ_службы_вне_сети=False):
        자신.путь = Path(путь)
        자신.путь.mkdir(parents=True, exist_ok=True)
        자신.ИТ_службы_вне_сети = ИТ_службы_вне_сети

    def Подготовить(자신, запрос):
        Название, версия_ЗНАЧЕН_65c6ecdc = анализировать_запрос(запрос)
        Ключ_материал = Название + ('==' + версия_ЗНАЧЕН_65c6ecdc if версия_ЗНАЧЕН_65c6ecdc else '')
        LOG_путь = 자신.путь / (Ключ_материал + '.json')
        распределение_путь = 자신.путь / (Ключ_материал + '.archive')
        if LOG_путь.is_file() and распределение_путь.is_file():
            LOG_ЗАПИСЬ = json.loads(LOG_путь.read_text())
            данные = распределение_путь.read_bytes()
            if hashlib.sha256(данные).hexdigest() != LOG_ЗАПИСЬ['sha256']:
                raise ValueError('저장된 распределение_ЗНАЧЕН 파일의 SHA-256 불일치')
        else:
            if 자신.ИТ_службы_вне_сети:
                raise ValueError('ИТ_службы_вне_сети 저장소에 없는 пакет: ' + запрос)
            АДРЕС = 'https://pypi.org/pypi/' + Название + ('/' + версия_ЗНАЧЕН_65c6ecdc if версия_ЗНАЧЕН_65c6ecdc else '') + '/json'
            msinfo32_exe = json.loads(чтение_веб(АДРЕС, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            соискатель = [ввод_ЗНАЧЕН for ввод_ЗНАЧЕН in msinfo32_exe['urls'] if not ввод_ЗНАЧЕН.get('yanked') and ввод_ЗНАЧЕН['filename'].endswith('-none-any.whl')]
            if not соискатель and Название.startswith('micropython-'):
                соискатель = [ввод_ЗНАЧЕН for ввод_ЗНАЧЕН in msinfo32_exe['urls'] if not ввод_ЗНАЧЕН.get('yanked') and ввод_ЗНАЧЕН['filename'].endswith('.tar.gz')]
            if not соискатель:
                raise ValueError('지원되는 순수 Python распределение_ЗНАЧЕН 파일이 없습니다.')
            выделение_ЗНАЧЕН = соискатель[0]
            данные = чтение_веб(выделение_ЗНАЧЕН['url'], 4194304)
            if hashlib.sha256(данные).hexdigest() != выделение_ЗНАЧЕН['digests']['sha256']:
                raise ValueError('PyPI распределение_ЗНАЧЕН файл SHA-256 불일치')
            LOG_ЗАПИСЬ = {'name': Название, 'version': msinfo32_exe['info']['version'], 'filename': выделение_ЗНАЧЕН['filename'],
                    'url': выделение_ЗНАЧЕН['url'], 'sha256': выделение_ЗНАЧЕН['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            распаковать(LOG_ЗАПИСЬ['filename'], данные, Название, LOG_ЗАПИСЬ['version'])
            распределение_путь.write_bytes(данные)
            LOG_путь.write_text(json.dumps(LOG_ЗАПИСЬ, ensure_ascii=False, indent=2) + '\n')
        if LOG_ЗАПИСЬ['name'] != Название or версия_ЗНАЧЕН_65c6ecdc and LOG_ЗАПИСЬ['version'] != версия_ЗНАЧЕН_65c6ecdc:
            raise ValueError('корень_репозитория Название·버전 불일치')
        파일들 = распаковать(LOG_ЗАПИСЬ['filename'], данные, Название, LOG_ЗАПИСЬ['version'])
        return передать_пакет(Название, LOG_ЗАПИСЬ['version'], 파일들, LOG_ЗАПИСЬ['url'])


class пакет_запрос(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            запрос = bytearray()
            while b'\n' not in запрос and len(запрос) < 100:
                блок_ЗНАЧЕН_652d4b53 = 자신.request.recv(100 - len(запрос))
                if not блок_ЗНАЧЕН_652d4b53:
                    return
                запрос.extend(блок_ЗНАЧЕН_652d4b53)
            if not запрос.endswith(b'\n') or запрос.count(b'\n') != 1:
                raise ValueError('잘못된 пакет запрос')
            ответ = 자신.server.корень_репозитория.Подготовить(запрос[:-1].decode('ascii'))
        except Exception as ошибка:
            HEAD_ЗНАЧЕН = json.dumps({'error': str(ошибка)[:500]}, ensure_ascii=False).encode()
            ответ = b'JKP1' + struct.pack('>I', len(HEAD_ЗНАЧЕН)) + HEAD_ЗНАЧЕН
        try:
            자신.request.sendall(ответ)
        except OSError:
            pass


class пакет_Ретрансляция:
    def __init__(자신, номер_порта=8027, путь=None, ИТ_службы_вне_сети=False):
        자신.сервер_ЗНАЧЕН = socketserver.TCPServer(('127.0.0.1', номер_порта), пакет_запрос, bind_and_activate=False)
        자신.сервер_ЗНАЧЕН.allow_reuse_address = True
        자신.сервер_ЗНАЧЕН.server_bind()
        자신.сервер_ЗНАЧЕН.server_activate()
        자신.сервер_ЗНАЧЕН.корень_репозитория = пакет_репозиторий(путь or задача_корень/'build/pip-cache', ИТ_службы_вне_сети)
        자신.номер_порта = 자신.сервер_ЗНАЧЕН.server_address[1]
        자신.поток_ЗНАЧЕН_5b72a632 = threading.Thread(target=자신.сервер_ЗНАЧЕН.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.поток_ЗНАЧЕН_5b72a632.start()
        return 자신

    def __exit__(자신, *аргументы):
        자신.сервер_ЗНАЧЕН.shutdown()
        자신.сервер_ЗНАЧЕН.server_close()
        자신.поток_ЗНАЧЕН_5b72a632.join(timeout=2)


def запустить():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--port', type=int, default=8027)
    анализатор_48ee4b1b.add_argument('--cache', type=Path, default=задача_корень/'build/pip-cache')
    анализатор_48ee4b1b.add_argument('--offline', action='store_true')
    анализатор_48ee4b1b.add_argument('--fetch', help='실행 없이 호환 распределение_ЗНАЧЕН 파일을 내려받아 검사·Store_ЗНАЧЕН')
    аргументы = анализатор_48ee4b1b.parse_args()
    if аргументы.fetch:
        данные = пакет_репозиторий(аргументы.cache, аргументы.offline).Подготовить(аргументы.fetch)
        print('пакет Подготовить 완료:', аргументы.fetch, len(данные), 'байт_ЗНАЧЕН')
        return
    with пакет_Ретрансляция(аргументы.port, аргументы.cache, аргументы.offline) as Ретрансляция_ЗНАЧЕН:
        print('пакет Ретрансляция_ЗНАЧЕН: 127.0.0.1:' + str(Ретрансляция_ЗНАЧЕН.номер_порта), flush=True)
        try:
            Ретрансляция_ЗНАЧЕН.поток_ЗНАЧЕН_5b72a632.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    запустить()
