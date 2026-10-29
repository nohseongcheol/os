#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ইনস্টল_করুন_মান·실행한다."""
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

প্রকল্প_মূল = Path(__file__).resolve().parents[1]


def 요청해석(요청):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', 요청)
    if not 맞음:
        raise ValueError('পাঁজা নাম 또는 নাম==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def বৈধ_করুন_পথ(নাম, সংস্থাপন_পথ=True):
    পথ_2 = PurePosixPath(নাম)
    if পথ_2.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in নাম.split('/')):
        raise ValueError('허용하지 않는 পাঁজা পথ_2: ' + নাম)
    if '\\' in নাম or any(ord(অক্ষর_মান) < 32 or ord(অক্ষর_মান) == 127 for অক্ষর_মান in নাম):
        raise ValueError('잘못된 পাঁজা পথ_2 문자')
    if সংস্থাপন_পথ and (len(('/lib/' + নাম).encode()) > 63 or নাম in ('বাংলা.py', 'পাঁজা.py')):
        raise ValueError('পাঁজা পথ_2 제한 또는 অমনোনীত_মান লাইব্রেরি 충돌: ' + নাম)
    return নাম


def 압축풀기(ফাইল_ভুক্তি_নাম, ডাটা, নাম, সংস্করণ_মান):
    파일들 = {}
    명세들 = []
    def 추가(পথ_2, সামগ্রি_মান):
        বৈধ_করুন_পথ(পথ_2)
        if পথ_2 in 파일들:
            raise ValueError('중복 পাঁজা পথ_2: ' + পথ_2)
        if len(সামগ্রি_মান) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + পথ_2)
        সামগ্রি_মান.decode('utf-8')
        파일들[পথ_2] = সামগ্রি_মান
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 উত্স_ট্রী 16개·합계 64 KiB 이하여야 합니다.')
    if ফাইল_ভুক্তি_নাম.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ডাটা)) as পাঁজা:
            항목들 = পাঁজা.infolist()
            if len(항목들) > 256 or sum(ভুক্তি_মান.file_size for ভুক্তি_মান in 항목들) > 1048576:
                raise ValueError('সংগ্রহ_করা_মান রিলিজ_স্টোরেজ আকার 제한 초과')
            কাজ_তালিকা = [ভুক্তি_মান for ভুক্তি_মান in 항목들 if ভুক্তি_মান.filename.endswith('.dist-info/WHEEL')]
            if len(কাজ_তালিকা) != 1:
                raise ValueError('wheel কাজ_মান 명세가 필요합니다.')
            কাজ_মান = email.parser.Parser().parsestr(পাঁজা.read(কাজ_তালিকা[0]).decode())
            if কাজ_মান.get('Root-Is-Purelib', '').lower() != 'true' or not ফাইল_ভুক্তি_নাম.endswith('-none-any.whl'):
                raise ValueError('C প্রসার_মান·플랫폼 전용 wheel은 지원하지 않습니다.')
            for ভুক্তি_মান in 항목들:
                পথ_2 = ভুক্তি_মান.filename.rstrip('/')
                বৈধ_করুন_পথ(পথ_2, False)
                if (ভুক্তি_মান.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if ভুক্তি_মান.filename.endswith('/'):
                    continue
                if '.dist-info/' in পথ_2:
                    if পথ_2.endswith('/METADATA'):
                        명세들.append(পাঁজা.read(ভুক্তি_মান).decode())
                    continue
                if not পথ_2.endswith('.py') or '.data/' in পথ_2:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + পথ_2)
                추가(পথ_2, পাঁজা.read(ভুক্তি_মান))
    elif ফাইল_ভুক্তি_নাম.endswith('.tar.gz') and নাম.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py কার্যকর_করুন_আদেশ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ডাটা), mode='r|gz') as পাঁজা:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for ভুক্তি_মান in পাঁজা:
                항목수 += 1
                전체크기 += ভুক্তি_মান.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('সংগ্রহ_করা_মান রিলিজ_স্টোরেজ আকার 제한 초과')
                বৈধ_করুন_পথ(ভুক্তি_মান.name, False)
                부분들 = ভুক্তি_মান.name.split('/')
                뿌리들.add(부분들[0])
                if ভুক্তি_মান.isdir():
                    continue
                if not ভুক্তি_মান.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython উত্স_ট্রী 배포형')
                পথ_2 = '/'.join(부분들[1:])
                সামগ্রি_মান = পাঁজা.extractfile(ভুক্তি_মান).read()
                if পথ_2.endswith('PKG-INFO'):
                    명세들.append(সামগ্রি_মান.decode())
                elif পথ_2.endswith('.py') and পথ_2 not in ('setup.py',):
                    추가(পথ_2, সামগ্রি_মান)
                elif '.egg-info/' not in পথ_2 and not পথ_2.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + পথ_2)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 মূল_মান 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* উত্স_ট্রী 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != নাম or 명세.get('Version') != সংস্করণ_মান:
        raise ValueError('배포 메타데이터의 নাম·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ইমেইল, 한도):
    if not ইমেইল.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ইমেইল, timeout=30) as উত্তর_দিন:
        if not উত্তর_দিন.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ইমেইল অপসারণ_করা_মান')
        ডাটা = উত্তর_দিন.read(한도 + 1)
    if len(ডাটা) > 한도:
        raise ValueError('배포 নথির_নাম আকার 제한 초과')
    return ডাটা


def স্থানান্তর_পাঁজা(নাম, সংস্করণ_মান, 파일들, 출처):
    명세 = {'name': নাম, 'version': সংস্করণ_মান, 'source': 출처, 'files': [
        {'path': পথ_2, 'size': len(ডাটা), 'sha256': hashlib.sha256(ডাটা).hexdigest()}
        for পথ_2, ডাটা in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('পাঁজা 명세 আকার 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[ভুক্তি_মান['path']] for ভুক্তি_মান in 명세['files'])


class পাঁজা_সংগ্রহস্থলের:
    def __init__(자신, পথ_2, তথ্য_প্রযুক্তি_অফলাইন=False):
        자신.পথ_2 = Path(পথ_2)
        자신.পথ_2.mkdir(parents=True, exist_ok=True)
        자신.তথ্য_প্রযুক্তি_অফলাইন = তথ্য_প্রযুক্তি_অফলাইন

    def প্রস্তুত_করুন(자신, 요청):
        নাম, সংস্করণ_মান = 요청해석(요청)
        열쇠 = নাম + ('==' + সংস্করণ_মান if সংস্করণ_মান else '')
        লগ_পথ = 자신.পথ_2 / (열쇠 + '.json')
        배포경로 = 자신.পথ_2 / (열쇠 + '.archive')
        if লগ_পথ.is_file() and 배포경로.is_file():
            লগ_সারি = json.loads(লগ_পথ.read_text())
            ডাটা = 배포경로.read_bytes()
            if hashlib.sha256(ডাটা).hexdigest() != লগ_সারি['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.তথ্য_প্রযুক্তি_অফলাইন:
                raise ValueError('তথ্য_প্রযুক্তি_অফলাইন 저장소에 없는 পাঁজা: ' + 요청)
            ইমেইল = 'https://pypi.org/pypi/' + নাম + ('/' + সংস্করণ_মান if সংস্করণ_মান else '') + '/json'
            সিসটেম_তথ্য = json.loads(웹읽기(ইমেইল, 4194304).decode())
            if সিসটেম_তথ্য['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [ভুক্তি_মান for ভুক্তি_মান in সিসটেম_তথ্য['urls'] if not ভুক্তি_মান.get('yanked') and ভুক্তি_মান['filename'].endswith('-none-any.whl')]
            if not 후보 and নাম.startswith('micropython-'):
                후보 = [ভুক্তি_মান for ভুক্তি_মান in সিসটেম_তথ্য['urls'] if not ভুক্তি_মান.get('yanked') and ভুক্তি_মান['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            বাছাই_মান = 후보[0]
            ডাটা = 웹읽기(বাছাই_মান['url'], 4194304)
            if hashlib.sha256(ডাটা).hexdigest() != বাছাই_মান['digests']['sha256']:
                raise ValueError('PyPI 배포 নথির_নাম SHA-256 불일치')
            লগ_সারি = {'name': নাম, 'version': সিসটেম_তথ্য['info']['version'], 'filename': বাছাই_মান['filename'],
                    'url': বাছাই_মান['url'], 'sha256': বাছাই_মান['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(লগ_সারি['filename'], ডাটা, নাম, লগ_সারি['version'])
            배포경로.write_bytes(ডাটা)
            লগ_পথ.write_text(json.dumps(লগ_সারি, ensure_ascii=False, indent=2) + '\n')
        if লগ_সারি['name'] != নাম or সংস্করণ_মান and লগ_সারি['version'] != সংস্করণ_মান:
            raise ValueError('সংগ্রহস্থলের_মূল নাম·버전 불일치')
        파일들 = 압축풀기(লগ_সারি['filename'], ডাটা, নাম, লগ_সারি['version'])
        return স্থানান্তর_পাঁজা(নাম, লগ_সারি['version'], 파일들, লগ_সারি['url'])


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
                raise ValueError('잘못된 পাঁজা 요청')
            উত্তর_দিন = 자신.server.সংগ্রহস্থলের_মূল.প্রস্তুত_করুন(요청[:-1].decode('ascii'))
        except Exception as ত্রুটি:
            머리 = json.dumps({'error': str(ত্রুটি)[:500]}, ensure_ascii=False).encode()
            উত্তর_দিন = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(উত্তর_দিন)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, পোর্ট_নম্বর=8027, পথ_2=None, তথ্য_প্রযুক্তি_অফলাইন=False):
        자신.সার্ভার_মান = socketserver.TCPServer(('127.0.0.1', পোর্ট_নম্বর), 꾸러미요청, bind_and_activate=False)
        자신.সার্ভার_মান.allow_reuse_address = True
        자신.সার্ভার_মান.server_bind()
        자신.সার্ভার_মান.server_activate()
        자신.সার্ভার_মান.সংগ্রহস্থলের_মূল = পাঁজা_সংগ্রহস্থলের(পথ_2 or প্রকল্প_মূল/'build/pip-cache', তথ্য_প্রযুক্তি_অফলাইন)
        자신.পোর্ট_নম্বর = 자신.সার্ভার_মান.server_address[1]
        자신.থ্রেড_মান = threading.Thread(target=자신.সার্ভার_মান.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.থ্রেড_মান.start()
        return 자신

    def __exit__(자신, *আর্গুমেন্ট_তালিকা):
        자신.সার্ভার_মান.shutdown()
        자신.সার্ভার_মান.server_close()
        자신.থ্রেড_মান.join(timeout=2)


def চালনা():
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('--port', type=int, default=8027)
    পার্সার_48ee4b1b.add_argument('--cache', type=Path, default=প্রকল্প_মূল/'build/pip-cache')
    পার্সার_48ee4b1b.add_argument('--offline', action='store_true')
    পার্সার_48ee4b1b.add_argument('--fetch', help='কার্যকর_করুন_আদেশ 없이 호환 배포 파일을 내려받아 검사·ভাণ্ডার_মান')
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    if আর্গুমেন্ট_তালিকা.fetch:
        ডাটা = পাঁজা_সংগ্রহস্থলের(আর্গুমেন্ট_তালিকা.cache, আর্গুমেন্ট_তালিকা.offline).প্রস্তুত_করুন(আর্গুমেন্ট_তালিকা.fetch)
        print('পাঁজা প্রস্তুত_করুন 완료:', আর্গুমেন্ট_তালিকা.fetch, len(ডাটা), 'বাইট_মান')
        return
    with 꾸러미중계(আর্গুমেন্ট_তালিকা.port, আর্গুমেন্ট_তালিকা.cache, আর্গুমেন্ট_তালিকা.offline) as 중계:
        print('পাঁজা 중계: 127.0.0.1:' + str(중계.পোর্ট_নম্বর), flush=True)
        try:
            중계.থ্রেড_মান.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    চালনা()
