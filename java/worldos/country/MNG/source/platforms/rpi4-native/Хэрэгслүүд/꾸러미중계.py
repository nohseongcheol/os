#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 суулгах_утга·실행한다."""
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
        raise ValueError('багц Нэр 또는 Нэр==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def баталгаажуулах_зам(Нэр, суурилуулалт_зам=True):
    ЗАМ = PurePosixPath(Нэр)
    if ЗАМ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Нэр.split('/')):
        raise ValueError('허용하지 않는 багц ЗАМ: ' + Нэр)
    if '\\' in Нэр or any(ord(тэмдэгт_утга) < 32 or ord(тэмдэгт_утга) == 127 for тэмдэгт_утга in Нэр):
        raise ValueError('잘못된 багц ЗАМ 문자')
    if суурилуулалт_зам and (len(('/lib/' + Нэр).encode()) > 63 or Нэр in ('한국어.py', 'багц.py')):
        raise ValueError('багц ЗАМ 제한 또는 өгөгдмөл_утга сан 충돌: ' + Нэр)
    return Нэр


def 압축풀기(файл_оролт_нэр, өгөгдөл, Нэр, хувилбар_утга):
    파일들 = {}
    명세들 = []
    def 추가(ЗАМ, Агуулга_утга):
        баталгаажуулах_зам(ЗАМ)
        if ЗАМ in 파일들:
            raise ValueError('중복 багц ЗАМ: ' + ЗАМ)
        if len(Агуулга_утга) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ЗАМ)
        Агуулга_утга.decode('utf-8')
        파일들[ЗАМ] = Агуулга_утга
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 эх_мод 16개·합계 64 KiB 이하여야 합니다.')
    if файл_оролт_нэр.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(өгөгдөл)) as багц:
            항목들 = багц.infolist()
            if len(항목들) > 256 or sum(оролт_утга.file_size for оролт_утга in 항목들) > 1048576:
                raise ValueError('Архив_утга гарц_Санах_ой Хэмжээ 제한 초과')
            нөхцөл_байдал_Жагсаалт = [оролт_утга for оролт_утга in 항목들 if оролт_утга.filename.endswith('.dist-info/WHEEL')]
            if len(нөхцөл_байдал_Жагсаалт) != 1:
                raise ValueError('wheel нөхцөл_байдал_утга 명세가 필요합니다.')
            нөхцөл_байдал_утга = email.parser.Parser().parsestr(багц.read(нөхцөл_байдал_Жагсаалт[0]).decode())
            if нөхцөл_байдал_утга.get('Root-Is-Purelib', '').lower() != 'true' or not файл_оролт_нэр.endswith('-none-any.whl'):
                raise ValueError('C өргөтгөл_утга·플랫폼 전용 wheel은 지원하지 않습니다.')
            for оролт_утга in 항목들:
                ЗАМ = оролт_утга.filename.rstrip('/')
                баталгаажуулах_зам(ЗАМ, False)
                if (оролт_утга.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if оролт_утга.filename.endswith('/'):
                    continue
                if '.dist-info/' in ЗАМ:
                    if ЗАМ.endswith('/METADATA'):
                        명세들.append(багц.read(оролт_утга).decode())
                    continue
                if not ЗАМ.endswith('.py') or '.data/' in ЗАМ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ЗАМ)
                추가(ЗАМ, багц.read(оролт_утга))
    elif файл_оролт_нэр.endswith('.tar.gz') and Нэр.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Гүйцэтгэх_команд 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(өгөгдөл), mode='r|gz') as багц:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for оролт_утга in багц:
                항목수 += 1
                전체크기 += оролт_утга.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('Архив_утга гарц_Санах_ой Хэмжээ 제한 초과')
                баталгаажуулах_зам(оролт_утга.name, False)
                부분들 = оролт_утга.name.split('/')
                뿌리들.add(부분들[0])
                if оролт_утга.isdir():
                    continue
                if not оролт_утга.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython эх_мод 배포형')
                ЗАМ = '/'.join(부분들[1:])
                Агуулга_утга = багц.extractfile(оролт_утга).read()
                if ЗАМ.endswith('PKG-INFO'):
                    명세들.append(Агуулга_утга.decode())
                elif ЗАМ.endswith('.py') and ЗАМ not in ('setup.py',):
                    추가(ЗАМ, Агуулга_утга)
                elif '.egg-info/' not in ЗАМ and not ЗАМ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ЗАМ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* эх_мод 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != Нэр or 명세.get('Version') != хувилбар_утга:
        raise ValueError('배포 메타데이터의 Нэр·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(хаяг, 한도):
    if not хаяг.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(хаяг, timeout=30) as хариулах:
        if not хариулах.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 хаяг зөөх_утга')
        өгөгдөл = хариулах.read(한도 + 1)
    if len(өгөгдөл) > 한도:
        raise ValueError('배포 Файл Хэмжээ 제한 초과')
    return өгөгдөл


def дамжуулах_багц(Нэр, хувилбар_утга, 파일들, 출처):
    명세 = {'name': Нэр, 'version': хувилбар_утга, 'source': 출처, 'files': [
        {'path': ЗАМ, 'size': len(өгөгдөл), 'sha256': hashlib.sha256(өгөгдөл).hexdigest()}
        for ЗАМ, өгөгдөл in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('багц 명세 Хэмжээ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[оролт_утга['path']] for оролт_утга in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, ЗАМ, 오프라인=False):
        자신.ЗАМ = Path(ЗАМ)
        자신.ЗАМ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def Бэлтгэх(자신, 요청):
        Нэр, хувилбар_утга = 요청해석(요청)
        열쇠 = Нэр + ('==' + хувилбар_утга if хувилбар_утга else '')
        бичих_зам = 자신.ЗАМ / (열쇠 + '.json')
        배포경로 = 자신.ЗАМ / (열쇠 + '.archive')
        if бичих_зам.is_file() and 배포경로.is_file():
            бичих_мөр_6e8b375a = json.loads(бичих_зам.read_text())
            өгөгдөл = 배포경로.read_bytes()
            if hashlib.sha256(өгөгдөл).hexdigest() != бичих_мөр_6e8b375a['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 багц: ' + 요청)
            хаяг = 'https://pypi.org/pypi/' + Нэр + ('/' + хувилбар_утга if хувилбар_утга else '') + '/json'
            системийн_мэдээлэл = json.loads(웹읽기(хаяг, 4194304).decode())
            if системийн_мэдээлэл['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [оролт_утга for оролт_утга in системийн_мэдээлэл['urls'] if not оролт_утга.get('yanked') and оролт_утга['filename'].endswith('-none-any.whl')]
            if not 후보 and Нэр.startswith('micropython-'):
                후보 = [оролт_утга for оролт_утга in системийн_мэдээлэл['urls'] if not оролт_утга.get('yanked') and оролт_утга['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            сонгосон_хэсэг_утга = 후보[0]
            өгөгдөл = 웹읽기(сонгосон_хэсэг_утга['url'], 4194304)
            if hashlib.sha256(өгөгдөл).hexdigest() != сонгосон_хэсэг_утга['digests']['sha256']:
                raise ValueError('PyPI 배포 Файл SHA-256 불일치')
            бичих_мөр_6e8b375a = {'name': Нэр, 'version': системийн_мэдээлэл['info']['version'], 'filename': сонгосон_хэсэг_утга['filename'],
                    'url': сонгосон_хэсэг_утга['url'], 'sha256': сонгосон_хэсэг_утга['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(бичих_мөр_6e8b375a['filename'], өгөгдөл, Нэр, бичих_мөр_6e8b375a['version'])
            배포경로.write_bytes(өгөгдөл)
            бичих_зам.write_text(json.dumps(бичих_мөр_6e8b375a, ensure_ascii=False, indent=2) + '\n')
        if бичих_мөр_6e8b375a['name'] != Нэр or хувилбар_утга and бичих_мөр_6e8b375a['version'] != хувилбар_утга:
            raise ValueError('저장소 Нэр·버전 불일치')
        파일들 = 압축풀기(бичих_мөр_6e8b375a['filename'], өгөгдөл, Нэр, бичих_мөр_6e8b375a['version'])
        return дамжуулах_багц(Нэр, бичих_мөр_6e8b375a['version'], 파일들, бичих_мөр_6e8b375a['url'])


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
                raise ValueError('잘못된 багц 요청')
            хариулах = 자신.server.저장소.Бэлтгэх(요청[:-1].decode('ascii'))
        except Exception as Алдаа:
            머리 = json.dumps({'error': str(Алдаа)[:500]}, ensure_ascii=False).encode()
            хариулах = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(хариулах)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, ЗАМ=None, 오프라인=False):
        자신.сервер_утга = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.сервер_утга.allow_reuse_address = True
        자신.сервер_утга.server_bind()
        자신.сервер_утга.server_activate()
        자신.сервер_утга.저장소 = 꾸러미저장소(ЗАМ or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.сервер_утга.server_address[1]
        자신.яриа_утга = threading.Thread(target=자신.сервер_утга.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.яриа_утга.start()
        return 자신

    def __exit__(자신, *인수):
        자신.сервер_утга.shutdown()
        자신.сервер_утга.server_close()
        자신.яриа_утга.join(timeout=2)


def Ажиллуулах():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='Гүйцэтгэх_команд 없이 호환 배포 파일을 내려받아 검사·хадгалах_утга')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        өгөгдөл = 꾸러미저장소(인수.cache, 인수.offline).Бэлтгэх(인수.fetch)
        print('багц Бэлтгэх 완료:', 인수.fetch, len(өгөгдөл), 'байт_утга')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('багц 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.яриа_утга.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Ажиллуулах()
