#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 ইনষ্টল_কৰক_মান·실행한다."""
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
        raise ValueError('বাণ্ডল নাম 또는 নাম==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def বৈধকৰণ_কৰক_পথ(নাম, ইনষ্টলেশ্বন_পথ=True):
    পথ = PurePosixPath(নাম)
    if পথ.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in নাম.split('/')):
        raise ValueError('허용하지 않는 বাণ্ডল পথ: ' + নাম)
    if '\\' in নাম or any(ord(বৰ্ণ_মান) < 32 or ord(বৰ্ণ_মান) == 127 for বৰ্ণ_মান in নাম):
        raise ValueError('잘못된 বাণ্ডল পথ 문자')
    if ইনষ্টলেশ্বন_পথ and (len(('/lib/' + নাম).encode()) > 63 or নাম in ('한국어.py', 'বাণ্ডল.py')):
        raise ValueError('বাণ্ডল পথ 제한 또는 ডিফ_ল্ট_মান লাইব্ৰেৰী 충돌: ' + নাম)
    return নাম


def 압축풀기(ফাইল_প্রবিষ্ট_নাম, ডাটা, নাম, সংস্কৰণ_মান):
    파일들 = {}
    명세들 = []
    def 추가(পথ, সামগ্ৰী_মান):
        বৈধকৰণ_কৰক_পথ(পথ)
        if পথ in 파일들:
            raise ValueError('중복 বাণ্ডল পথ: ' + পথ)
        if len(সামগ্ৰী_মান) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + পথ)
        সামগ্ৰী_মান.decode('utf-8')
        파일들[পথ] = সামগ্ৰী_মান
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 উৎস_ট্ৰি 16개·합계 64 KiB 이하여야 합니다.')
    if ফাইল_প্রবিষ্ট_নাম.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(ডাটা)) as বাণ্ডল:
            항목들 = বাণ্ডল.infolist()
            if len(항목들) > 256 or sum(প্রবিষ্ট_মান.file_size for প্রবিষ্ট_মান in 항목들) > 1048576:
                raise ValueError('অভিলেখাগাৰ_মান ৰিলিজ_ষ্ট_ৰেজ মাপ 제한 초과')
            কেছ_সূচী = [প্রবিষ্ট_মান for প্রবিষ্ট_মান in 항목들 if প্রবিষ্ট_মান.filename.endswith('.dist-info/WHEEL')]
            if len(কেছ_সূচী) != 1:
                raise ValueError('wheel কেছ_মান 명세가 필요합니다.')
            কেছ_মান = email.parser.Parser().parsestr(বাণ্ডল.read(কেছ_সূচী[0]).decode())
            if কেছ_মান.get('Root-Is-Purelib', '').lower() != 'true' or not ফাইল_প্রবিষ্ট_নাম.endswith('-none-any.whl'):
                raise ValueError('C সম্প্রসাৰণ_মান·플랫폼 전용 wheel은 지원하지 않습니다.')
            for প্রবিষ্ট_মান in 항목들:
                পথ = প্রবিষ্ট_মান.filename.rstrip('/')
                বৈধকৰণ_কৰক_পথ(পথ, False)
                if (প্রবিষ্ট_মান.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if প্রবিষ্ট_মান.filename.endswith('/'):
                    continue
                if '.dist-info/' in পথ:
                    if পথ.endswith('/METADATA'):
                        명세들.append(বাণ্ডল.read(প্রবিষ্ট_মান).decode())
                    continue
                if not পথ.endswith('.py') or '.data/' in পথ:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + পথ)
                추가(পথ, বাণ্ডল.read(প্রবিষ্ট_মান))
    elif ফাইল_প্রবিষ্ট_নাম.endswith('.tar.gz') and নাম.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py নিষ্পাদন_আদেশ 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(ডাটা), mode='r|gz') as বাণ্ডল:
            뿌리들 = set()
            항목수 = 0
            전체크기 = 0
            for প্রবিষ্ট_মান in বাণ্ডল:
                항목수 += 1
                전체크기 += প্রবিষ্ট_মান.size
                if 항목수 > 256 or 전체크기 > 1048576:
                    raise ValueError('অভিলেখাগাৰ_মান ৰিলিজ_ষ্ট_ৰেজ মাপ 제한 초과')
                বৈধকৰণ_কৰক_পথ(প্রবিষ্ট_মান.name, False)
                부분들 = প্রবিষ্ট_মান.name.split('/')
                뿌리들.add(부분들[0])
                if প্রবিষ্ট_মান.isdir():
                    continue
                if not প্রবিষ্ট_মান.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython উৎস_ট্ৰি 배포형')
                পথ = '/'.join(부분들[1:])
                সামগ্ৰী_মান = বাণ্ডল.extractfile(প্রবিষ্ট_মান).read()
                if পথ.endswith('PKG-INFO'):
                    명세들.append(সামগ্ৰী_মান.decode())
                elif পথ.endswith('.py') and পথ not in ('setup.py',):
                    추가(পথ, সামগ্ৰী_মান)
                elif '.egg-info/' not in পথ and not পথ.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + পথ)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 ৰুট_মান 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* উৎস_ট্ৰি 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if 요청해석(명세.get('Name', ''))[0] != নাম or 명세.get('Version') != সংস্কৰণ_মান:
        raise ValueError('배포 메타데이터의 নাম·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ঠিকনা, 한도):
    if not ঠিকনা.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(ঠিকনা, timeout=30) as প্ৰত্যুত্তৰ_দিয়ক:
        if not প্ৰত্যুত্তৰ_দিয়ক.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 ঠিকনা লৈ_যাওক_মান')
        ডাটা = প্ৰত্যুত্তৰ_দিয়ক.read(한도 + 1)
    if len(ডাটা) > 한도:
        raise ValueError('배포 নথিপত্ৰ মাপ 제한 초과')
    return ডাটা


def স্থানান্তৰণ_বাণ্ডল(নাম, সংস্কৰণ_মান, 파일들, 출처):
    명세 = {'name': নাম, 'version': সংস্কৰণ_মান, 'source': 출처, 'files': [
        {'path': পথ, 'size': len(ডাটা), 'sha256': hashlib.sha256(ডাটা).hexdigest()}
        for পথ, ডাটা in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('বাণ্ডল 명세 মাপ 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[প্রবিষ্ট_মান['path']] for প্রবিষ্ট_মান in 명세['files'])


class 꾸러미저장소:
    def __init__(자신, পথ, 오프라인=False):
        자신.পথ = Path(পথ)
        자신.পথ.mkdir(parents=True, exist_ok=True)
        자신.오프라인 = 오프라인

    def প্ৰস্তুত_কৰক(자신, 요청):
        নাম, সংস্কৰণ_মান = 요청해석(요청)
        열쇠 = নাম + ('==' + সংস্কৰণ_মান if সংস্কৰণ_মান else '')
        লগ_পথ = 자신.পথ / (열쇠 + '.json')
        배포경로 = 자신.পথ / (열쇠 + '.archive')
        if লগ_পথ.is_file() and 배포경로.is_file():
            লগ_শাৰী = json.loads(লগ_পথ.read_text())
            ডাটা = 배포경로.read_bytes()
            if hashlib.sha256(ডাটা).hexdigest() != লগ_শাৰী['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.오프라인:
                raise ValueError('오프라인 저장소에 없는 বাণ্ডল: ' + 요청)
            ঠিকনা = 'https://pypi.org/pypi/' + নাম + ('/' + সংস্কৰণ_মান if সংস্কৰণ_মান else '') + '/json'
            ছিষ্টেম_তথ্য = json.loads(웹읽기(ঠিকনা, 4194304).decode())
            if ছিষ্টেম_তথ্য['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [প্রবিষ্ট_মান for প্রবিষ্ট_মান in ছিষ্টেম_তথ্য['urls'] if not প্রবিষ্ট_মান.get('yanked') and প্রবিষ্ট_মান['filename'].endswith('-none-any.whl')]
            if not 후보 and নাম.startswith('micropython-'):
                후보 = [প্রবিষ্ট_মান for প্রবিষ্ট_মান in ছিষ্টেম_তথ্য['urls'] if not প্রবিষ্ট_মান.get('yanked') and প্রবিষ্ট_মান['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            চয়ন_মান = 후보[0]
            ডাটা = 웹읽기(চয়ন_মান['url'], 4194304)
            if hashlib.sha256(ডাটা).hexdigest() != চয়ন_মান['digests']['sha256']:
                raise ValueError('PyPI 배포 নথিপত্ৰ SHA-256 불일치')
            লগ_শাৰী = {'name': নাম, 'version': ছিষ্টেম_তথ্য['info']['version'], 'filename': চয়ন_মান['filename'],
                    'url': চয়ন_মান['url'], 'sha256': চয়ন_মান['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(লগ_শাৰী['filename'], ডাটা, নাম, লগ_শাৰী['version'])
            배포경로.write_bytes(ডাটা)
            লগ_পথ.write_text(json.dumps(লগ_শাৰী, ensure_ascii=False, indent=2) + '\n')
        if লগ_শাৰী['name'] != নাম or সংস্কৰণ_মান and লগ_শাৰী['version'] != সংস্কৰণ_মান:
            raise ValueError('저장소 নাম·버전 불일치')
        파일들 = 압축풀기(লগ_শাৰী['filename'], ডাটা, নাম, লগ_শাৰী['version'])
        return স্থানান্তৰণ_বাণ্ডল(নাম, লগ_শাৰী['version'], 파일들, লগ_শাৰী['url'])


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
                raise ValueError('잘못된 বাণ্ডল 요청')
            প্ৰত্যুত্তৰ_দিয়ক = 자신.server.저장소.প্ৰস্তুত_কৰক(요청[:-1].decode('ascii'))
        except Exception as ত্ৰুটি:
            머리 = json.dumps({'error': str(ত্ৰুটি)[:500]}, ensure_ascii=False).encode()
            প্ৰত্যুত্তৰ_দিয়ক = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(প্ৰত্যুত্তৰ_দিয়ক)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, 접속번호=8027, পথ=None, 오프라인=False):
        자신.ছাৰ্ভাৰ_মান = socketserver.TCPServer(('127.0.0.1', 접속번호), 꾸러미요청, bind_and_activate=False)
        자신.ছাৰ্ভাৰ_মান.allow_reuse_address = True
        자신.ছাৰ্ভাৰ_মান.server_bind()
        자신.ছাৰ্ভাৰ_মান.server_activate()
        자신.ছাৰ্ভাৰ_মান.저장소 = 꾸러미저장소(পথ or 기준/'build/pip-cache', 오프라인)
        자신.접속번호 = 자신.ছাৰ্ভাৰ_মান.server_address[1]
        자신.আঁহ_মান = threading.Thread(target=자신.ছাৰ্ভাৰ_মান.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.আঁহ_মান.start()
        return 자신

    def __exit__(자신, *인수):
        자신.ছাৰ্ভাৰ_মান.shutdown()
        자신.ছাৰ্ভাৰ_মান.server_close()
        자신.আঁহ_মান.join(timeout=2)


def সঞ্চালন():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--port', type=int, default=8027)
    해석기.add_argument('--cache', type=Path, default=기준/'build/pip-cache')
    해석기.add_argument('--offline', action='store_true')
    해석기.add_argument('--fetch', help='নিষ্পাদন_আদেশ 없이 호환 배포 파일을 내려받아 검사·জমা_কৰক_মান')
    인수 = 해석기.parse_args()
    if 인수.fetch:
        ডাটা = 꾸러미저장소(인수.cache, 인수.offline).প্ৰস্তুত_কৰক(인수.fetch)
        print('বাণ্ডল প্ৰস্তুত_কৰক 완료:', 인수.fetch, len(ডাটা), 'বাইট_মান')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('বাণ্ডল 중계: 127.0.0.1:' + str(중계.접속번호), flush=True)
        try:
            중계.আঁহ_মান.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    সঞ্চালন()
