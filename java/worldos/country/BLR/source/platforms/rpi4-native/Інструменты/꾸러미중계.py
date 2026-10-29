#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 усталяваць_значэнне·실행한다."""
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
        raise ValueError('пакет Назва 또는 Назва==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def праверыць_шлях(Назва, усталяванне_шлях=True):
    ШЛЯХ = PurePosixPath(Назва)
    if ШЛЯХ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Назва.split('/')):
        raise ValueError('허용하지 않는 пакет ШЛЯХ: ' + Назва)
    if '\\' in Назва or any(ord(сімвал_значэнне_068c2631) < 32 or ord(сімвал_значэнне_068c2631) == 127 for сімвал_значэнне_068c2631 in Назва):
        raise ValueError('잘못된 пакет ШЛЯХ 문자')
    if усталяванне_шлях and (len(('/lib/' + Назва).encode()) > 63 or Назва in ('한국어.py', 'пакет.py')):
        raise ValueError('пакет ШЛЯХ 제한 또는 значэнне_па_змаўчанні бібліятэка 충돌: ' + Назва)
    return Назва


def 압축풀기(файл_увядзенне_імя, дадзеныя, Назва, версія_значэнне):
    파일들 = {}
    명세들 = []
    def 추가(ШЛЯХ, кантэнт_значэнне):
        праверыць_шлях(ШЛЯХ)
        if ШЛЯХ in 파일들:
            raise ValueError('중복 пакет ШЛЯХ: ' + ШЛЯХ)
        if len(кантэнт_значэнне) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ШЛЯХ)
        кантэнт_значэнне.decode('utf-8')
        파일들[ШЛЯХ] = кантэнт_значэнне
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 крыніца_дрэва 16개·합계 64 KiB 이하여야 합니다.')
    if файл_увядзенне_імя.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(дадзеныя)) as пакет:
            항목들 = пакет.infolist()
            if len(항목들) > 256 or sum(увядзенне_значэнне.file_size for увядзенне_значэнне in 항목들) > 1048576:
                raise ValueError('Архіў_значэнне выпуск_Сховішча Памер 제한 초과')
            зварот_Спіс = [увядзенне_значэнне for увядзенне_значэнне in 항목들 if увядзенне_значэнне.filename.endswith('.dist-info/WHEEL')]
            if len(зварот_Спіс) != 1:
                raise ValueError('wheel зварот_значэнне 명세가 필요합니다.')
            зварот_значэнне = email.parser.Parser().parsestr(пакет.read(зварот_Спіс[0]).decode())
            if зварот_значэнне.get('Root-Is-Purelib', '').lower() != 'true' or not файл_увядзенне_імя.endswith('-none-any.whl'):
                raise ValueError('C пашырэнне_значэнне·플랫폼 전용 wheel은 지원하지 않습니다.')
            for увядзенне_значэнне in 항목들:
                ШЛЯХ = увядзенне_значэнне.filename.rstrip('/')
                праверыць_шлях(ШЛЯХ, False)
                if (увядзенне_значэнне.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if увядзенне_значэнне.filename.endswith('/'):
                    continue
                if '.dist-info/' in ШЛЯХ:
                    if ШЛЯХ.endswith('/METADATA'):
                        명세들.append(пакет.read(увядзенне_значэнне).decode())
                    continue
                if not ШЛЯХ.endswith('.py') or '.data/' in ШЛЯХ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ШЛЯХ)
                추가(ШЛЯХ, пакет.read(увядзенне_значэнне))
    elif файл_увядзенне_імя.endswith('.tar.gz') and Назва.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py выканаць_каманда 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(дадзеныя), mode='r|gz') as пакет:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for увядзенне_значэнне in пакет:
                항목수 += 1
                전체크기 += увядзенне_значэнне.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Архіў_значэнне выпуск_Сховішча Памер 제한 초과')
                праверыць_шлях(увядзенне_значэнне.name, False)
                부분들 = увядзенне_значэнне.name.split('/')
                뿌리들.add(부분들[0])
                if увядзенне_значэнне.isdir():
                    continue
                if not увядзенне_значэнне.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython крыніца_дрэва 배포형')
                ШЛЯХ = '/'.join(부분들[1:])
                кантэнт_значэнне = пакет.extractfile(увядзенне_значэнне).read()
                if ШЛЯХ.endswith('PKG-INFO'):
                    명세들.append(кантэнт_значэнне.decode())
                elif ШЛЯХ.endswith('.py') and ШЛЯХ not in ('setup.py',):
                    추가(ШЛЯХ, кантэнт_значэнне)
                elif '.egg-info/' not in ШЛЯХ and not ШЛЯХ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ШЛЯХ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* крыніца_дрэва 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Назва or 명세.get('Version') != версія_значэнне:
        raise ValueError('배포 메타데이터의 Назва·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(адрас, 한도):
    if not адрас.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(адрас, timeout=30) as адказаць:
        if not адказаць.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 адрас перамясціць_значэнне')
        дадзеныя = адказаць.read(한도 + 1)
    if len(дадзеныя) > 한도:
        raise ValueError('배포 Файл Памер 제한 초과')
    return дадзеныя


def перанос_пакет(Назва, версія_значэнне, 파일들, 출처):
    명세 = {'name': Назва, 'version': версія_значэнне, 'source': 출처, 'files': [
        {'path': ШЛЯХ, 'size': len(дадзеныя), 'sha256': hashlib.sha256(дадзеныя).hexdigest()}
        for ШЛЯХ, дадзеныя in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('пакет 명세 Памер 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[увядзенне_значэнне['path']] for увядзенне_значэнне in 명세['files'])


class пакет_рэпазіторый:
    def __init__(자신, ШЛЯХ, аддзел_інфармацыйных_тэхналогій_не_ў_сетцы=False):
        자신.ШЛЯХ = Path(ШЛЯХ)
        자신.ШЛЯХ.mkdir(parents=True, exist_ok=True)
        자신.аддзел_інфармацыйных_тэхналогій_не_ў_сетцы = аддзел_інфармацыйных_тэхналогій_не_ў_сетцы

    def Падрыхтаваць(자신, 요청):
        Назва, версія_значэнне = 요청해석(요청)
        열쇠 = Назва + ('==' + версія_значэнне if версія_значэнне else '')
        журнал_шлях = 자신.ШЛЯХ / (열쇠 + '.json')
        배포경로 = 자신.ШЛЯХ / (열쇠 + '.archive')
        if журнал_шлях.is_file() and 배포경로.is_file():
            журнал_запіс = json.loads(журнал_шлях.read_text())
            дадзеныя = 배포경로.read_bytes()
            if hashlib.sha256(дадзеныя).hexdigest() != журнал_запіс['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.аддзел_інфармацыйных_тэхналогій_не_ў_сетцы:
                raise ValueError('аддзел_інфармацыйных_тэхналогій_не_ў_сетцы 저장소에 없는 пакет: ' + 요청)
            адрас = 'https://pypi.org/pypi/' + Назва + ('/' + версія_значэнне if версія_значэнне else '') + '/json'
            Сістэмная_інфармацыя = json.loads(웹읽기(адрас, 4194304).decode())
            if Сістэмная_інфармацыя['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [увядзенне_значэнне for увядзенне_значэнне in Сістэмная_інфармацыя['urls'] if not увядзенне_значэнне.get('yanked') and увядзенне_значэнне['filename'].endswith('-none-any.whl')]
            if not 후보 and Назва.startswith('micropython-'):
                후보 = [увядзенне_значэнне for увядзенне_значэнне in Сістэмная_інфармацыя['urls'] if not увядзенне_значэнне.get('yanked') and увядзенне_значэнне['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            вылучанае_значэнне = 후보[0]
            дадзеныя = 웹읽기(вылучанае_значэнне['url'], 4194304)
            if hashlib.sha256(дадзеныя).hexdigest() != вылучанае_значэнне['digests']['sha256']:
                raise ValueError('PyPI 배포 Файл SHA-256 불일치')
            журнал_запіс = {'name': Назва, 'version': Сістэмная_інфармацыя['info']['version'], 'filename': вылучанае_значэнне['filename'],
                    'url': вылучанае_значэнне['url'], 'sha256': вылучанае_значэнне['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(журнал_запіс['filename'], дадзеныя, Назва, журнал_запіс['version'])
            배포경로.write_bytes(дадзеныя)
            журнал_шлях.write_text(json.dumps(журнал_запіс, ensure_ascii=False, indent=2) + '\n')
        if журнал_запіс['name'] != Назва or версія_значэнне and журнал_запіс['version'] != версія_значэнне:
            raise ValueError('저장소 Назва·버전 불일치')
        파일들 = 압축풀기(журнал_запіс['filename'], дадзеныя, Назва, журнал_запіс['version'])
        return перанос_пакет(Назва, журнал_запіс['version'], 파일들, журнал_запіс['url'])


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
            адказаць = 자신.server.저장소.Падрыхтаваць(요청[:-1].decode('ascii'))
        except Exception as ПАМЫЛКА:
            머리 = json.dumps({'error': str(ПАМЫЛКА)[:500]}, ensure_ascii=False).encode()
            адказаць = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(адказаць)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, нумар_порта=8027, ШЛЯХ=None, аддзел_інфармацыйных_тэхналогій_не_ў_сетцы=False):
        자신.сервер_значэнне = socketserver.TCPServer(('127.0.0.1', нумар_порта), 꾸러미요청, bind_and_activate=False)
        자신.сервер_значэнне.allow_reuse_address = True
        자신.сервер_значэнне.server_bind()
        자신.сервер_значэнне.server_activate()
        자신.сервер_значэнне.저장소 = пакет_рэпазіторый(ШЛЯХ or 기준/'build/pip-cache', аддзел_інфармацыйных_тэхналогій_не_ў_сетцы)
        자신.нумар_порта = 자신.сервер_значэнне.server_address[1]
        자신.паток_значэнне_5b72a632 = threading.Thread(target=자신.сервер_значэнне.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.паток_значэнне_5b72a632.start()
        return 자신

    def __exit__(자신, *인수):
        자신.сервер_значэнне.shutdown()
        자신.сервер_значэнне.server_close()
        자신.паток_значэнне_5b72a632.join(timeout=2)


def Выканаць():
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('--port', type=int, default=8027)
    аналізатар_48ee4b1b.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    аналізатар_48ee4b1b.add_argument('--offline', action='store_true')
    аналізатар_48ee4b1b.add_argument('--fetch', help='выканаць_каманда 없이 호환 배포 파일을 내려받아 검사·сховішча_значэнне')
    인수 = аналізатар_48ee4b1b.parse_args()
    if 인수.fetch:
        дадзеныя = пакет_рэпазіторый(인수.cache, 인수.offline).Падрыхтаваць(인수.fetch)
        print('пакет Падрыхтаваць 완료:', 인수.fetch, len(дадзеныя), 'байт_значэнне')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('пакет 중계: 127.0.0.1:' + str(중계.нумар_порта), flush=True)
        try:
            중계.паток_значэнне_5b72a632.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Выканаць()
