"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
검증해시 = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    נאָמען = 'micropython-' + 배포판
    압축꾸러미 = 기준경로 / 'vendor' / (נאָמען + '.tar.gz')
    if not 압축꾸러미.is_file() or hashlib.sha256(압축꾸러미.read_bytes()).hexdigest() != 검증해시:
        raise SystemExit('MicroPython 소스 없음/해시 불일치: ' + str(압축꾸러미))
    원본자료 = 기준경로 / 'build' / נאָמען
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(압축꾸러미)) as 타르꾸러미:
            for 구성원 in 타르꾸러미.getmembers():
                경로 = Path(구성원.name)
                if 경로.is_absolute() or '..' in 경로.parts or 경로.parts[0] != נאָמען:
                    raise SystemExit('안전하지 않은 소스 경로')
                if 구성원.isfile() or 구성원.isdir():
                    타르꾸러미.extract(구성원, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(검증해시 + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))
