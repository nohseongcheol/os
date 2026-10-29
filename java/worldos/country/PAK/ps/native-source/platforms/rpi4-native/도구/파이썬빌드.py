"""고정한 공식 MicroPython 소스로 자체 SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

배포판 = '1.24.1'
검증해시 = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def 파이썬만들기(기준경로, 시언어번역기, 연결편집기):
    نوم = 'micropython-' + 배포판
    ارشیف = 기준경로 / 'vendor' / (نوم + '.tar.gz')
    if not ارشیف.is_file() or hashlib.sha256(ارشیف.read_bytes()).hexdigest() != 검증해시:
        raise SystemExit('MicroPython سرچینه_ونه 없음/해시 불일치: ' + str(ارشیف))
    원본자료 = 기준경로 / 'build' / نوم
    if not (원본자료 / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(ارشیف)) as 타르꾸러미:
            for شمېره in 타르꾸러미.getmembers():
                يونلور = Path(شمېره.name)
                if يونلور.is_absolute() or '..' in يونلور.parts or يونلور.parts[0] != نوم:
                    raise SystemExit('안전하지 않은 سرچینه_ونه يونلور')
                if شمېره.isfile() or شمېره.isdir():
                    타르꾸러미.extract(شمېره, str(기준경로 / 'build'))
        (원본자료 / '.jkoros-source-sha256').write_text(검증해시 + '\n')
    뉴리브포함경로 = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(뉴리브포함경로) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE 필요')
    subprocess.check_call(['make', '-j2', 'CC=' + 시언어번역기, 'LD=' + 연결편집기, 'NEWLIB_INCLUDE=' + 뉴리브포함경로], cwd=str(기준경로 / '파이썬연결'))
