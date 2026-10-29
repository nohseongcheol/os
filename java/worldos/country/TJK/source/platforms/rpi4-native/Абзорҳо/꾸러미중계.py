#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 насб_кардан_қимат·실행한다."""
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
        raise ValueError('баста Ном 또는 Ном==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def санҷидани_эътибор_масир(Ном, насб_масир=True):
    масир = PurePosixPath(Ном)
    if масир.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Ном.split('/')):
        raise ValueError('허용하지 않는 баста масир: ' + Ном)
    if '\\' in Ном or any(ord(аломат_қимат_068c2631) < 32 or ord(аломат_қимат_068c2631) == 127 for аломат_қимат_068c2631 in Ном):
        raise ValueError('잘못된 баста масир 문자')
    if насб_масир and (len(('/lib/' + Ном).encode()) > 63 or Ном in ('한국어.py', 'баста.py')):
        raise ValueError('баста масир 제한 또는 қимати_пешфарз китобхона 충돌: ' + Ном)
    return Ном


def 압축풀기(файл_ворида_ном, иттилоот, Ном, версия_қимат):
    파일들 = {}
    명세들 = []
    def 추가(масир, Мӯҳтаво_қимат):
        санҷидани_эътибор_масир(масир)
        if масир in 파일들:
            raise ValueError('중복 баста масир: ' + масир)
        if len(Мӯҳтаво_қимат) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + масир)
        Мӯҳтаво_қимат.decode('utf-8')
        파일들[масир] = Мӯҳтаво_қимат
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 манбаъ_дарахт 16개·합계 64 KiB 이하여야 합니다.')
    if файл_ворида_ном.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(иттилоот)) as баста:
            항목들 = баста.infolist()
            if len(항목들) > 256 or sum(ворида_қимат.file_size for ворида_қимат in 항목들) > 1048576:
                raise ValueError('Бойгонӣ_қимат нашр_Захирагоҳ андоза_кардан 제한 초과')
            кор_Рӯйхат = [ворида_қимат for ворида_қимат in 항목들 if ворида_қимат.filename.endswith('.dist-info/WHEEL')]
            if len(кор_Рӯйхат) != 1:
                raise ValueError('wheel кор_қимат 명세가 필요합니다.')
            кор_қимат = email.parser.Parser().parsestr(баста.read(кор_Рӯйхат[0]).decode())
            if кор_қимат.get('Root-Is-Purelib', '').lower() != 'true' or not файл_ворида_ном.endswith('-none-any.whl'):
                raise ValueError('C изофа_қимат·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ворида_қимат in 항목들:
                масир = ворида_қимат.filename.rstrip('/')
                санҷидани_эътибор_масир(масир, False)
                if (ворида_қимат.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ворида_қимат.filename.endswith('/'):
                    continue
                if '.dist-info/' in масир:
                    if масир.endswith('/METADATA'):
                        명세들.append(баста.read(ворида_қимат).decode())
                    continue
                if not масир.endswith('.py') or '.data/' in масир:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + масир)
                추가(масир, баста.read(ворида_қимат))
    elif файл_ворида_ном.endswith('.tar.gz') and Ном.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py иҷро_кардан_фармон 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(иттилоот), mode='r|gz') as баста:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ворида_қимат in баста:
                항목수 += 1
                전체크기 += ворида_қимат.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Бойгонӣ_қимат нашр_Захирагоҳ андоза_кардан 제한 초과')
                санҷидани_эътибор_масир(ворида_қимат.name, False)
                부분들 = ворида_қимат.name.split('/')
                뿌리들.add(부분들[0])
                if ворида_қимат.isdir():
                    continue
                if not ворида_қимат.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython манбаъ_дарахт 배포형')
                масир = '/'.join(부분들[1:])
                Мӯҳтаво_қимат = баста.extractfile(ворида_қимат).read()
                if масир.endswith('PKG-INFO'):
                    명세들.append(Мӯҳтаво_қимат.decode())
                elif масир.endswith('.py') and масир not in ('setup.py',):
                    추가(масир, Мӯҳтаво_қимат)
                elif '.egg-info/' not in масир and not масир.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + масир)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* манбаъ_дарахт 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Ном or 명세.get('Version') != версия_қимат:
        raise ValueError('배포 메타데이터의 Ном·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(суроға, 한도):
    if not суроға.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(суроға, timeout=30) as ҷавоб_додан:
        if not ҷавоб_додан.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 суроға интиқол_додан_қимат')
        иттилоот = ҷавоб_додан.read(한도 + 1)
    if len(иттилоот) > 한도:
        raise ValueError('배포 Файл андоза_кардан 제한 초과')
    return иттилоот


def интиқол_баста(Ном, версия_қимат, 파일들, 출처):
    명세 = {'name': Ном, 'version': версия_қимат, 'source': 출처, 'files': [
        {'path': масир, 'size': len(иттилоот), 'sha256': hashlib.sha256(иттилоот).hexdigest()}
        for масир, иттилоот in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('баста 명세 андоза_кардан 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ворида_қимат['path']] for ворида_қимат in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, масир, 오프라인=False):
        자신.масир = Path(масир)
        자신.масир.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Омода_кардан(자신, 요청):
        Ном, версия_қимат = 요청해석(요청)
        열쇠 = Ном + ('==' + версия_қимат if версия_қимат else '')
        сабт_кардан_масир = 자신.масир / (열쇠 + '.json')
        배포경로 = 자신.масир / (열쇠 + '.archive')
        if сабт_кардан_масир.is_file() and 배포경로.is_file():
            сабт_кардан_сабт = json.loads(сабт_кардан_масир.read_text())
            иттилоот = 배포경로.read_bytes()
            if hashlib.sha256(иттилоот).hexdigest() != сабт_кардан_сабт['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 баста: ' + 요청)
            суроға = 'https://pypi.org/pypi/' + Ном + ('/' + версия_қимат if версия_қимат else '') + '/json'
            Маълумоти_система = json.loads(웹읽기(суроға, 4194304).decode())
            if Маълумоти_система['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ворида_қимат for ворида_қимат in Маълумоти_система['urls'] if not ворида_қимат.get('yanked') and ворида_қимат['filename'].endswith('-none-any.whl')]
            if not 후보 and Ном.startswith('micropython-'):
                후보 = [ворида_қимат for ворида_қимат in Маълумоти_система['urls'] if not ворида_қимат.get('yanked') and ворида_қимат['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            интихоб_қимат = 후보[0]
            иттилоот = 웹읽기(интихоб_қимат['url'], 4194304)
            if hashlib.sha256(иттилоот).hexdigest() != интихоб_қимат['digests']['sha256']:
                raise ValueError('PyPI 배포 Файл SHA-256 불일치')
            сабт_кардан_сабт = {'name': Ном, 'version': Маълумоти_система['info']['version'], 'filename': интихоб_қимат['filename'],
                    'url': интихоб_қимат['url'], 'sha256': интихоб_қимат['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(сабт_кардан_сабт['filename'], иттилоот, Ном, сабт_кардан_сабт['version'])
            배포경로.write_bytes(иттилоот)
            сабт_кардан_масир.write_text(json.dumps(сабт_кардан_сабт, ensure_ascii=False, indent=2) + '\n')
        if сабт_кардан_сабт['name'] != Ном or версия_қимат and сабт_кардан_сабт['version'] != версия_қимат:
            raise ValueError('저장소 Ном·버전 불일치')
        파일들 = 압축풀기(сабт_кардан_сабт['filename'], иттилоот, Ном, сабт_кардан_сабт['version'])
        return интиқол_баста(Ном, сабт_кардан_сабт['version'], 파일들, сабт_кардан_сабт['url'])


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
                raise ValueError('잘못된 баста 요청')
            ҷавоб_додан = 자신.server.저장소.Омода_кардан(요청[:-1].decode('ascii'))
        except Exception as Хато:
            머리 = json.dumps({'error': str(Хато)[:500]}, ensure_ascii=False).encode()
            ҷавоб_додан = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(ҷавоб_додан)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, масир=None, 오프라인=False):
        자신.сервер_қимат = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.сервер_қимат.allow_reuse_address = True
        자신.сервер_қимат.server_bind()
        자신.сервер_қимат.server_activate()
        자신.сервер_қимат.저장소 = 꾸러미저장소(масир or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.сервер_қимат.server_address[1]
        자신.ришта_қимат = threading.Thread(target=자신.сервер_қимат.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ришта_қимат.start()
        return 자신

    def __exit__(자신, *인수):
        자신.сервер_қимат.shutdown()
        자신.сервер_қимат.server_close()
        자신.ришта_қимат.join(timeout=2)


def порча():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='иҷро_кардан_фармон 없이 호환 배포 파일을 내려받아 검사·ҳифз_кардан_қимат')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        иттилоот = 꾸러미저장소(인수.cache, 인수.offline).Омода_кардан(인수.fetch)
        print('баста Омода_кардан 완료:', 인수.fetch, len(иттилоот), 'байт_қимат')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('баста 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.ришта_қимат.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    порча()
