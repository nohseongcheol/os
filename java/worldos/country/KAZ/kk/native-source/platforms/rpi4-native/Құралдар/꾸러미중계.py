#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 орнату_мән·실행한다."""
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

жоба_түбір = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('жинау Аты 또는 Аты==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def тексеру_жол(Аты, орнатым_жол=True):
    Жол_2 = PurePosixPath(Аты)
    if Жол_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Аты.split('/')):
        raise ValueError('허용하지 않는 жинау Жол_2: ' + Аты)
    if '\\' in Аты or any(ord(таңба_мән) < 32 or ord(таңба_мән) == 127 for таңба_мән in Аты):
        raise ValueError('잘못된 жинау Жол_2 문자')
    if орнатым_жол and (len(('/lib/' + Аты).encode()) > 63 or Аты in ('한국어.py', 'жинау.py')):
        raise ValueError('жинау Жол_2 제한 또는 әдепкі_мән кітапхана 충돌: ' + Аты)
    return Аты


def қысылған_файлды_қалпына_келтіру(файл_енгізу_аты, деректер, Аты, нұсқа_мән):
    파일들 = {}
    명세들 = []
    def қосу_енгізу(Жол_2, мазмұн_мән):
        тексеру_жол(Жол_2)
        if Жол_2 in 파일들:
            raise ValueError('중복 жинау Жол_2: ' + Жол_2)
        if len(мазмұн_мән) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + Жол_2)
        мазмұн_мән.decode('utf-8')
        파일들[Жол_2] = мазмұн_мән
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 көз_дарақ 16개·합계 64 KiB 이하여야 합니다.')
    if файл_енгізу_аты.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(деректер)) as жинау:
            항목들 = жинау.infolist()
            if len(항목들) > 256 or sum(енгізу_мән.file_size for енгізу_мән in 항목들) > 1048576:
                raise ValueError('Мұрағат_мән шығарылым_Жад Өлшемі 제한 초과')
            іс_Тізім = [енгізу_мән for енгізу_мән in 항목들 if енгізу_мән.filename.endswith('.dist-info/WHEEL')]
            if len(іс_Тізім) != 1:
                raise ValueError('wheel іс_мән 명세가 필요합니다.')
            іс_мән = email.parser.Parser().parsestr(жинау.read(іс_Тізім[0]).decode())
            if іс_мән.get('Root-Is-Purelib', '').lower() != 'true' or not файл_енгізу_аты.endswith('-none-any.whl'):
                raise ValueError('C кеңейтім_мән·플랫폼 전용 wheel은 지원하지 않습니다.')
            for енгізу_мән in 항목들:
                Жол_2 = енгізу_мән.filename.rstrip('/')
                тексеру_жол(Жол_2, False)
                if (енгізу_мән.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if енгізу_мән.filename.endswith('/'):
                    continue
                if '.dist-info/' in Жол_2:
                    if Жол_2.endswith('/METADATA'):
                        명세들.append(жинау.read(енгізу_мән).decode())
                    continue
                if not Жол_2.endswith('.py') or '.data/' in Жол_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + Жол_2)
                қосу_енгізу(Жол_2, жинау.read(енгізу_мән))
    elif файл_енгізу_аты.endswith('.tar.gz') and Аты.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py орындау_пәрмен 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(деректер), mode='r|gz') as жинау:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for енгізу_мән in жинау:
                항목수 += 1
                전체크기 += енгізу_мән.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Мұрағат_мән шығарылым_Жад Өлшемі 제한 초과')
                тексеру_жол(енгізу_мән.name, False)
                부분들 = енгізу_мән.name.split('/')
                뿌리들.add(부분들[0])
                if енгізу_мән.isdir():
                    continue
                if not енгізу_мән.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython көз_дарақ 배포형')
                Жол_2 = '/'.join(부분들[1:])
                мазмұн_мән = жинау.extractfile(енгізу_мән).read()
                if Жол_2.endswith('PKG-INFO'):
                    명세들.append(мазмұн_мән.decode())
                elif Жол_2.endswith('.py') and Жол_2 not in ('setup.py',):
                    қосу_енгізу(Жол_2, мазмұн_мән)
                elif '.egg-info/' not in Жол_2 and not Жол_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + Жол_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 түбір_мән 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* көз_дарақ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    сипаттама = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(сипаттама.get('Name', ''))[0] != Аты or сипаттама.get('Version') != нұсқа_мән:
        raise ValueError('배포 메타데이터의 Аты·버전 불일치')
    if сипаттама.get_all('Requires-Dist') or сипаттама.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(мекенжай, 한도):
    if not мекенжай.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(мекенжай, timeout=30) as жауап:
        if not жауап.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 мекенжай жылжыту_мән')
        деректер = жауап.read(한도 + 1)
    if len(деректер) > 한도:
        raise ValueError('배포 Файл Өлшемі 제한 초과')
    return деректер


def аудару_жинау(Аты, нұсқа_мән, 파일들, 출처):
    сипаттама = {'name': Аты, 'version': нұсқа_мән, 'source': 출처, 'files': [
        {'path': Жол_2, 'size': len(деректер), 'sha256': hashlib.sha256(деректер).hexdigest()}
        for Жол_2, деректер in sorted(파일들.items())]}
    머리 = json.dumps(сипаттама, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('жинау сипаттама Өлшемі 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[енгізу_мән['path']] for енгізу_мән in сипаттама['files'])


class жинау_репозиторий:
    def __init__(자신, Жол_2, ақпараттық_жүйелер_Офлайн=False):
        자신.Жол_2 = Path(Жол_2)
        자신.Жол_2.mkdir(parents=True, exist_ok=True)
        자신.ақпараттық_жүйелер_Офлайн = ақпараттық_жүйелер_Офлайн

    def Дайындау(자신, 요청):
        Аты, нұсқа_мән = 요청해석(요청)
        열쇠 = Аты + ('==' + нұсқа_мән if нұсқа_мән else '')
        журнал_жол_5f8d12bf = 자신.Жол_2 / (열쇠 + '.json')
        배포경로 = 자신.Жол_2 / (열쇠 + '.archive')
        if журнал_жол_5f8d12bf.is_file() and 배포경로.is_file():
            журнал_жол = json.loads(журнал_жол_5f8d12bf.read_text())
            деректер = 배포경로.read_bytes()
            if hashlib.sha256(деректер).hexdigest() != журнал_жол['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.ақпараттық_жүйелер_Офлайн:
                raise ValueError('ақпараттық_жүйелер_Офлайн 저장소에 없는 жинау: ' + 요청)
            мекенжай = 'https://pypi.org/pypi/' + Аты + ('/' + нұсқа_мән if нұсқа_мән else '') + '/json'
            Жүйелік_ақпарат = json.loads(웹읽기(мекенжай, 4194304).decode())
            if Жүйелік_ақпарат['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [енгізу_мән for енгізу_мән in Жүйелік_ақпарат['urls'] if not енгізу_мән.get('yanked') and енгізу_мән['filename'].endswith('-none-any.whl')]
            if not 후보 and Аты.startswith('micropython-'):
                후보 = [енгізу_мән for енгізу_мән in Жүйелік_ақпарат['urls'] if not енгізу_мән.get('yanked') and енгізу_мән['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            таңдау_мән = 후보[0]
            деректер = 웹읽기(таңдау_мән['url'], 4194304)
            if hashlib.sha256(деректер).hexdigest() != таңдау_мән['digests']['sha256']:
                raise ValueError('PyPI 배포 Файл SHA-256 불일치')
            журнал_жол = {'name': Аты, 'version': Жүйелік_ақпарат['info']['version'], 'filename': таңдау_мән['filename'],
                    'url': таңдау_мән['url'], 'sha256': таңдау_мән['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            қысылған_файлды_қалпына_келтіру(журнал_жол['filename'], деректер, Аты, журнал_жол['version'])
            배포경로.write_bytes(деректер)
            журнал_жол_5f8d12bf.write_text(json.dumps(журнал_жол, ensure_ascii=False, indent=2) + '\n')
        if журнал_жол['name'] != Аты or нұсқа_мән and журнал_жол['version'] != нұсқа_мән:
            raise ValueError('репозиторий_түбір Аты·버전 불일치')
        파일들 = қысылған_файлды_қалпына_келтіру(журнал_жол['filename'], деректер, Аты, журнал_жол['version'])
        return аудару_жинау(Аты, журнал_жол['version'], 파일들, журнал_жол['url'])


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
                raise ValueError('잘못된 жинау 요청')
            жауап = 자신.server.репозиторий_түбір.Дайындау(요청[:-1].decode('ascii'))
        except Exception as Қате:
            머리 = json.dumps({'error': str(Қате)[:500]}, ensure_ascii=False).encode()
            жауап = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(жауап)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, порт_нөмірі=8027, Жол_2=None, ақпараттық_жүйелер_Офлайн=False):
        자신.сервер_мән = socketserver.TCPServer(('127.0.0.1', порт_нөмірі), 꾸러미요청, bind_and_activate=False)
        자신.сервер_мән.allow_reuse_address = True
        자신.сервер_мән.server_bind()
        자신.сервер_мән.server_activate()
        자신.сервер_мән.репозиторий_түбір = жинау_репозиторий(Жол_2 or жоба_түбір/'build/pip-cache', ақпараттық_жүйелер_Офлайн)
        자신.порт_нөмірі = 자신.сервер_мән.server_address[1]
        자신.ағын_мән = threading.Thread(target=자신.сервер_мән.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ағын_мән.start()
        return 자신

    def __exit__(자신, *Аргументтер):
        자신.сервер_мән.shutdown()
        자신.сервер_мән.server_close()
        자신.ағын_мән.join(timeout=2)


def Орындау_2():
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('--port', type=int, default=8027)
    талдау_құралы_48ee4b1b.add_argument('--cache', type=Path, default=жоба_түбір/'build/pip-cache')
    талдау_құралы_48ee4b1b.add_argument('--offline', action='store_true')
    талдау_құралы_48ee4b1b.add_argument('--fetch', help='орындау_пәрмен 없이 호환 배포 파일을 내려받아 검사·сақтау_мән')
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    if Аргументтер.fetch:
        деректер = жинау_репозиторий(Аргументтер.cache, Аргументтер.offline).Дайындау(Аргументтер.fetch)
        print('жинау Дайындау 완료:', Аргументтер.fetch, len(деректер), 'байт_мән')
        return
    with 꾸러미중계(Аргументтер.port, Аргументтер.cache, Аргументтер.offline) as 중계:
        print('жинау 중계: 127.0.0.1:' + str(중계.порт_нөмірі), flush=True)
        try:
            중계.ағын_мән.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Орындау_2()
