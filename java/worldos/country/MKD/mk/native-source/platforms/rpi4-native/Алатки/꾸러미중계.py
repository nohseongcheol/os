#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 инсталирај_VALUE·실행한다."""
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

Project_корен = Path(__file__).resolve().parents[1]


def разложи_Барање_на_HTTP(Барање_на_HTTP):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', Барање_на_HTTP)
    if not 맞음:
        raise ValueError('пакет Име 또는 Име==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def потврди_патека(Име, инсталација_патека=True):
    ПАТЕКА = PurePosixPath(Име)
    if ПАТЕКА.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Име.split('/')):
        raise ValueError('허용하지 않는 пакет ПАТЕКА: ' + Име)
    if '\\' in Име or any(ord(знак_VALUE) < 32 or ord(знак_VALUE) == 127 for знак_VALUE in Име):
        raise ValueError('잘못된 пакет ПАТЕКА 문자')
    if инсталација_патека and (len(('/lib/' + Име).encode()) > 63 or Име in ('Македонски.py', 'пакет.py')):
        raise ValueError('пакет ПАТЕКА 제한 또는 стандардна_вредност библиотека 충돌: ' + Име)
    return Име


def 압축풀기(датотека_внес_име, податоци, Име, верзија_VALUE):
    파일들 = {}
    명세들 = []
    def 추가(ПАТЕКА, Содржина_VALUE):
        потврди_патека(ПАТЕКА)
        if ПАТЕКА in 파일들:
            raise ValueError('중복 пакет ПАТЕКА: ' + ПАТЕКА)
        if len(Содржина_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ПАТЕКА)
        Содржина_VALUE.decode('utf-8')
        파일들[ПАТЕКА] = Содржина_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 извор_дрво 16개·합계 64 KiB 이하여야 합니다.')
    if датотека_внес_име.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(податоци)) as пакет:
            항목들 = пакет.infolist()
            if len(항목들) > 256 or sum(внес_VALUE.file_size for внес_VALUE in 항목들) > 1048576:
                raise ValueError('Архива_VALUE издание_Склад Големина 제한 초과')
            задача_Список = [внес_VALUE for внес_VALUE in 항목들 if внес_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(задача_Список) != 1:
                raise ValueError('wheel задача_VALUE_102996da 명세가 필요합니다.')
            задача_VALUE_102996da = email.parser.Parser().parsestr(пакет.read(задача_Список[0]).decode())
            if задача_VALUE_102996da.get('Root-Is-Purelib', '').lower() != 'true' or not датотека_внес_име.endswith('-none-any.whl'):
                raise ValueError('C наставка_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for внес_VALUE in 항목들:
                ПАТЕКА = внес_VALUE.filename.rstrip('/')
                потврди_патека(ПАТЕКА, False)
                if (внес_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if внес_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in ПАТЕКА:
                    if ПАТЕКА.endswith('/METADATA'):
                        명세들.append(пакет.read(внес_VALUE).decode())
                    continue
                if not ПАТЕКА.endswith('.py') or '.data/' in ПАТЕКА:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ПАТЕКА)
                추가(ПАТЕКА, пакет.read(внес_VALUE))
    elif датотека_внес_име.endswith('.tar.gz') and Име.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Изврши_наредба 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(податоци), mode='r|gz') as пакет:
            뿌리들 = set()
            внес_COUNT = 0
            전체크기 = 0
            for внес_VALUE in пакет:
                внес_COUNT += 1
                전체크기 += внес_VALUE.size
                if внес_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Архива_VALUE издание_Склад Големина 제한 초과')
                потврди_патека(внес_VALUE.name, False)
                부분들 = внес_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if внес_VALUE.isdir():
                    continue
                if not внес_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython извор_дрво 배포형')
                ПАТЕКА = '/'.join(부분들[1:])
                Содржина_VALUE = пакет.extractfile(внес_VALUE).read()
                if ПАТЕКА.endswith('PKG-INFO'):
                    명세들.append(Содржина_VALUE.decode())
                elif ПАТЕКА.endswith('.py') and ПАТЕКА not in ('setup.py',):
                    추가(ПАТЕКА, Содржина_VALUE)
                elif '.egg-info/' not in ПАТЕКА and not ПАТЕКА.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ПАТЕКА)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 корен_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* извор_дрво 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if разложи_Барање_на_HTTP(명세.get('Name', ''))[0] != Име or 명세.get('Version') != верзија_VALUE:
        raise ValueError('배포 메타데이터의 Име·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(адреса, 한도):
    if not адреса.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(адреса, timeout=30) as одговори:
        if not одговори.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 адреса премести_VALUE')
        податоци = одговори.read(한도 + 1)
    if len(податоци) > 한도:
        raise ValueError('배포 Датотека Големина 제한 초과')
    return податоци


def пренос_пакет(Име, верзија_VALUE, 파일들, 출처):
    명세 = {'name': Име, 'version': верзија_VALUE, 'source': 출처, 'files': [
        {'path': ПАТЕКА, 'size': len(податоци), 'sha256': hashlib.sha256(податоци).hexdigest()}
        for ПАТЕКА, податоци in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('пакет 명세 Големина 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[внес_VALUE['path']] for внес_VALUE in 명세['files'])


class пакет_склад:
    def __init__(자신, ПАТЕКА, информатичка_технологија_Исклучен=False):
        자신.ПАТЕКА = Path(ПАТЕКА)
        자신.ПАТЕКА.mkdir(parents=True, exist_ok=True)
        자신.информатичка_технологија_Исклучен = информатичка_технологија_Исклучен

    def Подготви(자신, Барање_на_HTTP):
        Име, верзија_VALUE = разложи_Барање_на_HTTP(Барање_на_HTTP)
        열쇠 = Име + ('==' + верзија_VALUE if верзија_VALUE else '')
        LOG_патека = 자신.ПАТЕКА / (열쇠 + '.json')
        배포경로 = 자신.ПАТЕКА / (열쇠 + '.archive')
        if LOG_патека.is_file() and 배포경로.is_file():
            LOG_ред = json.loads(LOG_патека.read_text())
            податоци = 배포경로.read_bytes()
            if hashlib.sha256(податоци).hexdigest() != LOG_ред['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.информатичка_технологија_Исклучен:
                raise ValueError('информатичка_технологија_Исклучен 저장소에 없는 пакет: ' + Барање_на_HTTP)
            адреса = 'https://pypi.org/pypi/' + Име + ('/' + верзија_VALUE if верзија_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(адреса, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [внес_VALUE for внес_VALUE in msinfo32_exe['urls'] if not внес_VALUE.get('yanked') and внес_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Име.startswith('micropython-'):
                후보 = [внес_VALUE for внес_VALUE in msinfo32_exe['urls'] if not внес_VALUE.get('yanked') and внес_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            селекција_VALUE = 후보[0]
            податоци = 웹읽기(селекција_VALUE['url'], 4194304)
            if hashlib.sha256(податоци).hexdigest() != селекција_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Датотека SHA-256 불일치')
            LOG_ред = {'name': Име, 'version': msinfo32_exe['info']['version'], 'filename': селекција_VALUE['filename'],
                    'url': селекција_VALUE['url'], 'sha256': селекција_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_ред['filename'], податоци, Име, LOG_ред['version'])
            배포경로.write_bytes(податоци)
            LOG_патека.write_text(json.dumps(LOG_ред, ensure_ascii=False, indent=2) + '\n')
        if LOG_ред['name'] != Име or верзија_VALUE and LOG_ред['version'] != верзија_VALUE:
            raise ValueError('склад_корен Име·버전 불일치')
        파일들 = 압축풀기(LOG_ред['filename'], податоци, Име, LOG_ред['version'])
        return пренос_пакет(Име, LOG_ред['version'], 파일들, LOG_ред['url'])


class пакет_Барање_на_HTTP(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            Барање_на_HTTP = bytearray()
            while b'\n' not in Барање_на_HTTP and len(Барање_на_HTTP) < 100:
                조각 = 자신.request.recv(100 - len(Барање_на_HTTP))
                if not 조각:
                    return
                Барање_на_HTTP.extend(조각)
            if not Барање_на_HTTP.endswith(b'\n') or Барање_на_HTTP.count(b'\n') != 1:
                raise ValueError('잘못된 пакет Барање_на_HTTP')
            одговори = 자신.server.склад_корен.Подготви(Барање_на_HTTP[:-1].decode('ascii'))
        except Exception as ГРЕШКА:
            머리 = json.dumps({'error': str(ГРЕШКА)[:500]}, ensure_ascii=False).encode()
            одговори = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(одговори)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, број_на_порта=8027, ПАТЕКА=None, информатичка_технологија_Исклучен=False):
        자신.сервер_VALUE = socketserver.TCPServer(('127.0.0.1', број_на_порта), пакет_Барање_на_HTTP, bind_and_activate=False)
        자신.сервер_VALUE.allow_reuse_address = True
        자신.сервер_VALUE.server_bind()
        자신.сервер_VALUE.server_activate()
        자신.сервер_VALUE.склад_корен = пакет_склад(ПАТЕКА or Project_корен/'build/pip-cache', информатичка_технологија_Исклучен)
        자신.број_на_порта = 자신.сервер_VALUE.server_address[1]
        자신.нишка_VALUE = threading.Thread(target=자신.сервер_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.нишка_VALUE.start()
        return 자신

    def __exit__(자신, *Аргументи):
        자신.сервер_VALUE.shutdown()
        자신.сервер_VALUE.server_close()
        자신.нишка_VALUE.join(timeout=2)


def Изврши_2():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--port', type=int, default=8027)
    анализатор_48ee4b1b.add_argument('--cache', type=Path, default=Project_корен/'build/pip-cache')
    анализатор_48ee4b1b.add_argument('--offline', action='store_true')
    анализатор_48ee4b1b.add_argument('--fetch', help='Изврши_наредба 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    Аргументи = анализатор_48ee4b1b.parse_args()
    if Аргументи.fetch:
        податоци = пакет_склад(Аргументи.cache, Аргументи.offline).Подготви(Аргументи.fetch)
        print('пакет Подготви 완료:', Аргументи.fetch, len(податоци), 'бајт_VALUE')
        return
    with 꾸러미중계(Аргументи.port, Аргументи.cache, Аргументи.offline) as 중계:
        print('пакет 중계: 127.0.0.1:' + str(중계.број_на_порта), flush=True)
        try:
            중계.нишка_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Изврши_2()
