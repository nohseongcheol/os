#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ᎯᏘᏅᏛᎦ_ᏧᎬᏩᎶᏗᏯ·실행한다."""
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
        raise ValueError('ᎦᏇᏅᎯ ᏚᏙᎥᎢ 또는 ᏚᏙᎥᎢ==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def ᎪᎯᏳᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ(ᏚᏙᎥᎢ, ᎦᏘᏅᏛᏍᏗ_ᎠᏍᏓᏩᏛᏍᏗ=True):
    ᎠᏍᏓᏩᏛᏍᏗ = PurePosixPath(ᏚᏙᎥᎢ)
    if ᎠᏍᏓᏩᏛᏍᏗ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in ᏚᏙᎥᎢ.split('/')):
        raise ValueError('허용하지 않는 ᎦᏇᏅᎯ ᎠᏍᏓᏩᏛᏍᏗ: ' + ᏚᏙᎥᎢ)
    if '\\' in ᏚᏙᎥᎢ or any(ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) < 32 or ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ) == 127 for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in ᏚᏙᎥᎢ):
        raise ValueError('잘못된 ᎦᏇᏅᎯ ᎠᏍᏓᏩᏛᏍᏗ 문자')
    if ᎦᏘᏅᏛᏍᏗ_ᎠᏍᏓᏩᏛᏍᏗ and (len(('/lib/' + ᏚᏙᎥᎢ).encode()) > 63 or ᏚᏙᎥᎢ in ('한국어.py', 'ᎦᏇᏅᎯ.py')):
        raise ValueError('ᎦᏇᏅᎯ ᎠᏍᏓᏩᏛᏍᏗ 제한 또는 ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ ᏧᏂᎪᎵᏰᏗᎢ 충돌: ' + ᏚᏙᎥᎢ)
    return ᏚᏙᎥᎢ


def 압축풀기(ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ, ᏚᏙᎥᎢ, ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ):
    파일들 = {}
    명세들 = []
    def 추가(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ):
        ᎪᎯᏳᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ(ᎠᏍᏓᏩᏛᏍᏗ)
        if ᎠᏍᏓᏩᏛᏍᏗ in 파일들:
            raise ValueError('중복 ᎦᏇᏅᎯ ᎠᏍᏓᏩᏛᏍᏗ: ' + ᎠᏍᏓᏩᏛᏍᏗ)
        if len(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + ᎠᏍᏓᏩᏛᏍᏗ)
        ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.decode('utf-8')
        파일들[ᎠᏍᏓᏩᏛᏍᏗ] = ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 ᎦᏟᏌᏅᎯ_ᏡᎬ 16개·합계 64 KiB 이하여야 합니다.')
    if ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ᎦᏟᏌᏅᎯ)) as ᎦᏇᏅᎯ:
            항목들 = ᎦᏇᏅᎯ.infolist()
            if len(항목들) > 256 or sum(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.file_size for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 항목들) > 1048576:
                raise ValueError('ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ 해제 ᎢᎩᏓ 제한 초과')
            ᎢᏳᎵᏍᏔᏅᎢ_ᏕᎦᏅᏅᏛ = [Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 항목들 if Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.filename.endswith('.dist-info/WHEEL')]
            if len(ᎢᏳᎵᏍᏔᏅᎢ_ᏕᎦᏅᏅᏛ) != 1:
                raise ValueError('wheel ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ 명세가 필요합니다.')
            ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ = email.parser.Parser().parsestr(ᎦᏇᏅᎯ.read(ᎢᏳᎵᏍᏔᏅᎢ_ᏕᎦᏅᏅᏛ[0]).decode())
            if ᎢᏳᎵᏍᏔᏅᎢ_ᏧᎬᏩᎶᏗᏯ.get('Root-Is-Purelib', '').lower() != 'true' or not ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ.endswith('-none-any.whl'):
                raise ValueError('C ᎪᏯᏅᎯᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ·플랫폼 전용 wheel은 지원하지 않습니다.')
            for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 항목들:
                ᎠᏍᏓᏩᏛᏍᏗ = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.filename.rstrip('/')
                ᎪᎯᏳᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ(ᎠᏍᏓᏩᏛᏍᏗ, False)
                if (Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.filename.endswith('/'):
                    continue
                if '.dist-info/' in ᎠᏍᏓᏩᏛᏍᏗ:
                    if ᎠᏍᏓᏩᏛᏍᏗ.endswith('/METADATA'):
                        명세들.append(ᎦᏇᏅᎯ.read(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ).decode())
                    continue
                if not ᎠᏍᏓᏩᏛᏍᏗ.endswith('.py') or '.data/' in ᎠᏍᏓᏩᏛᏍᏗ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + ᎠᏍᏓᏩᏛᏍᏗ)
                추가(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᏇᏅᎯ.read(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ))
    elif ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ.endswith('.tar.gz') and ᏚᏙᎥᎢ.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ᎦᏟᏌᏅᎯ), mode='r|gz') as ᎦᏇᏅᎯ:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in ᎦᏇᏅᎯ:
                항목수 += 1
                전체크기 += Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('ᎠᏍᏆᏂᎪᏛᎢ_ᏧᎬᏩᎶᏗᏯ 해제 ᎢᎩᏓ 제한 초과')
                ᎪᎯᏳᏙᏗ_ᎠᏍᏓᏩᏛᏍᏗ(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.name, False)
                부분들 = Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.name.split('/')
                뿌리들.add(부분들[0])
                if Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.isdir():
                    continue
                if not Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython ᎦᏟᏌᏅᎯ_ᏡᎬ 배포형')
                ᎠᏍᏓᏩᏛᏍᏗ = '/'.join(부분들[1:])
                ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ = ᎦᏇᏅᎯ.extractfile(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ).read()
                if ᎠᏍᏓᏩᏛᏍᏗ.endswith('PKG-INFO'):
                    명세들.append(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.decode())
                elif ᎠᏍᏓᏩᏛᏍᏗ.endswith('.py') and ᎠᏍᏓᏩᏛᏍᏗ not in ('setup.py',):
                    추가(ᎠᏍᏓᏩᏛᏍᏗ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ)
                elif '.egg-info/' not in ᎠᏍᏓᏩᏛᏍᏗ and not ᎠᏍᏓᏩᏛᏍᏗ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + ᎠᏍᏓᏩᏛᏍᏗ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 뿌리 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* ᎦᏟᏌᏅᎯ_ᏡᎬ 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != ᏚᏙᎥᎢ or 명세.get('Version') != ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ:
        raise ValueError('배포 메타데이터의 ᏚᏙᎥᎢ·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, 한도):
    if not ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, timeout=30) as 응답:
        if not 응답.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ᎪᏪᎵ_ᏫᏗᎦᏅᏗ ᎯᎲᎾ_ᏧᎬᏩᎶᏗᏯ')
        ᎦᏟᏌᏅᎯ = 응답.read(한도 + 1)
    if len(ᎦᏟᏌᏅᎯ) > 한도:
        raise ValueError('배포 ᎠᏍᏆᏂᎪᏙᏗ ᎢᎩᏓ 제한 초과')
    return ᎦᏟᏌᏅᎯ


def ᎠᎲᏍᏗ_ᎦᏇᏅᎯ(ᏚᏙᎥᎢ, ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ, 파일들, 출처):
    명세 = {'name': ᏚᏙᎥᎢ, 'version': ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ, 'source': 출처, 'files': [
        {'path': ᎠᏍᏓᏩᏛᏍᏗ, 'size': len(ᎦᏟᏌᏅᎯ), 'sha256': hashlib.sha256(ᎦᏟᏌᏅᎯ).hexdigest()}
        for ᎠᏍᏓᏩᏛᏍᏗ, ᎦᏟᏌᏅᎯ in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('ᎦᏇᏅᎯ 명세 ᎢᎩᏓ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['path']] for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, ᎠᏍᏓᏩᏛᏍᏗ, 오프라인=False):
        자신.ᎠᏍᏓᏩᏛᏍᏗ = Path(ᎠᏍᏓᏩᏛᏍᏗ)
        자신.ᎠᏍᏓᏩᏛᏍᏗ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def ᎭᏛᏅᎢᏍᏓ(자신, 요청):
        ᏚᏙᎥᎢ, ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ = 요청해석(요청)
        열쇠 = ᏚᏙᎥᎢ + ('==' + ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ if ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ else '')
        ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎠᏍᏓᏩᏛᏍᏗ = 자신.ᎠᏍᏓᏩᏛᏍᏗ / (열쇠 + '.json')
        배포경로 = 자신.ᎠᏍᏓᏩᏛᏍᏗ / (열쇠 + '.archive')
        if ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎠᏍᏓᏩᏛᏍᏗ.is_file() and 배포경로.is_file():
            ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = json.loads(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎠᏍᏓᏩᏛᏍᏗ.read_text())
            ᎦᏟᏌᏅᎯ = 배포경로.read_bytes()
            if hashlib.sha256(ᎦᏟᏌᏅᎯ).hexdigest() != ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 ᎦᏇᏅᎯ: ' + 요청)
            ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = 'https://pypi.org/pypi/' + ᏚᏙᎥᎢ + ('/' + ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ if ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ᎪᏪᎵ_ᏫᏗᎦᏅᏗ, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in msinfo32_exe['urls'] if not Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.get('yanked') and Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['filename'].endswith('-none-any.whl')]
            if not 후보 and ᏚᏙᎥᎢ.startswith('micropython-'):
                후보 = [Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in msinfo32_exe['urls'] if not Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.get('yanked') and Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ = 후보[0]
            ᎦᏟᏌᏅᎯ = 웹읽기(ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ['url'], 4194304)
            if hashlib.sha256(ᎦᏟᏌᏅᎯ).hexdigest() != ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ['digests']['sha256']:
                raise ValueError('PyPI 배포 ᎠᏍᏆᏂᎪᏙᏗ SHA-256 불일치')
            ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = {'name': ᏚᏙᎥᎢ, 'version': msinfo32_exe['info']['version'], 'filename': ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ['filename'],
                    'url': ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ['url'], 'sha256': ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['filename'], ᎦᏟᏌᏅᎯ, ᏚᏙᎥᎢ, ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['version'])
            배포경로.write_bytes(ᎦᏟᏌᏅᎯ)
            ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎠᏍᏓᏩᏛᏍᏗ.write_text(json.dumps(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ, ensure_ascii=False, indent=2) + '\n')
        if ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['name'] != ᏚᏙᎥᎢ or ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ and ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['version'] != ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ:
            raise ValueError('저장소 ᏚᏙᎥᎢ·버전 불일치')
        파일들 = 압축풀기(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['filename'], ᎦᏟᏌᏅᎯ, ᏚᏙᎥᎢ, ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['version'])
        return ᎠᎲᏍᏗ_ᎦᏇᏅᎯ(ᏚᏙᎥᎢ, ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['version'], 파일들, ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ['url'])


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
                raise ValueError('잘못된 ᎦᏇᏅᎯ 요청')
            응답 = 자신.server.저장소.ᎭᏛᏅᎢᏍᏓ(요청[:-1].decode('ascii'))
        except Exception as ᎦᎵᏓᏍᏔᏅ:
            머리 = json.dumps({'error': str(ᎦᎵᏓᏍᏔᏅ)[:500]}, ensure_ascii=False).encode()
            응답 = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(응답)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, ᎠᏍᏓᏩᏛᏍᏗ=None, 오프라인=False):
        자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.allow_reuse_address = True
        자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.server_bind()
        자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.server_activate()
        자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.저장소 = 꾸러미저장소(ᎠᏍᏓᏩᏛᏍᏗ or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.server_address[1]
        자신.ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ = threading.Thread(target=자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.start()
        return 자신

    def __exit__(자신, *인수):
        자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.shutdown()
        자신.ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.server_close()
        자신.ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.join(timeout=2)


def ᎠᎢᏎᏍᏗ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 없이 호환 배포 파일을 내려받아 검사·Store_ᏧᎬᏩᎶᏗᏯ')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        ᎦᏟᏌᏅᎯ = 꾸러미저장소(인수.cache, 인수.offline).ᎭᏛᏅᎢᏍᏓ(인수.fetch)
        print('ᎦᏇᏅᎯ ᎭᏛᏅᎢᏍᏓ 완료:', 인수.fetch, len(ᎦᏟᏌᏅᎯ), 'byte_ᏧᎬᏩᎶᏗᏯ')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('ᎦᏇᏅᎯ 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
