#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 орнотуу_маани·실행한다."""
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
        raise ValueError('пакет Аты 또는 Аты==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def жарактуулугун_текшерүү_жол(Аты, орнотуу_жол=True):
    ЖОЛ = PurePosixPath(Аты)
    if ЖОЛ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Аты.split('/')):
        raise ValueError('허용하지 않는 пакет ЖОЛ: ' + Аты)
    if '\\' in Аты or any(ord(символ_маани_068c2631) < 32 or ord(символ_маани_068c2631) == 127 for символ_маани_068c2631 in Аты):
        raise ValueError('잘못된 пакет ЖОЛ 문자')
    if орнотуу_жол and (len(('/lib/' + Аты).encode()) > 63 or Аты in ('한국어.py', 'пакет.py')):
        raise ValueError('пакет ЖОЛ 제한 또는 жарыяланбаган_маани жыйнак 충돌: ' + Аты)
    return Аты


def 압축풀기(файл_киргизме_жазуу_аты, берилмелер, Аты, нуска_маани):
    파일들 = {}
    명세들 = []
    def 추가(ЖОЛ, Мазмун_маани):
        жарактуулугун_текшерүү_жол(ЖОЛ)
        if ЖОЛ in 파일들:
            raise ValueError('중복 пакет ЖОЛ: ' + ЖОЛ)
        if len(Мазмун_маани) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ЖОЛ)
        Мазмун_маани.decode('utf-8')
        파일들[ЖОЛ] = Мазмун_маани
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 башат_дарак 16개·합계 64 KiB 이하여야 합니다.')
    if файл_киргизме_жазуу_аты.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(берилмелер)) as пакет:
            항목들 = пакет.infolist()
            if len(항목들) > 256 or sum(киргизме_жазуу_маани.file_size for киргизме_жазуу_маани in 항목들) > 1048576:
                raise ValueError('Архив_маани чыгаруу_сактагыч Өлчөмү 제한 초과')
            иш_Тизме = [киргизме_жазуу_маани for киргизме_жазуу_маани in 항목들 if киргизме_жазуу_маани.filename.endswith('.dist-info/WHEEL')]
            if len(иш_Тизме) != 1:
                raise ValueError('wheel иш_маани 명세가 필요합니다.')
            иш_маани = email.parser.Parser().parsestr(пакет.read(иш_Тизме[0]).decode())
            if иш_маани.get('Root-Is-Purelib', '').lower() != 'true' or not файл_киргизме_жазуу_аты.endswith('-none-any.whl'):
                raise ValueError('C кеңейтүү_маани·플랫폼 전용 wheel은 지원하지 않습니다.')
            for киргизме_жазуу_маани in 항목들:
                ЖОЛ = киргизме_жазуу_маани.filename.rstrip('/')
                жарактуулугун_текшерүү_жол(ЖОЛ, False)
                if (киргизме_жазуу_маани.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if киргизме_жазуу_маани.filename.endswith('/'):
                    continue
                if '.dist-info/' in ЖОЛ:
                    if ЖОЛ.endswith('/METADATA'):
                        명세들.append(пакет.read(киргизме_жазуу_маани).decode())
                    continue
                if not ЖОЛ.endswith('.py') or '.data/' in ЖОЛ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ЖОЛ)
                추가(ЖОЛ, пакет.read(киргизме_жазуу_маани))
    elif файл_киргизме_жазуу_аты.endswith('.tar.gz') and Аты.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py аткаруу_буйрук 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(берилмелер), mode='r|gz') as пакет:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for киргизме_жазуу_маани in пакет:
                항목수 += 1
                전체크기 += киргизме_жазуу_маани.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Архив_маани чыгаруу_сактагыч Өлчөмү 제한 초과')
                жарактуулугун_текшерүү_жол(киргизме_жазуу_маани.name, False)
                부분들 = киргизме_жазуу_маани.name.split('/')
                뿌리들.add(부분들[0])
                if киргизме_жазуу_маани.isdir():
                    continue
                if not киргизме_жазуу_маани.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython башат_дарак 배포형')
                ЖОЛ = '/'.join(부분들[1:])
                Мазмун_маани = пакет.extractfile(киргизме_жазуу_маани).read()
                if ЖОЛ.endswith('PKG-INFO'):
                    명세들.append(Мазмун_маани.decode())
                elif ЖОЛ.endswith('.py') and ЖОЛ not in ('setup.py',):
                    추가(ЖОЛ, Мазмун_маани)
                elif '.egg-info/' not in ЖОЛ and not ЖОЛ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ЖОЛ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* башат_дарак 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Аты or 명세.get('Version') != нуска_маани:
        raise ValueError('배포 메타데이터의 Аты·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(дарек, 한도):
    if not дарек.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(дарек, timeout=30) as жооп_берүү:
        if not жооп_берүү.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 дарек жылдыруу_маани')
        берилмелер = жооп_берүү.read(한도 + 1)
    if len(берилмелер) > 한도:
        raise ValueError('배포 Файл Өлчөмү 제한 초과')
    return берилмелер


def ташүү_пакет(Аты, нуска_маани, 파일들, 출처):
    명세 = {'name': Аты, 'version': нуска_маани, 'source': 출처, 'files': [
        {'path': ЖОЛ, 'size': len(берилмелер), 'sha256': hashlib.sha256(берилмелер).hexdigest()}
        for ЖОЛ, берилмелер in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('пакет 명세 Өлчөмү 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[киргизме_жазуу_маани['path']] for киргизме_жазуу_маани in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, ЖОЛ, 오프라인=False):
        자신.ЖОЛ = Path(ЖОЛ)
        자신.ЖОЛ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Даярдоо(자신, 요청):
        Аты, нуска_маани = 요청해석(요청)
        열쇠 = Аты + ('==' + нуска_маани if нуска_маани else '')
        жазуу_жол = 자신.ЖОЛ / (열쇠 + '.json')
        배포경로 = 자신.ЖОЛ / (열쇠 + '.archive')
        if жазуу_жол.is_file() and 배포경로.is_file():
            жазуу_катар = json.loads(жазуу_жол.read_text())
            берилмелер = 배포경로.read_bytes()
            if hashlib.sha256(берилмелер).hexdigest() != жазуу_катар['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 пакет: ' + 요청)
            дарек = 'https://pypi.org/pypi/' + Аты + ('/' + нуска_маани if нуска_маани else '') + '/json'
            Система_маалыматы = json.loads(웹읽기(дарек, 4194304).decode())
            if Система_маалыматы['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [киргизме_жазуу_маани for киргизме_жазуу_маани in Система_маалыматы['urls'] if not киргизме_жазуу_маани.get('yanked') and киргизме_жазуу_маани['filename'].endswith('-none-any.whl')]
            if not 후보 and Аты.startswith('micropython-'):
                후보 = [киргизме_жазуу_маани for киргизме_жазуу_маани in Система_маалыматы['urls'] if not киргизме_жазуу_маани.get('yanked') and киргизме_жазуу_маани['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            белгилөө_маани = 후보[0]
            берилмелер = 웹읽기(белгилөө_маани['url'], 4194304)
            if hashlib.sha256(берилмелер).hexdigest() != белгилөө_маани['digests']['sha256']:
                raise ValueError('PyPI 배포 Файл SHA-256 불일치')
            жазуу_катар = {'name': Аты, 'version': Система_маалыматы['info']['version'], 'filename': белгилөө_маани['filename'],
                    'url': белгилөө_маани['url'], 'sha256': белгилөө_маани['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(жазуу_катар['filename'], берилмелер, Аты, жазуу_катар['version'])
            배포경로.write_bytes(берилмелер)
            жазуу_жол.write_text(json.dumps(жазуу_катар, ensure_ascii=False, indent=2) + '\n')
        if жазуу_катар['name'] != Аты or нуска_маани and жазуу_катар['version'] != нуска_маани:
            raise ValueError('저장소 Аты·버전 불일치')
        파일들 = 압축풀기(жазуу_катар['filename'], берилмелер, Аты, жазуу_катар['version'])
        return ташүү_пакет(Аты, жазуу_катар['version'], 파일들, жазуу_катар['url'])


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
            жооп_берүү = 자신.server.저장소.Даярдоо(요청[:-1].decode('ascii'))
        except Exception as Ката:
            머리 = json.dumps({'error': str(Ката)[:500]}, ensure_ascii=False).encode()
            жооп_берүү = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(жооп_берүү)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, ЖОЛ=None, 오프라인=False):
        자신.сервер_маани = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.сервер_маани.allow_reuse_address = True
        자신.сервер_маани.server_bind()
        자신.сервер_маани.server_activate()
        자신.сервер_маани.저장소 = 꾸러미저장소(ЖОЛ or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.сервер_маани.server_address[1]
        자신.трэд_маани = threading.Thread(target=자신.сервер_маани.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.трэд_маани.start()
        return 자신

    def __exit__(자신, *인수):
        자신.сервер_маани.shutdown()
        자신.сервер_маани.server_close()
        자신.трэд_маани.join(timeout=2)


def Жүргүзүү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='аткаруу_буйрук 없이 호환 배포 파일을 내려받아 검사·сактагыч_маани')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        берилмелер = 꾸러미저장소(인수.cache, 인수.offline).Даярдоо(인수.fetch)
        print('пакет Даярдоо 완료:', 인수.fetch, len(берилмелер), 'байт_маани')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('пакет 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.трэд_маани.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Жүргүзүү()
