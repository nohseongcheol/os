#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 урнаштыру_VALUE_6a28baa5·실행한다."""
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

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('пакет исем 또는 исем==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def тикшерү_юл(исем, урнаштыру_юл=True):
    Yul = PurePosixPath(исем)
    if Yul.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in исем.split('/')):
        raise ValueError('허용하지 않는 пакет Yul: ' + исем)
    if '\\' in исем or any(ord(символ_VALUE_068c2631) < 32 or ord(символ_VALUE_068c2631) == 127 for символ_VALUE_068c2631 in исем):
        raise ValueError('잘못된 пакет Yul 문자')
    if урнаштыру_юл and (len(('/lib/' + исем).encode()) > 63 or исем in ('Татарча.py', 'пакет.py')):
        raise ValueError('пакет Yul 제한 또는 килешенгәнчә_кыйммәт библиотека 충돌: ' + исем)
    return исем


def 압축풀기(файл_кертү_исем, мәгълүмат, исем, версия_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(Yul, Эчтәлек_VALUE):
        тикшерү_юл(Yul)
        if Yul in 파일들:
            raise ValueError('중복 пакет Yul: ' + Yul)
        if len(Эчтәлек_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Yul)
        Эчтәлек_VALUE.decode('utf-8')
        파일들[Yul] = Эчтәлек_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 чыганак_агач 16개·합계 64 KiB 이하여야 합니다.')
    if файл_кертү_исем.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(мәгълүмат)) as пакет:
            항목들 = пакет.infolist()
            if len(항목들) > 256 or sum(кертү_VALUE.file_size for кертү_VALUE in 항목들) > 1048576:
                raise ValueError('Архив_VALUE Чыгарылыш_Саклагыч үлчәмен_үзгәртү 제한 초과')
            бирем_Исемлек = [кертү_VALUE for кертү_VALUE in 항목들 if кертү_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(бирем_Исемлек) != 1:
                raise ValueError('wheel бирем_VALUE_102996da 명세가 필요합니다.')
            бирем_VALUE_102996da = email.parser.Parser().parsestr(пакет.read(бирем_Исемлек[0]).decode())
            if бирем_VALUE_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not файл_кертү_исем.endswith('-none-any.whl'):
                raise ValueError('C өстәмә_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for кертү_VALUE in 항목들:
                Yul = кертү_VALUE.filename.rstrip('/')
                тикшерү_юл(Yul, False)
                if (кертү_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if кертү_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in Yul:
                    if Yul.endswith('/METADATA'):
                        명세들.append(пакет.read(кертү_VALUE).decode())
                    continue
                if not Yul.endswith('.py') or '.data/' in Yul:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Yul)
                추가(Yul, пакет.read(кертү_VALUE))
    elif файл_кертү_исем.endswith('.tar.gz') and исем.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py үтәргә_команда 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(мәгълүмат), mode='r|gz') as пакет:
            뿌리들 = set()
            кертү_COUNT = 0
            전체크기 = 0
            for кертү_VALUE in пакет:
                кертү_COUNT += 1
                전체크기 += кертү_VALUE.size
                if кертү_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Архив_VALUE Чыгарылыш_Саклагыч үлчәмен_үзгәртү 제한 초과')
                тикшерү_юл(кертү_VALUE.name, False)
                부분들 = кертү_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if кертү_VALUE.isdir():
                    continue
                if not кертү_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython чыганак_агач 배포형')
                Yul = '/'.join(부분들[1:])
                Эчтәлек_VALUE = пакет.extractfile(кертү_VALUE).read()
                if Yul.endswith('PKG-INFO'):
                    명세들.append(Эчтәлек_VALUE.decode())
                elif Yul.endswith('.py') and Yul not in ('setup.py',):
                    추가(Yul, Эчтәлек_VALUE)
                elif '.egg-info/' not in Yul and not Yul.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Yul)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 тамыр_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* чыганак_агач 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != исем or 명세.get('Version') != версия_VALUE:
        raise ValueError('배포 메타데이터의 исем·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(адрес, 한도):
    if not адрес.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(адрес, timeout=30) as җавап_бирү:
        if not җавап_бирү.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 адрес күчерү_VALUE')
        мәгълүмат = җавап_бирү.read(한도 + 1)
    if len(мәгълүмат) > 한도:
        raise ValueError('배포 Birem үлчәмен_үзгәртү 제한 초과')
    return мәгълүмат


def күчерү_пакет(исем, версия_VALUE, 파일들, 출처):
    명세 = {'name': исем, 'version': версия_VALUE, 'source': 출처, 'files': [
        {'path': Yul, 'size': len(мәгълүмат), 'sha256': hashlib.sha256(мәгълүмат).hexdigest()}
        for Yul, мәгълүмат in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('пакет 명세 үлчәмен_үзгәртү 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[кертү_VALUE['path']] for кертү_VALUE in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, Yul, 오프라인=False):
        자신.Yul = Path(Yul)
        자신.Yul.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Әзерләү(자신, 요청):
        исем, версия_VALUE = 요청해석(요청)
        열쇠 = исем + ('==' + версия_VALUE if версия_VALUE else '')
        LOG_юл_5f8d12bf = 자신.Yul / (열쇠 + '.json')
        배포경로 = 자신.Yul / (열쇠 + '.archive')
        if LOG_юл_5f8d12bf.is_file() and 배포경로.is_file():
            LOG_юл = json.loads(LOG_юл_5f8d12bf.read_text())
            мәгълүмат = 배포경로.read_bytes()
            if hashlib.sha256(мәгълүмат).hexdigest() != LOG_юл['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 пакет: ' + 요청)
            адрес = 'https://pypi.org/pypi/' + исем + ('/' + версия_VALUE if версия_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(адрес, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [кертү_VALUE for кертү_VALUE in msinfo32_exe['urls'] if not кертү_VALUE.get('yanked') and кертү_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and исем.startswith('micropython-'):
                후보 = [кертү_VALUE for кертү_VALUE in msinfo32_exe['urls'] if not кертү_VALUE.get('yanked') and кертү_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            тамгаланган_өлеш_VALUE = 후보[0]
            мәгълүмат = 웹읽기(тамгаланган_өлеш_VALUE['url'], 4194304)
            if hashlib.sha256(мәгълүмат).hexdigest() != тамгаланган_өлеш_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Birem SHA-256 불일치')
            LOG_юл = {'name': исем, 'version': msinfo32_exe['info']['version'], 'filename': тамгаланган_өлеш_VALUE['filename'],
                    'url': тамгаланган_өлеш_VALUE['url'], 'sha256': тамгаланган_өлеш_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_юл['filename'], мәгълүмат, исем, LOG_юл['version'])
            배포경로.write_bytes(мәгълүмат)
            LOG_юл_5f8d12bf.write_text(json.dumps(LOG_юл, ensure_ascii=False, indent=2) + '\n')
        if LOG_юл['name'] != исем or версия_VALUE and LOG_юл['version'] != версия_VALUE:
            raise ValueError('저장소 исем·버전 불일치')
        파일들 = 압축풀기(LOG_юл['filename'], мәгълүмат, исем, LOG_юл['version'])
        return күчерү_пакет(исем, LOG_юл['version'], 파일들, LOG_юл['url'])


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
            җавап_бирү = 자신.server.저장소.Әзерләү(요청[:-1].decode('ascii'))
        except Exception as Хата:
            머리 = json.dumps({'error': str(Хата)[:500]}, ensure_ascii=False).encode()
            җавап_бирү = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(җавап_бирү)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, Yul=None, 오프라인=False):
        자신.сервер_VALUE = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.сервер_VALUE.allow_reuse_address = True
        자신.сервер_VALUE.server_bind()
        자신.сервер_VALUE.server_activate()
        자신.сервер_VALUE.저장소 = 꾸러미저장소(Yul or экранга_җибәрү_тамыр/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.сервер_VALUE.server_address[1]
        자신.агым_VALUE_5b72a632 = threading.Thread(target=자신.сервер_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.агым_VALUE_5b72a632.start()
        return 자신

    def __exit__(자신, *인수):
        자신.сервер_VALUE.shutdown()
        자신.сервер_VALUE.server_close()
        자신.агым_VALUE_5b72a632.join(timeout=2)


def эшләтү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=экранга_җибәрү_тамыр/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='үтәргә_команда 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        мәгълүмат = 꾸러미저장소(인수.cache, 인수.offline).Әзерләү(인수.fetch)
        print('пакет Әзерләү 완료:', 인수.fetch, len(мәгълүмат), 'байт_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('пакет 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.агым_VALUE_5b72a632.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    эшләтү()
